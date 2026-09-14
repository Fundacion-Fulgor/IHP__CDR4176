v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 -1103120 -1113200 -1102050 -1112720 {flags=graph
y1=-0.046
y2=1.4
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.6e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v90
v0"
color="4 17"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1}
B 2 -1103120 -1112680 -1102050 -1112200 {flags=graph
y1=-0.069
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.6e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v270
v180"
color="21 17"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1}
B 2 -1101890 -1113220 -1100820 -1112740 {flags=graph
y1=-0.057
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.6e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v180
v90"
color="21 17"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1}
B 2 -1101900 -1112670 -1100830 -1112190 {flags=graph
y1=-0.057
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.6e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="v270
v0"
color="10 17"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1}
B 2 -1101650 -1113730 -1100580 -1113250 {flags=graph
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.6e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="pi_vout
vout"
color="6 10"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1
y1=-0.13}
N -1103560 -1113540 -1103560 -1113510 {lab=GND}
N -1103560 -1113630 -1103560 -1113600 {lab=vdd}
N -1102750 -1113380 -1102750 -1113350 {lab=GND}
N -1102600 -1113500 -1102500 -1113500 {lab=v0}
N -1102600 -1113420 -1102500 -1113420 {lab=v270}
N -1102600 -1113480 -1102500 -1113480 {lab=v90}
N -1102600 -1113440 -1102500 -1113440 {lab=v180}
N -1102750 -1113590 -1102750 -1113540 {lab=vdd}
N -1103480 -1113630 -1103480 -1113600 {lab=vc}
N -1103480 -1113540 -1103480 -1113510 {lab=GND}
N -1102940 -1113500 -1102900 -1113500 {lab=vc}
N -1103560 -1113340 -1103560 -1113310 {lab=GND}
N -1103560 -1113430 -1103560 -1113400 {lab=vss}
N -1102200 -1113330 -1102200 -1113300 {lab="vss, vss"}
N -1102360 -1113520 -1102300 -1113520 {lab=v0}
N -1102360 -1113480 -1102300 -1113480 {lab=v180}
N -1102360 -1113440 -1102300 -1113440 {lab=v90}
N -1102360 -1113400 -1102300 -1113400 {lab=v270}
N -1102080 -1113610 -1102080 -1113570 {lab=vdd}
N -1102210 -1113610 -1102210 -1113570 {lab="vdd, vdd, vdd, vdd, vss, vss, vss, vss" vss}
N -1101880 -1113450 -1101780 -1113450 {lab=pi_vout}
N -1101760 -1113710 -1101760 -1113690 {lab=vdd}
N -1101760 -1113570 -1101760 -1113550 {lab=vss}
N -1101680 -1113570 -1101660 -1113570 {lab=vout}
N -1101660 -1113630 -1101660 -1113570 {lab=vout}
N -1101900 -1113630 -1101870 -1113630 {lab=pi_vout}
N -1102080 -1113330 -1102080 -1113310 {lab=vss}
C {devices/vsource.sym} -1103560 -1113570 0 0 {name=Vdd1 value=\{vdd\} savecurrent=false
}
C {devices/gnd.sym} -1103560 -1113510 0 0 {name=l4 lab=GND}
C {devices/gnd.sym} -1102750 -1113350 0 0 {name=l2 lab=GND}
C {devices/lab_pin.sym} -1102500 -1113420 2 0 {name=p2 sig_type=std_logic lab=v270}
C {devices/lab_pin.sym} -1102500 -1113480 2 0 {name=p4 sig_type=std_logic lab=v90
}
C {devices/lab_pin.sym} -1102500 -1113440 2 0 {name=p5 sig_type=std_logic lab=v180}
C {devices/lab_pin.sym} -1102500 -1113500 2 0 {name=p6 sig_type=std_logic lab=v0}
C {devices/code.sym} -1103875 -1113045 0 0 {name=s1 only_toplevel=false 
value="

.save v(vin1) v(v0) v(v90) v(v270) v(v180) v(vin2) v(vout) v(pi_vout) v(vdd)

.param vdd = 1.14
.options TEMP = -40

.tran 5p 16n
.save all

.control
run
set color0=white
write tran_logic.raw

meas tran ymax MAX v(vdd) from=0 to=1n
let vdd_half = ymax/2


*TT
*meas tran SKEW0_90 TRIG v(v0) VAL=vdd_half RISE=3 TARG v(v90) VAL=vdd_half RISE=4
*meas tran SKEW90_180 TRIG v(v90) VAL=vdd_half RISE=3 TARG v(v180) VAL=vdd_half RISE=3
*meas tran SKEW180_270 TRIG v(v180) VAL=vdd_half RISE=3 TARG v(v270) VAL=vdd_half RISE=4
*meas tran SKEW270_0 TRIG v(v270) VAL=vdd_half RISE=4 TARG v(v0) VAL=vdd_half RISE=3

*FF
*meas tran SKEW0_90 TRIG v(v0) VAL=vdd_half RISE=5 TARG v(v90) VAL=vdd_half RISE=5
*meas tran SKEW90_180 TRIG v(v90) VAL=vdd_half RISE=5 TARG v(v180) VAL=vdd_half RISE=6
*meas tran SKEW180_270 TRIG v(v180) VAL=vdd_half RISE=5 TARG v(v270) VAL=vdd_half RISE=5
*meas tran SKEW270_0 TRIG v(v270) VAL=vdd_half RISE=5 TARG v(v0) VAL=vdd_half RISE=5

*SS
meas tran SKEW0_90 TRIG v(v0) VAL=vdd_half RISE=15 TARG v(v90) VAL=vdd_half RISE=16
meas tran SKEW90_180 TRIG v(v90) VAL=vdd_half RISE=15 TARG v(v180) VAL=vdd_half RISE=16
meas tran SKEW180_270 TRIG v(v180) VAL=vdd_half RISE=15 TARG v(v270) VAL=vdd_half RISE=15
meas tran SKEW270_0 TRIG v(v270) VAL=vdd_half RISE=15 TARG v(v0) VAL=vdd_half RISE=15

meas tran T90 TRIG v(v90) VAL=vdd_half RISE=3 TARG v(v90) VAL=vdd_half RISE=4
meas tran T180 TRIG v(v180) VAL=vdd_half RISE=3 TARG v(v180) VAL=vdd_half RISE=4
meas tran T270 TRIG v(v270) VAL=vdd_half RISE=3 TARG v(v270) VAL=vdd_half RISE=4
meas tran T0 TRIG v(v0) VAL=vdd_half RISE=3 TARG v(v0) VAL=vdd_half RISE=4

let period_0 = T0
let period_90 = T90
let period_180 = T180
let period_270 = T270

let phase0_90 = (SKEW0_90 / period_0) * 360 
let phase90_180 = (SKEW90_180 / period_0) * 360
let phase180_270 = (SKEW180_270 / period_0) * 360
let phase270_0 = (SKEW270_0 / period_0) * 360


meas tran PW0 TRIG v(v0) VAL=vdd_half RISE=3 TARG v(v0) VAL=vdd_half FALL=4
meas tran PW90 TRIG v(v90) VAL=vdd_half RISE=3 TARG v(v90) VAL=vdd_half FALL=4
meas tran PW180 TRIG v(v180) VAL=vdd_half RISE=3 TARG v(v180) VAL=vdd_half FALL=3
meas tran PW270 TRIG v(v270) VAL=vdd_half RISE=3 TARG v(v270) VAL=vdd_half FALL=3

let Duty0 = PW0 / period_0
let Duty90 = PW90 / period_90
let Duty180 = PW180 / period_180
let Duty270 = PW270 / period_270


let freq = 1 / period_0

print SKEW0_90 SKEW90_180 SKEW180_270 SKEW270_0 phase0_90 phase90_180 phase180_270 phase270_0 PW0 PW90 PW180 PW270 Duty0 Duty90 Duty180 Duty270 freq

.endc
"}
C {devices/code_shown.sym} -1103900 -1113160 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_ss
*.include sg13g2_stdcell.spice

"}
C {devices/launcher.sym} -1103320 -1113595 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir tran_logic.raw] tran"
}
C {devices/launcher.sym} -1103321.875 -1113538.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {devices/lab_pin.sym} -1103480 -1113630 2 0 {name=p3 sig_type=std_logic lab=vc}
C {devices/vsource.sym} -1103480 -1113570 0 0 {name=Vdd4 value=0.9 savecurrent=false
}
C {devices/gnd.sym} -1103480 -1113510 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} -1103560 -1113630 2 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1102750 -1113590 2 0 {name=p9 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1102940 -1113500 0 0 {name=p10 sig_type=std_logic lab=vc}
C {8xPI/8xPI.sym} -1102320 -1113310 0 0 {name=x3}
C {devices/vsource.sym} -1103560 -1113370 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} -1103560 -1113310 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} -1103560 -1113430 2 0 {name=p14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1102200 -1113300 2 0 {name=p13 sig_type=std_logic lab="vss, vss"}
C {devices/lab_pin.sym} -1102360 -1113520 0 0 {name=p15 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} -1102360 -1113480 0 0 {name=p16 sig_type=std_logic lab=v180}
C {devices/lab_pin.sym} -1102360 -1113440 0 0 {name=p17 sig_type=std_logic lab=v90
}
C {devices/lab_pin.sym} -1102360 -1113400 0 0 {name=p18 sig_type=std_logic lab=v270}
C {devices/lab_pin.sym} -1102080 -1113610 0 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1102210 -1113610 0 0 {name=p20 sig_type=std_logic lab="vdd, vdd, vdd, vdd, vss, vss, vss, vss"}
C {devices/lab_pin.sym} -1101780 -1113450 2 0 {name=p21 sig_type=std_logic lab=pi_vout}
C {clock_gen/clock_gen.sym} -1102750 -1113460 0 0 {name=x1}
C {devices/lab_pin.sym} -1101760 -1113710 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -1101760 -1113550 0 0 {name=p7 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} -1101680 -1113570 3 0 {name=p11 sig_type=std_logic lab=vout}
C {devices/lab_pin.sym} -1101900 -1113630 0 0 {name=p12 sig_type=std_logic lab=pi_vout}
C {div_freq_x8/div_freq_x8.sym} -1101890 -1113560 0 0 {name=x2
}
C {devices/lab_pin.sym} -1102080 -1113310 0 0 {name=p22 sig_type=std_logic lab=vss}
