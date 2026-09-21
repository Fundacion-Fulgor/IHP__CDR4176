v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 400 -590 400 -530 {lab=VDD}
N 400 -450 400 -390 {lab=VSS}
N 400 -280 400 -220 {lab=VDD}
N 400 -140 400 -80 {lab=VSS}
N 450 -180 540 -180 {lab=PH1}
N 470 -490 540 -490 {lab=PH1}
N 540 -340 540 -180 {lab=PH1}
N 240 -180 330 -180 {lab=#net1}
N 240 -330 240 -180 {lab=#net1}
N 240 -490 350 -490 {lab=#net1}
N 130 -330 240 -330 {lab=#net1}
N 240 -490 240 -330 {lab=#net1}
N 540 -340 650 -340 {lab=PH1}
N 540 -490 540 -340 {lab=PH1}
C {inv_d2_CDR/inv_d2_CDR.sym} 400 -490 0 0 {name=x13
}
C {lab_pin.sym} 400 -390 3 0 {name=p35 sig_type=std_logic lab=VSS}
C {inv_d2_CDR/inv_d2_CDR.sym} 400 -180 0 1 {name=x14
}
C {lab_pin.sym} 400 -280 3 1 {name=p36 sig_type=std_logic lab=VDD}
C {iopin.sym} 400 -590 0 0 {name=p1 lab=VDD}
C {iopin.sym} 400 -80 0 0 {name=p2 lab=VSS}
C {iopin.sym} 650 -340 0 0 {name=p3 lab=PH1}
C {iopin.sym} 130 -330 2 0 {name=p4 lab=PH0}
