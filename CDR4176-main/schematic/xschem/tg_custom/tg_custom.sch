v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 490 -1330 530 -1330 {
lab=VSN}
N 570 -1390 570 -1360 {
lab=VIN}
N 570 -1330 620 -1330 {
lab=VBN}
N 570 -1290 570 -1270 {
lab=VOUT}
N 570 -1290 740 -1290 {
lab=VOUT}
N 570 -1300 570 -1290 {
lab=VOUT}
N 570 -1360 740 -1360 {
lab=VIN}
N 740 -1300 740 -1290 {
lab=VOUT}
N 780 -1330 820 -1330 {
lab=VSP}
N 700 -1330 740 -1330 {lab=VBP}
C {sg13g2_pr/sg13_lv_nmos.sym} 550 -1330 2 1 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {iopin.sym} 570 -1390 0 0 {name=p1 lab=VIN}
C {iopin.sym} 490 -1330 0 1 {name=p3 lab=VSN}
C {iopin.sym} 570 -1270 0 0 {name=p4 lab=VOUT}
C {sg13g2_pr/sg13_lv_pmos.sym} 760 -1330 0 1 {name=M2
l=0.13u
w=0.3u
ng=2
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 820 -1330 0 0 {name=p2 lab=VSP}
C {lab_pin.sym} 620 -1330 1 1 {name=p5 sig_type=std_logic lab=VBN}
C {lab_pin.sym} 700 -1330 1 1 {name=p6 sig_type=std_logic lab=VBP}
C {iopin.sym} 730 -1460 0 0 {name=p7 lab=VBN}
C {iopin.sym} 730 -1430 0 0 {name=p8 lab=VBP}
