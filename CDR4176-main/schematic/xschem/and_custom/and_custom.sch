v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 430 -160 460 -160 {lab=OUT}
N 250 -60 360 -60 {lab=VSS}
N 250 -250 360 -250 {lab=VDD}
N 250 -270 250 -250 {lab=VDD}
N 150 -250 250 -250 {lab=VDD}
N 250 -60 250 -40 {lab=VSS}
N 150 -60 250 -60 {lab=VSS}
N 260 -160 310 -160 {lab=#net1}
N 360 -250 360 -200 {lab=VDD}
N 50 -180 90 -180 {lab=A}
N 50 -140 90 -140 {lab=B}
N 360 -120 360 -60 {lab=VSS}
N 150 -250 150 -230 {lab=VDD}
N 150 -90 150 -60 {lab=VSS}
C {ipin.sym} 50 -180 0 0 {name=p1 lab=A}
C {iopin.sym} 250 -270 0 0 {name=p2 lab=VDD}
C {opin.sym} 460 -160 0 0 {name=p3 lab=OUT}
C {iopin.sym} 250 -40 0 0 {name=p4 lab=VSS}
C {ipin.sym} 50 -140 0 0 {name=p5 lab=B}
C {inv_CDR/inv_CDR.sym} 270 -20 0 0 {name=x1}
C {nand_custom/nand_custom.sym} 50 -40 0 0 {name=x2}
