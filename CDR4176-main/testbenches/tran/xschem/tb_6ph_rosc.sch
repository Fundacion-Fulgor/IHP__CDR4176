v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1020 -580 2090 -100 {flags=graph
y1=-0.015
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1
color="12 9"
node="v0_pex
v0"}
N 1040 -850 1070 -850 {lab=vc}
N 1220 -680 1220 -650 {lab=vss}
N 1220 -910 1220 -880 {lab=vdd}
N 1370 -830 1470 -830 {lab=v0}
N 1370 -810 1470 -810 {lab=v3}
N 1370 -770 1470 -770 {lab=v5}
N 1370 -750 1470 -750 {lab=v4}
N 1370 -790 1470 -790 {lab=v2}
N 1370 -730 1470 -730 {lab=v1}
N 1570 -940 1570 -910 {lab=vc}
N 1570 -850 1570 -820 {lab=GND}
N 1570 -680 1570 -650 {lab=GND}
N 1570 -770 1570 -740 {lab=vss}
N 1690 -680 1690 -650 {lab=GND}
N 1690 -770 1690 -740 {lab=vdd}
C {devices/code_shown.sym} 80 -510 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
*.include sg13g2_stdcell.spice

"}
C {devices/launcher.sym} 170 -765 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir 6ph_rosc.raw] tran"
}
C {devices/launcher.sym} 168.125 -708.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {devices/code.sym} 725 -775 0 0 {name=s1 only_toplevel=false 
value="
.options rshunt = 1e12
.save v(v0) v(v1) v(v2) v(v3) v(v4) v(v5) v(v6) v(v0_pex) v(v1_pex) v(v2_pex) v(v3_pex) v(v4_pex) v(v5_pex) v(v6_pex)
.tran 2p 20n


.control
run
set color0=white

set filetype = ascii
write 6ph_rosc.raw

*let period_0 = T0
*let period_1 = T1
*let period_2 = T2


meas tran T0 TRIG v(v0) VAL=0.6 RISE=5 TARG v(v0) VAL=0.6 RISE=6
meas tran T0_pex TRIG v(v0_pex) VAL=0.6 RISE=5 TARG v(v0_pex) VAL=0.6 RISE=6

let freq_0 = 1/T0

plot freq_0

.endc
"}
C {devices/lab_pin.sym} 1040 -850 0 0 {name=p12 sig_type=std_logic lab=vc}
C {devices/lab_pin.sym} 1220 -650 0 0 {name=p13 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 1220 -910 2 0 {name=p15 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1470 -830 2 0 {name=p16 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} 1470 -810 2 0 {name=p17 sig_type=std_logic lab=v3}
C {devices/lab_pin.sym} 1470 -770 2 0 {name=p18 sig_type=std_logic lab=v5}
C {devices/lab_pin.sym} 1470 -750 2 0 {name=p19 sig_type=std_logic lab=v4}
C {devices/lab_pin.sym} 1470 -790 2 0 {name=p20 sig_type=std_logic lab=v2}
C {devices/lab_pin.sym} 1470 -730 2 0 {name=p21 sig_type=std_logic lab=v1}
C {6ph_rosc/6ph_rosc.sym} 1220 -780 0 0 {name=x1
}
C {devices/lab_pin.sym} 1570 -940 2 0 {name=p22 sig_type=std_logic lab=vc}
C {devices/vsource.sym} 1570 -880 0 0 {name=Vdd2 value=0.9 savecurrent=false
}
C {devices/gnd.sym} 1570 -820 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 1570 -710 0 0 {name=Vdd5 value=0 savecurrent=false
}
C {devices/gnd.sym} 1570 -650 0 0 {name=l2 lab=GND
value=0}
C {devices/lab_pin.sym} 1570 -770 2 0 {name=p23 sig_type=std_logic lab=vss}
C {devices/vsource.sym} 1690 -710 0 0 {name=Vdd6 value=1.2 savecurrent=false
}
C {devices/gnd.sym} 1690 -650 0 0 {name=l3 lab=GND}
C {devices/lab_pin.sym} 1690 -770 2 0 {name=p24 sig_type=std_logic lab=vdd}
