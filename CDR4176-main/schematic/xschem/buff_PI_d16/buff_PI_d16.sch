v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 400 -80 480 -80 {lab=VSS}
N 70 -150 110 -150 {lab=VIN}
N 160 -110 160 -80 {lab=VSS}
N 160 -220 160 -190 {lab=VDD}
N 230 -150 270 -150 {lab=#net1}
N 320 -220 320 -190 {lab=VDD}
N 160 -220 320 -220 {lab=VDD}
N 320 -110 320 -80 {lab=VSS}
N 160 -80 320 -80 {lab=VSS}
N 390 -150 430 -150 {lab=#net2}
N 480 -110 480 -80 {lab=VSS}
N 480 -220 480 -190 {lab=VDD}
N 400 -220 480 -220 {lab=VDD}
N 550 -150 590 -150 {lab=#net3}
N 480 -80 640 -80 {lab=VSS}
N 640 -110 640 -80 {lab=VSS}
N 640 -220 640 -190 {lab=VDD}
N 480 -220 640 -220 {lab=VDD}
N 710 -150 750 -150 {lab=VOUT}
N 400 -260 400 -220 {lab=VDD}
N 320 -220 400 -220 {lab=VDD}
N 400 -80 400 -40 {lab=VSS}
N 320 -80 400 -80 {lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 160 -150 0 0 {name=x7}
C {inv_PI_d4/inv_PI_d4.sym} 320 -150 0 0 {name=x8}
C {inv_PI_d8/inv_PI_d8.sym} 480 -150 0 0 {name=x9}
C {inv_PI_d16/inv_PI_d16.sym} 640 -150 0 0 {name=x10}
C {ipin.sym} 70 -150 0 0 {name=p4 lab=VIN}
C {opin.sym} 750 -150 0 0 {name=p3 lab=VOUT}
C {iopin.sym} 400 -260 0 0 {name=p1 lab=VDD}
C {iopin.sym} 400 -40 0 0 {name=p2 lab=VSS}
