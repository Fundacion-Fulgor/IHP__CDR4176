v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 60 -70 80 -70 {lab=VIN}
N 200 -70 220 -70 {lab=VOUT}
N 130 -130 130 -110 {lab=VDD}
N 130 -30 130 -10 {lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 130 -70 0 0 {name=x1[1:0]}
C {ipin.sym} 60 -70 0 0 {name=p4 lab=VIN}
C {opin.sym} 220 -70 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 130 -130 0 0 {name=p1 lab=VDD}
C {iopin.sym} 130 -10 0 0 {name=p2 lab=VSS}
