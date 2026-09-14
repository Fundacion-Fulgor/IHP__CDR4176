v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 525 -200 525 -110 {lab=VSS}
N 865 -110 905 -110 {lab=VSS}
N 905 -200 905 -110 {lab=VSS}
N 525 -230 565 -230 {lab=VSS}
N 565 -230 565 -110 {lab=VSS}
N 525 -110 565 -110 {lab=VSS}
N 865 -230 905 -230 {lab=VSS}
N 865 -230 865 -110 {lab=VSS}
N 525 -290 525 -260 {lab=#net1}
N 905 -290 905 -260 {lab=#net2}
N 525 -290 625 -290 {lab=#net1}
N 625 -330 625 -290 {lab=#net1}
N 805 -290 905 -290 {lab=#net2}
N 805 -330 805 -290 {lab=#net2}
N 905 -360 905 -290 {lab=#net2}
N 525 -580 525 -490 {lab=VDD}
N 905 -580 905 -490 {lab=VDD}
N 715 -580 905 -580 {lab=VDD}
N 485 -460 525 -460 {lab=VDD}
N 485 -580 485 -460 {lab=VDD}
N 485 -580 525 -580 {lab=VDD}
N 905 -460 945 -460 {lab=VDD}
N 945 -580 945 -460 {lab=VDD}
N 905 -580 945 -580 {lab=VDD}
N 625 -430 625 -390 {lab=#net3}
N 565 -460 605 -460 {lab=#net4}
N 825 -460 865 -460 {lab=#net3}
N 805 -430 805 -390 {lab=#net4}
N 605 -460 805 -430 {lab=#net4}
N 625 -430 825 -460 {lab=#net3}
N 715 -360 715 -310 {lab=CTRL}
N 715 -360 765 -360 {lab=CTRL}
N 715 -110 715 -60 {lab=VSS}
N 715 -110 865 -110 {lab=VSS}
N 665 -360 715 -360 {lab=CTRL}
N 565 -110 715 -110 {lab=VSS}
N 715 -630 715 -580 {lab=VDD}
N 525 -580 715 -580 {lab=VDD}
N 525 -370 525 -290 {lab=#net1}
N 905 -400 905 -360 {lab=#net2}
N 945 -230 1025 -230 {lab=CLKN}
N 565 -360 625 -360 {lab=VSS}
N 805 -360 865 -360 {lab=VSS}
N 365 -400 525 -400 {lab=#net1}
N 525 -430 525 -400 {lab=#net1}
N 365 -430 365 -400 {lab=#net1}
N 365 -580 365 -490 {lab=VDD}
N 405 -580 485 -580 {lab=VDD}
N 365 -460 405 -460 {lab=VDD}
N 405 -580 405 -460 {lab=VDD}
N 365 -580 405 -580 {lab=VDD}
N 905 -400 1065 -400 {lab=#net2}
N 905 -430 905 -400 {lab=#net2}
N 1065 -430 1065 -400 {lab=#net2}
N 1065 -580 1065 -490 {lab=VDD}
N 1025 -580 1065 -580 {lab=VDD}
N 1025 -460 1065 -460 {lab=VDD}
N 1025 -580 1025 -460 {lab=VDD}
N 945 -580 1025 -580 {lab=VDD}
N 1105 -460 1175 -460 {lab=VSS}
N 255 -460 325 -460 {lab=VSS}
N 405 -230 485 -230 {lab=CLKP}
N 905 -360 1120 -360 {lab=#net2}
N 1240 -360 1310 -360 {lab=VOUTDP}
N 330 -370 525 -370 {lab=#net1}
N 525 -400 525 -370 {lab=#net1}
N 140 -370 210 -370 {lab=VOUTDN}
N 280 -330 280 -305 {lab=VSS}
N 280 -435 280 -410 {lab=VDD}
N 1170 -320 1170 -295 {lab=VSS}
N 1170 -425 1170 -400 {lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 505 -230 0 0 {name=M1
l=0.13u
w=1.5u
ng=10
m=3
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 925 -230 0 1 {name=M2
l=0.13u
w=1.5u
ng=10
m=3
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 645 -360 0 1 {name=M3
l=0.13u
w=0.3u
ng=2
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 785 -360 0 0 {name=M4
l=0.13u
w=0.3u
ng=2
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 885 -460 0 0 {name=M6
l=0.13u
w=1.5u
ng=10
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 545 -460 0 1 {name=M5
l=0.13u
w=1.5u
ng=10
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 715 -60 0 0 {name=p1 lab=VSS}
C {ipin.sym} 405 -230 0 0 {name=p2 lab=CLKP}
C {ipin.sym} 1025 -230 0 1 {name=p4 lab=CLKN}
C {iopin.sym} 715 -630 0 0 {name=p5 lab=VDD}
C {ipin.sym} 715 -310 0 0 {name=p7 lab=CTRL}
C {lab_pin.sym} 565 -360 1 0 {name=p8 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 865 -360 1 0 {name=p9 sig_type=std_logic lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 345 -460 0 0 {name=M7
l=0.13u
w=1.5u
ng=10
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 1085 -460 0 1 {name=M8
l=0.13u
w=1.5u
ng=10
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} 255 -460 1 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1175 -460 1 0 {name=p11 sig_type=std_logic lab=VSS}
C {opin.sym} 140 -370 2 0 {name=p19 lab=VOUTDN}
C {opin.sym} 1310 -360 0 0 {name=p6 lab=VOUTDP}
C {buff_d8/buff_d8.sym} 1170 -360 0 0 {name=x1}
C {buff_d8/buff_d8.sym} 280 -370 0 1 {name=x2}
C {lab_pin.sym} 280 -305 2 0 {name=p12 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 280 -435 2 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1170 -295 2 0 {name=p14 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1170 -425 2 0 {name=p15 sig_type=std_logic lab=VDD}
