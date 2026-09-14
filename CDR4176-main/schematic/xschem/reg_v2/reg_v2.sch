v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 280 -660 320 -660 {lab=CLK_B}
N 120 -660 160 -660 {lab=CLK}
N 60 -380 100 -380 {lab=#net1}
N 220 -380 260 -380 {lab=#net2}
N 1040 -360 1080 -360 {lab=#net3}
N 150 -460 150 -420 {lab=VDD}
N 150 -340 150 -300 {lab=VSS}
N 150 -180 150 -140 {lab=VDD}
N 60 -100 100 -100 {lab=D}
N 220 -100 260 -100 {lab=#net4}
N 340 -60 340 -20 {lab=CLK}
N 970 -320 970 -280 {lab=VSS}
N 970 -60 970 0 {lab=VSS}
N 1040 -100 1080 -100 {lab=#net5}
N 900 -360 920 -360 {lab=Q}
N 900 -520 900 -360 {lab=Q}
N 1240 -100 1260 -100 {lab=#net6}
N 1260 -360 1260 -100 {lab=#net6}
N 1240 -360 1260 -360 {lab=#net6}
N 60 -520 60 -380 {lab=#net1}
N 460 -380 460 -100 {lab=#net7}
N 970 -460 970 -400 {lab=VDD}
N 970 -180 970 -140 {lab=VDD}
N 280 -440 280 -420 {lab=VSS}
N 340 -460 340 -420 {lab=CLK}
N 280 -340 280 -300 {lab=VDD}
N 280 -180 280 -140 {lab=VSS}
N 150 -60 150 -0 {lab=VSS}
N 280 -60 280 -40 {lab=VDD}
N 210 -620 210 -580 {lab=VSS}
N 210 -740 210 -700 {lab=VDD}
N 340 -340 340 -140 {lab=CLK_B}
N 1160 -320 1160 -140 {lab=CLK}
N 460 -380 580 -380 {lab=#net7}
N 1260 -360 1330 -360 {lab=#net6}
N 420 -380 460 -380 {lab=#net7}
N 1570 -360 1680 -360 {lab=Q}
N 1450 -360 1570 -360 {lab=Q}
N 700 -380 810 -380 {lab=#net1}
N 420 -100 460 -100 {lab=#net7}
N 1100 -420 1100 -400 {lab=VSS}
N 1160 -440 1160 -400 {lab=CLK_B}
N 1100 -320 1100 -280 {lab=VDD}
N 1160 -60 1160 -20 {lab=CLK_B}
N 1100 -180 1100 -140 {lab=VSS}
N 1100 -60 1100 -40 {lab=VDD}
N 810 -380 810 -100 {lab=#net1}
N 630 -340 630 -280 {lab=VSS}
N 630 -460 630 -420 {lab=VDD}
N 810 -520 810 -380 {lab=#net1}
N 60 -520 810 -520 {lab=#net1}
N 1380 -320 1380 -260 {lab=VSS}
N 1380 -440 1380 -400 {lab=VDD}
N 900 -520 1570 -520 {lab=Q}
N 1570 -520 1570 -360 {lab=Q}
N 810 -100 920 -100 {lab=#net1}
C {lab_wire.sym} 150 -460 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 150 -180 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 970 -180 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 970 -460 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 150 -300 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 970 -280 0 0 {name=p9 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 970 0 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 150 0 0 0 {name=p14 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 280 -300 2 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 280 -440 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 280 -180 2 0 {name=p17 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 280 -40 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {iopin.sym} 210 -740 0 0 {name=p19 lab=VDD}
C {iopin.sym} 210 -580 0 0 {name=p20 lab=VSS}
C {ipin.sym} 120 -660 0 0 {name=p21 lab=CLK}
C {lab_wire.sym} 320 -660 0 1 {name=p22 sig_type=std_logic lab=CLK_B}
C {ipin.sym} 60 -100 0 0 {name=p25 lab=D}
C {lab_wire.sym} 340 -460 0 1 {name=p34 sig_type=std_logic lab=CLK}
C {lab_wire.sym} 340 -20 0 1 {name=p35 sig_type=std_logic lab=CLK}
C {lab_wire.sym} 340 -240 0 1 {name=p36 sig_type=std_logic lab=CLK_B}
C {lab_wire.sym} 1160 -230 0 1 {name=p37 sig_type=std_logic lab=CLK}
C {opin.sym} 1680 -360 0 0 {name=p38 lab=Q}
C {tg_custom/tg_custom.sym} 340 -380 2 1 {name=x3}
C {inv/inv.sym} 120 -520 0 0 {name=x9}
C {inv/inv.sym} 60 -240 0 0 {name=x4}
C {inv/inv.sym} 60 40 0 0 {name=x8}
C {inv/inv.sym} 880 -220 0 0 {name=x11}
C {inv/inv.sym} 880 40 0 0 {name=x10}
C {tg_custom/tg_custom.sym} 340 -100 2 1 {name=x2}
C {lab_wire.sym} 1100 -280 2 0 {name=p23 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1100 -420 2 0 {name=p24 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 1160 -440 0 1 {name=p32 sig_type=std_logic lab=CLK_B}
C {tg_custom/tg_custom.sym} 1160 -360 2 1 {name=x6}
C {lab_wire.sym} 1100 -180 2 0 {name=p11 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 1100 -40 2 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1160 -20 0 1 {name=p33 sig_type=std_logic lab=CLK_B}
C {tg_custom/tg_custom.sym} 1160 -100 2 1 {name=x7}
C {lab_wire.sym} 630 -460 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 630 -280 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 540 -240 0 0 {name=x5}
C {lab_wire.sym} 1380 -440 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1380 -260 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 1290 -220 0 0 {name=x1}
