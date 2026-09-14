v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 90 -160 90 -140 {lab=VSS}
N 90 -265 90 -220 {lab=VS[0]}
N 90 -265 150 -265 {lab=VS[0]}
N 370 -160 370 -140 {lab=VSS}
N 370 -265 370 -220 {lab=VS[1]}
N 370 -265 430 -265 {lab=VS[1]}
N 660 -160 660 -140 {lab=VSS}
N 660 -265 660 -220 {lab=VS[2]}
N 660 -265 720 -265 {lab=VS[2]}
N 105 -380 105 -360 {lab=GND}
N 105 -460 105 -440 {lab=VSS}
N 240 -490 240 -440 {lab=VDD}
N 240 -385 240 -360 {lab=VSS}
N 510 -520 510 -490 {lab=VDD}
N 510 -390 510 -360 {lab=VSS}
N 370 -440 410 -440 {lab=VS[2:0]}
N 610 -440 750 -440 {lab="vo_st7, vo_st6, vo_st5, vo_st4, vo_st3, vo_st2, vo_st1"}
N 800 -500 800 -480 {lab=VDD}
N 800 -400 800 -380 {lab=VSS}
N 980 -440 1070 -440 {lab=VSS}
N 870 -440 920 -440 {lab=#net1}
C {netlist_not_shown.sym} 95 -685 0 0 {name=SIMULATION_THERMO_3TO7_V2 only_toplevel=false

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
write \{$output_path\}V2out1.raw V(vo_st7)

* --- ESTADO 2: Entrada 010 (Salidas T1, T2 activas) ---
alterparam a=0 b=1 c=0
reset
tran 0.2PS 500PS 
setplot tran2
plot vo_st7 vo_st6 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out2.raw V(vo_st7) V(vo_st6)

* --- ESTADO 3: Entrada 011 (Salidas T1, T2, T3 activas) ---
alterparam a=0 b=1 c=1
reset
tran 0.2PS 500PS 
setplot tran3
plot vo_st7 vo_st6 vo_st5 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out3.raw V(vo_st7) V(vo_st6) V(vo_st5)

* --- ESTADO 4: Entrada 100 (Salidas T1 a T4 activas) ---
alterparam a=1 b=0 c=0
reset
tran 0.2PS 500PS 
setplot tran4
plot  vo_st7 vo_st6 vo_st5 vo_st4 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out4.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4)

* --- ESTADO 5: Entrada 101 (Salidas T1 a T5 activas) ---
alterparam a=1 b=0 c=1
reset
tran 0.2PS 500PS 
setplot tran5
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out5.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3)

* --- ESTADO 6: Entrada 110 (Salidas T1 a T6 activas) ---
alterparam a=1 b=1 c=0
reset
tran 0.2PS 500PS 
setplot tran6
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 vo_st2 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out6.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3) V(vo_st2)

* --- ESTADO 7: Entrada 111 (Salidas T1 a T7 activas) ---
alterparam a=1 b=1 c=1
reset
tran 0.2PS 500PS 
setplot tran7
plot vo_st7 vo_st6 vo_st5 vo_st4 vo_st3 vo_st2 vo_st1 ylabel Vout xlabel Vin
set filetype =ascii
write \{$output_path\}V2out7.raw V(vo_st7) V(vo_st6) V(vo_st5) V(vo_st4) V(vo_st3) V(vo_st2) V(vo_st1)
.endc
.end"}
C {lab_pin.sym} 150 -265 2 0 {name=p25 sig_type=std_logic lab=VS[0]}
C {vsource.sym} 90 -190 0 0 {name=V7 value="PULSE(\{a*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {lab_pin.sym} 430 -265 2 0 {name=p1 sig_type=std_logic lab=VS[1]}
C {vsource.sym} 370 -190 0 0 {name=V1 value="PULSE(\{b*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {lab_pin.sym} 720 -265 2 0 {name=p3 sig_type=std_logic lab=VS[2]}
C {vsource.sym} 660 -190 0 0 {name=V2 value="PULSE(\{c*1.2\} \{d*1.2\} 250PS 2PS 2PS 500PS)" savecurrent=false}
C {vsource.sym} 105 -410 0 0 {name=V3 value=DC\{VSS\} savecurrent=false}
C {gnd.sym} 105 -360 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 105 -460 1 0 {name=p5 sig_type=std_logic lab=VSS}
C {vsource.sym} 240 -415 0 0 {name=V4 value=DC\{VDD\} savecurrent=false}
C {lab_pin.sym} 240 -485 1 0 {name=p24 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 90 -140 3 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 240 -360 3 0 {name=p6 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 370 -140 3 0 {name=p2 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 660 -140 3 0 {name=p4 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 370 -440 0 0 {name=p9 sig_type=std_logic lab=VS[2:0]}
C {lab_pin.sym} 510 -520 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 510 -360 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 710 -300 0 0 {name=x4[6:0]}
C {capa.sym} 950 -440 3 0 {name=C3[6:0]
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 1070 -440 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 675 -440 1 0 {name=p15 sig_type=std_logic lab="vo_st7, vo_st6, vo_st5, vo_st4, vo_st3, vo_st2, vo_st1"}
C {lab_pin.sym} 800 -380 2 0 {name=p26 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 800 -500 0 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/launcher.sym} 300 -650 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read [file join $netlist_dir tran_8XPI.raw] tran"
}
C {devices/launcher.sym} 300 -600 0 0 {name=h1
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {3to7_deco_v2/3to7_deco_v2.sym} 380 -370 0 0 {name=x1}
