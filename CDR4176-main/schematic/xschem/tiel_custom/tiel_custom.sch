v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 120 -40 120 -20 {lab=VSS}
N 40 -90 80 -90 {lab=#net1}
N 40 -220 80 -220 {lab=#net1}
N 120 -140 160 -140 {lab=VOUT}
N 120 -270 120 -250 {lab=VDD}
N 120 -220 140 -220 {lab=VDD}
N 140 -270 140 -220 {lab=VDD}
N 120 -90 140 -90 {lab=VSS}
N 140 -90 140 -40 {lab=VSS}
N 120 -270 140 -270 {lab=VDD}
N 120 -290 120 -270 {lab=VDD}
N 120 -40 140 -40 {lab=VSS}
N 120 -60 120 -40 {lab=VSS}
N 120 -190 120 -170 {lab=#net1}
N 120 -140 120 -120 {lab=VOUT}
N 40 -170 40 -90 {lab=#net1}
N 40 -170 120 -170 {lab=#net1}
N 40 -220 40 -170 {lab=#net1}
C {sg13g2_pr/sg13_lv_pmos.sym} 100 -220 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 120 -290 0 0 {name=p1 lab=VDD}
C {iopin.sym} 120 -20 0 0 {name=p2 lab=VSS}
C {opin.sym} 160 -140 0 0 {name=p3 lab=VOUT}
C {sg13g2_pr/sg13_lv_nmos.sym} 100 -90 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
