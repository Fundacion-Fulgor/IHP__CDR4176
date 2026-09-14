v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 290 -350 330 -350 {lab=VINI}
N 290 -270 330 -270 {lab=VINQ}
N 290 -310 330 -310 {lab=VINIB}
N 290 -230 330 -230 {lab=VINQB}
N 420 -420 420 -400 {lab=VDD}
N 340 -160 340 -140 {lab=VSS}
N 510 -290 600 -290 {lab=#net1}
N 650 -420 650 -330 {lab=VDD}
N 420 -420 650 -420 {lab=VDD}
N 420 -440 420 -420 {lab=VDD}
N 650 -250 650 -160 {lab=VSS}
N 340 -160 650 -160 {lab=VSS}
N 340 -180 340 -160 {lab=VSS}
N 830 -420 830 -330 {lab=VDD}
N 830 -250 830 -160 {lab=VSS}
N 900 -290 960 -290 {lab=VOUT}
N 430 -180 430 -100 {lab=VS[1:0]}
N 410 -180 410 -100 {lab=VST[7:0]}
N 720 -290 780 -290 {lab=#net2}
N 650 -420 830 -420 {lab=VDD}
N 650 -160 830 -160 {lab=VSS}
C {MUX_4_1/MUX_4_1.sym} 210 -140 0 0 {name=x1[7:0]}
C {ipin.sym} 290 -350 0 0 {name=p3 lab=VINI}
C {ipin.sym} 290 -270 0 0 {name=p4 lab=VINQ}
C {ipin.sym} 290 -310 0 0 {name=p15 lab=VINIB}
C {ipin.sym} 290 -230 0 0 {name=p17 lab=VINQB}
C {iopin.sym} 420 -440 0 0 {name=p1 lab=VDD}
C {iopin.sym} 340 -140 2 0 {name=p2 lab=VSS}
C {inv_PI/inv_PI.sym} 560 -150 0 0 {name=x2}
C {opin.sym} 960 -290 0 0 {name=p5 lab=VOUT}
C {ipin.sym} 290 -80 0 0 {name=p6 lab=VS[1:0]}
C {ipin.sym} 290 -40 0 0 {name=p7 lab=VST[7:0]}
C {lab_pin.sym} 430 -100 2 0 {name=p8 sig_type=std_logic lab=VS[1:0]}
C {lab_pin.sym} 410 -100 0 0 {name=p9 sig_type=std_logic lab=VST[7:0]}
C {buff_PI_d16/buff_PI_d16.sym} 830 -290 0 0 {name=x1}
