v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 950 -570 2020 -90 {flags=graph
y1=-0.02
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
v3_pex"}
N 50 -340 50 -310 {lab=vc_pex}
N 50 -250 50 -220 {lab=GND}
N 260 -310 290 -310 {lab=vc_pex}
N 50 -80 50 -50 {lab=GND}
N 50 -170 50 -140 {lab=vss_pex}
N 170 -80 170 -50 {lab=GND}
N 170 -170 170 -140 {lab=vdd_pex}
N 440 -140 440 -110 {lab=vss_pex}
N 440 -370 440 -340 {lab=vdd_pex}
N 590 -290 690 -290 {lab=v0_pex}
N 590 -270 690 -270 {lab=v3_pex}
N 590 -230 690 -230 {lab=v5_pex}
N 590 -210 690 -210 {lab=v4_pex}
N 590 -250 690 -250 {lab=v2_pex}
N 590 -190 690 -190 {lab=v1_pex}
C {devices/lab_pin.sym} 50 -340 2 0 {name=p3 sig_type=std_logic lab=vc_pex}
C {devices/vsource.sym} 50 -280 0 0 {name=Vdd4 value=0.9 savecurrent=false
}
C {devices/gnd.sym} 50 -220 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} 260 -310 0 0 {name=p1 sig_type=std_logic lab=vc_pex}
C {devices/vsource.sym} 50 -110 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} 50 -50 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} 50 -170 2 0 {name=p14 sig_type=std_logic lab=vss_pex}
C {devices/vsource.sym} 170 -110 0 0 {name=Vdd1 value=1.2 savecurrent=false
}
C {devices/gnd.sym} 170 -50 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} 170 -170 2 0 {name=p8 sig_type=std_logic lab=vdd_pex}
C {devices/lab_pin.sym} 440 -110 0 0 {name=p2 sig_type=std_logic lab=vss_pex}
C {devices/lab_pin.sym} 440 -370 2 0 {name=p4 sig_type=std_logic lab=vdd_pex}
C {devices/lab_pin.sym} 690 -290 2 0 {name=p9 sig_type=std_logic lab=v0_pex}
C {devices/lab_pin.sym} 690 -270 2 0 {name=p5 sig_type=std_logic lab=v3_pex}
C {devices/lab_pin.sym} 690 -230 2 0 {name=p6 sig_type=std_logic lab=v5_pex}
C {devices/lab_pin.sym} 690 -210 2 0 {name=p7 sig_type=std_logic lab=v4_pex}
C {devices/lab_pin.sym} 690 -250 2 0 {name=p10 sig_type=std_logic lab=v2_pex}
C {devices/lab_pin.sym} 690 -190 2 0 {name=p11 sig_type=std_logic lab=v1_pex}
C {devices/code_shown.sym} 10 -500 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
*.include sg13g2_stdcell.spice

"}
C {devices/code_shown.sym} 20 -600 0 0 {name=MODEL2 only_toplevel=true
format="tcleval( @value )"
value="
.include \"$SCRIPT_DIR/CDR4176-main/schematic/xschem/6ph_rosc/6ph_rosc_pex.spice\"
"}
C {devices/launcher.sym} 100 -755 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir 6ph_rosc_pex.raw] tran"
}
C {devices/launcher.sym} 98.125 -698.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {devices/code.sym} 655 -765 0 0 {name=s1 only_toplevel=false 
value="
.options rshunt = 1e12
.save v(v0) v(v1) v(v2) v(v3) v(v4) v(v5) v(v6) v(v0_pex) v(v1_pex) v(v2_pex) v(v3_pex) v(v4_pex) v(v5_pex) v(v6_pex)
.tran 2p 20n

.control
run
set color0=white
set filetype = ascii
write 6ph_rosc_pex.raw

*let period_0 = T0
*let period_1 = T1
*let period_2 = T2


meas tran T0 TRIG v(v0) VAL=0.6 RISE=5 TARG v(v0) VAL=0.6 RISE=6
meas tran T0_pex TRIG v(v0_pex) VAL=0.6 RISE=5 TARG v(v0_pex) VAL=0.6 RISE=6

let freq_0 = 1/T0
let freq_0_pex = 1/T0_pex

plot freq_0 freq_0_pex

.endc
"}
C {6ph_rosc/6ph_rosc_pex.sym} 440 -240 0 0 {name=x2
}
C {devices/launcher.sym} 110 -815 0 0 {name=h2
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir 6ph_rosc.raw] tran"
}
