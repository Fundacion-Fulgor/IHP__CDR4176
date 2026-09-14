v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 470 -450 470 -430 {lab=VDD}
N 630 -450 750 -450 {lab=VDD}
N 750 -450 750 -430 {lab=VDD}
N 470 -70 470 -50 {lab=VSS}
N 630 -50 750 -50 {lab=VSS}
N 750 -70 750 -50 {lab=VSS}
N 470 -370 470 -330 {lab=#net1}
N 470 -250 470 -230 {lab=X}
N 470 -170 470 -130 {lab=#net2}
N 750 -370 750 -330 {lab=#net3}
N 750 -250 750 -230 {lab=Q}
N 750 -170 750 -130 {lab=#net4}
N 410 -200 430 -200 {lab=CLK_B}
N 410 -300 430 -300 {lab=CLK}
N 330 -400 430 -400 {lab=D}
N 330 -250 330 -100 {lab=D}
N 330 -100 430 -100 {lab=D}
N 290 -250 330 -250 {lab=D}
N 330 -400 330 -250 {lab=D}
N 610 -400 710 -400 {lab=X}
N 610 -250 610 -100 {lab=X}
N 610 -100 710 -100 {lab=X}
N 690 -200 710 -200 {lab=CLK}
N 690 -300 710 -300 {lab=CLK_B}
N 470 -400 530 -400 {lab=VDD}
N 530 -450 530 -400 {lab=VDD}
N 470 -450 530 -450 {lab=VDD}
N 470 -300 530 -300 {lab=VDD}
N 530 -400 530 -300 {lab=VDD}
N 750 -400 810 -400 {lab=VDD}
N 810 -450 810 -400 {lab=VDD}
N 750 -450 810 -450 {lab=VDD}
N 750 -300 810 -300 {lab=VDD}
N 810 -400 810 -300 {lab=VDD}
N 470 -200 530 -200 {lab=VSS}
N 530 -100 530 -50 {lab=VSS}
N 470 -50 530 -50 {lab=VSS}
N 470 -100 530 -100 {lab=VSS}
N 530 -200 530 -100 {lab=VSS}
N 750 -200 810 -200 {lab=VSS}
N 810 -200 810 -100 {lab=VSS}
N 750 -100 810 -100 {lab=VSS}
N 750 -50 810 -50 {lab=VSS}
N 810 -100 810 -50 {lab=VSS}
N 630 -50 630 -30 {lab=VSS}
N 530 -50 630 -50 {lab=VSS}
N 630 -470 630 -450 {lab=VDD}
N 530 -450 630 -450 {lab=VDD}
N 570 -250 610 -250 {lab=X}
N 470 -270 470 -250 {lab=X}
N 610 -400 610 -250 {lab=X}
N 570 -270 570 -250 {lab=X}
N 470 -250 570 -250 {lab=X}
N 750 -250 850 -250 {lab=Q}
N 750 -270 750 -250 {lab=Q}
N 210 -180 230 -180 {lab=CLK_B}
N 60 -180 90 -180 {lab=CLK}
N 140 -240 140 -220 {lab=VDD}
N 140 -140 140 -120 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 450 -300 0 0 {name=M2
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 450 -200 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 450 -400 0 0 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 450 -100 0 0 {name=M4
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 730 -300 0 0 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 730 -200 0 0 {name=M6
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 730 -400 0 0 {name=M7
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 730 -100 0 0 {name=M8
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {ipin.sym} 290 -250 0 0 {name=p1 lab=D}
C {opin.sym} 850 -250 0 0 {name=p2 lab=Q}
C {iopin.sym} 630 -470 0 0 {name=p3 lab=VDD}
C {lab_pin.sym} 570 -270 2 0 {name=p4 sig_type=std_logic lab=X}
C {iopin.sym} 630 -30 0 0 {name=p5 lab=VSS}
C {ipin.sym} 410 -300 0 0 {name=p6 lab=CLK}
C {lab_pin.sym} 690 -300 0 0 {name=p8 sig_type=std_logic lab=CLK_B}
C {lab_pin.sym} 690 -200 0 0 {name=p9 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 410 -200 0 0 {name=p7 sig_type=std_logic lab=CLK_B}
C {inv/inv.sym} 50 -40 0 0 {name=x1}
C {lab_pin.sym} 60 -180 0 0 {name=p10 sig_type=std_logic lab=CLK}
C {lab_pin.sym} 230 -180 2 0 {name=p11 sig_type=std_logic lab=CLK_B}
C {lab_pin.sym} 140 -240 0 0 {name=p12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 140 -120 0 0 {name=p13 sig_type=std_logic lab=VSS}
