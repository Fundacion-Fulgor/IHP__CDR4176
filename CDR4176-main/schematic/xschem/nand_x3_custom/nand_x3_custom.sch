v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 340 -300 340 -260 {lab=#net1}
N 340 -200 340 -160 {lab=#net2}
N 140 -430 140 -410 {lab=OUT}
N 140 -410 340 -410 {lab=OUT}
N 340 -430 340 -410 {lab=OUT}
N 340 -410 520 -410 {lab=OUT}
N 520 -430 520 -410 {lab=OUT}
N 140 -510 140 -490 {lab=VDD}
N 200 -510 340 -510 {lab=VDD}
N 340 -510 340 -490 {lab=VDD}
N 400 -510 520 -510 {lab=VDD}
N 520 -510 520 -490 {lab=VDD}
N 340 -530 340 -510 {lab=VDD}
N 80 -460 100 -460 {lab=A}
N 280 -460 300 -460 {lab=B}
N 460 -460 480 -460 {lab=C}
N 280 -330 300 -330 {lab=A}
N 280 -230 300 -230 {lab=B}
N 280 -130 300 -130 {lab=C}
N 140 -460 200 -460 {lab=VDD}
N 200 -510 200 -460 {lab=VDD}
N 140 -510 200 -510 {lab=VDD}
N 340 -460 400 -460 {lab=VDD}
N 400 -510 400 -460 {lab=VDD}
N 340 -510 400 -510 {lab=VDD}
N 520 -460 580 -460 {lab=VDD}
N 580 -510 580 -460 {lab=VDD}
N 520 -510 580 -510 {lab=VDD}
N 340 -330 420 -330 {lab=VSS}
N 420 -130 420 -80 {lab=VSS}
N 340 -80 420 -80 {lab=VSS}
N 340 -100 340 -80 {lab=VSS}
N 340 -230 420 -230 {lab=VSS}
N 420 -330 420 -230 {lab=VSS}
N 340 -130 420 -130 {lab=VSS}
N 420 -230 420 -130 {lab=VSS}
N 340 -80 340 -60 {lab=VSS}
N 340 -380 340 -360 {lab=OUT}
N 340 -380 380 -380 {lab=OUT}
N 340 -410 340 -380 {lab=OUT}
C {sg13g2_pr/sg13_lv_pmos.sym} 120 -460 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 320 -460 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 500 -460 0 0 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 320 -330 0 0 {name=M4
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 320 -230 0 0 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 320 -130 0 0 {name=M6
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {ipin.sym} 280 -330 0 0 {name=p8 lab=A}
C {ipin.sym} 280 -230 0 0 {name=p1 lab=B}
C {ipin.sym} 280 -130 0 0 {name=p2 lab=C}
C {lab_pin.sym} 80 -460 0 0 {name=p6 sig_type=std_logic lab=A}
C {lab_pin.sym} 280 -460 0 0 {name=p3 sig_type=std_logic lab=B}
C {lab_pin.sym} 460 -460 0 0 {name=p4 sig_type=std_logic lab=C}
C {iopin.sym} 340 -60 1 0 {name=p5 lab=VSS}
C {iopin.sym} 340 -530 3 0 {name=p7 lab=VDD}
C {opin.sym} 380 -380 0 0 {name=p9 lab=OUT}
