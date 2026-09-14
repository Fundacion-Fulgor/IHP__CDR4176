v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 50 -80 70 -80 {lab=VIN}
N 190 -80 210 -80 {lab=VOUT}
N 120 -140 120 -120 {lab=VDD}
N 120 -40 120 -20 {lab=VSS}
C {inv_PI_d4/inv_PI_d4.sym} 120 -80 0 0 {name=x1[1:0]}
C {ipin.sym} 50 -80 0 0 {name=p4 lab=VIN}
C {opin.sym} 210 -80 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 120 -140 0 0 {name=p1 lab=VDD}
C {iopin.sym} 120 -20 0 0 {name=p2 lab=VSS}
