v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N 530 -430 530 -360 {lab=#net1}
N 970 -430 1040 -430 {lab=VOUT}
N 530 -280 530 -230 {lab=VS}
N 530 -640 530 -590 {lab=VS}
N 470 -510 470 -460 {lab=VSS}
N 470 -410 470 -360 {lab=VDD}
N 400 -430 530 -430 {lab=#net1}
N 530 -510 530 -430 {lab=#net1}
N 210 -430 280 -430 {lab=VS}
N 330 -490 330 -470 {lab=VDD}
N 330 -390 330 -370 {lab=VSS}
N 230 -610 230 -590 {lab=VDD}
N 230 -510 230 -490 {lab=VSS}
N 380 -550 450 -550 {lab=#net2}
N 120 -550 180 -550 {lab=VINA}
N 230 -380 230 -360 {lab=VDD}
N 230 -280 230 -260 {lab=VSS}
N 380 -320 450 -320 {lab=#net3}
N 120 -320 180 -320 {lab=VINB}
N 380 -750 450 -750 {lab=#net2}
N 380 -750 380 -550 {lab=#net2}
N 300 -550 380 -550 {lab=#net2}
N 380 -120 450 -120 {lab=#net3}
N 380 -320 380 -120 {lab=#net3}
N 470 -710 470 -660 {lab=VSS}
N 470 -210 470 -160 {lab=VDD}
N 300 -320 380 -320 {lab=#net3}
N 650 -750 650 -550 {lab=#net4}
N 650 -320 650 -120 {lab=#net5}
N 970 -430 970 -320 {lab=VOUT}
N 970 -550 970 -430 {lab=VOUT}
N 610 -750 650 -750 {lab=#net4}
N 610 -550 650 -550 {lab=#net4}
N 610 -320 650 -320 {lab=#net5}
N 610 -120 650 -120 {lab=#net5}
N 260 -750 330 -750 {lab=tieh}
N 470 -840 470 -790 {lab=VDD}
N 240 -120 310 -120 {lab=tiel}
N 470 -80 470 -30 {lab=VSS}
N 200 -850 200 -800 {lab=VDD}
N 200 -700 200 -650 {lab=VSS}
N 180 -220 180 -170 {lab=VDD}
N 180 -70 180 -20 {lab=VSS}
N 530 -820 530 -790 {lab=tieh}
N 470 -640 470 -590 {lab=VDD}
N 530 -80 530 -40 {lab=tiel}
N 470 -280 470 -230 {lab=VSS}
N 820 -510 820 -470 {lab=tieh}
N 820 -280 820 -240 {lab=tieh}
N 530 -190 530 -160 {lab=tieh}
N 820 -390 820 -360 {lab=tiel}
N 820 -620 820 -590 {lab=tiel}
N 530 -710 530 -670 {lab=tiel}
N 760 -640 760 -590 {lab=VDD}
N 760 -510 760 -460 {lab=VSS}
N 760 -410 760 -360 {lab=VDD}
N 760 -280 760 -230 {lab=VSS}
N 650 -320 740 -320 {lab=#net5}
N 650 -550 740 -550 {lab=#net4}
N 900 -550 970 -550 {lab=VOUT}
N 900 -320 970 -320 {lab=VOUT}
C {opin.sym} 1040 -430 0 0 {name=p2 lab=VOUT}
C {ipin.sym} 120 -550 0 0 {name=p3 lab=VINA}
C {ipin.sym} 120 -320 0 0 {name=p1 lab=VINB}
C {ipin.sym} 210 -430 0 0 {name=p4 lab=VS}
C {lab_wire.sym} 530 -230 2 0 {name=p6 sig_type=std_logic lab=VS}
C {lab_wire.sym} 530 -640 2 0 {name=p5 sig_type=std_logic lab=VS}
C {iopin.sym} 470 -640 2 0 {name=p7 lab=VDD}
C {iopin.sym} 470 -230 2 0 {name=p8 lab=VSS}
C {lab_wire.sym} 470 -460 2 0 {name=p10 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 470 -410 2 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 330 -490 2 0 {name=p12 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 330 -370 2 0 {name=p13 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 230 -610 2 0 {name=p9 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 230 -490 2 0 {name=p14 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 230 -380 2 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 230 -260 2 0 {name=p16 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 470 -840 2 0 {name=p17 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 470 -660 2 0 {name=p18 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 470 -210 2 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 470 -30 2 0 {name=p20 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 760 -460 0 0 {name=p27 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 760 -640 2 0 {name=p28 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 760 -230 0 1 {name=p29 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 760 -410 0 0 {name=p32 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 -850 2 0 {name=p33 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 200 -650 2 0 {name=p34 sig_type=std_logic lab=VSS
}
C {lab_wire.sym} 180 -220 2 0 {name=p35 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 180 -20 2 0 {name=p36 sig_type=std_logic lab=VSS
}
C {lab_wire.sym} 310 -120 0 1 {name=p37 sig_type=std_logic lab=tiel
}
C {lab_wire.sym} 330 -750 0 1 {name=p38 sig_type=std_logic lab=tieh
}
C {lab_wire.sym} 530 -40 0 1 {name=p21 sig_type=std_logic lab=tiel
}
C {lab_wire.sym} 530 -190 0 1 {name=p24 sig_type=std_logic lab=tieh
}
C {lab_wire.sym} 530 -670 0 1 {name=p22 sig_type=std_logic lab=tiel
}
C {lab_wire.sym} 530 -820 0 1 {name=p23 sig_type=std_logic lab=tieh
}
C {lab_wire.sym} 820 -240 0 1 {name=p26 sig_type=std_logic lab=tieh
}
C {lab_wire.sym} 820 -470 0 1 {name=p25 sig_type=std_logic lab=tieh
}
C {lab_wire.sym} 820 -620 0 1 {name=p30 sig_type=std_logic lab=tiel
}
C {lab_wire.sym} 820 -390 0 1 {name=p31 sig_type=std_logic lab=tiel
}
C {tieh_custom/tieh_custom.sym} 200 -750 0 0 {name=x12}
C {tiel_custom/tiel_custom.sym} 180 -120 0 0 {name=x7}
C {tg_custom/tg_custom.sym} 530 -750 0 0 {name=x14}
C {tg_custom/tg_custom.sym} 530 -550 0 0 {name=x15[1:0]}
C {tg_custom/tg_custom.sym} 530 -320 0 0 {name=x16}
C {tg_custom/tg_custom.sym} 530 -120 0 0 {name=x17[1:0]}
C {inv/inv.sym} 240 -290 0 0 {name=x10}
C {inv_PI/inv_PI.sym} 140 -410 0 0 {name=x4}
C {inv_PI/inv_PI.sym} 140 -180 0 0 {name=x9}
C {tg_custom/tg_custom.sym} 820 -550 0 0 {name=x11
}
C {tg_custom/tg_custom.sym} 820 -320 0 0 {name=x13
}
