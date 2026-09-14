v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 150 -380 150 -360 {lab=xxx}
N 230 -360 300 -360 {lab=xxx}
N 300 -380 300 -360 {lab=xxx}
N 150 -360 230 -360 {lab=xxx}
N 150 -470 150 -440 {lab=VDD}
N 220 -470 300 -470 {lab=VDD}
N 300 -460 300 -440 {lab=VDD}
N 220 -510 220 -470 {lab=VDD}
N 170 -470 220 -470 {lab=VDD}
N 150 -410 170 -410 {lab=VDD}
N 170 -470 170 -410 {lab=VDD}
N 150 -470 170 -470 {lab=VDD}
N 300 -410 330 -410 {lab=VDD}
N 330 -460 330 -410 {lab=VDD}
N 300 -460 330 -460 {lab=VDD}
N 300 -470 300 -460 {lab=VDD}
N 230 -150 230 -110 {lab=VSS}
N 230 -210 280 -210 {lab=VSS}
N 280 -210 280 -150 {lab=VSS}
N 230 -150 280 -150 {lab=VSS}
N 230 -180 230 -150 {lab=VSS}
N 230 -300 280 -300 {lab=VSS}
N 230 -340 230 -330 {lab=xxx}
N 230 -270 230 -240 {lab=#net1}
N 280 -300 280 -210 {lab=VSS}
N 150 -300 190 -300 {lab=A}
N 150 -210 190 -210 {lab=B}
N 90 -410 110 -410 {lab=A}
N 240 -410 260 -410 {lab=B}
N 230 -340 300 -340 {lab=xxx}
N 230 -360 230 -340 {lab=xxx}
C {sg13g2_pr/sg13_lv_nmos.sym} 210 -300 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 130 -410 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 210 -210 0 0 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 280 -410 0 0 {name=M4
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 220 -510 3 0 {name=p3 lab=VDD}
C {iopin.sym} 230 -110 1 0 {name=p4 lab=VSS}
C {lab_pin.sym} 90 -410 0 0 {name=p6 sig_type=std_logic lab=A}
C {lab_pin.sym} 240 -410 0 0 {name=p7 sig_type=std_logic lab=B}
C {ipin.sym} 150 -300 0 0 {name=p8 lab=A}
C {ipin.sym} 150 -210 0 0 {name=p1 lab=B}
C {opin.sym} 300 -340 0 0 {name=p2 lab=OUT}
