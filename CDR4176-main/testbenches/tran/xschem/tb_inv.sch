v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1040 -530 2110 -50 {flags=graph
y1=-0.44
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
dataset=-1
unitx=1
logx=0
logy=0
hilight_wave=0
color="12 10"
node="vin 
voutx"}
N 310 -340 310 -320 {lab=vdd}
N 120 -250 120 -220 {lab=GND}
N 120 -340 120 -310 {lab=vdd}
N 40 -250 40 -220 {lab=GND}
N 40 -340 40 -310 {lab=vss}
N 120 -80 120 -60 {lab=GND}
N 120 -170 120 -140 {lab=vin}
N 240 -280 260 -280 {lab=vin}
N 310 -240 310 -220 {lab=vss}
N 380 -280 420 -280 {lab=voutx}
C {devices/code.sym} 25 -555 0 0 {name=s2 only_toplevel=false 
value="
.tran 5p 16n
.save all

.control
run
set color0=white
write inv.raw


.endc
"}
C {devices/code_shown.sym} 200 -540 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt

"}
C {inv/inv.sym} 220 -140 0 0 {name=x1}
C {devices/vsource.sym} 120 -280 0 0 {name=Vdd1 value=1.2 savecurrent=false
}
C {devices/gnd.sym} 120 -220 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} 120 -340 2 0 {name=p8 sig_type=std_logic lab=vdd}
C {devices/vsource.sym} 40 -280 0 0 {name=Vdd3 value=0 savecurrent=false
}
C {devices/gnd.sym} 40 -220 0 0 {name=l6 lab=GND
value=0}
C {devices/lab_pin.sym} 40 -340 2 0 {name=p14 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 120 -170 0 0 {name=p1 sig_type=std_logic lab=vin}
C {devices/vsource.sym} 120 -110 0 0 {name=VIN1 value="PULSE(0 1.2 0 10p 10p 490p 1n)" savecurrent=false
}
C {devices/gnd.sym} 120 -60 0 0 {name=l5 lab=GND}
C {devices/lab_pin.sym} 310 -220 2 0 {name=p3 sig_type=std_logic lab=vss}
C {devices/lab_pin.sym} 310 -340 0 0 {name=p4 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 240 -280 0 0 {name=p2 sig_type=std_logic lab=vin}
C {devices/lab_pin.sym} 420 -280 2 0 {name=p5 sig_type=std_logic lab=voutx}
C {devices/launcher.sym} 590 -335 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir inv.raw] tran"
}
C {devices/launcher.sym} 588.125 -278.75 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
