************************************************************************
* auCdl Netlist:
*
* Library Name:  biasing_circuits
* Top Cell Name: CR11_1
* View Name:     schematic
* Netlisted on:  Apr  4 17:14:35 2019
************************************************************************

*.BIPOLAR
*.RESI = 2000
*.RESVAL
*.CAPVAL
*.DIOPERI
*.DIOAREA
*.EQUATION
*.SCALE METER
*.MEGA
.PARAM

*.GLOBAL gnd!
**+        vdd!

*.PIN gnd!
*+    vdd!

************************************************************************
* Library Name: biasing_circuits
* Cell Name:    CR11_1
* View Name:    schematic
************************************************************************

.SUBCKT CR11_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
MM1 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net9 net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM2 Vbiasn net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

