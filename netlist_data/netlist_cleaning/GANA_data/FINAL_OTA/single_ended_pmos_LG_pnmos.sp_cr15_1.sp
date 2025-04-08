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


.SUBCKT LG_pnmos Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM1 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasp net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net6 net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM10 net6 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS

.SUBCKT CR15_1 Vbiasp
*.PININFO Vbiasp:O
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_pmos
xiLG_pnmos Biasp LG_Vbiasn LG_Vbiasp LG_pnmos
xibCR15_1 Biasp CR15_1
.END