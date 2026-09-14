v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 50 -190 80 -190 {lab=A}
N 50 -160 80 -160 {lab=B}
N 50 -130 80 -130 {lab=C}
N 140 -90 140 -60 {lab=VSS}
N 250 -60 350 -60 {lab=VSS}
N 350 -120 350 -60 {lab=VSS}
N 250 -60 250 -40 {lab=VSS}
N 140 -60 250 -60 {lab=VSS}
N 140 -260 140 -230 {lab=VDD}
N 250 -260 350 -260 {lab=VDD}
N 350 -260 350 -200 {lab=VDD}
N 250 -280 250 -260 {lab=VDD}
N 140 -260 250 -260 {lab=VDD}
N 250 -160 300 -160 {lab=#net1}
N 420 -160 450 -160 {lab=OUT}
C {iopin.sym} 250 -280 0 0 {name=p2 lab=VDD}
C {iopin.sym} 250 -40 0 0 {name=p4 lab=VSS}
C {ipin.sym} 50 -190 0 0 {name=p1 lab=A}
C {ipin.sym} 50 -160 0 0 {name=p3 lab=B}
C {ipin.sym} 50 -130 0 0 {name=p5 lab=C}
C {opin.sym} 450 -160 0 0 {name=p6 lab=OUT}
C {nand_x3_custom/nand_x3_custom.sym} 60 -60 0 0 {name=x1}
C {inv/inv.sym} 260 -20 0 0 {name=x2}
