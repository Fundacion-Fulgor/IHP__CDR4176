v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 140 -280 140 -260 {lab=OUT}
N 300 -430 300 -400 {lab=#net1}
N 300 -280 300 -260 {lab=OUT}
N 300 -460 330 -460 {lab=VDD}
N 300 -370 330 -370 {lab=VDD}
N 330 -460 330 -370 {lab=VDD}
N 140 -200 140 -160 {lab=VSS}
N 140 -230 180 -230 {lab=VSS}
N 300 -230 340 -230 {lab=VSS}
N 300 -200 300 -160 {lab=VSS}
N 240 -230 260 -230 {lab=B}
N 300 -570 330 -570 {lab=VDD}
N 300 -640 300 -600 {lab=VDD}
N 300 -640 330 -640 {lab=VDD}
N 330 -640 330 -570 {lab=VDD}
N 300 -660 300 -640 {lab=VDD}
N 300 -540 300 -490 {lab=#net2}
N 330 -570 330 -460 {lab=VDD}
N 210 -570 260 -570 {lab=A}
N 210 -460 260 -460 {lab=B}
N 210 -370 260 -370 {lab=C}
N 460 -280 460 -260 {lab=OUT}
N 400 -230 420 -230 {lab=C}
N 140 -280 300 -280 {lab=OUT}
N 460 -200 460 -160 {lab=VSS}
N 180 -160 300 -160 {lab=VSS}
N 340 -160 460 -160 {lab=VSS}
N 180 -230 180 -160 {lab=VSS}
N 140 -160 180 -160 {lab=VSS}
N 340 -230 340 -160 {lab=VSS}
N 320 -160 340 -160 {lab=VSS}
N 460 -230 500 -230 {lab=VSS}
N 500 -230 500 -160 {lab=VSS}
N 460 -160 500 -160 {lab=VSS}
N 80 -230 100 -230 {lab=A}
N 300 -280 460 -280 {lab=OUT}
N 320 -160 320 -140 {lab=VSS}
N 300 -160 320 -160 {lab=VSS}
N 300 -310 300 -280 {lab=OUT}
N 300 -310 460 -310 {lab=OUT}
N 300 -340 300 -310 {lab=OUT}
C {sg13g2_pr/sg13_lv_nmos.sym} 120 -230 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 280 -370 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 280 -230 0 0 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 280 -460 0 0 {name=M4
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 300 -660 3 0 {name=p3 lab=VDD}
C {iopin.sym} 320 -140 1 0 {name=p4 lab=VSS}
C {lab_pin.sym} 240 -230 0 0 {name=p6 sig_type=std_logic lab=B}
C {ipin.sym} 210 -460 0 0 {name=p7 lab=B}
C {ipin.sym} 210 -370 0 0 {name=p8 lab=C}
C {opin.sym} 460 -310 0 0 {name=p1 lab=OUT}
C {sg13g2_pr/sg13_lv_pmos.sym} 280 -570 0 0 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {ipin.sym} 210 -570 0 0 {name=p2 lab=A}
C {sg13g2_pr/sg13_lv_nmos.sym} 440 -230 0 0 {name=M6
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 80 -230 0 0 {name=p5 sig_type=std_logic lab=A}
C {lab_pin.sym} 400 -230 0 0 {name=p9 sig_type=std_logic lab=C}
