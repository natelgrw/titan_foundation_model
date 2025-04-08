************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: single_ended_miller_compensated_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:09:34 2019
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
* Cell Name:    single_ended_miller_compensated_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_miller_compensated_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM13 Voutp net38 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM9 net38 net35 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net35 net35 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM12 Voutp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM11 net33 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM10 net38 Vinn net33 net39 pmos w=WA l=LA nfin=nA4
MM7 net35 Vinp net33 net39 pmos w=WA l=LA nfin=nA4
CC2 Voutp net38 1p
.ENDS


.SUBCKT LG_pmos_l1 Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM0 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM8 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM10 Vbiasn Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR6_2 Vbiasn1 Vbiasn2 Vbiasp
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp:O
MM2 Vbiasp Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn2 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM4 Vbiasn1 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM5 net15 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn2 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM6 net15 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA5
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_miller_compensated_pmos
xiLG_pmos_l1 Biasp LG_Vbiasn LG_Vbiasp LG_pmos_l1
xibCR6_2 Biasn1 Biasn2 Biasp CR6_2
.END