v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 60 -100 80 -100 {lab=VIN}
N 200 -100 220 -100 {lab=VOUT}
N 130 -160 130 -140 {lab=VDD}
N 130 -60 130 -40 {lab=VSS}
C {inv/inv.sym} 40 40 0 0 {name=x1[1:0]}
C {ipin.sym} 60 -100 0 0 {name=p4 lab=VIN}
C {opin.sym} 220 -100 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 130 -160 0 0 {name=p1 lab=VDD}
C {iopin.sym} 130 -40 0 0 {name=p2 lab=VSS}
