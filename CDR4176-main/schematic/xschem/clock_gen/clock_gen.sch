v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 200 -740 230 -740 {lab=CTRL}
N 380 -570 380 -540 {lab=VSS}
N 380 -800 380 -770 {lab=VDD}
N 530 -720 630 -720 {lab=v0}
N 530 -660 630 -660 {lab=v5}
N 530 -680 630 -680 {lab=v2}
N 530 -700 630 -700 {lab=v3}
N 530 -620 630 -620 {lab=v1}
N 530 -640 630 -640 {lab=v4}
N 1130 -650 1230 -650 {lab=PH180}
N 1130 -690 1230 -690 {lab=PH90}
N 1130 -720 1230 -720 {lab=PH0}
N 1130 -620 1230 -620 {lab=PH270}
N 730 -720 830 -720 {lab=v0}
N 730 -700 830 -700 {lab=v1}
N 730 -680 830 -680 {lab=v2}
N 730 -660 830 -660 {lab=v3}
N 730 -640 830 -640 {lab=v4}
N 730 -620 830 -620 {lab=v5}
N 980 -590 980 -560 {lab=VSS}
N 980 -780 980 -750 {lab=v0}
C {6ph_rosc/6ph_rosc.sym} 380 -670 0 0 {name=x1}
C {devices/lab_pin.sym} 630 -660 2 0 {name=p5 sig_type=std_logic lab=v5}
C {devices/lab_pin.sym} 630 -680 2 0 {name=p6 sig_type=std_logic lab=v2
}
C {devices/lab_pin.sym} 630 -700 2 0 {name=p7 sig_type=std_logic lab=v3}
C {devices/lab_pin.sym} 630 -720 2 0 {name=p9 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} 630 -620 2 0 {name=p10 sig_type=std_logic lab=v1}
C {devices/lab_pin.sym} 630 -640 2 0 {name=p11 sig_type=std_logic lab=v4
}
C {iopin.sym} 380 -800 0 0 {name=p3 lab=VDD}
C {iopin.sym} 380 -540 0 0 {name=p4 lab=VSS}
C {ipin.sym} 200 -740 0 0 {name=p1 lab=CTRL}
C {opin.sym} 1230 -720 0 0 {name=p22 lab=PH0}
C {opin.sym} 1230 -690 0 0 {name=p23 lab=PH90}
C {opin.sym} 1230 -650 0 0 {name=p24 lab=PH180}
C {opin.sym} 1230 -620 0 0 {name=p25 lab=PH270}
C {6to4/6to4.sym} 980 -670 0 0 {name=x22}
C {devices/lab_pin.sym} 730 -720 0 0 {name=p2 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} 730 -700 0 0 {name=p8 sig_type=std_logic lab=v1}
C {devices/lab_pin.sym} 730 -680 0 0 {name=p12 sig_type=std_logic lab=v2}
C {devices/lab_pin.sym} 730 -660 0 0 {name=p13 sig_type=std_logic lab=v3}
C {devices/lab_pin.sym} 730 -640 0 0 {name=p14 sig_type=std_logic lab=v4}
C {devices/lab_pin.sym} 730 -620 0 0 {name=p15 sig_type=std_logic lab=v5}
C {devices/lab_pin.sym} 980 -780 2 0 {name=p16 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 980 -560 2 0 {name=p17 sig_type=std_logic lab=VSS}
