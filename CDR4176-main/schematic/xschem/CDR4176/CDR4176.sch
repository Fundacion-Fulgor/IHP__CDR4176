v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 450 -220 480 -220 {lab=voutpi}
N 300 -120 300 -70 {lab=VSS}
N 520 -70 590 -70 {lab=VSS}
N 590 -160 590 -70 {lab=VSS}
N 710 -220 740 -220 {lab=voutdiv}
N 590 -70 790 -70 {lab=VSS}
N 790 -180 790 -70 {lab=VSS}
N 590 -370 590 -280 {lab=VDD}
N 220 -370 220 -320 {lab=VDD}
N 790 -370 790 -260 {lab=VDD}
N 590 -370 790 -370 {lab=VDD}
N 520 -370 590 -370 {lab=VDD}
N 860 -220 940 -220 {lab=VOUT}
N 80 -200 160 -200 {lab=VS[4:0]}
N 80 -170 160 -170 {lab=VCONT}
N 520 -410 520 -370 {lab=VDD}
N 520 -70 520 -30 {lab=VSS}
N 300 -70 520 -70 {lab=VSS}
N 450 -260 450 -220 {lab=voutpi}
N 420 -220 450 -220 {lab=voutpi}
N 710 -260 710 -220 {lab=voutdiv}
N 690 -220 710 -220 {lab=voutdiv}
N 360 -370 520 -370 {lab=VDD}
N 270 -370 270 -320 {lab=VDD}
N 220 -370 270 -370 {lab=VDD}
N 320 -370 320 -320 {lab=VDD}
N 270 -370 320 -370 {lab=VDD}
N 360 -370 360 -320 {lab=VDD}
N 320 -370 360 -370 {lab=VDD}
C {8xPI_top/8xPI_top.sym} 40 0 0 0 {name=x1}
C {div_freq_x8/div_freq_x8.sym} 460 -150 0 0 {name=x2}
C {buff_PI_d16/buff_PI_d16.sym} 790 -220 0 0 {name=x3}
C {ipin.sym} 80 -200 0 0 {name=p1 lab=VS[4:0]}
C {ipin.sym} 80 -170 0 0 {name=p2 lab=VCONT}
C {opin.sym} 940 -220 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 520 -410 0 0 {name=p4 lab=VDD}
C {iopin.sym} 520 -30 0 0 {name=p5 lab=VSS}
C {lab_pin.sym} 450 -260 1 0 {name=p6 sig_type=std_logic lab=voutpi}
C {lab_pin.sym} 710 -260 1 0 {name=p7 sig_type=std_logic lab=voutdiv}
