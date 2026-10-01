v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N -1400 -520 -1400 -480 {lab=iv2}
N -640 -510 -640 -470 {lab=iv1}
N -1400 -420 -1400 -380 {lab=VSS}
N -640 -410 -640 -370 {lab=VSS}
N -1400 -270 -1400 -230 {lab=iv0}
N -1400 -170 -1400 -130 {lab=VSS}
N -1400 -780 -1400 -740 {lab=iv4}
N -640 -770 -640 -730 {lab=iv3}
N -640 -670 -640 -630 {lab=VSS}
N -1400 -680 -1400 -640 {lab=VSS}
N -1150 -30 -1150 10 {lab=VDD}
N -1050 70 -1050 130 {
lab=GND}
N -1050 -30 -1050 10 {lab=VSS}
N -1150 70 -1150 110 {lab=VSS}
N -640 -290 -640 -250 {lab=vcont}
N -640 -190 -640 -150 {lab=VSS}
N 630 -390 630 -370 {lab=#net1}
N 670 -460 680 -460 {lab=VDD}
N 580 -460 590 -460 {lab=VSS}
N 630 -310 630 -300 {lab=VSS}
N 570 -510 630 -510 {lab=vout}
N 630 0 630 20 {lab=#net2}
N 670 -70 680 -70 {lab=VDD}
N 580 -70 590 -70 {lab=VSS}
N 630 80 630 90 {lab=VSS}
N 570 -120 630 -120 {lab=v8i}
N 570 -550 570 -510 {lab=vout}
N 510 -510 570 -510 {lab=vout}
N 570 -170 570 -120 {lab=v8i}
N 510 -120 570 -120 {lab=v8i}
C {devices/vsource.sym} -640 -440 0 0 {name=Vdd9 value="dc 0 ac 0 pulse(0, 1.2, \{2*cyc_p_fase*Tclk\},\{SR_control\},\{SR_control\}, \{2*cyc_p_fase*Tclk\}, \{4*cyc_p_fase*Tclk\})"}
C {devices/vsource.sym} -1400 -450 0 0 {name=Vdd10 value="dc 0 ac 0 pulse(0, 1.2, \{4*cyc_p_fase*Tclk\},\{SR_control\},\{SR_control\}, \{4*cyc_p_fase*Tclk\}, \{8*cyc_p_fase*Tclk\}) "}
C {devices/lab_pin.sym} -1400 -520 0 0 {name=p49 sig_type=std_logic lab=iv2}
C {devices/lab_pin.sym} -640 -510 0 0 {name=p50 sig_type=std_logic lab=iv1}
C {devices/vsource.sym} -1400 -200 0 0 {name=Vdd11 value="dc 0 ac 0 pulse(0, 1.2, \{cyc_p_fase*Tclk\},\{SR_control\},\{SR_control\}, \{cyc_p_fase*Tclk\}, \{2*cyc_p_fase*Tclk\})"}
C {devices/lab_pin.sym} -1400 -270 0 0 {name=p53 sig_type=std_logic lab=iv0}
C {devices/vsource.sym} -640 -700 0 0 {name=Vdd1 value="dc 0 ac 0 pulse(1.2, 0, \{8*cyc_p_fase*Tclk\},\{SR_control\},\{SR_control\}, \{8*cyc_p_fase*Tclk\}, \{16*cyc_p_fase*Tclk\})"}
C {devices/vsource.sym} -1400 -710 0 0 {name=Vdd2 value="dc 0 ac 0 pulse(0, 1.2, \{24*cyc_p_fase*Tclk\},\{SR_control\},\{SR_control\}, \{16*cyc_p_fase*Tclk\}, \{40*cyc_p_fase*Tclk\}) "}
C {devices/lab_pin.sym} -1400 -780 0 0 {name=p11 sig_type=std_logic lab=iv4}
C {devices/lab_pin.sym} -640 -770 0 0 {name=p10 sig_type=std_logic lab=iv3}
C {netlist_not_shown.sym} -1440 -20 0 0 {name=s1 only_toplevel=true 

value="

* Circuit Parameters
.param vdd = 1.2
.param vss = 0.0
.param Tclk = 1375p
.param cyc_p_fase = 4
.param SR_control=110p
.options TEMP = 27.0
.OPTION RSHUNT=1e10

* Include Models
.lib cornerMOSlv.lib mos_tt
.inc /foss/designs/IHP__CDR4176/CDR4176-main/netlist/pex/8xPI_top_pex.spice


* OP Parameters & Singals to save
.save V(vout) V(v8i) I(VI8xPI)

*Simulations
.control
	set output_path = ../../verification/python/
	set ngdebug
	set verbose
	tran 5PS 221NS
	set filetype = ascii
        write \{$output_path\}tran_linearity_8xPI_top_pex.raw 
.endc
.end"}
C {devices/vsource.sym} -1150 40 0 0 {name=Vdd4 value=vdd}
C {devices/lab_pin.sym} -1150 -30 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} -1050 40 0 0 {name=Vdd3 value=vss}
C {devices/gnd.sym} -1050 130 0 0 {name=l6 lab=GND}
C {devices/lab_pin.sym} -1050 -30 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1150 110 2 0 {name=p12 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1400 -640 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -640 -630 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1400 -380 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -640 -370 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1400 -130 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -490 0 0 {name=p7 sig_type=std_logic lab="iv4,iv3,iv2,iv1,iv0"}
C {devices/lab_pin.sym} 390 -410 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 390 -670 0 0 {name=p13 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} -640 -220 0 0 {name=Vdd5 value=0.9}
C {devices/lab_pin.sym} -640 -290 0 0 {name=p9 sig_type=std_logic lab=vcont}
C {devices/lab_pin.sym} -640 -150 2 0 {name=p14 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -460 0 0 {name=p15 sig_type=std_logic lab=vcont}
C {capa.sym} 630 -340 0 0 {name=C1
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} 680 -460 2 0 {name=p68 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -460 0 0 {name=p69 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 630 -300 3 0 {name=p70 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -100 0 0 {name=p16 sig_type=std_logic lab="VSS,VSS,VSS,VSS,VSS"}
C {devices/lab_pin.sym} 390 -20 0 0 {name=p17 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 390 -220 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 250 -70 0 0 {name=p19 sig_type=std_logic lab=vcont}
C {capa.sym} 630 50 0 0 {name=C2
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} 680 -70 2 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 580 -70 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 630 90 3 0 {name=p22 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 570 -550 1 0 {name=p23 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} 570 -170 1 0 {name=p24 sig_type=std_logic lab=v8i}
C {ammeter.sym} 390 -640 0 0 {name=VI8xPI savecurrent=true spice_ignore=0}
C {8xPI_top/8xPI_top_pex.sym} 390 -510 0 0 {name=x6}
C {8xPI_top/8xPI_top_pex.sym} 390 -120 0 0 {name=x1}
C {inv_CDR/inv_CDR.sym} 490 -550 1 0 {name=x2}
C {inv_CDR/inv_CDR.sym} 490 -160 1 0 {name=x3}
