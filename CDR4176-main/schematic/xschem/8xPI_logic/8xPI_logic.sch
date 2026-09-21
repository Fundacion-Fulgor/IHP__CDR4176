v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1020 -540 1060 -540 {lab=#net1}
N 950 -500 950 -460 {lab=VSS}
N 1020 -460 1110 -460 {lab=VSS}
N 1110 -500 1110 -460 {lab=VSS}
N 950 -620 950 -580 {lab=VDD}
N 1020 -620 1110 -620 {lab=VDD}
N 1110 -620 1110 -580 {lab=VDD}
N 840 -540 900 -540 {lab=Sbuff[4]}
N 1180 -540 1220 -540 {lab=SQ[1]}
N 630 -250 670 -250 {lab=SQ[0]}
N 470 -540 510 -540 {lab=#net2}
N 400 -500 400 -460 {lab=VSS}
N 400 -460 560 -460 {lab=VSS}
N 560 -500 560 -460 {lab=VSS}
N 400 -620 400 -580 {lab=VDD}
N 400 -620 560 -620 {lab=VDD}
N 560 -620 560 -580 {lab=VDD}
N 290 -540 350 -540 {lab=S[3]}
N 630 -540 670 -540 {lab=SQ[2]}
N 450 -260 510 -260 {lab=S[4]}
N 450 -240 510 -240 {lab=S[3]}
N 1570 -540 1610 -540 {lab=SCb[7:1]}
N 1500 -500 1500 -460 {lab=VSS}
N 1500 -460 1660 -460 {lab=VSS}
N 1660 -500 1660 -460 {lab=VSS}
N 1500 -620 1500 -580 {lab=VDD}
N 1500 -620 1660 -620 {lab=VDD}
N 1660 -620 1660 -580 {lab=VDD}
N 1390 -540 1450 -540 {lab=Sbuff[3]}
N 1730 -540 1770 -540 {lab=SC[7:1]}
N 1030 -250 1070 -250 {lab=STQ[7:1]}
N 850 -260 910 -260 {lab=SC[7:1]}
N 850 -240 910 -240 {lab=ST[7:1]}
N 1020 -680 1020 -620 {lab=VDD}
N 560 -620 950 -620 {lab=VDD}
N 1020 -460 1020 -400 {lab=VSS}
N 560 -460 950 -460 {lab=VSS}
N 560 -350 560 -310 {lab=VDD}
N 560 -190 560 -150 {lab=VSS}
N 1110 -620 1500 -620 {lab=VDD}
N 1110 -460 1500 -460 {lab=VSS}
N 950 -620 1020 -620 {lab=VDD}
N 950 -460 1020 -460 {lab=VSS}
N 960 -190 960 -150 {lab=VSS}
N 770 -150 960 -150 {lab=VSS}
N 770 -350 960 -350 {lab=VDD}
N 960 -350 960 -310 {lab=VDD}
N 770 -410 770 -350 {lab=VDD}
N 560 -350 770 -350 {lab=VDD}
N 770 -150 770 -90 {lab=VSS}
N 560 -150 770 -150 {lab=VSS}
N 170 -340 230 -340 {lab=S[3]}
N 280 -440 280 -380 {lab=VDD}
N 280 -300 280 -240 {lab=VSS}
C {inv_CDR/inv_CDR.sym} 860 -400 0 0 {name=x1}
C {inv_CDR/inv_CDR.sym} 1020 -400 0 0 {name=x2}
C {xor_custom/xor_custom.sym} 460 -160 0 0 {name=x3}
C {ipin.sym} 740 -660 0 0 {name=p1 lab=S[4:3]}
C {iopin.sym} 1020 -400 0 0 {name=p2 lab=VSS}
C {lab_pin.sym} 170 -340 0 0 {name=p3 sig_type=std_logic lab=S[3]}
C {opin.sym} 1070 -250 0 0 {name=p4 lab=STQ[7:1]}
C {lab_pin.sym} 1220 -540 2 0 {name=p5 sig_type=std_logic lab=SQ[1]}
C {lab_pin.sym} 670 -250 2 0 {name=p6 sig_type=std_logic lab=SQ[0]}
C {inv_CDR/inv_CDR.sym} 310 -400 0 0 {name=x4}
C {inv_CDR/inv_CDR.sym} 470 -400 0 0 {name=x5}
C {lab_pin.sym} 290 -540 0 0 {name=p7 sig_type=std_logic lab=S[3]}
C {lab_pin.sym} 670 -540 2 0 {name=p8 sig_type=std_logic lab=SQ[2]}
C {lab_pin.sym} 450 -260 0 0 {name=p9 sig_type=std_logic lab=S[4]}
C {lab_pin.sym} 450 -240 0 0 {name=p10 sig_type=std_logic lab=S[3]}
C {inv_CDR/inv_CDR.sym} 1410 -400 0 0 {name=x6[6:0]}
C {inv_CDR/inv_CDR.sym} 1570 -400 0 0 {name=x7[6:0]}
C {lab_pin.sym} 1590 -540 1 0 {name=p13 sig_type=std_logic lab=SCb[7:1]}
C {lab_pin.sym} 1770 -540 2 0 {name=p14 sig_type=std_logic lab=SC[7:1]
}
C {xor_custom/xor_custom.sym} 860 -160 0 0 {name=x1[6:0]}
C {lab_pin.sym} 850 -260 0 0 {name=p15 sig_type=std_logic lab=SC[7:1]}
C {ipin.sym} 850 -240 0 0 {name=p17 lab=ST[7:1]}
C {iopin.sym} 1020 -680 0 0 {name=p12 lab=VDD}
C {lab_pin.sym} 770 -410 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 770 -90 0 0 {name=p18 sig_type=std_logic lab=VSS}
C {opin.sym} 800 -660 0 0 {name=p19 lab=SQ[2:0]}
C {buff_d8/buff_d8.sym} 280 -340 0 0 {name=x6}
C {lab_pin.sym} 280 -440 0 0 {name=p20 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 280 -240 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 350 -340 2 0 {name=p22 sig_type=std_logic lab=Sbuff[3]}
C {lab_pin.sym} 840 -540 0 0 {name=p23 sig_type=std_logic lab=S[4]}
C {lab_pin.sym} 1390 -540 0 0 {name=p11 sig_type=std_logic lab=Sbuff[3]}
