v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1170 -1150 2240 -670 {flags=graph
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
B 2 60 -1290 1130 -810 {flags=graph
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
N 60 -420 60 -390 {lab=vc}
N 60 -330 60 -300 {lab=GND}
N 270 -390 300 -390 {lab=vc}
N 60 -160 60 -130 {lab=GND}
N 60 -250 60 -220 {lab=vss}
N 450 -270 450 -240 {lab=vss}
N 180 -160 180 -130 {lab=GND}
N 180 -250 180 -220 {lab=vdd}
N 450 -460 450 -430 {lab=vdd}
N 600 -390 700 -390 {lab=v0}
N 600 -370 700 -370 {lab=v90}
N 600 -330 700 -330 {lab=v180}
N 600 -310 700 -310 {lab=v270}
N 1170 -210 1170 -180 {lab=GND}
N 1050 -210 1050 -180 {lab="vss, vss"}
N 890 -400 950 -400 {lab=v0}
N 890 -360 950 -360 {lab=v180}
N 890 -320 950 -320 {lab=v90}
N 890 -280 950 -280 {lab=v270}
N 1170 -490 1170 -450 {lab=vdd}
N 1040 -490 1040 -450 {lab="vss, vss, vss, vss, vdd, vdd, vdd, vdd" vss}
N 1370 -330 1470 -330 {lab=vout}
C {clock_gen/clock_gen.sym} 450 -350 0 0 {name=x1}
C {devices/lab_pin.sym} 60 -420 2 0 {name=p3 sig_type=std_logic lab=vc}
C {devices/vsource.sym} 60 -360 0 0 {name=Vdd4 value=0.9 savecurrent=false
}
C {devices/gnd.sym} 60 -300 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} 270 -390 0 0 {name=p1 sig_type=std_logic lab=vc}
C {devices/vsource.sym} 60 -190 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} 60 -130 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} 60 -250 2 0 {name=p14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 450 -240 2 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/vsource.sym} 180 -190 0 0 {name=Vdd1 value=1.2 savecurrent=false
}
C {devices/gnd.sym} 180 -130 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} 180 -250 2 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 450 -460 2 0 {name=p4 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 700 -390 2 0 {name=p9 sig_type=std_logic lab=v0}
C {devices/code_shown.sym} 40 -760 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
*.include sg13g2_stdcell.spice

"}
C {devices/code.sym} 75 -625 0 0 {name=s1 only_toplevel=false 
value="
.save v(v0) v(v1) v(v2) v(v3) v(v4) v(v5) v(v90) v(v270) v(v0_) v(v180) v(vout)

.tran 2p 5n

.control
run
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
C {devices/launcher.sym} 330 -555 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir rosc.raw] tran"
}
C {devices/launcher.sym} 328.125 -498.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {devices/lab_pin.sym} 700 -370 2 0 {name=p5 sig_type=std_logic lab=v90}
C {devices/lab_pin.sym} 700 -330 2 0 {name=p6 sig_type=std_logic lab=v180}
C {devices/lab_pin.sym} 700 -310 2 0 {name=p7 sig_type=std_logic lab=v270}
C {8xPI/8xPI.sym} 930 -190 0 0 {name=x3}
C {devices/gnd.sym} 1170 -180 0 0 {name=l3 lab=GND}
C {devices/lab_pin.sym} 1050 -180 2 0 {name=p13 sig_type=std_logic lab="vss, vss"}
C {devices/lab_pin.sym} 890 -400 0 0 {name=p15 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} 890 -360 0 0 {name=p16 sig_type=std_logic lab=v180}
C {devices/lab_pin.sym} 890 -320 0 0 {name=p17 sig_type=std_logic lab=v90
}
C {devices/lab_pin.sym} 890 -280 0 0 {name=p18 sig_type=std_logic lab=v270}
C {devices/lab_pin.sym} 1170 -490 0 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1040 -490 0 0 {name=p20 sig_type=std_logic lab="vss, vss, vss, vss, vdd, vdd, vdd, vdd"}
C {devices/lab_pin.sym} 1470 -330 2 0 {name=p21 sig_type=std_logic lab=vout}
