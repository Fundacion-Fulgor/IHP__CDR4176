v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 340 -260 1410 220 {flags=graph
y1=-0.11
y2=1.7
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=6e-09
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="in
out
clk"
color="4 5 12"
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=-1}
N -400 -30 -400 0 {lab=GND}
N -400 -120 -400 -90 {lab=vdd}
N -510 -30 -510 0 {lab=GND}
N -510 -120 -510 -90 {lab=vss}
N 130 -70 130 -50 {lab=vdd}
N 130 50 130 70 {lab=vss}
N -510 150 -510 180 {lab=GND}
N -510 60 -510 90 {lab=clk}
N 0 50 20 50 {lab=clk}
N 20 10 20 50 {lab=clk}
N 20 10 50 10 {lab=clk}
N -510 320 -510 350 {lab=GND}
N -510 230 -510 260 {lab=in}
N -30 -40 -10 -40 {lab=in}
N -10 -40 -10 -10 {lab=in}
N 210 -0 260 -0 {lab=out}
N -10 -10 50 -10 {lab=in}
C {devices/vsource.sym} -400 -60 0 0 {name=Vdd1 value=1.2 savecurrent=false
}
C {devices/gnd.sym} -400 0 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} -400 -120 2 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/vsource.sym} -510 -60 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} -510 0 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} -510 -120 2 0 {name=p14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 130 -70 1 0 {name=p1 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 130 70 3 0 {name=p2 sig_type=std_logic lab=vss}
C {devices/code_shown.sym} -870 -290 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
*.include sg13g2_stdcell.spice

"}
C {devices/vsource.sym} -510 120 0 0 {name=Vdd2 value="dc 0 ac 0 pulse(0, 1.2, 0,50p,50p, 335p, 770p)" savecurrent=false
}
C {devices/gnd.sym} -510 180 0 0 {name=l1 lab=GND
value="dc 0 ac 0 pulse(0, 1.2, 0,50p,50p, 335p, 770p)"}
C {devices/lab_pin.sym} -510 60 2 0 {name=p3 sig_type=std_logic lab=clk}
C {devices/lab_pin.sym} 0 50 0 0 {name=p4 sig_type=std_logic lab=clk}
C {devices/vsource.sym} -510 290 0 0 {name=Vdd4 value="dc 0 ac 0 pulse(0, 1.2, 250p,50p,50p, 950p, 2n)" savecurrent=false
}
C {devices/gnd.sym} -510 350 0 0 {name=l2 lab=GND
value="dc 0 ac 0 pulse(0, 1.2, 0,50p,50p, 335p, 770p)"}
C {devices/lab_pin.sym} -510 230 2 0 {name=p5 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} -30 -40 0 0 {name=p6 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 260 0 2 0 {name=p7 sig_type=std_logic lab=out}
C {devices/launcher.sym} 400 265 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir tran_logic.raw] tran"
}
C {devices/code.sym} -815 -125 0 0 {name=s1 only_toplevel=false 
value="
.save v(clk) v(in) v(out)


.tran 5p 6n

.control
run
set color0=white
write tran_logic.raw

.endc
"}
C {reg_v2/reg_v2.sym} 20 50 0 0 {name=x1}
