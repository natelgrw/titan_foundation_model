************************************************************************
* auCdl Netlist:
*
* Library Name:  biasing_circuits
* Top Cell Name: CR4_2
* View Name:     schematic
* Netlisted on:  Apr  4 17:17:18 2019
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
* Cell Name:    CR4_2
* View Name:    schematic
************************************************************************

.SUBCKT CR4_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM11 net023 net024 Vbiasn gnd! nmos w=27.0n l=LA nfin=nA1
MM8 net025 net010 net023 gnd! nmos w=27.0n l=LA nfin=nA2
MM9 net024 net024 net023 gnd! nmos w=27.0n l=LA nfin=nA3
MM7 net010 net010 net025 gnd! nmos w=WA l=LA nfin=nA4
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA5
MM0 Vbiasp net025 gnd! gnd! nmos w=WA l=LA nfin=nA6
MM10 net024 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA7
MM4 net010 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA8
MM3 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA7
MM1 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA9
.ENDS

