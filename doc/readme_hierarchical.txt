source ./SOURCEME

##inv_PI_d2 — jerarquía + autoload + leaf PCells (sin gallery)

./eda netlist CDR4176-main/schematic/xschem/inv_PI_d2/inv_PI_d2.sch
klayout -n sg13g2 -zz -r scripts/hierarchical.py \
  -rd netlist=CDR4176-main/simulation/inv_PI_d2/inv_PI_d2.spice \
  -rd output=CDR4176-main/simulation/inv_PI_d2/inv_PI_d2.gds \
  -rd autoload=1 \
  -rd reuse_dir=CDR4176-main/layout/klayout \
  -rd leaf=1 \
  -rd gallery=0

##nand_custom — top “solo dispositivos” (sin reusar celdas jerárquicas), genera PCells leaf directamente (sin gallery)

./eda netlist CDR4176-main/schematic/xschem/nand_custom/nand_custom.sch
klayout -n sg13g2 -zz -r scripts/hierarchical.py \
  -rd netlist=CDR4176-main/simulation/nand_custom/nand_custom.spice \
  -rd output=CDR4176-main/simulation/nand_custom/nand_custom.gds \
  -rd leaf=1 \
  -rd gallery=0
