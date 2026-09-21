v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 120 -110 140 -110 {lab=#net1}
N 120 -280 150 -280 {lab=#net1}
N 270 -280 320 -280 {lab=CLKOUT}
N 80 -90 140 -90 {lab=CLKIN}
N 220 -240 220 -220 {lab=VSS}
N 120 -280 120 -110 {lab=#net1}
N 320 -280 320 -100 {lab=CLKOUT}
N 220 -340 220 -320 {lab=VDD}
N 220 -170 220 -150 {lab=VDD}
N 220 -50 220 -30 {lab=VSS}
N 320 -100 360 -100 {lab=CLKOUT}
N 310 -100 320 -100 {lab=CLKOUT}
C {reg_v2/reg_v2.sym} 110 -50 0 0 {name=x1}
C {inv_CDR/inv_CDR.sym} 310 -140 0 1 {name=x4}
C {iopin.sym} 220 -340 0 0 {name=p1 lab=VDD}
C {iopin.sym} 220 -220 0 0 {name=p2 lab=VSS}
C {ipin.sym} 80 -90 0 0 {name=p3 lab=CLKIN}
C {lab_pin.sym} 220 -170 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 220 -30 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {opin.sym} 360 -100 0 0 {name=p4 lab=CLKOUT}
