v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 100 -60 100 -40 {lab=VSS}
N 220 -40 340 -40 {lab=VSS}
N 200 -120 290 -120 {lab=#net1}
N 340 -80 340 -40 {lab=VSS}
N 100 -200 100 -180 {lab=VDD}
N 220 -200 340 -200 {lab=VDD}
N 340 -200 340 -160 {lab=VDD}
N 410 -120 440 -120 {lab=OUT}
N 40 -140 70 -140 {lab=A}
N 40 -100 70 -100 {lab=B}
N 220 -230 220 -200 {lab=VDD}
N 100 -200 220 -200 {lab=VDD}
N 220 -40 220 -20 {lab=VSS}
N 100 -40 220 -40 {lab=VSS}
C {iopin.sym} 220 -230 0 0 {name=p2 lab=VDD}
C {iopin.sym} 220 -20 0 0 {name=p4 lab=VSS}
C {opin.sym} 430 -120 0 0 {name=p3 lab=OUT}
C {ipin.sym} 40 -140 0 0 {name=p1 lab=A}
C {ipin.sym} 40 -100 0 0 {name=p5 lab=B}
C {nor_custom/nor_custom.sym} 40 -50 0 0 {name=x1}
C {inv/inv.sym} 250 20 0 0 {name=x2}
