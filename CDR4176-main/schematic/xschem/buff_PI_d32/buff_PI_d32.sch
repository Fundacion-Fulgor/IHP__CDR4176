v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 240 -220 240 -190 {lab=VDD}
N 240 -110 240 -80 {lab=VSS}
N 470 -220 470 -190 {lab=VDD}
N 470 -110 470 -80 {lab=VSS}
N 700 -220 700 -190 {lab=VDD}
N 700 -110 700 -80 {lab=VSS}
N 540 -150 650 -150 {lab=#net1}
N 310 -150 420 -150 {lab=#net2}
N 770 -150 860 -150 {lab=VOUT}
N 130 -150 190 -150 {lab=VIN}
C {buff_PI_d16/buff_PI_d16.sym} 240 -150 0 0 {name=x5}
C {inv_PI_d16/inv_PI_d16.sym} 470 -150 0 0 {name=x15}
C {devices/lab_pin.sym} 470 -220 2 0 {name=p53 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 470 -80 2 0 {name=p54 sig_type=std_logic lab=VSS}
C {inv_PI_d32/inv_PI_d32.sym} 700 -150 0 0 {name=x20}
C {devices/lab_pin.sym} 700 -220 2 0 {name=p64 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 700 -80 2 0 {name=p65 sig_type=std_logic lab=VSS}
C {opin.sym} 860 -150 0 0 {name=p22 lab=VOUT}
C {iopin.sym} 240 -80 0 0 {name=p10 lab=VSS}
C {iopin.sym} 240 -220 0 0 {name=p9 lab=VDD}
C {ipin.sym} 130 -150 0 0 {name=p5 lab=VIN}
