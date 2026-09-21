v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 50 -70 70 -70 {lab=VIN}
N 190 -70 210 -70 {lab=VOUT}
N 120 -130 120 -110 {lab=VDD}
N 120 -30 120 -10 {lab=VSS}
C {inv_d8_CDR/inv_d8_CDR.sym} 120 -70 0 0 {name=x1[1:0]}
C {ipin.sym} 50 -70 0 0 {name=p4 lab=VIN}
C {opin.sym} 210 -70 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 120 -130 0 0 {name=p1 lab=VDD}
C {iopin.sym} 120 -10 0 0 {name=p2 lab=VSS}
