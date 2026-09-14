v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 770 -500 770 -400 {lab="VSTQ[7:1], VSQ[2]"}
N 550 -590 620 -590 {lab=VST[7:1]}
N 80 -340 120 -340 {lab=VCONT}
N 900 -460 900 -400 {lab=VDD}
N 900 -160 900 -100 {lab=VSS}
N 1100 -280 1160 -280 {lab=VOUT}
N 270 -220 270 -160 {lab=VSS}
N 270 -440 270 -380 {lab=VDD}
N 1010 -530 1010 -470 {lab=VSS}
N 450 -700 450 -640 {lab=VDD}
N 310 -590 350 -590 {lab=VS[2:0]}
N 780 -160 780 -100 {lab=VSQ[1:0]}
N 740 -100 780 -100 {lab=VSQ[1:0]}
N 820 -610 860 -610 {lab=VS[4:3]}
N 1160 -610 1200 -610 {lab=VSQ[2:0]}
N 820 -570 860 -570 {lab=VST[7:1]}
N 1160 -570 1200 -570 {lab=VSTQ[7:1]}
N 1010 -710 1010 -650 {lab=VDD}
N 450 -540 450 -480 {lab=VSS}
N 640 -350 680 -350 {lab=VI}
N 600 -310 680 -310 {lab=VIB}
N 640 -230 680 -230 {lab=#net1}
N 600 -270 680 -270 {lab=VQ}
N 420 -340 480 -340 {lab=VI}
N 420 -320 480 -320 {lab=VQ}
N 420 -280 480 -280 {lab=VIB}
N 420 -260 480 -260 {lab=VQB}
C {8xPI/8xPI.sym} 660 -140 0 0 {name=x1}
C {clock_gen/clock_gen.sym} 270 -300 0 0 {name=x2}
C {3to7_deco_v2/3to7_deco_v2.sym} 320 -520 0 0 {name=x3}
C {ipin.sym} 80 -340 0 0 {name=p6 lab=VCONT
}
C {iopin.sym} 900 -460 2 0 {name=p1 lab=VDD}
C {iopin.sym} 900 -100 2 0 {name=p3 lab=VSS
}
C {devices/lab_pin.sym} 270 -440 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {opin.sym} 1160 -280 0 0 {name=p8 lab=VOUT}
C {devices/lab_pin.sym} 270 -160 2 0 {name=p4 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1010 -470 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 450 -700 2 0 {name=p10 sig_type=std_logic lab=VDD}
C {ipin.sym} 180 -520 0 0 {name=p11 lab=VS[4:0]

}
C {devices/lab_pin.sym} 310 -590 0 0 {name=p12 sig_type=std_logic lab=VS[2:0]}
C {devices/lab_pin.sym} 820 -610 0 0 {name=p13 sig_type=std_logic lab=VS[4:3]}
C {devices/lab_pin.sym} 620 -590 2 0 {name=p14 sig_type=std_logic lab=VST[7:1]}
C {devices/lab_pin.sym} 770 -500 2 0 {name=p15 sig_type=std_logic lab="VSTQ[7:1], VSQ[2]"}
C {8xPI_logic/8xPI_logic.sym} 1010 -590 0 0 {name=x4}
C {devices/lab_pin.sym} 1200 -610 2 0 {name=p16 sig_type=std_logic lab=VSQ[2:0]}
C {devices/lab_pin.sym} 740 -100 0 0 {name=p17 sig_type=std_logic lab=VSQ[1:0]}
C {devices/lab_pin.sym} 820 -570 0 0 {name=p18 sig_type=std_logic lab=VST[7:1]}
C {devices/lab_pin.sym} 1200 -570 2 0 {name=p19 sig_type=std_logic lab=VSTQ[7:1]}
C {devices/lab_pin.sym} 1010 -710 2 0 {name=p20 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 450 -480 0 0 {name=p21 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 640 -350 0 0 {name=p22 sig_type=std_logic lab=VI}
C {devices/lab_pin.sym} 600 -310 0 0 {name=p23 sig_type=std_logic lab=VIB}
C {devices/lab_pin.sym} 640 -230 0 0 {name=p24 sig_type=std_logic lab=VQB}
C {devices/lab_pin.sym} 600 -270 0 0 {name=p25 sig_type=std_logic lab=VQ}
C {devices/lab_pin.sym} 480 -340 2 0 {name=p7 sig_type=std_logic lab=VI}
C {devices/lab_pin.sym} 480 -320 2 0 {name=p9 sig_type=std_logic lab=VQ}
C {devices/lab_pin.sym} 480 -280 2 0 {name=p26 sig_type=std_logic lab=VIB}
C {devices/lab_pin.sym} 480 -260 2 0 {name=p27 sig_type=std_logic lab=VQB}
