v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 440 -640 800 -640 {lab=#net1}
N 800 -640 800 -610 {lab=#net1}
N 640 -800 840 -800 {lab=#net2}
N 840 -800 840 -610 {lab=#net2}
N 400 -960 400 -400 {lab=#net3}
N 230 -960 400 -960 {lab=#net3}
N 420 -800 420 -400 {lab=#net2}
N 230 -800 420 -800 {lab=#net2}
N 440 -640 440 -400 {lab=#net1}
N 230 -640 440 -640 {lab=#net1}
N 600 -960 600 -380 {lab=#net3}
N 640 -800 640 -380 {lab=#net2}
N 420 -800 640 -800 {lab=#net2}
N 400 -960 600 -960 {lab=#net3}
N 1190 -640 1660 -640 {lab=#net1}
N 1190 -640 1190 -610 {lab=#net1}
N 1150 -800 1150 -610 {lab=#net2}
N 1150 -800 1380 -800 {lab=#net2}
N 1170 -510 1170 -410 {lab=#net4}
N 1130 -460 1130 -410 {lab=#net3}
N 1060 -460 1130 -460 {lab=#net3}
N 1060 -960 1060 -460 {lab=#net3}
N 780 -420 780 -380 {lab=#net3}
N 690 -420 780 -420 {lab=#net3}
N 690 -960 690 -420 {lab=#net3}
N 600 -960 690 -960 {lab=#net3}
N 820 -460 820 -380 {lab=#net5}
N 960 -960 1060 -960 {lab=#net3}
N 800 -640 1190 -640 {lab=#net1}
N 840 -800 1150 -800 {lab=#net2}
N 1380 -800 1380 -410 {lab=#net2}
N 1340 -960 1340 -410 {lab=#net3}
N 1060 -960 1340 -960 {lab=#net3}
N 1660 -640 1660 -410 {lab=#net1}
N 1630 -800 1630 -410 {lab=#net2}
N 1380 -800 1630 -800 {lab=#net2}
N 1600 -960 1600 -410 {lab=#net3}
N 1340 -960 1600 -960 {lab=#net3}
N 160 -1020 160 -1000 {lab=VDD}
N 160 -920 160 -900 {lab=VSS}
N 160 -860 160 -840 {lab=VDD}
N 160 -760 160 -740 {lab=VSS}
N 160 -700 160 -680 {lab=VDD}
N 160 -600 160 -570 {lab=VSS}
N 340 -350 360 -350 {lab=VSS}
N 480 -350 500 -350 {lab=VDD}
N 540 -350 560 -350 {lab=VSS}
N 680 -350 700 -350 {lab=VDD}
N 720 -350 740 -350 {lab=VSS}
N 860 -350 880 -350 {lab=VDD}
N 720 -550 750 -550 {lab=VSS}
N 890 -550 920 -550 {lab=VDD}
N 900 -350 920 -350 {lab=VSS}
N 1000 -350 1020 -350 {lab=VDD}
N 1060 -350 1080 -350 {lab=VSS}
N 1220 -350 1240 -350 {lab=VDD}
N 1270 -350 1290 -350 {lab=VSS}
N 1430 -350 1450 -350 {lab=VDD}
N 80 -960 110 -960 {lab=S[2]}
N 80 -800 110 -800 {lab=S[1]}
N 80 -640 110 -640 {lab=S[1]}
N 420 -260 420 -220 {lab=ST[1]}
N 620 -250 620 -220 {lab=ST[2]}
N 800 -250 800 -220 {lab=ST[3]}
N 1150 -240 1150 -220 {lab=ST[5]}
N 960 -280 960 -220 {lab=ST[4]}
N 1360 -240 1360 -220 {lab=ST[6]}
N 1630 -240 1630 -220 {lab=ST[7]}
N 1540 -350 1560 -350 {lab=VSS}
N 1700 -350 1720 -350 {lab=VDD}
N 1090 -580 1110 -580 {lab=VSS}
N 1230 -580 1250 -580 {lab=VDD}
N 960 -960 960 -400 {lab=#net3}
N 690 -960 960 -960 {lab=#net3}
C {inv_CDR/inv_CDR.sym} 70 -820 0 0 {name=x1}
C {inv_CDR/inv_CDR.sym} 70 -660 0 0 {name=x2}
C {inv_CDR/inv_CDR.sym} 70 -500 0 0 {name=x3}
C {nor_x3_custom/nor_x3_custom.sym} 340 -440 1 0 {name=x4}
C {nor_custom/nor_custom.sym} 550 -410 1 0 {name=x5}
C {nor_custom/nor_custom.sym} 730 -410 1 0 {name=x6}
C {inv_CDR/inv_CDR.sym} 820 -440 1 0 {name=x7}
C {nand_custom/nand_custom.sym} 1030 -450 1 0 {name=x8}
C {nand_custom/nand_custom.sym} 1240 -450 1 0 {name=x9}
C {and_custom/and_custom.sym} 700 -670 1 0 {name=x11}
C {or_custom/or_custom.sym} 1100 -630 1 0 {name=x12}
C {nand_x3_custom/nand_x3_custom.sym} 1530 -430 1 0 {name=x10}
C {opin.sym} 270 -1070 0 0 {name=p48 lab=ST[7:1]}
C {ipin.sym} 340 -1050 0 0 {name=p49 lab=S[2:0]}
C {lab_pin.sym} 420 -220 3 0 {name=p3 sig_type=std_logic lab=ST[1]}
C {lab_pin.sym} 620 -220 3 0 {name=p1 sig_type=std_logic lab=ST[2]}
C {lab_pin.sym} 800 -220 3 0 {name=p2 sig_type=std_logic lab=ST[3]}
C {lab_pin.sym} 960 -220 3 0 {name=p4 sig_type=std_logic lab=ST[4]}
C {lab_pin.sym} 1150 -220 3 0 {name=p5 sig_type=std_logic lab=ST[5]}
C {lab_pin.sym} 1360 -220 3 0 {name=p6 sig_type=std_logic lab=ST[6]}
C {lab_pin.sym} 1630 -220 3 0 {name=p7 sig_type=std_logic lab=ST[7]}
C {lab_pin.sym} 80 -960 0 0 {name=p8 sig_type=std_logic lab=S[2]}
C {lab_pin.sym} 80 -800 0 0 {name=p9 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 80 -640 0 0 {name=p10 sig_type=std_logic lab=S[0]}
C {iopin.sym} 160 -1020 0 0 {name=p11 lab=VDD}
C {iopin.sym} 160 -900 0 0 {name=p12 lab=VSS}
C {lab_pin.sym} 160 -860 0 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 160 -740 0 0 {name=p15 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 160 -570 0 0 {name=p13 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 160 -700 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 340 -350 3 0 {name=p17 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 540 -350 3 0 {name=p18 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 720 -350 3 0 {name=p19 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 900 -350 3 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1060 -350 3 0 {name=p21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1270 -350 3 0 {name=p22 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1540 -350 3 0 {name=p23 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1020 -350 1 0 {name=p26 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 880 -350 1 0 {name=p27 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1240 -350 1 0 {name=p28 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1450 -350 1 0 {name=p29 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1720 -350 1 0 {name=p30 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 700 -350 1 0 {name=p24 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 500 -350 1 0 {name=p25 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 920 -550 1 0 {name=p31 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1250 -580 1 0 {name=p32 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1090 -580 3 0 {name=p33 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 720 -550 3 0 {name=p34 sig_type=std_logic lab=VSS}
