v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 -1240 -1780 -170 -1300 {flags=graph
y1=-0.073
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=5e-09
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1
color="12 9 7 10"
node="v0
v90
v180
v270"}
B 2 -2350 -1920 -1280 -1440 {flags=graph
y1=-0.064
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=5e-09
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v0
vout
v90"
color="10 6 11"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=2}
N -2350 -1050 -2350 -1020 {lab=vc}
N -2350 -960 -2350 -930 {lab=GND}
N -2140 -1020 -2110 -1020 {lab=vc}
N -2350 -790 -2350 -760 {lab=GND}
N -2350 -880 -2350 -850 {lab=vss}
N -1960 -900 -1960 -870 {lab=vss}
N -2230 -790 -2230 -760 {lab=GND}
N -2230 -880 -2230 -850 {lab=vdd}
N -1960 -1090 -1960 -1060 {lab=vdd}
N -1810 -1020 -1710 -1020 {lab=v0}
N -1810 -1000 -1710 -1000 {lab=v90}
N -1810 -960 -1710 -960 {lab=v180}
N -1810 -940 -1710 -940 {lab=v270}
N -1220 -1230 -1220 -1210 {lab=vdd}
N -1220 -1130 -1220 -1110 {lab=vss}
N -1150 -1170 -1105 -1170 {lab=#net1}
N -1105 -1170 -1105 -1145 {lab=#net1}
N -1105 -1080 -1105 -1065 {lab=vss}
N -1290 -1170 -1270 -1170 {lab=v0}
N -815 -1230 -815 -1210 {lab=vdd}
N -815 -1130 -815 -1110 {lab=vss}
N -745 -1170 -700 -1170 {lab=#net2}
N -700 -1170 -700 -1145 {lab=#net2}
N -700 -1080 -700 -1065 {lab=vss}
N -885 -1170 -865 -1170 {lab=v90}
N -1215 -985 -1215 -965 {lab=vdd}
N -1215 -885 -1215 -865 {lab=vss}
N -1145 -925 -1100 -925 {lab=#net3}
N -1100 -925 -1100 -900 {lab=#net3}
N -1100 -835 -1100 -820 {lab=vss}
N -1285 -925 -1265 -925 {lab=v180}
N -810 -990 -810 -970 {lab=vdd}
N -810 -890 -810 -870 {lab=vss}
N -740 -930 -695 -930 {lab=#net4}
N -695 -930 -695 -905 {lab=#net4}
N -695 -840 -695 -825 {lab=vss}
N -880 -930 -860 -930 {lab=v270}
C {devices/lab_pin.sym} -2350 -1050 2 0 {name=p3 sig_type=std_logic lab=vc}
C {devices/vsource.sym} -2350 -990 0 0 {name=Vdd4 value=0.9 savecurrent=false
}
C {devices/gnd.sym} -2350 -930 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} -2140 -1020 0 0 {name=p1 sig_type=std_logic lab=vc}
C {devices/vsource.sym} -2350 -820 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} -2350 -760 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} -2350 -880 2 0 {name=p14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1960 -870 2 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/vsource.sym} -2230 -820 0 0 {name=Vdd1 value=1.2 savecurrent=false
}
C {devices/gnd.sym} -2230 -760 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} -2230 -880 2 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1960 -1090 2 0 {name=p4 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1710 -1020 2 0 {name=p9 sig_type=std_logic lab=v0}
C {devices/code_shown.sym} -2370 -1390 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.inc /foss/designs/IHP__CDR4176/CDR4176-main/netlist/pex/clock_gen_pex.spice

"}
C {devices/code.sym} -2335 -1255 0 0 {name=s1 only_toplevel=false 
value="
.options rshunt = 1e9
.options method=gear reltol=5e-3 abstol=1e-8 vntol=1e-4
.save v(v0) v(v90) v(v180) v(v270) 



.control
	set ngdebug
	set verbose
	tran 5p 29n
	
set color0=white 
write rosc.raw


*meas tran SKEW0_1 TRIG v(v0) VAL=0.6 RISE=3 TARG v(v1) VAL=0.6 RISE=4
*meas tran SKEW1_2 TRIG v(v1) VAL=0.6 RISE=3 TARG v(v2) VAL=0.6 RISE=4
*meas tran SKEW2_3 TRIG v(v2) VAL=0.6 RISE=3 TARG v(v3) VAL=0.6 RISE=4
*meas tran SKEW3_4 TRIG v(v3) VAL=0.6 RISE=3 TARG v(v4) VAL=0.6 RISE=5
*meas tran SKEW4_5 TRIG v(v4) VAL=0.6 RISE=3 TARG v(v5) VAL=0.6 RISE=4
*meas tran SKEW5_0 TRIG v(v5) VAL=0.6 RISE=3 TARG v(v0) VAL=0.6 RISE=4


*meas tran T0 TRIG v(v0) VAL=0.6 RISE=3 TARG v(v0) VAL=0.6 RISE=4
*meas tran T1 TRIG v(v1) VAL=0.6 RISE=3 TARG v(v1) VAL=0.6 RISE=4
*meas tran T2 TRIG v(v2) VAL=0.6 RISE=3 TARG v(v2) VAL=0.6 RISE=4
*meas tran T3 TRIG v(v3) VAL=0.6 RISE=3 TARG v(v3) VAL=0.6 RISE=4
*meas tran T4 TRIG v(v4) VAL=0.6 RISE=3 TARG v(v4) VAL=0.6 RISE=4
*meas tran T5 TRIG v(v5) VAL=0.6 RISE=3 TARG v(v5) VAL=0.6 RISE=4

*let period_0 = T0
*let period_1 = T1
*let period_2 = T2
*let period_3 = T3
*let period_4 = T4
*let period_5 = T5

*let phase0_1 = ((SKEW0_1 / period_0) * 360) -360 
*let phase1_2 = ((SKEW1_2 / period_0) * 360) -360 
*let phase2_3 = ((SKEW2_3 / period_0) * 360) -360 
*let phase3_4 = ((SKEW3_4 / period_0) * 360) -360 
*let phase4_5 = ((SKEW4_5 / period_0) * 360) -360 
*let phase5_0 = ((SKEW5_0 / period_0) * 360) -360 

*let freq0 = 1/T0
*let freq5 = 1/T5

*meas tran PW0 TRIG v(v0) VAL=0.6 RISE=3 TARG v(v0) VAL=0.6 FALL=4
*meas tran PW1 TRIG v(v1) VAL=0.6 RISE=3 TARG v(v1) VAL=0.6 FALL=4
*meas tran PW2 TRIG v(v2) VAL=0.6 RISE=3 TARG v(v2) VAL=0.6 FALL=4
*meas tran PW3 TRIG v(v3) VAL=0.6 RISE=3 TARG v(v3) VAL=0.6 FALL=4
*meas tran PW4 TRIG v(v4) VAL=0.6 RISE=3 TARG v(v4) VAL=0.6 FALL=4
*meas tran PW5 TRIG v(v5) VAL=0.6 RISE=3 TARG v(v5) VAL=0.6 FALL=4

*let Duty0 = PW0 / period_0
*let Duty1 = PW1 / period_1
*let Duty2 = PW2 / period_2
*let Duty3 = PW3 / period_3
*let Duty4 = PW4 / period_4
*let Duty5 = PW5 / period_5

meas tran SKEW0_90 TRIG v(v0) VAL=0.6 RISE=3 TARG v(v90) VAL=0.6 RISE=3
meas tran SKEW90_180 TRIG v(v90) VAL=0.6 RISE=3 TARG v(v180) VAL=0.6 RISE=4
meas tran SKEW180_270 TRIG v(v180) VAL=0.6 RISE=3 TARG v(v270) VAL=0.6 RISE=3
meas tran SKEW270_0 TRIG v(v270) VAL=0.6 RISE=3 TARG v(v0) VAL=0.6 RISE=3

meas tran T0 TRIG v(v0) VAL=0.6 RISE=3 TARG v(v0) VAL=0.6 RISE=4
meas tran T90 TRIG v(v90) VAL=0.6 RISE=3 TARG v(v90) VAL=0.6 RISE=4
meas tran T180 TRIG v(v180) VAL=0.6 RISE=3 TARG v(v180) VAL=0.6 RISE=4
meas tran T270 TRIG v(v270) VAL=0.6 RISE=3 TARG v(v270) VAL=0.6 RISE=4

let period_0 = T0
let period_90 = T90
let period_180 = T180
let period_270 = T270

let phase0_90 = ((SKEW0_90 / period_0) * 360) 
let phase90_180 = ((SKEW90_180 / period_90) * 360) 
let phase180_270 = ((SKEW180_270 / period_180) * 360)
let phase270_0 = ((SKEW270_0 / period_270) * 360)

meas tran PW0 TRIG v(v0) VAL=0.6 RISE=4 TARG v(v0) VAL=0.6 FALL=5
meas tran PW90 TRIG v(v90) VAL=0.6 RISE=3 TARG v(v90) VAL=0.6 FALL=4
meas tran PW180 TRIG v(v180) VAL=0.6 RISE=4 TARG v(v180) VAL=0.6 FALL=4
meas tran PW270 TRIG v(v270) VAL=0.6 RISE=4 TARG v(v270) VAL=0.6 FALL=4

let Duty0 = PW0 / period_0
let Duty90 = PW90 / period_90
let Duty180 = PW180 / period_180
let Duty270 = PW270 / period_270

let freq0 = 1/period_0

print phase0_90 phase90_180 phase180_270 phase270_0 Duty0 Duty90 Duty180 Duty270 freq0

.endc
"}
C {devices/launcher.sym} -2080 -1185 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/rosc.raw tran"
}
C {devices/launcher.sym} -2081.875 -1128.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {devices/lab_pin.sym} -1710 -1000 2 0 {name=p5 sig_type=std_logic lab=v90}
C {devices/lab_pin.sym} -1710 -960 2 0 {name=p6 sig_type=std_logic lab=v180}
C {devices/lab_pin.sym} -1710 -940 2 0 {name=p7 sig_type=std_logic lab=v270}
C {capa.sym} -1105 -1115 0 0 {name=C2
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} -1220 -1230 1 0 {name=p10 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1220 -1110 3 0 {name=p11 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1105 -1065 3 0 {name=p12 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1290 -1170 0 0 {name=p13 sig_type=std_logic lab=v0}
C {capa.sym} -700 -1115 0 0 {name=C1
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} -815 -1230 1 0 {name=p15 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -815 -1110 3 0 {name=p16 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -700 -1065 3 0 {name=p17 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -885 -1170 0 0 {name=p18 sig_type=std_logic lab=v90}
C {capa.sym} -1100 -870 0 0 {name=C3
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} -1215 -985 1 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1215 -865 3 0 {name=p20 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1100 -820 3 0 {name=p21 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1285 -925 0 0 {name=p22 sig_type=std_logic lab=v180}
C {capa.sym} -695 -875 0 0 {name=C4
m=1
value=1p
footprint=1206
device="ceramic capacitor"
}
C {devices/lab_pin.sym} -810 -990 1 0 {name=p23 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -810 -870 3 0 {name=p24 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -695 -825 3 0 {name=p25 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -880 -930 0 0 {name=p26 sig_type=std_logic lab=v270}
C {clock_gen/clock_gen_pex.sym} -1960 -980 0 0 {name=x1}
C {inv_PI/inv_PI.sym} -1310 -1030 0 0 {name=x2}
C {inv_PI/inv_PI.sym} -905 -1030 0 0 {name=x3}
C {inv_PI/inv_PI.sym} -900 -790 0 0 {name=x4}
C {inv_PI/inv_PI.sym} -1305 -785 0 0 {name=x5}
