v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 310 -760 310 -740 {lab=VDD}
N 310 -660 310 -640 {lab=VSS}
N 310 -580 310 -560 {lab=VDD}
N 310 -480 310 -460 {lab=VSS}
N 310 -400 310 -380 {lab=VDD}
N 310 -300 310 -280 {lab=VSS}
N 310 -220 310 -200 {lab=VDD}
N 310 -120 310 -100 {lab=VSS}
N 510 -760 510 -740 {lab=VDD}
N 510 -660 510 -640 {lab=VSS}
N 510 -580 510 -560 {lab=VDD}
N 510 -480 510 -460 {lab=VSS}
N 510 -400 510 -380 {lab=VDD}
N 510 -300 510 -280 {lab=VSS}
N 510 -220 510 -200 {lab=VDD}
N 510 -120 510 -100 {lab=VSS}
N 380 -340 460 -340 {lab=#net1}
N 380 -160 460 -160 {lab=#net2}
N 380 -520 460 -520 {lab=#net3}
N 380 -700 460 -700 {lab=#net4}
N 180 -700 260 -700 {lab=VINI}
N 580 -700 660 -700 {lab=VOUTI}
N 180 -520 260 -520 {lab=VINQ}
N 180 -340 260 -340 {lab=VINIB}
N 180 -160 260 -160 {lab=VINQB}
N 580 -520 660 -520 {lab=VOUTQ}
N 580 -340 660 -340 {lab=VOUTIB}
N 580 -160 660 -160 {lab=VOUTQB}
C {inv/inv.sym} 220 -560 0 0 {name=x0}
C {lab_wire.sym} 310 -640 2 0 {name=p13 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 220 -380 0 0 {name=x1}
C {lab_wire.sym} 310 -580 2 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 310 -460 2 0 {name=p2 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 220 -200 0 0 {name=x2}
C {lab_wire.sym} 310 -400 2 0 {name=p3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 310 -280 2 0 {name=p4 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 220 -20 0 0 {name=x3}
C {lab_wire.sym} 310 -220 2 0 {name=p5 sig_type=std_logic lab=VDD}
C {inv/inv.sym} 420 -560 0 0 {name=x4}
C {lab_wire.sym} 510 -760 2 0 {name=p7 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 510 -640 2 0 {name=p8 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 420 -380 0 0 {name=x5}
C {lab_wire.sym} 510 -580 2 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 510 -460 2 0 {name=p10 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 420 -200 0 0 {name=x6}
C {lab_wire.sym} 510 -400 2 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 510 -280 2 0 {name=p14 sig_type=std_logic lab=VSS}
C {inv/inv.sym} 420 -20 0 0 {name=x7}
C {lab_wire.sym} 510 -220 2 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 510 -100 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {iopin.sym} 310 -760 2 0 {name=p17 lab=VDD}
C {iopin.sym} 310 -100 2 0 {name=p6 lab=VSS}
C {ipin.sym} 180 -700 0 0 {name=p12 lab=VINI}
C {ipin.sym} 180 -520 0 0 {name=p18 lab=VINQ}
C {ipin.sym} 180 -340 0 0 {name=p19 lab=VINIB}
C {ipin.sym} 180 -160 0 0 {name=p20 lab=VINQB}
C {opin.sym} 660 -700 0 0 {name=p21 lab=VOUTI}
C {opin.sym} 660 -520 0 0 {name=p22 lab=VOUTQ}
C {opin.sym} 660 -340 0 0 {name=p23 lab=VOUTIB}
C {opin.sym} 660 -160 0 0 {name=p24 lab=VOUTQB}
