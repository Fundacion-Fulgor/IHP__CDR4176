source ./SOURCEME

./eda netlist --lvs

SETUP="${PDK_ROOT}/${PDK}/libs.tech/netgen/ihp-sg13g2_setup.tcl"

netgen -batch lvs \
  "CDR4176-main/schematic/xschem/CDR4176/CDR4176_extracted.cir CDR4176" \
  "CDR4176-main/simulation/CDR4176/CDR4176.spice CDR4176" \
  "$SETUP" \
  CDR4176_netgen_lvs.out

tail -n 60 CDR4176_netgen_lvs.out
