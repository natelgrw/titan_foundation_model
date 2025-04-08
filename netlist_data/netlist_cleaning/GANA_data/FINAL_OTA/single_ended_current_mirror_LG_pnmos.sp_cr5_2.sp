************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: single_ended_current_mirror
* View Name:     schematic
* Netlisted on:  Sep 11 21:07:33 2019
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
*+        vdd!

*.PIN gnd!
*+    vdd!

************************************************************************
* Library Name: OTA_class
* Cell Name:    single_ended_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_current_mirror Vbiasn Vinn Vinp Voutn
*.PININFO Vbiasn:I Vinn:I Vinp:I Voutn:O
MM8 net9 net9 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM7 Voutn net9 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net20 Vinp net16 gnd! nmos w=WA l=LA nfin=nA2
MM0 net11 Vinn net16 gnd! nmos w=WA l=LA nfin=nA2
MM4 net16 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM6 net9 net11 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM5 Voutn net20 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM1 net20 net20 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM2 net11 net11 vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_pnmos Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM1 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasp net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net6 net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM10 net6 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS

.SUBCKT CR5_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM5 net014 net014 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM4 net15 net014 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM6 net014 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


xiota LG_Vbiasn Vinn Vinp Voutn single_ended_current_mirror
xiLG_pnmos Biasp LG_Vbiasn LG_Vbiasp LG_pnmos
xibCR5_2 Biasn Biasp CR5_2
.END