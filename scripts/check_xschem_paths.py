from __future__ import annotations

import argparse
from bisect import bisect_right
from dataclasses import dataclass
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys


@dataclass(frozen=True)
class Violation:
    file_path: str
    line_number: int
    offending_reference: str
    message: str
    guidance: str

    def format(self) -> str:
        return (
            f"{self.file_path}:{self.line_number}: {self.offending_reference!r}: "
            f"{self.message}; {self.guidance}"
        )


@dataclass(frozen=True)
class Word:
    value: str
    start: int
    end: int
    braced: bool = False


TCL_VARIABLES = {
    "SCRIPT_DIR", "PDK", "PDK_ROOT", "IO_LIBRARY_PATH", "netlist_dir",
    "SPICE_SCRIPTS", "env(PDK)", "env(PDK_ROOT)", "env(SPICE_SCRIPTS)",
    "env(SCRIPT_DIR)",
}
TARGET_EXTENSIONS = (".sch", ".sym", ".spice", ".cir")
FILE_ATTRS = {"schematic", "model", "file", "stimulus", "spice_file"}
VARIABLE = re.compile(r"\$(?:\{([^}]+)\}|([:\w]+(?:\([^)]*\))?))")

XSCHEM_BUILTIN_DEVICES = frozenset({
    "ammeter.sym", "bus_slice.sym", "capa.sym", "code.sym", "code_shown.sym",
    "delay.sym", "diode.sym", "generic.sym", "gnd.sym", "ind.sym",
    "ipin.sym", "iopin.sym", "isource.sym", "lab_pin.sym", "lab_wire.sym",
    "launcher.sym", "netlist_not_shown.sym", "nmos.sym", "noconn.sym", "npn.sym",
    "opin.sym", "param.sym", "pmos.sym", "pnp.sym", "probe.sym",
    "relay.sym", "res.sym", "std_logic.sym", "subcircuit.sym", "subcircuit2.sym",
    "switch.sym", "title.sym", "title-2.sym", "transformer.sym", "vdd.sym",
    "view.sym", "voltmeter.sym", "vsource.sym", "vss.sym", "zener.sym",
})

KNOWN_PDK_MODELS = frozenset({
    "IHP_PDK_basic_components.lib", "IHP_PDK_nonlinear_components.lib",
    "IHP_PDK_stdcells.lib", "cap_cmomf.lib", "cap_cmomi.lib",
    "capacitors_mod.lib", "capacitors_mod_mismatch.lib", "capacitors_stat.lib",
    "cornerCAP.lib", "cornerDIO.lib", "cornerHBT.lib", "cornerMOSCAP.lib",
    "cornerMOShv.lib", "cornerMOSlv.lib", "cornerPNP.lib", "cornerRES.lib",
    "diodes.lib", "models.spice", "resistors_mod.lib", "resistors_mod_mismatch.lib",
    "resistors_parm.lib", "resistors_stat.lib", "sg13cmos5l_io_dummy.lib",
    "sg13cmos5l_io_fast_1p32V_3p6V_m40C.lib", "sg13cmos5l_io_fast_1p65V_3p6V_m40C.lib",
    "sg13cmos5l_io_slow_1p08V_3p0V_125C.lib", "sg13cmos5l_io_slow_1p35V_3p0V_125C.lib",
    "sg13cmos5l_io_typ_1p2V_3p3V_25C.lib", "sg13cmos5l_io_typ_1p5V_3p3V_25C.lib",
    "sg13cmos5l_pnpMPA_mod.lib", "sg13cmos5l_pnpMPA_stat.lib",
    "sg13cmos5l_stdcell_fast_1p32V_m40C.lib", "sg13cmos5l_stdcell_fast_1p65V_m40C.lib",
    "sg13cmos5l_stdcell_slow_1p08V_125C.lib", "sg13cmos5l_stdcell_slow_1p35V_125C.lib",
    "sg13cmos5l_stdcell_typ_1p20V_25C.lib", "sg13cmos5l_stdcell_typ_1p50V_25C.lib",
    "sg13g2_bondpad.lib", "sg13g2_dschottky_nbl1_mod.lib", "sg13g2_dschottky_nbl1_stat.lib",
    "sg13g2_esd.lib", "sg13g2_hbt_mod.lib", "sg13g2_hbt_mod_mismatch.lib",
    "sg13g2_hbt_stat.lib", "sg13g2_io_dummy.lib", "sg13g2_io_fast_1p32V_3p6V_m40C.lib",
    "sg13g2_io_fast_1p65V_3p6V_m40C.lib", "sg13g2_io_slow_1p08V_3p0V_125C.lib",
    "sg13g2_io_slow_1p35V_3p0V_125C.lib", "sg13g2_io_typ_1p2V_3p3V_25C.lib",
    "sg13g2_io_typ_1p5V_3p3V_25C.lib", "sg13g2_moscap_mismatch.lib",
    "sg13g2_moscap_mod.lib", "sg13g2_moscap_mod_mismatch.lib", "sg13g2_moscap_parm.lib",
    "sg13g2_moscap_stat.lib", "sg13g2_moshv_mismatch.lib", "sg13g2_moshv_mod.lib",
    "sg13g2_moshv_mod_mismatch.lib", "sg13g2_moshv_parm.lib", "sg13g2_moshv_stat.lib",
    "sg13g2_moslv_mismatch.lib", "sg13g2_moslv_mod.lib", "sg13g2_moslv_mod_mismatch.lib",
    "sg13g2_moslv_parm.lib", "sg13g2_moslv_stat.lib", "sg13g2_stdcell_fast_1p32V_m40C.lib",
    "sg13g2_stdcell_fast_1p65V_m40C.lib", "sg13g2_stdcell_slow_1p08V_125C.lib",
    "sg13g2_stdcell_slow_1p35V_125C.lib", "sg13g2_stdcell_typ_1p20V_25C.lib",
    "sg13g2_stdcell_typ_1p50V_25C.lib", "sg13g2_svaricaphv_mod.lib",
    "sg13g2_svaricaphv_mod_mismatch.lib",
})

KNOWN_PDK_SYMBOLS = frozenset({
    "A21O.sym", "A21OI.sym", "A221OI.sym", "A22OI.sym", "AND.sym", "AND3.sym", "AND4.sym",
    "ANTENNA.sym", "BUF.sym", "Bjt.sym", "Capacitor.sym", "DECAP.sym", "DFF.sym", "DFFQ.sym",
    "DLHQ.sym", "DLHR.sym", "DLHRQ.sym", "DLLR.sym", "DLLRQ.sym", "Diode.sym", "Diodevdd.sym",
    "Diodevss.sym", "EBUFN.sym", "EINVN.sym", "GCLK.sym", "IHP130_stdcells.sym", "IHP_testcases.sym",
    "INV.sym", "Inductor2.sym", "IsolBox.sym", "MUX2.sym", "MUX4.sym", "Mos.sym", "NAND.sym",
    "NAND3.sym", "NAND3_B.sym", "NAND4.sym", "NAND_B.sym", "NOR.sym", "NOR3.sym", "NOR4.sym",
    "NOR_B.sym", "O21AI.sym", "OR.sym", "OR3.sym", "OR4.sym", "Resistor.sym", "ResistorEU.sym",
    "SDFF.sym", "SDFFB.sym", "SDFFQ.sym", "SGCLK.sym", "SIGHOLD.sym", "Schottky.sym", "TIEHI.sym",
    "TIELO.sym", "Varicap.sym", "XNOR.sym", "XOR.sym", "ac_cap_cmomf.sym", "ac_cap_cmomi.sym",
    "ac_hbt_13g2.sym", "ac_lv_nmosrf.sym", "ac_mim_cap.sym", "ac_rfmim_cap.sym", "annotate_bip_params.sym",
    "annotate_fet_params.sym", "bondpad.sym", "cap_cmim.sym", "cap_cmomf.sym", "cap_cmomi.sym",
    "cap_cpara.sym", "cap_rfcmim.sym", "dantenna.sym", "dc_diode_op.sym", "dc_diode_temp.sym",
    "dc_esd_diodes.sym", "dc_esd_nmos_cl.sym", "dc_hbt_13g2.sym", "dc_hbt_13g2_5t.sym", "dc_hv_nmos.sym",
    "dc_hv_pmos.sym", "dc_isolbox.sym", "dc_logic_not.sym", "dc_lv_nmos.sym", "dc_lv_pmos.sym",
    "dc_mos_cs_temp.sym", "dc_mos_temp.sym", "dc_ntap1.sym", "dc_pnpMPA.sym", "dc_ptap1.sym",
    "dc_res_temp.sym", "dc_schottky.sym", "diodevdd_2kv.sym", "diodevdd_4kv.sym", "diodevss_2kv.sym",
    "diodevss_4kv.sym", "dpantenna.sym", "gallery.sym", "inductor.sym", "inductor3.sym", "inv_mc_tb.sym",
    "inv_sweep_tb.sym", "iso_dc_hv_nmos.sym", "iso_dc_lv_nmos.sym", "iso_dc_res.sym", "isolbox.sym",
    "isolbox_sweep_tb.sym", "mc_hbt_13g2.sym", "mc_hbt_13g2_ac.sym", "mc_hv_nmos_cs_loop.sym",
    "mc_hv_pmos_cs_loop.sym", "mc_lv_nmos_cs_loop.sym", "mc_lv_pmos_cs_loop.sym", "mc_mim_cap_ac.sym",
    "mc_res_op.sym", "moscap_n.sym", "moscap_p.sym", "nmoscl.sym", "nmoscl_2.sym", "nmoscl_4.sym",
    "npn13G2.sym", "npn13G2_5t.sym", "npn13G2l.sym", "npn13G2l_5t.sym", "npn13G2v.sym", "npn13G2v_5t.sym",
    "ntap1.sym", "pad.sym", "pnpMPA.sym", "portsource.sym", "ptap1.sym", "rfMos.sym", "rfcmim.sym",
    "rfnmos.sym", "rhigh.sym", "rppd.sym", "rsil.sym", "schottky_nbl1.sym", "sg13_hv_nmos.sym",
    "sg13_hv_pmos.sym", "sg13_hv_rf_nmos.sym", "sg13_hv_rf_pmos.sym", "sg13_lv_nmos.sym", "sg13_lv_pmos.sym",
    "sg13_lv_rf_nmos.sym", "sg13_lv_rf_pmos.sym", "sg13_svaricap.sym", "sg13cmos5l_a21o_1.sym",
    "sg13cmos5l_a21o_2.sym", "sg13cmos5l_a21oi_1.sym", "sg13cmos5l_a21oi_2.sym", "sg13cmos5l_a221oi_1.sym",
    "sg13cmos5l_a22oi_1.sym", "sg13cmos5l_and2_1.sym", "sg13cmos5l_and2_2.sym", "sg13cmos5l_and3_1.sym",
    "sg13cmos5l_and3_2.sym", "sg13cmos5l_and4_1.sym", "sg13cmos5l_and4_2.sym", "sg13cmos5l_antennanp.sym",
    "sg13cmos5l_buf_1.sym", "sg13cmos5l_buf_16.sym", "sg13cmos5l_buf_2.sym", "sg13cmos5l_buf_4.sym",
    "sg13cmos5l_buf_8.sym", "sg13cmos5l_decap_4.sym", "sg13cmos5l_decap_8.sym", "sg13cmos5l_dfrbp_1.sym",
    "sg13cmos5l_dfrbp_2.sym", "sg13cmos5l_dlhq_1.sym", "sg13cmos5l_dlhr_1.sym", "sg13cmos5l_dlhrq_1.sym",
    "sg13cmos5l_dllr_1.sym", "sg13cmos5l_dllrq_1.sym", "sg13cmos5l_dlygate4sd1_1.sym", "sg13cmos5l_dlygate4sd2_1.sym",
    "sg13cmos5l_dlygate4sd3_1.sym", "sg13cmos5l_ebufn_2.sym", "sg13cmos5l_ebufn_4.sym", "sg13cmos5l_ebufn_8.sym",
    "sg13cmos5l_einvn_2.sym", "sg13cmos5l_einvn_4.sym", "sg13cmos5l_einvn_8.sym", "sg13cmos5l_fill_1.sym",
    "sg13cmos5l_fill_2.sym", "sg13cmos5l_fill_4.sym", "sg13cmos5l_fill_8.sym", "sg13cmos5l_inv_1.sym",
    "sg13cmos5l_inv_16.sym", "sg13cmos5l_inv_2.sym", "sg13cmos5l_inv_4.sym", "sg13cmos5l_inv_8.sym",
    "sg13cmos5l_lgcp_1.sym", "sg13cmos5l_mux2_1.sym", "sg13cmos5l_mux2_2.sym", "sg13cmos5l_mux4_1.sym",
    "sg13cmos5l_nand2_1.sym", "sg13cmos5l_nand2_2.sym", "sg13cmos5l_nand2b_1.sym", "sg13cmos5l_nand2b_2.sym",
    "sg13cmos5l_nand3_1.sym", "sg13cmos5l_nand3b_1.sym", "sg13cmos5l_nand4_1.sym", "sg13cmos5l_nor2_1.sym",
    "sg13cmos5l_nor2_2.sym", "sg13cmos5l_nor2b_1.sym", "sg13cmos5l_nor2b_2.sym", "sg13cmos5l_nor3_1.sym",
    "sg13cmos5l_nor3_2.sym", "sg13cmos5l_nor4_1.sym", "sg13cmos5l_nor4_2.sym", "sg13cmos5l_o21ai_1.sym",
    "sg13cmos5l_or2_1.sym", "sg13cmos5l_or2_2.sym", "sg13cmos5l_or3_1.sym", "sg13cmos5l_or3_2.sym",
    "sg13cmos5l_or4_1.sym", "sg13cmos5l_or4_2.sym", "sg13cmos5l_sdfbbp_1.sym", "sg13cmos5l_sdfrbp_2.sym",
    "sg13cmos5l_sighold.sym", "sg13cmos5l_slgcp_1.sym", "sg13cmos5l_xnor2_1.sym", "sg13cmos5l_xor2_1.sym",
    "sg13g2_a21o_1.sym", "sg13g2_a21o_2.sym", "sg13g2_a21oi_1.sym", "sg13g2_a21oi_2.sym", "sg13g2_a221oi_1.sym",
    "sg13g2_a22oi_1.sym", "sg13g2_and2_1.sym", "sg13g2_and2_2.sym", "sg13g2_and3_1.sym", "sg13g2_and3_2.sym",
    "sg13g2_and4_1.sym", "sg13g2_and4_2.sym", "sg13g2_antennanp.sym", "sg13g2_buf_1.sym", "sg13g2_buf_16.sym",
    "sg13g2_buf_2.sym", "sg13g2_buf_4.sym", "sg13g2_buf_8.sym", "sg13g2_decap_4.sym", "sg13g2_decap_8.sym",
    "sg13g2_dfrbp_1.sym", "sg13g2_dfrbp_2.sym", "sg13g2_dfrbpq_1.sym", "sg13g2_dfrbpq_2.sym", "sg13g2_dlhq_1.sym",
    "sg13g2_dlhr_1.sym", "sg13g2_dlhrq_1.sym", "sg13g2_dllr_1.sym", "sg13g2_dllrq_1.sym", "sg13g2_dlygate4sd1_1.sym",
    "sg13g2_dlygate4sd2_1.sym", "sg13g2_dlygate4sd3_1.sym", "sg13g2_ebufn_2.sym", "sg13g2_ebufn_4.sym",
    "sg13g2_ebufn_8.sym", "sg13g2_einvn_2.sym", "sg13g2_einvn_4.sym", "sg13g2_einvn_8.sym", "sg13g2_fill_1.sym",
    "sg13g2_fill_2.sym", "sg13g2_fill_4.sym", "sg13g2_fill_8.sym", "sg13g2_inv_1.sym", "sg13g2_inv_16.sym",
    "sg13g2_inv_2.sym", "sg13g2_inv_4.sym", "sg13g2_inv_8.sym", "sg13g2_lgcp_1.sym", "sg13g2_mux2_1.sym",
    "sg13g2_mux2_2.sym", "sg13g2_mux4_1.sym", "sg13g2_nand2_1.sym", "sg13g2_nand2_2.sym", "sg13g2_nand2b_1.sym",
    "sg13g2_nand2b_2.sym", "sg13g2_nand3_1.sym", "sg13g2_nand3b_1.sym", "sg13g2_nand4_1.sym", "sg13g2_nor2_1.sym",
    "sg13g2_nor2_2.sym", "sg13g2_nor2b_1.sym", "sg13g2_nor2b_2.sym", "sg13g2_nor3_1.sym", "sg13g2_nor3_2.sym",
    "sg13g2_nor4_1.sym", "sg13g2_nor4_2.sym", "sg13g2_o21ai_1.sym", "sg13g2_or2_1.sym", "sg13g2_or2_2.sym",
    "sg13g2_or3_1.sym", "sg13g2_or3_2.sym", "sg13g2_or4_1.sym", "sg13g2_or4_2.sym", "sg13g2_sdfbbp_1.sym",
    "sg13g2_sdfrbp_1.sym", "sg13g2_sdfrbp_2.sym", "sg13g2_sdfrbpq_1.sym", "sg13g2_sdfrbpq_2.sym", "sg13g2_sighold.sym",
    "sg13g2_slgcp_1.sym", "sg13g2_tiehi.sym", "sg13g2_tielo.sym", "sg13g2_xnor2_1.sym", "sg13g2_xor2_1.sym",
    "sp_mim_cap.sym", "sp_parasitic_cap.sym", "sp_rfmim_cap.sym", "sub.sym", "tran_bondpad.sym",
    "tran_cap_cmomf.sym", "tran_cap_cmomi.sym", "tran_logic_nand.sym", "tran_logic_not.sym", "tran_mim_cap.sym",
    "tran_moscap_n.sym", "tran_moscap_p.sym",
})

KNOWN_IO_SYMBOLS = frozenset({
    "sg13g2_Clamp_N15N15D.sym", "sg13g2_Clamp_N20N0D.sym", "sg13g2_Clamp_N2N2D.sym",
    "sg13g2_Clamp_N43N43D4R.sym", "sg13g2_Clamp_N8N8D.sym", "sg13g2_Clamp_P15N15D.sym",
    "sg13g2_Clamp_P15N15D_noptap.sym", "sg13g2_Clamp_P20N0D.sym", "sg13g2_Clamp_P20N0D_noptap.sym",
    "sg13g2_Clamp_P2N2D.sym", "sg13g2_Clamp_P2N2D_noptap.sym", "sg13g2_Clamp_P8N8D.sym",
    "sg13g2_Clamp_P8N8D_noptap.sym", "sg13g2_Corner.sym", "sg13g2_Corner_noptap.sym",
    "sg13g2_DCNDiode.sym", "sg13g2_DCPDiode.sym", "sg13g2_DCPDiode_noptap.sym",
    "sg13g2_Filler1000.sym", "sg13g2_Filler10000.sym", "sg13g2_Filler200.sym",
    "sg13g2_Filler2000.sym", "sg13g2_Filler400.sym", "sg13g2_Filler4000.sym",
    "sg13g2_GateDecode.sym", "sg13g2_GateDecode_noptap.sym", "sg13g2_GateLevelUpInv.sym",
    "sg13g2_GateLevelUpInv_noptap.sym", "sg13g2_IOPadASig.sym", "sg13g2_IOPadAVdd.sym",
    "sg13g2_IOPadAVddAVss.sym", "sg13g2_IOPadAVss.sym", "sg13g2_IOPadAnalog.sym",
    "sg13g2_IOPadIOVdd.sym", "sg13g2_IOPadIOVddAccess.sym", "sg13g2_IOPadIOVss.sym",
    "sg13g2_IOPadIn.sym", "sg13g2_IOPadInOut16mA.sym", "sg13g2_IOPadInOut30mA.sym",
    "sg13g2_IOPadInOut4mA.sym", "sg13g2_IOPadOut16mA.sym", "sg13g2_IOPadOut30mA.sym",
    "sg13g2_IOPadOut4mA.sym", "sg13g2_IOPadRF.sym", "sg13g2_IOPadTriOut16mA.sym",
    "sg13g2_IOPadTriOut30mA.sym", "sg13g2_IOPadTriOut4mA.sym", "sg13g2_IOPadVdd.sym",
    "sg13g2_IOPadVddVss.sym", "sg13g2_IOPadVss.sym", "sg13g2_LevelDown.sym",
    "sg13g2_LevelDown_noptap.sym", "sg13g2_LevelUp.sym", "sg13g2_LevelUpInv.sym",
    "sg13g2_LevelUpInv_noptap.sym", "sg13g2_LevelUp_noptap.sym", "sg13g2_RCClampInverter.sym",
    "sg13g2_RCClampInverter_noptap.sym", "sg13g2_RCClampResistor.sym",
    "sg13g2_SecondaryProtection.sym", "sg13g2_SecondaryProtection_noptap.sym",
    "sg13g2_io_inv_x1.sym", "sg13g2_io_inv_x1_noptap.sym", "sg13g2_io_nand2_x1.sym",
    "sg13g2_io_nand2_x1_noptap.sym", "sg13g2_io_nor2_x1.sym", "sg13g2_io_nor2_x1_noptap.sym",
    "sg13g2_io_tie.sym", "sg13g2_io_tie_noptap.sym",
})


def _group_end(text: str, start: int) -> int:
    opening = text[start]
    closing = {"{": "}", "[": "]", '"': '"', "'": "'"}[opening]
    depth = 1
    pos = start + 1
    while pos < len(text):
        char = text[pos]
        if char == "\\" and pos + 1 < len(text):
            pos += 2
            continue
        if char == closing:
            depth -= 1
            if depth == 0:
                return pos + 1
        elif char == opening and opening in "{[":
            depth += 1
        pos += 1
    raise ValueError(f"unclosed {opening!r} delimiter")


def _word(text: str, pos: int) -> Word:
    start = pos
    if text[pos] in "{\"'":
        end = _group_end(text, pos)
        return Word(text[pos + 1:end - 1], pos + 1, end, text[pos] == "{")
    while pos < len(text) and not text[pos].isspace() and text[pos] != ";":
        if text[pos] == "[":
            pos = _group_end(text, pos)
        elif text[pos] == "\\" and pos + 1 < len(text) and text[pos + 1].isspace():
            pos += 2
        else:
            pos += 1
    return Word(text[start:pos], start, pos)


def _spice_words(line: str) -> list[Word]:
    words: list[Word] = []
    pos = 0
    while pos < len(line):
        if line[pos].isspace():
            pos += 1
            continue
        if line[pos] == ";" or line[pos:pos + 2] == "$ ":
            break
        start = pos
        if line[pos] in "\"'":
            end = _group_end(line, pos)
            words.append(Word(line[start + 1:end - 1], start + 1, end, braced=False))
            pos = end
        else:
            while pos < len(line) and not line[pos].isspace() and line[pos] != ";" and line[pos:pos + 2] != "$ ":
                if line[pos] in "\"'":
                    pos = _group_end(line, pos)
                else:
                    pos += 1
            words.append(Word(line[start:pos], start, pos, braced=False))
    return words


def _commands(text: str) -> list[list[Word]]:
    commands: list[list[Word]] = []
    words: list[Word] = []
    pos = 0
    while pos < len(text):
        if text[pos] in ";\n":
            if words:
                commands.append(words)
                words = []
            pos += 1
        elif text[pos].isspace():
            pos += 1
        elif not words and text[pos] == "#":
            end = text.find("\n", pos)
            pos = len(text) if end < 0 else end
        else:
            token = _word(text, pos)
            words.append(token)
            pos = token.end
    if words:
        commands.append(words)
    return commands


def _extract_ngspice_vars(ref: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    pattern = re.compile(
        r"\{\$&([A-Za-z_]\w*)\}"
        r"|\$(&[A-Za-z_]\w*)"
        r"|\{\$([A-Za-z_]\w*)\}"
        r"|\$\{([A-Za-z_]\w*)\}"
        r"|\$([A-Za-z_]\w*)"
    )
    for m in pattern.finditer(ref):
        matched_str = m.group(0)
        var_name = m.group(1) or (m.group(2).lstrip("&") if m.group(2) else None) or m.group(3) or m.group(4) or m.group(5)
        if var_name and var_name not in TCL_VARIABLES:
            results.append((matched_str, var_name))
    return results


def _check_root_existence(
    rel_path: str,
    file_path: str,
    line: int,
    ref: str,
    repo_root: Path | None,
    staged_paths: set[str] | None = None,
) -> Violation | None:
    norm_path = posixpath.normpath(rel_path.replace("\\", "/")).lstrip("/")
    if not norm_path or norm_path == ".":
        return None

    if staged_paths is not None:
        if norm_path not in staged_paths:
            return Violation(
                file_path,
                line,
                ref,
                f"referenced local symbol or dependency does not exist: {ref}",
                "verify the referenced file exists in the repository or PDK",
            )
        return None

    if repo_root is not None:
        target = repo_root / norm_path
        if not target.is_file():
            return Violation(
                file_path,
                line,
                ref,
                f"referenced local symbol or dependency does not exist: {ref}",
                "verify the referenced file exists in the repository or PDK",
            )
        return None

    return None


def _check_local_existence(
    ref: str,
    file_path: str,
    line: int,
    repo_root: Path | None,
    staged_paths: set[str] | None = None,
) -> Violation | None:
    ref_norm = ref.replace("\\", "/").strip("\"'")
    if not ref_norm:
        return None

    if ref_norm in XSCHEM_BUILTIN_DEVICES:
        return None
    if ref_norm.startswith("devices/"):
        dev = ref_norm[len("devices/"):]
        if dev in XSCHEM_BUILTIN_DEVICES:
            return None
        return None

    if ref_norm in KNOWN_PDK_MODELS or Path(ref_norm).name in KNOWN_PDK_MODELS:
        return None

    if ref_norm in KNOWN_PDK_SYMBOLS:
        return None
    if ref_norm.startswith(("sg13g2_pr/", "sg13cmos5l_pr/")):
        sym = ref_norm.split("/", 1)[1]
        if sym in KNOWN_PDK_SYMBOLS:
            return None

    if ref_norm in KNOWN_IO_SYMBOLS:
        return None
    if ref_norm.startswith("sg13g2_io/"):
        sym = ref_norm.split("/", 1)[1]
        if sym in KNOWN_IO_SYMBOLS:
            return None

    if staged_paths is not None:
        cand_paths = [
            posixpath.normpath(posixpath.join(posixpath.dirname(file_path), ref_norm)),
            ref_norm.lstrip("/"),
            f"CDR4176-main/schematic/xschem/{ref_norm.lstrip('/')}",
            f"CDR4176-main/testbenches/tran/xschem/{ref_norm.lstrip('/')}",
            f"CDR4176-main/layout/klayout/{ref_norm.lstrip('/')}",
            f"design/{ref_norm.lstrip('/')}",
            f"openpdk-libraries/ihp-sg13g2/sg13g2_io/xschem/{ref_norm.lstrip('/')}",
        ]
        for c in cand_paths:
            if c in staged_paths:
                return None

        if "/" not in ref_norm:
            if any(
                (p.endswith(f"/{ref_norm}") or p == ref_norm)
                for p in staged_paths
                if not p.startswith(("simulation/", "runs/"))
                and "/project_io/" not in p
                and not p.startswith("project_io/")
            ):
                return None

        return Violation(
            file_path,
            line,
            ref,
            f"referenced local symbol or dependency does not exist: {ref}",
            "verify the referenced file exists in the repository or PDK",
        )

    if repo_root is not None:
        pdk_root_path = repo_root / "IHP-Open-PDK"
        if "PDK_ROOT" in os.environ and os.environ["PDK_ROOT"]:
            ext_pdk = Path(os.environ["PDK_ROOT"])
            if ext_pdk.is_dir():
                pdk_root_path = ext_pdk

        file_dir = (repo_root / file_path).parent

        search_dirs = [
            file_dir,
            repo_root,
            repo_root / "CDR4176-main" / "schematic" / "xschem",
            repo_root / "CDR4176-main" / "testbenches" / "tran" / "xschem",
            repo_root / "CDR4176-main" / "layout" / "klayout",
            repo_root / "design",
            repo_root / "openpdk-libraries" / "ihp-sg13g2" / "sg13g2_io" / "xschem",
            pdk_root_path / "ihp-sg13g2" / "libs.tech" / "xschem",
            pdk_root_path / "ihp-sg13g2" / "libs.tech" / "xschem" / "sg13g2_pr",
            pdk_root_path / "ihp-sg13g2" / "libs.ref" / "sg13g2_pr" / "xschem",
            pdk_root_path / "ihp-sg13g2" / "libs.ref" / "sg13g2_stdcell" / "sym" / "xschem",
            pdk_root_path / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models",
        ]

        for sd in search_dirs:
            if (sd / ref_norm).exists():
                return None

        if "/" not in ref_norm:
            for base in (
                repo_root / "CDR4176-main",
                repo_root / "design",
                repo_root / "openpdk-libraries",
                pdk_root_path / "ihp-sg13g2" / "libs.tech" / "xschem",
                pdk_root_path / "ihp-sg13g2" / "libs.ref",
            ):
                if base.is_dir():
                    matches = list(base.glob(f"**/{ref_norm}"))
                    filtered = [
                        m for m in matches
                        if "simulation" not in m.parts
                        and "runs" not in m.parts
                        and "project_io" not in m.parts
                    ]
                    if filtered:
                        return None

        return Violation(
            file_path,
            line,
            ref,
            f"referenced local symbol or dependency does not exist: {ref}",
            "verify the referenced file exists in the repository or PDK",
        )

    return None


def _path_issue(
    ref: str,
    file_path: str,
    line: int,
    tcl: bool,
    in_control: bool = False,
    control_vars: set[str] | None = None,
    is_runtime_output: bool = False,
    repo_root: Path | None = None,
    check_existence: bool = False,
    staged_paths: set[str] | None = None,
) -> Violation | None:
    ref = ref.strip().strip("\"'")

    def issue(message: str, guidance: str = "use a library-relative name or an approved Tcl root") -> Violation:
        return Violation(file_path, line, ref, message, guidance)

    if not ref:
        return None

    if tcl and "[" in ref:
        if not (ref.startswith("[") and _group_end(ref, 0) == len(ref)):
            return issue("unsupported Tcl bracket expression in path", "use a direct approved-variable path")
        commands = _commands(ref[1:-1])
        if len(commands) != 1 or [w.value for w in commands[0][:2]] != ["file", "join"]:
            return issue("unsupported Tcl bracket expression in path", "use a direct approved-variable path")
        parts = commands[0][2:]
        if not parts or any("[" in part.value for part in parts):
            return issue("unsupported Tcl file join expression", "use a direct approved-variable path")

        for idx, part in enumerate(parts):
            if part.value.startswith(("/", "\\", "~")) or re.match(r"^[A-Za-z]:", part.value):
                found = _path_issue(
                    part.value, file_path, line, not part.braced, in_control,
                    control_vars, is_runtime_output, repo_root, check_existence, staged_paths,
                )
                if found:
                    return found
            elif part.value.startswith("$"):
                matches = list(VARIABLE.finditer(part.value))
                for match in matches:
                    name = match[1] or match[2]
                    if name not in TCL_VARIABLES:
                        return issue(f"undeclared variable '${name}' in path operand")
                    if idx == 0 and name in {"PDK", "env(PDK)"}:
                        return issue("PDK is a suffix component, not a filesystem root", "use $PDK_ROOT/$PDK/... in Tcl/tcleval")

        raw_parts = [p.value.strip("\"'") for p in parts]
        if raw_parts[0].startswith("$"):
            var_part = raw_parts[0]
            rest_parts = raw_parts[1:]
            m_var = VARIABLE.match(var_part)
            if not m_var:
                return issue("unsupported variable syntax in path operand")
            var_name = m_var[1] or m_var[2]
            if var_name not in TCL_VARIABLES and not in_control:
                return issue(f"undeclared variable '${var_name}' in path operand")
            if var_name in {"PDK", "env(PDK)"}:
                return issue("PDK is a suffix component, not a filesystem root", "use $PDK_ROOT/$PDK/... in Tcl/tcleval")

            first_suffix = var_part[m_var.end():].replace("\\", "/")
            clean_suffix = first_suffix.lstrip("/")
            components = []
            if clean_suffix:
                components.append(clean_suffix)
            for p in rest_parts:
                components.append(p.replace("\\", "/").lstrip("/"))
            norm_joined = posixpath.normpath(posixpath.join(*components)) if components else ""

            if var_name in {"SCRIPT_DIR", "env(SCRIPT_DIR)"}:
                if norm_joined == ".." or norm_joined.startswith("../"):
                    return issue("relative path in file join traverses outside repository root")
                if check_existence and not is_runtime_output:
                    missing = _check_root_existence(norm_joined, file_path, line, ref, repo_root, staged_paths)
                    if missing:
                        return missing
                return None
            elif norm_joined == ".." or norm_joined.startswith("../"):
                return issue("relative path in file join traverses outside variable root")
            elif var_name in {"PDK_ROOT", "env(PDK_ROOT)"}:
                pdk_stripped = re.sub(r"^(\$(?:\{PDK\}|PDK)|ihp-sg13g2)/", "", norm_joined)
                target_name = Path(pdk_stripped).name
                if target_name not in KNOWN_PDK_MODELS and target_name not in KNOWN_PDK_SYMBOLS:
                    if check_existence and not is_runtime_output:
                        missing = _check_local_existence(pdk_stripped, file_path, line, repo_root, staged_paths)
                        if missing:
                            return Violation(
                                file_path, line, ref,
                                f"referenced local symbol or dependency does not exist: {ref}",
                                "verify the referenced file exists in the repository or PDK",
                            )
                return None
            return None
        else:
            joined_full = posixpath.normpath(posixpath.join(posixpath.dirname(file_path), *raw_parts))
            if joined_full == ".." or joined_full.startswith("../"):
                return issue("relative path in file join traverses outside repository root")
            if check_existence and not is_runtime_output:
                missing = _check_local_existence(joined_full, file_path, line, repo_root, staged_paths)
                if missing:
                    return Violation(
                        file_path, line, ref,
                        f"referenced local symbol or dependency does not exist: {ref}",
                        "verify the referenced file exists in the repository or PDK",
                    )
            return None

    obsolete = re.search(r"IHP-Open-PDK/.*/libs\.ref/sg13g2_io/xschem/([^/]+)$", ref)
    if obsolete:
        return issue("obsolete PDK IO library prefix", f"use bare IO symbol name {obsolete[1]!r}")

    if re.match(r"^[A-Za-z]:", ref):
        return issue("Windows drive path is not portable")
    if ref.startswith(("\\", "//")):
        return issue("UNC or Windows rooted path is not portable")
    if ref.startswith("/") or ref.lower().startswith("file:"):
        return issue("literal absolute POSIX path is not portable")
    if ref.startswith("~"):
        return issue("tilde expansion depends on the user's environment")

    root_match = VARIABLE.match(ref)
    if root_match:
        root_name = root_match[1] or root_match[2]
        if root_name in {"PDK", "env(PDK)"}:
            return issue("PDK is a suffix component, not a filesystem root", "use $PDK_ROOT/$PDK/... in Tcl/tcleval")
        if root_name not in TCL_VARIABLES and not in_control:
            return issue(f"undeclared variable '${root_name}' in path operand")

        raw_suffix = ref[root_match.end():].replace("\\", "/").lstrip("/")
        normalized_suffix = posixpath.normpath(raw_suffix) if raw_suffix else ""

        if root_name in {"SCRIPT_DIR", "env(SCRIPT_DIR)"}:
            if normalized_suffix == ".." or normalized_suffix.startswith("../"):
                return issue("relative path traverses outside repository root")
            if check_existence and not is_runtime_output:
                missing = _check_root_existence(normalized_suffix, file_path, line, ref, repo_root, staged_paths)
                if missing:
                    return missing
            return None
        elif normalized_suffix == ".." or normalized_suffix.startswith("../"):
            return issue("relative path traverses outside variable root")
        elif root_name in {"PDK_ROOT", "env(PDK_ROOT)"}:
            pdk_stripped = re.sub(r"^(\$(?:\{PDK\}|PDK)|ihp-sg13g2)/", "", normalized_suffix)
            target_name = Path(pdk_stripped).name
            if target_name in KNOWN_PDK_MODELS or target_name in KNOWN_PDK_SYMBOLS:
                return None
            if check_existence and not is_runtime_output:
                missing = _check_local_existence(pdk_stripped, file_path, line, repo_root, staged_paths)
                if missing:
                    return Violation(
                        file_path, line, ref,
                        f"referenced local symbol or dependency does not exist: {ref}",
                        "verify the referenced file exists in the repository or PDK",
                    )
            return None

    ng_vars = _extract_ngspice_vars(ref)
    cleaned_ref = ref

    if ng_vars:
        if in_control:
            active_vars = control_vars or set()
            for matched_token, var_name in ng_vars:
                if var_name not in active_vars:
                    return issue(
                        f"unassigned ngspice variable '${var_name}' in .control path operand",
                        "assign the variable with 'set' or 'let' in .control before use",
                    )
                cleaned_ref = cleaned_ref.replace(matched_token, "_VAR_")
        elif tcl:
            matches = list(VARIABLE.finditer(ref))
            for match in matches:
                name = match[1] or match[2]
                if name not in TCL_VARIABLES:
                    return issue(f"undeclared variable '${name}' in path operand")
            cleaned_ref = VARIABLE.sub("_VAR_", ref)
        else:
            first_var = ng_vars[0][1]
            return issue(
                f"ngspice variable '${first_var}' used outside .control block",
                "ngspice variable expansion is only valid inside .control",
            )
    else:
        matches = list(VARIABLE.finditer(ref))
        if "$" in VARIABLE.sub("", ref):
            return issue("unsupported variable syntax in path operand")
        for match in matches:
            name = match[1] or match[2]
            if not tcl:
                return issue(f"variable '${name}' used outside Tcl/tcleval interpolation")
            if name not in TCL_VARIABLES:
                return issue(f"undeclared variable '${name}' in path operand")
        if matches:
            cleaned_ref = VARIABLE.sub("_VAR_", ref)

    path = cleaned_ref.replace("\\", "/")
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(file_path), path))
    if normalized == ".." or normalized.startswith("../"):
        return issue("relative path traverses outside repository root")

    if check_existence and not is_runtime_output:
        missing = _check_local_existence(ref, file_path, line, repo_root, staged_paths)
        if missing:
            return missing

    return None


def _scan_tcl(
    text: str,
    file_path: str,
    base_line: int,
    repo_root: Path | None = None,
    staged_paths: set[str] | None = None,
    check_existence: bool = False,
) -> list[Violation]:
    violations: list[Violation] = []
    for words in _commands(text):
        values = [word.value for word in words]
        operand = None
        if values[:2] == ["xschem", "raw_read"] and len(words) >= 3:
            operand = words[2]
        elif values[0] == "source":
            index = 3 if values[1:2] == ["-encoding"] else 1
            if index < len(words):
                operand = words[index]
        elif values[0] == "load":
            index = 1
            while index < len(words) and words[index].value.startswith("-"):
                index += 1
            if index < len(words):
                operand = words[index]
        if operand:
            line = base_line + text.count("\n", 0, operand.start)
            found = _path_issue(
                operand.value,
                file_path,
                line,
                tcl=not operand.braced,
                in_control=False,
                is_runtime_output=False,
                repo_root=repo_root,
                check_existence=check_existence,
                staged_paths=staged_paths,
            )
            if found:
                violations.append(found)
    return violations


def _scan_spice(
    text: str,
    file_path: str,
    base_line: int,
    tcl: bool,
    repo_root: Path | None = None,
    staged_paths: set[str] | None = None,
    check_existence: bool = False,
) -> list[Violation]:
    violations: list[Violation] = []
    raw_lines = text.splitlines()
    logical_lines: list[tuple[int, str]] = []

    for offset, raw_line in enumerate(raw_lines):
        line_no = base_line + offset
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(("*", "$ ", ";", "//")):
            continue
        if stripped.startswith("+") and logical_lines:
            prev_line_no, prev_text = logical_lines[-1]
            logical_lines[-1] = (prev_line_no, prev_text + " " + stripped[1:].strip())
        else:
            logical_lines.append((line_no, stripped))

    in_control = False
    control_vars: set[str] = set()

    for number, stripped in logical_lines:
        words = _spice_words(stripped)
        if not words:
            continue
        if words[0].value.lower() == "inline":
            words = words[1:]
        if not words:
            continue

        cmd = words[0].value.lower()

        if cmd == ".control":
            in_control = True
            control_vars = set()
            continue
        elif cmd == ".endc":
            in_control = False
            control_vars = set()
            continue

        if in_control:
            if cmd == "let" and len(words) >= 2:
                assignment = " ".join(w.value for w in words[1:])
                m_let = re.match(r"^([A-Za-z_]\w*)\s*=", assignment)
                if m_let:
                    control_vars.add(m_let.group(1))
            elif cmd == "set" and len(words) >= 2:
                assignment = " ".join(w.value for w in words[1:])
                found_assignments = re.findall(r"\b([A-Za-z_]\w*)\s*=", assignment)
                if found_assignments:
                    for var in found_assignments:
                        control_vars.add(var)
                else:
                    first_ident = words[1].value.split("=")[0].strip()
                    if re.match(r"^[A-Za-z_]\w*$", first_ident):
                        control_vars.add(first_ident)

        operands: list[Word] = []
        is_runtime = False
        check_exist = False

        if cmd in {"write", "wrdata"}:
            operands = words[1:2]
            is_runtime = True
            check_exist = False
        elif cmd in {".include", ".inc"}:
            operands = words[1:2]
            is_runtime = False
            check_exist = check_existence
        elif cmd == ".lib":
            if len(words) >= 2:
                operands = words[1:2]
                is_runtime = False
                check_exist = check_existence
        elif cmd in {"source", "load"}:
            operands = words[1:]
            is_runtime = False
            check_exist = check_existence

        for operand in operands:
            found = _path_issue(
                operand.value,
                file_path,
                number,
                tcl=tcl,
                in_control=in_control,
                control_vars=control_vars,
                is_runtime_output=is_runtime,
                repo_root=repo_root,
                check_existence=check_exist,
                staged_paths=staged_paths,
            )
            if found:
                violations.append(found)

    return violations


def _attribute_word(text: str, pos: int) -> Word:
    if text[pos] != '"':
        return _word(text, pos)
    start = pos + 1
    pos = start
    while pos < len(text):
        if text[pos] == "\\" and pos + 1 < len(text):
            pos += 2
            continue
        if text[pos] == '"':
            remaining = text[pos + 1:].lstrip()
            if not remaining or re.match(r"\w+\s*=", remaining):
                return Word(text[start:pos], start, pos + 1)
        pos += 1
    raise ValueError("unclosed quoted attribute")


def _attributes(text: str) -> dict[str, Word]:
    attrs: dict[str, Word] = {}
    pos = 0
    while pos < len(text):
        if text[pos].isspace() or text[pos] == ";":
            pos += 1
            continue
        match = re.match(r"([\w]+)\s*=\s*", text[pos:])
        if not match:
            pos = _word(text, pos).end
            continue
        key = match[1].lower()
        pos += match.end()
        if pos >= len(text):
            break
        token = _attribute_word(text, pos)
        value = token.value.replace('\\"', '"').replace("\\{", "{").replace("\\}", "}")
        attrs[key] = Word(value, token.start, token.end, token.braced)
        pos = token.end
    return attrs


def _scan_attrs(
    text: str,
    file_path: str,
    base_line: int,
    parent_tcl: bool = False,
    template: bool = False,
    repo_root: Path | None = None,
    staged_paths: set[str] | None = None,
    check_existence: bool = False,
) -> list[Violation]:
    violations: list[Violation] = []
    attrs = _attributes(text)
    format_word = attrs.get("format")
    if format_word:
        tcl = bool(re.search(r"\btcleval\s*\(", format_word.value))
    else:
        tcl = parent_tcl
    for key, token in attrs.items():
        line = base_line + text.count("\n", 0, token.start)
        if key in FILE_ATTRS:
            check_exist = False
            if check_existence:
                if key in {"schematic", "file", "spice_file"}:
                    check_exist = True
                elif key == "model":
                    val = token.value.lower()
                    check_exist = bool("/" in val or any(val.endswith(ext) for ext in (".lib", ".spice", ".mod", ".cir")))
            found = _path_issue(
                token.value, file_path, line, tcl=False, repo_root=repo_root,
                check_existence=check_exist, staged_paths=staged_paths,
            )
            if found:
                violations.append(found)
        elif key == "tclcommand":
            violations.extend(_scan_tcl(token.value, file_path, line, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence))
        elif key in {"value", "code"}:
            violations.extend(_scan_spice(token.value, file_path, line, tcl=tcl, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence))
        elif key == "format":
            val = token.value
            m_eval = re.search(r"\btcleval\s*\((.*)\)\s*$", val, re.DOTALL)
            if m_eval:
                val = m_eval.group(1)
            violations.extend(_scan_spice(val, file_path, line, tcl=tcl, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence))
        elif key == "template" and not template:
            violations.extend(
                _scan_attrs(token.value, file_path, line, parent_tcl=tcl, template=True, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence)
            )
    return violations


def parse_content(
    content: str,
    file_rel_path: str,
    repo_root: Path | None = None,
    staged_paths: set[str] | None = None,
    check_existence: bool = False,
) -> list[Violation]:
    violations: list[Violation] = []
    pos = 0
    try:
        if Path(file_rel_path).suffix.lower() in {".spice", ".cir"}:
            return _scan_spice(content, file_rel_path, 1, tcl=False, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence)
        offsets = [0] + [match.end() for match in re.finditer("\n", content)]
        while pos < len(content):
            if content[pos].isspace():
                pos += 1
                continue
            start = pos
            record = content[pos]
            pos += 1
            words: list[Word] = []
            while pos < len(content) and content[pos] != "\n":
                if content[pos].isspace() or content[pos] == ";":
                    pos += 1
                    continue
                token = _word(content, pos)
                words.append(token)
                pos = token.end
            line = bisect_right(offsets, start)
            if record == "C":
                if len(words) != 6 or not words[0].braced or not words[-1].braced:
                    raise ValueError("malformed component record: expected symbol, four coordinates and attributes")
                found = _path_issue(
                    words[0].value, file_rel_path, line, tcl=False,
                    repo_root=repo_root, check_existence=check_existence, staged_paths=staged_paths,
                )
                if found:
                    violations.append(found)
                attrs = words[-1]
                violations.extend(
                    _scan_attrs(attrs.value, file_rel_path, bisect_right(offsets, attrs.start), repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence)
                )
            elif record == "K" and words:
                violations.extend(
                    _scan_attrs(words[0].value, file_rel_path, bisect_right(offsets, words[0].start), repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence)
                )
            elif record in {"S", "V", "E", "G"} and words:
                violations.extend(
                    _scan_spice(words[0].value, file_rel_path, bisect_right(offsets, words[0].start), tcl=False, repo_root=repo_root, staged_paths=staged_paths, check_existence=check_existence)
                )
    except ValueError as error:
        violations.append(Violation(
            file_rel_path, content.count("\n", 0, pos) + 1, "",
            f"cannot statically parse source: {error}", "use well-formed literal or approved-variable path syntax",
        ))
    return violations


def _git_run(args: list[str], repo_root: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git"] + args, cwd=repo_root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=True,
    )


def run_checker(
    staged: bool,
    repo_root_arg: str | None,
    check_existence: bool = False,
) -> tuple[int, list[Violation], int]:
    violations: list[Violation] = []
    checked = 0
    try:
        root = Path(repo_root_arg) if repo_root_arg else Path(os.fsdecode(
            _git_run(["rev-parse", "--show-toplevel"], Path.cwd()).stdout
        ).strip())
        root = root.resolve()

        if staged:
            raw_stage = _git_run(["ls-files", "--stage", "-z"], root).stdout
            stage_zero_blobs: dict[str, str] = {}
            stage_zero_paths: set[str] = set()
            for entry in raw_stage.split(b"\0"):
                if not entry:
                    continue
                header, raw_path = entry.split(b"\t", 1)
                mode, oid, stage = header.decode("ascii").split()
                path = os.fsdecode(raw_path)
                if mode == "160000":
                    continue
                if stage == "0":
                    stage_zero_paths.add(path)
                    stage_zero_blobs[path] = oid
                else:
                    violations.append(Violation(path, 1, path, "unmerged source file in index", "resolve merge conflict"))
                if mode == "120000" and path.lower().endswith(TARGET_EXTENSIONS):
                    violations.append(Violation(path, 1, path, "symlink .sch/.sym source not allowed", "use a regular source file"))

            raw_diff = _git_run(["diff", "--cached", "--name-status", "-z"], root).stdout
            tokens = [os.fsdecode(t) for t in raw_diff.split(b"\0") if t]
            staged_modified_sources: set[str] = set()
            has_deletions_or_renames = False

            pos = 0
            while pos < len(tokens):
                status = tokens[pos][0]
                pos += 1
                if status in {"R", "C"}:
                    pos += 1
                    new_p = tokens[pos]
                    pos += 1
                    if status == "R":
                        has_deletions_or_renames = True
                    if new_p.lower().endswith(TARGET_EXTENSIONS):
                        staged_modified_sources.add(new_p)
                elif status == "D":
                    pos += 1
                    has_deletions_or_renames = True
                else:
                    p = tokens[pos]
                    pos += 1
                    if p.lower().endswith(TARGET_EXTENSIONS):
                        staged_modified_sources.add(p)

            if check_existence and has_deletions_or_renames:
                sources_to_check = [p for p in sorted(stage_zero_paths) if p.lower().endswith(TARGET_EXTENSIONS)]
            else:
                sources_to_check = [p for p in sorted(staged_modified_sources) if p in stage_zero_paths]

            for path in sources_to_check:
                oid = stage_zero_blobs[path]
                content = _git_run(["cat-file", "blob", oid], root).stdout.decode("utf-8", errors="replace")
                checked += 1
                violations.extend(parse_content(content, path, repo_root=root, staged_paths=stage_zero_paths, check_existence=check_existence))

        else:
            tracked_output = _git_run(["ls-files", "-z"], root).stdout
            tracked_paths = [os.fsdecode(token) for token in tracked_output.split(b"\0") if token]

            untracked_output = _git_run(["ls-files", "--others", "--exclude-standard", "-z"], root).stdout
            untracked_paths = [os.fsdecode(token) for token in untracked_output.split(b"\0") if token]

            all_paths = sorted(set(tracked_paths + untracked_paths))
            for path in all_paths:
                if not path.lower().endswith(TARGET_EXTENSIONS):
                    continue
                full = root / path
                if not full.exists():
                    continue
                if full.is_symlink() or any(parent.is_symlink() for parent in full.parents if parent != root and root in parent.parents):
                    violations.append(Violation(path, 1, path, "working-tree source traverses symlink", "use a regular source file"))
                    continue
                if not full.is_file():
                    continue
                content = full.read_text(encoding="utf-8", errors="replace")
                checked += 1
                violations.extend(parse_content(content, path, repo_root=root, staged_paths=None, check_existence=check_existence))

    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError, IndexError) as error:
        violations.append(Violation("git", 1, "", f"path check failed: {error}", "fix the read/index error and retry"))
    return int(bool(violations)), violations, checked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Statically check tracked Xschem and SPICE path references")
    parser.add_argument("--staged", action="store_true", help="check changed index blobs, not working-tree files")
    parser.add_argument(
        "--check-existence",
        action="store_true",
        help="verify referenced local files and dependencies exist on disk or in the index (dependency audit)",
    )
    parser.add_argument("--repo-root", help="repository to inspect (defaults to current repository)")
    args = parser.parse_args(argv)
    code, violations, count = run_checker(args.staged, args.repo_root, check_existence=args.check_existence)
    for violation in violations:
        print(violation.format(), file=sys.stderr)
    if violations:
        if args.check_existence:
            dep_count = sum(1 for v in violations if "does not exist" in v.message)
            port_count = len(violations) - dep_count
            if dep_count and port_count:
                print(
                    f"Checked {count} file(s). Found {len(violations)} violation(s) "
                    f"({port_count} path portability, {dep_count} dependency audit).",
                    file=sys.stderr,
                )
            elif dep_count:
                print(
                    f"Checked {count} file(s). Found {len(violations)} dependency audit violation(s).",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Checked {count} file(s). Found {len(violations)} path portability violation(s).",
                    file=sys.stderr,
                )
        else:
            print(f"Checked {count} file(s). Found {len(violations)} path portability violation(s).", file=sys.stderr)
    else:
        label = "path portability and dependency audit" if args.check_existence else "path portability"
        print(f"Checked {count} file(s). 0 {label} violations found.")
    return code


if __name__ == "__main__":
    sys.exit(main())
