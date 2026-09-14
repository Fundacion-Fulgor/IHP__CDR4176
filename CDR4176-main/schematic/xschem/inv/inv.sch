v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 170 -140 170 -110 {lab=VOUT}
N 90 -140 90 -80 {lab=VIN}
N 90 -210 90 -140 {lab=VIN}
N 170 -30 170 -10 {lab=VSS}
N 50 -140 90 -140 {lab=VIN}
N 90 -80 130 -80 {lab=VIN}
N 90 -210 130 -210 {lab=VIN}
N 170 -140 210 -140 {lab=VOUT}
N 170 -180 170 -140 {lab=VOUT}
N 170 -260 170 -240 {lab=VDD}
N 170 -210 190 -210 {lab=VDD}
N 190 -260 190 -210 {lab=VDD}
N 170 -80 190 -80 {lab=VSS}
N 190 -80 190 -30 {lab=VSS}
N 170 -260 190 -260 {lab=VDD}
N 170 -280 170 -260 {lab=VDD}
N 170 -30 190 -30 {lab=VSS}
N 170 -50 170 -30 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 150 -210 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 170 -280 0 0 {name=p1 lab=VDD}
C {iopin.sym} 170 -10 0 0 {name=p2 lab=VSS}
C {opin.sym} 210 -140 0 0 {name=p3 lab=VOUT}
C {ipin.sym} 50 -140 0 0 {name=p4 lab=VIN}
C {sg13g2_pr/sg13_lv_nmos.sym} 150 -80 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
