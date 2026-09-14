v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 140 -220 140 -200 {lab=VDD}
N 240 -220 350 -220 {lab=VDD}
N 350 -220 350 -180 {lab=VDD}
N 140 -80 140 -60 {lab=VSS}
N 240 -60 350 -60 {lab=VSS}
N 350 -100 350 -60 {lab=VSS}
N 230 -140 300 -140 {lab=#net1}
N 50 -160 90 -160 {lab=A}
N 50 -140 90 -140 {lab=B}
N 50 -120 90 -120 {lab=C}
N 420 -140 450 -140 {lab=OUT}
N 240 -240 240 -220 {lab=VDD}
N 140 -220 240 -220 {lab=VDD}
N 240 -60 240 -40 {lab=VSS}
N 140 -60 240 -60 {lab=VSS}
C {nor_x3_custom/nor_x3_custom.sym} 50 -60 0 0 {name=x1}
C {inv/inv.sym} 260 0 0 0 {name=x2}
C {iopin.sym} 240 -240 0 0 {name=p2 lab=VDD}
C {iopin.sym} 240 -40 0 0 {name=p4 lab=VSS}
C {opin.sym} 450 -140 0 0 {name=p3 lab=OUT}
C {ipin.sym} 50 -160 0 0 {name=p1 lab=A}
C {ipin.sym} 50 -140 0 0 {name=p5 lab=B}
C {ipin.sym} 50 -120 0 0 {name=p6 lab=C}
