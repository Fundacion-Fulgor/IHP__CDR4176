v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 220 -360 220 -330 {lab=VDD}
N 220 -250 220 -220 {lab=VSS}
N 220 -160 220 -130 {lab=VDD}
N 220 -50 220 -20 {lab=VSS}
N 290 -90 400 -90 {lab=#net1}
N 290 -290 400 -290 {lab=#net1}
N 400 -190 400 -90 {lab=#net1}
N 560 -260 560 -230 {lab=VDD}
N 560 -150 560 -120 {lab=VSS}
N 630 -190 730 -190 {lab=PHOUT}
N 70 -90 170 -90 {lab=PH1}
N 70 -290 170 -290 {lab=PH0}
N 400 -190 510 -190 {lab=#net1}
N 400 -290 400 -190 {lab=#net1}
C {inv_PI_d2/inv_PI_d2.sym} 220 -290 0 0 {name=x5}
C {devices/lab_pin.sym} 220 -220 2 0 {name=p23 sig_type=std_logic lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 220 -90 0 0 {name=x6}
C {devices/lab_pin.sym} 220 -160 2 0 {name=p24 sig_type=std_logic lab=VDD}
C {inv_PI_d2/inv_PI_d2.sym} 560 -190 0 0 {name=x7}
C {devices/lab_pin.sym} 560 -260 2 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 560 -120 2 0 {name=p27 sig_type=std_logic lab=VSS}
C {iopin.sym} 220 -360 0 0 {name=p1 lab=VDD}
C {iopin.sym} 220 -20 0 0 {name=p2 lab=VSS}
C {ipin.sym} 70 -290 0 0 {name=p3 lab=PH0}
C {ipin.sym} 70 -90 0 0 {name=p4 lab=PH1}
C {opin.sym} 730 -190 0 0 {name=p5 lab=PHOUT}
