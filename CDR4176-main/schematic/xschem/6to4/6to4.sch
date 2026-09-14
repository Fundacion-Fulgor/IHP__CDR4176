v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1265 -700 1365 -700 {lab=V2}
N 1265 -800 1365 -800 {lab=V1}
N 1275 -140 1375 -140 {lab=V5}
N 1550 -70 1550 -40 {lab=VSS}
N 1550 -340 1550 -310 {lab=VDD}
N 1275 -240 1375 -240 {lab=V4}
N 1540 -900 1540 -870 {lab=VDD}
N 1540 -630 1540 -600 {lab=VSS}
N 1410 -1080 1410 -1050 {lab=VDD}
N 1410 -970 1410 -940 {lab=VSS}
N 1410 -550 1410 -520 {lab=VDD}
N 1410 -440 1410 -410 {lab=VSS}
N 1640 -1080 1640 -1050 {lab=VDD}
N 1640 -970 1640 -940 {lab=VSS}
N 1260 -480 1360 -480 {lab=V3}
N 1260 -1010 1360 -1010 {lab=V0}
N 1640 -550 1640 -520 {lab=VDD}
N 1640 -440 1640 -410 {lab=VSS}
N 1970 -1010 2070 -1010 {lab=PH0}
N 1970 -190 2070 -190 {lab=PH270}
N 250 -900 350 -900 {lab=v360}
N 550 -900 650 -900 {lab=v180}
N 770 -900 870 -900 {lab=v90}
N 1070 -900 1170 -900 {lab=v270}
N 970 -1050 970 -1020 {lab=VDD}
N 1780 -850 1780 -750 {lab=v90}
N 1770 -580 1770 -480 {lab=v180}
N 1780 -290 1780 -190 {lab=v270}
N 1770 -1110 1770 -1010 {lab=v360}
N 970 -780 970 -750 {lab=VSS}
N 1780 -750 1850 -750 {lab=v90}
N 1780 -190 1850 -190 {lab=v270}
N 1720 -750 1780 -750 {lab=v90}
N 1770 -1010 1850 -1010 {lab=v360}
N 1770 -480 1850 -480 {lab=v180}
N 1730 -190 1780 -190 {lab=v270}
N 1480 -1010 1590 -1010 {lab=#net1}
N 1480 -480 1590 -480 {lab=#net2}
N 1710 -480 1770 -480 {lab=v180}
N 1710 -1010 1770 -1010 {lab=v360}
N 450 -1050 450 -1020 {lab=VDD}
N 450 -780 450 -750 {lab=VSS}
N 1900 -1080 1900 -1050 {lab=VDD}
N 1900 -970 1900 -940 {lab=VSS}
N 1970 -750 2070 -750 {lab=PH90}
N 1900 -820 1900 -790 {lab=VDD}
N 1900 -710 1900 -680 {lab=VSS}
N 1970 -480 2070 -480 {lab=PH180}
N 1900 -550 1900 -520 {lab=VDD}
N 1900 -440 1900 -410 {lab=VSS}
N 1900 -260 1900 -230 {lab=VDD}
N 1900 -150 1900 -120 {lab=VSS}
C {PI_clk/PI_clk.sym} 1350 -50 0 0 {name=x16}
C {devices/lab_pin.sym} 1550 -40 2 0 {name=p55 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1550 -340 2 0 {name=p56 sig_type=std_logic lab=VDD}
C {PI_clk/PI_clk.sym} 1340 -610 0 0 {name=x2}
C {devices/lab_pin.sym} 1540 -900 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1540 -600 2 0 {name=p13 sig_type=std_logic lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 1410 -1010 0 0 {name=x8}
C {devices/lab_pin.sym} 1410 -1080 2 0 {name=p31 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1410 -940 2 0 {name=p32 sig_type=std_logic lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 1410 -480 0 0 {name=x9}
C {devices/lab_pin.sym} 1410 -550 2 0 {name=p33 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1410 -410 2 0 {name=p34 sig_type=std_logic lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 1640 -1010 0 0 {name=x10}
C {devices/lab_pin.sym} 1640 -1080 2 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1640 -940 2 0 {name=p36 sig_type=std_logic lab=VSS}
C {inv_PI_d2/inv_PI_d2.sym} 1640 -480 0 0 {name=x11}
C {devices/lab_pin.sym} 1640 -550 2 0 {name=p40 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1640 -410 2 0 {name=p41 sig_type=std_logic lab=VSS}
C {opin.sym} 2070 -1010 0 0 {name=p22 lab=PH0}
C {opin.sym} 2070 -750 0 0 {name=p23 lab=PH90}
C {opin.sym} 2070 -480 0 0 {name=p24 lab=PH180}
C {opin.sym} 2070 -190 0 0 {name=p25 lab=PH270}
C {flywheel_clk/flywheel_clk.sym} 450 -900 0 0 {name=x7
}
C {flywheel_clk/flywheel_clk.sym} 970 -900 0 0 {name=x12
}
C {devices/lab_pin.sym} 250 -900 0 0 {name=p26 sig_type=std_logic lab=v360
}
C {devices/lab_pin.sym} 650 -900 2 0 {name=p27 sig_type=std_logic lab=v180
}
C {devices/lab_pin.sym} 770 -900 0 0 {name=p28 sig_type=std_logic lab=v90
}
C {devices/lab_pin.sym} 1170 -900 2 0 {name=p29 sig_type=std_logic lab=v270
}
C {devices/lab_pin.sym} 970 -1050 2 0 {name=p42 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1780 -850 1 0 {name=p43 sig_type=std_logic lab=v90
}
C {devices/lab_pin.sym} 1770 -580 1 0 {name=p44 sig_type=std_logic lab=v180
}
C {devices/lab_pin.sym} 1780 -290 1 0 {name=p45 sig_type=std_logic lab=v270
}
C {devices/lab_pin.sym} 1770 -1110 1 0 {name=p46 sig_type=std_logic lab=v360
}
C {devices/lab_pin.sym} 970 -750 2 0 {name=p48 sig_type=std_logic lab=VSS}
C {ipin.sym} 1260 -1010 0 0 {name=p1 lab=V0}
C {ipin.sym} 1270 -800 0 0 {name=p3 lab=V1}
C {ipin.sym} 1270 -700 0 0 {name=p4 lab=V2}
C {ipin.sym} 1260 -480 0 0 {name=p5 lab=V3}
C {ipin.sym} 1280 -240 0 0 {name=p6 lab=V4}
C {ipin.sym} 1280 -140 0 0 {name=p7 lab=V5}
C {iopin.sym} 450 -1050 0 0 {name=p9 lab=VDD}
C {iopin.sym} 450 -750 0 0 {name=p10 lab=VSS}
C {buff_PI_d32/buff_PI_d32.sym} 1900 -1010 0 0 {name=x1}
C {devices/lab_pin.sym} 1900 -1080 2 0 {name=p11 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1900 -940 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {buff_PI_d32/buff_PI_d32.sym} 1900 -750 0 0 {name=x4}
C {devices/lab_pin.sym} 1900 -820 2 0 {name=p14 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1900 -680 2 0 {name=p15 sig_type=std_logic lab=VSS}
C {buff_PI_d32/buff_PI_d32.sym} 1900 -480 0 0 {name=x3}
C {devices/lab_pin.sym} 1900 -550 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1900 -410 2 0 {name=p8 sig_type=std_logic lab=VSS}
C {buff_PI_d32/buff_PI_d32.sym} 1900 -190 0 0 {name=x5}
C {devices/lab_pin.sym} 1900 -260 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1900 -120 2 0 {name=p18 sig_type=std_logic lab=VSS}
