v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 100 -390 140 -390 {lab=VINA}
N 100 -370 140 -370 {lab=VINB}
N 100 -190 140 -190 {lab=VINC}
N 100 -170 140 -170 {lab=VIND}
N 190 -270 190 -230 {lab=VDD}
N 150 -330 150 -290 {lab=VSS}
N 150 -130 150 -90 {lab=VSS}
N 190 -470 190 -430 {lab=VDD}
N 190 -330 190 -290 {lab=VS[0]}
N 190 -130 190 -90 {lab=VS[1]}
N 400 -230 400 -190 {lab=VSS}
N 440 -370 440 -330 {lab=VDD}
N 440 -230 440 -190 {lab=VST}
N 310 -290 390 -290 {lab=#net1}
N 310 -270 390 -270 {lab=#net2}
N 310 -380 310 -290 {lab=#net1}
N 240 -380 310 -380 {lab=#net1}
N 310 -270 310 -180 {lab=#net2}
N 240 -180 310 -180 {lab=#net2}
N 490 -280 590 -280 {lab=VOUT}
C {MUX_2_1/MUX_2_1.sym} 110 -100 0 0 {name=x3}
C {lab_wire.sym} 190 -270 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 150 -290 2 0 {name=p13 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 190 -290 2 0 {name=p17 sig_type=std_logic lab=VS[0]}
C {MUX_2_1/MUX_2_1.sym} 360 -200 0 0 {name=x5}
C {lab_wire.sym} 150 -90 2 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 190 -470 2 0 {name=p21 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 440 -190 2 0 {name=p22 sig_type=std_logic lab=VST}
C {lab_wire.sym} 190 -90 2 0 {name=p18 sig_type=std_logic lab=VS[1]}
C {opin.sym} 590 -280 0 0 {name=p2 lab=VOUT}
C {iopin.sym} 440 -370 0 0 {name=p1 lab=VDD}
C {iopin.sym} 400 -190 2 0 {name=p5 lab=VSS}
C {ipin.sym} 100 -390 0 0 {name=p3 lab=VINA}
C {ipin.sym} 100 -370 0 0 {name=p4 lab=VINB}
C {ipin.sym} 100 -190 0 0 {name=p6 lab=VINC}
C {ipin.sym} 100 -170 0 0 {name=p7 lab=VIND}
C {ipin.sym} 110 -270 0 0 {name=p16 lab=VS[1:0]}
C {ipin.sym} 110 -240 0 0 {name=p19 lab=VST}
C {MUX_2_1/MUX_2_1.sym} 110 -300 0 0 {name=x1}
