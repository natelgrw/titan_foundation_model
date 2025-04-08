************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:09:58 2019
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

*.GLOBAL vdd!
+        gnd!

*.PIN vdd!
*+    gnd!

************************************************************************
* Library Name: OTA_class
* Cell Name:    single_ended_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM9 Voutp net12 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM8 net12 net12 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM7 Voutp Vinn net10 net14 pmos w=WA l=LA nfin=nA2
MM6 net12 Vinp net10 net14 pmos w=WA l=LA nfin=nA2
MM5 net10 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS


.SUBCKT LG_pmos_l1 Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM0 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM8 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM10 Vbiasn Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR14_1 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 net010 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
RR0 Vbiasn net010 res=rK
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_pmos
xiLG_pmos_l1 Biasp LG_Vbiasn LG_Vbiasp LG_pmos_l1
xibCR14_1 Biasn Biasp CR14_1
.END