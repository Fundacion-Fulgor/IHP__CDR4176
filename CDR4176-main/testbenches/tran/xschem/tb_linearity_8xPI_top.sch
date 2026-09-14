v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
F {}
E {}
N -1110 0 -1110 20 {
lab=GND}
N -1110 -120 -1110 -60 {
lab=vinI}
N -1130 -120 -1110 -120 {
lab=vinI}
N -1110 190 -1110 210 {
lab=GND}
N -1110 70 -1110 130 {
lab=vinQ}
N -1130 70 -1110 70 {
lab=vinQ}
N -790 0 -790 20 {
lab=GND}
N -790 -120 -790 -60 {
lab=vinIB}
N -810 -120 -790 -120 {
lab=vinIB}
N -790 70 -790 130 {
lab=vinQB}
N -810 70 -790 70 {
lab=vinQB}
N -930 240 -930 280 {lab=VDD}
N -1100 330 -1080 330 {
lab=vinI}
N -1100 350 -1080 350 {
lab=vinQ}
N -1100 370 -1080 370 {
lab=vinIB}
N -1100 390 -1080 390 {
lab=vinQB}
N -780 330 -750 330 {
lab=VoutI1}
N -780 350 -750 350 {
lab=VoutQ1}
N -780 370 -750 370 {
lab=VoutIB1}
N -780 390 -750 390 {
lab=VoutQB1}
N -790 190 -790 210 {
lab=GND}
N -1400 130 -1400 170 {lab=VDD}
N -1110 -330 -1110 -290 {lab=v0}
N -790 -330 -790 -290 {lab=v1}
N -1300 230 -1300 290 {
lab=GND}
N -1300 130 -1300 170 {lab=VSS}
N -1110 -230 -1110 -190 {lab=VSS}
N -790 -230 -790 -190 {lab=VSS}
N -1400 230 -1400 270 {lab=VSS}
N -930 440 -930 480 {lab=VSS}
N -100 -160 -70 -160 {
lab=VoutI1}
N -100 -80 -70 -80 {
lab=VoutQ1}
N -100 -120 -70 -120 {
lab=VoutIB1}
N -100 -40 -70 -40 {
lab=VoutQB1}
N 150 30 150 70 {lab=VSS}
N 150 -250 150 -210 {lab=VDD}
N 370 -90 380 -90 {
lab=Vout}
N 30 30 30 70 {lab="v1, v0"}
N 20 -250 20 -210 {lab="vXOR, v6_st, v5_st, v4_st, v3_st, v2_st, v1_st, v0_st"}
N 370 -90 370 -60 {lab=Vout}
N 350 -90 370 -90 {
lab=Vout}
N 370 0 370 40 {lab=VSS}
N -160 270 -130 270 {
lab=VoutI2}
N -160 350 -130 350 {
lab=VoutQ2}
N -160 310 -130 310 {
lab=VoutIB2}
N -160 390 -130 390 {
lab=VoutQB2}
N 90 460 90 500 {lab=VSS}
N 90 180 90 220 {lab=VDD}
N 310 340 320 340 {
lab=Vout8I}
N -30 460 -30 500 {lab="VSS, VSS"}
N -40 180 -40 220 {lab="VSS, VSS, VSS, VSS, VSS, VSS, VSS, VSS"}
N 310 340 310 370 {lab=Vout8I}
N 290 340 310 340 {
lab=Vout8I}
N 310 430 310 470 {lab=VSS}
N 690 -370 690 -330 {lab=v0_st}
N 1010 -370 1010 -330 {lab=v1_st}
N 690 -270 690 -230 {lab=VSS}
N 1010 -270 1010 -230 {lab=VSS}
N 690 -110 690 -70 {lab=v2_st}
N 1010 -110 1010 -70 {lab=v3_st}
N 690 -10 690 30 {lab=VSS}
N 1010 -10 1010 30 {lab=VSS}
N 690 150 690 190 {lab=v4_st}
N 1010 150 1010 190 {lab=v5_st}
N 690 250 690 290 {lab=VSS}
N 1010 250 1010 290 {lab=VSS}
N 690 400 690 440 {lab=v6_st}
N 690 500 690 540 {lab=VSS}
N -930 520 -930 560 {lab=VDD}
N -1100 610 -1080 610 {
lab=vinI}
N -1100 630 -1080 630 {
lab=vinQ}
N -1100 650 -1080 650 {
lab=vinIB}
N -1100 670 -1080 670 {
lab=vinQB}
N -780 610 -750 610 {
lab=VoutI2}
N -780 630 -750 630 {
lab=VoutQ2}
N -780 650 -750 650 {
lab=VoutIB2}
N -780 670 -750 670 {
lab=VoutQB2}
N -930 720 -930 760 {lab=VSS}
N 690 610 690 650 {lab=vXOR}
N 690 710 690 750 {lab=VSS}
C {devices/gnd.sym} -1110 20 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -1110 -30 0 0 {name=Vin3 value="dc 0 ac 0 pulse(0, 1.2, 0, 25p, 25p, 225p, 500p) "}
C {devices/lab_pin.sym} -1130 -120 0 0 {name=p1 sig_type=std_logic lab=vinI}
C {devices/lab_pin.sym} -1130 70 0 0 {name=p2 sig_type=std_logic lab=vinQ}
C {devices/vsource.sym} -1110 160 0 0 {name=Vin4 value="dc 0 ac 0 pulse(0, 1.2, 125p, 25p, 25p, 225p, 500p ) "}
C {devices/gnd.sym} -790 20 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} -790 -30 0 0 {name=Vin5 value="dc 0 ac 0 pulse(0, 1.2, 250p, 25p, 25p, 225p, 500p ) "}
C {devices/lab_pin.sym} -810 -120 0 0 {name=p3 sig_type=std_logic lab=vinIB}
C {devices/vsource.sym} -790 160 0 0 {name=Vin6 value="dc 0 ac 0 pulse(0, 1.2, 375p, 25p, 25p, 225p, 500p ) "}
C {devices/lab_pin.sym} -810 70 0 0 {name=p6 sig_type=std_logic lab=vinQB}
C {4to4/4to4.sym} -930 360 0 0 {name=x4}
C {devices/lab_pin.sym} -930 240 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -1100 330 0 0 {name=p14 sig_type=std_logic lab=vinI}
C {devices/lab_pin.sym} -1100 350 0 0 {name=p8 sig_type=std_logic lab=vinQ}
C {devices/lab_pin.sym} -1100 370 0 0 {name=p17 sig_type=std_logic lab=vinIB}
C {devices/lab_pin.sym} -1100 390 0 0 {name=p18 sig_type=std_logic lab=vinQB}
C {devices/lab_pin.sym} -750 330 2 0 {name=p19 sig_type=std_logic lab=VoutI1}
C {devices/lab_pin.sym} -750 350 2 0 {name=p20 sig_type=std_logic lab=VoutQ1}
C {devices/lab_pin.sym} -750 370 2 0 {name=p21 sig_type=std_logic lab=VoutIB1}
C {devices/lab_pin.sym} -750 390 2 0 {name=p22 sig_type=std_logic lab=VoutQB1}
C {devices/gnd.sym} -1110 210 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -790 210 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} -1400 200 0 0 {name=Vdd4 value=1.2}
C {devices/lab_pin.sym} -1400 130 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/vsource.sym} -790 -260 0 0 {name=Vdd1 value="dc 0 ac 0 pulse(0, 1.2, 40n, 25p, 25p, 40n, 80n)"}
C {devices/vsource.sym} -1110 -260 0 0 {name=Vdd2 value="dc 0 ac 0 pulse(0, 1.2, 20n, 25p, 25p, 40n, 80n) "}
C {devices/lab_pin.sym} -1110 -330 0 0 {name=p11 sig_type=std_logic lab=v0}
C {devices/lab_pin.sym} -790 -330 0 0 {name=p10 sig_type=std_logic lab=v1}
C {devices/vsource.sym} -1300 200 0 0 {name=Vdd3 value=0}
C {devices/gnd.sym} -1300 290 0 0 {name=l1 lab=GND}
C {devices/lab_pin.sym} -1300 130 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1110 -190 2 0 {name=p7 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -790 -190 2 0 {name=p9 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1400 270 2 0 {name=p12 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -930 480 2 0 {name=p13 sig_type=std_logic lab=VSS}
C {8xPI/8xPI.sym} -90 50 0 0 {name=x1}
C {devices/lab_pin.sym} -100 -160 0 0 {name=p15 sig_type=std_logic lab=VoutI1}
C {devices/lab_pin.sym} -100 -80 0 0 {name=p16 sig_type=std_logic lab=VoutQ1}
C {devices/lab_pin.sym} -100 -120 0 0 {name=p23 sig_type=std_logic lab=VoutIB1}
C {devices/lab_pin.sym} -100 -40 0 0 {name=p24 sig_type=std_logic lab=VoutQB1}
C {devices/lab_pin.sym} 150 70 2 0 {name=p25 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 150 -250 0 0 {name=p27 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 30 70 2 0 {name=p29 sig_type=std_logic lab="v1, v0"}
C {devices/lab_pin.sym} 20 -250 0 0 {name=p30 sig_type=std_logic lab="vXOR, v6_st, v5_st, v4_st, v3_st, v2_st, v1_st, v0_st"}
C {devices/lab_pin.sym} 380 -90 2 0 {name=p37 sig_type=std_logic lab=Vout}
C {capa.sym} 370 -30 0 0 {name=C1
m=1
value=25f
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 370 40 2 0 {name=p67 sig_type=std_logic lab=VSS}
C {8xPI/8xPI.sym} -150 480 0 0 {name=x2}
C {devices/lab_pin.sym} -160 270 0 0 {name=p28 sig_type=std_logic lab=VoutI2}
C {devices/lab_pin.sym} -160 350 0 0 {name=p31 sig_type=std_logic lab=VoutQ2}
C {devices/lab_pin.sym} -160 310 0 0 {name=p32 sig_type=std_logic lab=VoutIB2}
C {devices/lab_pin.sym} -160 390 0 0 {name=p33 sig_type=std_logic lab=VoutQB2}
C {devices/lab_pin.sym} 90 500 2 0 {name=p34 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 90 180 0 0 {name=p35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -30 500 2 0 {name=p36 sig_type=std_logic lab="VSS, VSS"}
C {devices/lab_pin.sym} -40 180 0 0 {name=p38 sig_type=std_logic lab="VSS, VSS, VSS, VSS, VSS, VSS, VSS, VSS"}
C {devices/lab_pin.sym} 320 340 2 0 {name=p39 sig_type=std_logic lab=Vout8I}
C {capa.sym} 310 400 0 0 {name=C2
m=1
value=25f
footprint=1206
device="ceramic capacitor"}
C {devices/lab_pin.sym} 310 470 2 0 {name=p40 sig_type=std_logic lab=VSS}
C {netlist_not_shown.sym} -1410 -250 0 0 {name=s1 only_toplevel=false 

value="

* Circuit Parameters
.param vdd = 1.2
.param vss = 0.0
.param a=0
.param b=0
.param c=0
.param d=1
.param Tclk = 500P
.options TEMP = 27.0

* Include Models
*.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
*.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
*.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ
*.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ
.lib cornerMOSlv.lib mos_tt


* OP Parameters & Singals to save
.save V(Vout) V(Vout8I) V(vinI) V(VoutI1) V(VoutI2) V(VoutQ1) V(VoutIB1) V(VoutQB1)

*Simulations
.control
*set output_path = tb_linearity_8xpi/
	tran 5PS 80NS
	*setplot tran1
	*plot v0 v1+1.5 v0_st+3 v6_st+4.5 Vout+6 Vout8I+7.5 ylabel vout xlabel vin
	set filetype = ascii
        write tran_linearity_termoless.raw V(Vout) V(Vout8I) V(vinI) V(VoutI1) V(VoutI2) V(VoutQ1) V(VoutIB1) V(VoutQB1)
	*write \{$output_path\}tran_linearity_termoless.raw V(Vout) V(Vout8I) V(vinI) V(VoutI1) V(VoutI2) V(VoutQ1) V(VoutIB1) V(VoutQB1)
.endc
.end"}
C {devices/vsource.sym} 1010 -300 0 0 {name=Vdd5 value="dc 0 ac 0 pulse(0, 1.2, 15n, 25p, 25p, 5n, 20n)"}
C {devices/vsource.sym} 690 -300 0 0 {name=Vdd6 value="dc 0 ac 0 pulse(0, 1.2, 17.5n, 25p, 25p, 2.5n, 20n) "}
C {devices/lab_pin.sym} 690 -370 0 0 {name=p43 sig_type=std_logic lab=v0_st}
C {devices/lab_pin.sym} 1010 -370 0 0 {name=p44 sig_type=std_logic lab=v1_st}
C {devices/lab_pin.sym} 690 -230 2 0 {name=p45 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1010 -230 2 0 {name=p46 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 1010 -40 0 0 {name=Vdd7 value="dc 0 ac 0 pulse(0, 1.2, 10n, 25p, 25p, 10n, 20n)"}
C {devices/vsource.sym} 690 -40 0 0 {name=Vdd8 value="dc 0 ac 0 pulse(0, 1.2, 12.5n, 25p, 25p, 7.5n, 20n) "}
C {devices/lab_pin.sym} 690 -110 0 0 {name=p41 sig_type=std_logic lab=v2_st}
C {devices/lab_pin.sym} 1010 -110 0 0 {name=p42 sig_type=std_logic lab=v3_st}
C {devices/lab_pin.sym} 690 30 2 0 {name=p47 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1010 30 2 0 {name=p48 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 1010 220 0 0 {name=Vdd9 value="dc 0 ac 0 pulse(0, 1.2, 5n, 25p, 25p, 15n, 20n)"}
C {devices/vsource.sym} 690 220 0 0 {name=Vdd10 value="dc 0 ac 0 pulse(0, 1.2, 7.5n, 25p, 25p, 12.5n, 20n) "}
C {devices/lab_pin.sym} 690 150 0 0 {name=p49 sig_type=std_logic lab=v4_st}
C {devices/lab_pin.sym} 1010 150 0 0 {name=p50 sig_type=std_logic lab=v5_st}
C {devices/lab_pin.sym} 690 290 2 0 {name=p51 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1010 290 2 0 {name=p52 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 690 470 0 0 {name=Vdd11 value="dc 0 ac 0 pulse(0, 1.2, 2.5n, 25p, 25p, 17.5n, 20n)"}
C {devices/lab_pin.sym} 690 400 0 0 {name=p53 sig_type=std_logic lab=v6_st}
C {devices/lab_pin.sym} 690 540 2 0 {name=p54 sig_type=std_logic lab=VSS}
C {4to4/4to4.sym} -930 640 0 0 {name=x3}
C {devices/lab_pin.sym} -930 520 0 0 {name=p55 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -1100 610 0 0 {name=p56 sig_type=std_logic lab=vinI}
C {devices/lab_pin.sym} -1100 630 0 0 {name=p57 sig_type=std_logic lab=vinQ}
C {devices/lab_pin.sym} -1100 650 0 0 {name=p58 sig_type=std_logic lab=vinIB}
C {devices/lab_pin.sym} -1100 670 0 0 {name=p59 sig_type=std_logic lab=vinQB}
C {devices/lab_pin.sym} -750 610 2 0 {name=p60 sig_type=std_logic lab=VoutI2}
C {devices/lab_pin.sym} -750 630 2 0 {name=p61 sig_type=std_logic lab=VoutQ2}
C {devices/lab_pin.sym} -750 650 2 0 {name=p62 sig_type=std_logic lab=VoutIB2}
C {devices/lab_pin.sym} -750 670 2 0 {name=p63 sig_type=std_logic lab=VoutQB2}
C {devices/lab_pin.sym} -930 760 2 0 {name=p64 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 690 680 0 0 {name=Vdd12 value="dc 0 ac 0 pulse(0, 1.2, 20n, 25p, 25p, 20n, 40n) "}
C {devices/lab_pin.sym} 690 610 0 0 {name=p65 sig_type=std_logic lab=vXOR}
C {devices/lab_pin.sym} 690 750 2 0 {name=p66 sig_type=std_logic lab=VSS}
