v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 240 -230 240 -200 {lab=VOUT}
N 160 -230 160 -170 {lab=VIN}
N 160 -300 160 -230 {lab=VIN}
N 120 -230 160 -230 {lab=VIN}
N 160 -170 200 -170 {lab=VIN}
N 160 -300 200 -300 {lab=VIN}
N 240 -230 300 -230 {lab=VOUT}
N 240 -270 240 -230 {lab=VOUT}
N 240 -300 300 -300 {lab=VBP}
N 240 -170 300 -170 {lab=xxx}
N 240 -370 240 -330 {lab=VDD}
N 240 -140 240 -100 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 220 -300 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 240 -370 0 0 {name=p1 lab=VDD}
C {iopin.sym} 240 -100 0 0 {name=p2 lab=VSS}
C {opin.sym} 300 -230 0 0 {name=p3 lab=VOUT}
C {ipin.sym} 120 -230 0 0 {name=p4 lab=VIN}
C {sg13g2_pr/sg13_lv_nmos.sym} 220 -170 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {iopin.sym} 300 -300 0 0 {name=p5 lab=VBP}
C {iopin.sym} 300 -170 0 0 {name=p6 lab=VBN}
