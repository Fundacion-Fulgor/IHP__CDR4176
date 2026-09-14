v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 200 -270 200 -210 {lab=CTRL}
N 200 -150 200 -90 {lab=CTRL}
N 380 -150 380 -90 {lab=CTRL}
N 200 -180 380 -180 {lab=VDD}
N 300 -90 380 -90 {lab=CTRL}
N 300 -270 380 -270 {lab=CTRL}
N 260 -310 260 -270 {lab=CTRL}
N 200 -270 260 -270 {lab=CTRL}
N 420 -180 480 -180 {lab=VOUTDP}
N 300 -270 300 -90 {lab=CTRL}
N 260 -270 300 -270 {lab=CTRL}
N 200 -90 300 -90 {lab=CTRL}
N 380 -270 380 -210 {lab=CTRL}
N 100 -180 160 -180 {lab=VOUTDN}
C {sg13g2_pr/sg13_lv_pmos.sym} 400 -180 0 1 {name=M10
l=0.13u
w=8u
ng=8
m=4
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 180 -180 0 0 {name=M9
l=0.13u
w=8u
ng=8
m=4
model=sg13_lv_pmos
spiceprefix=X
}
C {ipin.sym} 260 -310 1 0 {name=p3 lab=CTRL}
C {ipin.sym} 260 -180 1 0 {name=p4 lab=VDD}
C {ipin.sym} 100 -180 0 0 {name=p2 lab=VOUTDN}
C {ipin.sym} 480 -180 2 0 {name=p1 lab=VOUTDP}
