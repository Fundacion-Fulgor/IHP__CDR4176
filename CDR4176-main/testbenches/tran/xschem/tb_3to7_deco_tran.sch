v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 70 -80 70 -60 {lab=VSS}
N 70 -185 70 -140 {lab=VS[0]}
N 70 -185 130 -185 {lab=VS[0]}
N 350 -80 350 -60 {lab=VSS}
N 350 -185 350 -140 {lab=VS[1]}
N 350 -185 410 -185 {lab=VS[1]}
N 640 -80 640 -60 {lab=VSS}
N 640 -185 640 -140 {lab=VS[2]}
N 640 -185 700 -185 {lab=VS[2]}
N 85 -300 85 -280 {lab=GND}
N 85 -380 85 -360 {lab=VSS}
N 220 -410 220 -360 {lab=VDD}
N 220 -305 220 -280 {lab=VSS}
N 490 -440 490 -410 {lab=VDD}
N 490 -310 490 -280 {lab=VSS}
N 350 -360 390 -360 {lab=VS[2:0]}
N 590 -360 730 -360 {lab="vo_st7, vo_st6, vo_st5, vo_st4, vo_st3, vo_st2, vo_st1"}
N 780 -420 780 -400 {lab=VDD}
N 780 -320 780 -300 {lab=VSS}
N 960 -360 1050 -360 {lab=VSS}
N 850 -360 900 -360 {lab=#net1}
C {netlist_not_shown.sym} 75 -605 0 0 {name=SIMULATION_THERMO_3TO7 only_toplevel=false

value="

* Circuit Parameters
.param vdd = 1.2
.param vss = 0.0
.param a=0
.param b=0
.param c=0
.param d=1
.param Tclk = 500P
.options TEMP = 65.0

* Include Models
.lib cornerMOSlv.lib mos_tt
cornerMOSlv.lib mos_tt
cornerMOShv.lib mos_tt
cornerHBT.lib hbt_typ
cornerRES.lib res_typ

* OP Parameters & Singals to save
.save all

*Simulations
.control
set output_path = ./


* --- ESTADO 1: Entrada 001 (Salida T1 activa) ---
alterparam a=0 b=0 c=1
reset
tran 0.2PS 500PS	
setplot tran1
plot vo_st7 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out1.raw V(vo_st7)

* --- ESTADO 2: Entrada 010 (Salidas T1, T2 activas) ---
alterparam a=0 b=1 c=0
reset
tran 0.2PS 500PS 
setplot tran2
plot vo_st7 vo_st6 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out2.raw V(vo_st7) V(vo_st6)

* --- ESTADO 3: Entrada 011 (Salidas T1, T2, T3 activas) ---
alterparam a=0 b=1 c=1
reset
tran 0.2PS 500PS 
setplot tran3
plot vo_st7 vo_st6 vo_st5 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out3.raw V(vo_st7) V(vo_st6) V(vo_st5)

* --- ESTADO 4: Entrada 100 (Salidas T1 a T4 activas) ---
alterparam a=1 b=0 c=0
reset
tran 0.2PS 500PS 
setplot tran4
plot  vo_st7 vo_st6 vo_st5 vo_st4 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out4.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4)

* --- ESTADO 5: Entrada 101 (Salidas T1 a T5 activas) ---
alterparam a=1 b=0 c=1
reset
tran 0.2PS 500PS 
setplot tran5
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out5.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3)

* --- ESTADO 6: Entrada 110 (Salidas T1 a T6 activas) ---
alterparam a=1 b=1 c=0
reset
tran 0.2PS 500PS 
setplot tran6
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 vo_st2 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out6.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3) V(vo_st2)

* --- ESTADO 7: Entrada 111 (Salidas T1 a T7 activas) ---
alterparam a=1 b=1 c=1
reset
tran 0.2PS 500PS 
setplot tran7
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 vo_st2 vo_st1 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}out7.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3) V(vo_st2) V(vo_st1)
.endc
.end"}
C {lab_pin.sym} 130 -185 2 0 {name=p25 sig_type=std_logic lab=VS[0]}
C {vsource.sym} 70 -110 0 0 {name=V7 value="PULSE(\{a*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {lab_pin.sym} 410 -185 2 0 {name=p1 sig_type=std_logic lab=VS[1]}
C {vsource.sym} 350 -110 0 0 {name=V1 value="PULSE(\{b*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {lab_pin.sym} 700 -185 2 0 {name=p3 sig_type=std_logic lab=VS[2]}
C {vsource.sym} 640 -110 0 0 {name=V2 value="PULSE(\{c*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {vsource.sym} 85 -330 0 0 {name=V3 value=DC\{VSS\} savecurrent=false}
C {gnd.sym} 85 -280 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 85 -380 1 0 {name=p5 sig_type=std_logic lab=VSS}
C {vsource.sym} 220 -335 0 0 {name=V4 value=DC\{VDD\} savecurrent=false}
C {lab_pin.sym} 220 -405 1 0 {name=p24 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 70 -60 3 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 220 -280 3 0 {name=p6 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 350 -60 3 0 {name=p2 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 640 -60 3 0 {name=p4 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 350 -360 0 0 {name=p9 sig_type=std_logic lab=VS[2:0]}
C {lab_pin.sym} 490 -440 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 490 -280 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {3to7_deco/3to7_deco.sym} 350 -280 0 0 {name=x1}
C {inv/inv.sym} 690 -220 0 0 {name=x4[6:0]}
C {capa.sym} 930 -360 3 0 {name=C3[6:0]
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 1050 -360 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 655 -360 1 0 {name=p15 sig_type=std_logic lab="vo_st7, vo_st6, vo_st5, vo_st4, vo_st3, vo_st2, vo_st1"}
C {lab_pin.sym} 780 -300 2 0 {name=p26 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 780 -420 0 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/launcher.sym} 280 -570 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir tran_8XPI.raw] tran"
}
C {devices/launcher.sym} 280 -520 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
