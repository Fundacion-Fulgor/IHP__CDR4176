v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 390 -1220 450 -1220 {lab=#net1}
N 450 -1220 450 -1140 {lab=#net1}
N 450 -1140 480 -1140 {lab=#net1}
N 390 -1020 450 -1020 {lab=#net2}
N 450 -1100 450 -1020 {lab=#net2}
N 450 -1100 480 -1100 {lab=#net2}
N 460 -540 490 -540 {lab=#net3}
N 460 -580 460 -540 {lab=#net3}
N 400 -580 460 -580 {lab=#net3}
N 600 -1650 710 -1650 {lab=ST[1]}
N 600 -1430 710 -1430 {lab=ST[2]}
N 590 -1120 710 -1120 {lab=ST[3]}
N 600 -520 720 -520 {lab=ST[5]}
N 600 -320 720 -320 {lab=ST[6]}
N 590 -120 720 -120 {lab=ST[7]}
N 310 -670 310 -650 {lab=VDD}
N 300 -950 300 -930 {lab=VSS}
N 310 -510 310 -490 {lab=VSS}
N 520 -600 520 -580 {lab=VDD}
N 520 -460 520 -440 {lab=VSS}
N 460 -500 490 -500 {lab=S[0]}
N 460 -500 460 -440 {lab=S[0]}
N 200 -440 460 -440 {lab=S[0]}
N 200 -560 250 -560 {lab=S[2]}
N 200 -600 250 -600 {lab=S[1]}
N 520 -400 520 -380 {lab=VDD}
N 520 -260 520 -240 {lab=VSS}
N 200 -340 490 -340 {lab=S[0]}
N 200 -300 490 -300 {lab=S[1]}
N 520 -200 520 -180 {lab=VDD}
N 520 -60 520 -40 {lab=VSS}
N 200 -100 480 -100 {lab=S[2]}
N 200 -120 480 -120 {lab=S[1]}
N 200 -140 480 -140 {lab=S[0]}
N 300 -1150 300 -1130 {lab=VSS}
N 300 -1110 300 -1090 {lab=VDD}
N 300 -1310 300 -1290 {lab=VDD}
N 510 -1360 510 -1340 {lab=VSS}
N 510 -1200 510 -1180 {lab=VDD}
N 510 -1060 510 -1040 {lab=VSS}
N 510 -1580 510 -1560 {lab=VSS}
N 510 -1520 510 -1500 {lab=VDD}
N 510 -1740 510 -1720 {lab=VDD}
N 190 -1000 240 -1000 {lab=S[2]}
N 190 -1040 240 -1040 {lab=S[0]}
N 190 -1200 240 -1200 {lab=S[1]}
N 190 -1240 240 -1240 {lab=S[0]}
N 190 -1410 450 -1410 {lab=S[1]}
N 190 -1450 450 -1450 {lab=S[0]}
N 190 -1680 450 -1680 {lab=S[0]}
N 190 -1650 450 -1650 {lab=S[1]}
N 190 -1620 450 -1620 {lab=S[2]}
N 310 -860 310 -840 {lab=VDD}
N 520 -860 520 -840 {lab=VDD}
N 380 -800 470 -800 {lab=#net4}
N 310 -760 310 -740 {lab=VSS}
N 520 -760 520 -740 {lab=VSS}
N 590 -800 720 -800 {lab=ST[4]}
N 200 -800 260 -800 {lab=S[0]}
C {and_custom/and_custom.sym} 390 -1310 0 0 {name=x1}
C {and_x3_custom/and_x3_custom.sym} 410 -1560 0 0 {name=x2}
C {or_custom/or_custom.sym} 460 -1050 0 0 {name=x3}
C {and_custom/and_custom.sym} 180 -1100 0 0 {name=x4}
C {and_custom/and_custom.sym} 180 -900 0 0 {name=x5}
C {or_custom/or_custom.sym} 470 -450 0 0 {name=x6}
C {and_custom/and_custom.sym} 190 -460 0 0 {name=x7}
C {or_custom/or_custom.sym} 470 -250 0 0 {name=x8}
C {or_x3_custom/or_x3_custom.sym} 450 -20 0 0 {name=x9}
C {iopin.sym} 510 -1740 0 0 {name=p10 lab=VDD}
C {iopin.sym} 510 -1560 0 0 {name=p11 lab=VSS}
C {lab_pin.sym} 190 -1450 0 0 {name=p12 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 190 -1410 0 0 {name=p13 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 510 -1520 0 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 510 -1340 0 0 {name=p15 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 510 -1200 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 510 -1040 0 0 {name=p17 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 -600 0 0 {name=p18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 520 -400 0 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 520 -440 0 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 -240 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 -40 0 0 {name=p22 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 520 -200 0 0 {name=p23 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 190 -1240 0 0 {name=p24 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 190 -1200 0 0 {name=p25 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 190 -1040 0 0 {name=p26 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 190 -1000 0 0 {name=p27 sig_type=std_logic lab=S[2]}
C {lab_pin.sym} 310 -670 0 0 {name=p28 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 310 -490 0 0 {name=p29 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 300 -930 0 0 {name=p30 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 300 -1110 0 0 {name=p31 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 300 -1310 0 0 {name=p32 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 300 -1130 0 0 {name=p33 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 200 -600 0 0 {name=p34 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 200 -560 0 0 {name=p35 sig_type=std_logic lab=S[2]}
C {lab_pin.sym} 200 -440 0 0 {name=p36 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 200 -340 0 0 {name=p37 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 200 -300 0 0 {name=p38 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 200 -140 0 0 {name=p39 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 200 -120 0 0 {name=p40 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 200 -100 0 0 {name=p41 sig_type=std_logic lab=S[2]}
C {inv/inv.sym} 220 -660 0 0 {name=x10}
C {inv/inv.sym} 430 -660 0 0 {name=x11}
C {lab_pin.sym} 200 -800 0 0 {name=p42 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 310 -740 0 0 {name=p43 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 310 -860 0 0 {name=p44 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 520 -860 0 0 {name=p45 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 520 -740 0 0 {name=p46 sig_type=std_logic lab=VSS}
C {opin.sym} 230 -1800 0 0 {name=p48 lab=ST[7:1]}
C {ipin.sym} 300 -1780 0 0 {name=p49 lab=S[2:0]}
C {lab_pin.sym} 710 -1650 2 0 {name=p3 sig_type=std_logic lab=ST[1]}
C {lab_pin.sym} 710 -1430 2 0 {name=p1 sig_type=std_logic lab=ST[2]}
C {lab_pin.sym} 710 -1120 2 0 {name=p2 sig_type=std_logic lab=ST[3]}
C {lab_pin.sym} 720 -800 2 0 {name=p47 sig_type=std_logic lab=ST[4]}
C {lab_pin.sym} 720 -520 2 0 {name=p4 sig_type=std_logic lab=ST[5]}
C {lab_pin.sym} 720 -320 2 0 {name=p5 sig_type=std_logic lab=ST[6]}
C {lab_pin.sym} 720 -120 2 0 {name=p6 sig_type=std_logic lab=ST[7]}
C {lab_pin.sym} 190 -1680 0 0 {name=p7 sig_type=std_logic lab=S[0]}
C {lab_pin.sym} 190 -1650 0 0 {name=p8 sig_type=std_logic lab=S[1]}
C {lab_pin.sym} 190 -1620 0 0 {name=p9 sig_type=std_logic lab=S[2]}
