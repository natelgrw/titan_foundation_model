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


.SUBCKT LG_pmos Biasn Vbiasp
*.PININFO Biasn:I Vbiasp:O
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR13_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_miller_compensated_pmos
xiLG_pmos Biasn LG_Vbiasp LG_pmos
xibCR13_2 Biasn Vbiasp CR13_2
.END