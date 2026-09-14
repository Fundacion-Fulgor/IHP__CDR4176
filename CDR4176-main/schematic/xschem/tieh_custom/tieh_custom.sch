v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 100 -130 100 -80 {lab=#net1}
N 180 -30 180 -10 {lab=VSS}
N 100 -80 140 -80 {lab=#net1}
N 100 -210 140 -210 {lab=#net1}
N 180 -160 220 -160 {lab=VOUT}
N 180 -260 180 -240 {lab=VDD}
N 180 -210 200 -210 {lab=VDD}
N 200 -260 200 -210 {lab=VDD}
N 180 -80 200 -80 {lab=VSS}
N 200 -80 200 -30 {lab=VSS}
N 180 -260 200 -260 {lab=VDD}
N 180 -280 180 -260 {lab=VDD}
N 180 -30 200 -30 {lab=VSS}
N 180 -50 180 -30 {lab=VSS}
N 180 -180 180 -160 {lab=VOUT}
N 180 -130 180 -110 {lab=#net1}
N 100 -130 180 -130 {lab=#net1}
N 100 -210 100 -130 {lab=#net1}
C {sg13g2_pr/sg13_lv_pmos.sym} 160 -210 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 180 -280 0 0 {name=p1 lab=VDD}
C {iopin.sym} 180 -10 0 0 {name=p2 lab=VSS}
C {opin.sym} 220 -160 0 0 {name=p3 lab=VOUT}
C {sg13g2_pr/sg13_lv_nmos.sym} 160 -80 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
