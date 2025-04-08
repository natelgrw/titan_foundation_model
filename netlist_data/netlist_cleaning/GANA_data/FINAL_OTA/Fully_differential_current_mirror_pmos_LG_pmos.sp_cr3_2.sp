************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: fully_differential_current_mirror_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:02:54 2019
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
* Cell Name:    fully_differential_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_current_mirror_pmos Vbiasp Vbiasp1 Vinn Vinp Voutn Voutp
*.PININFO Vbiasp:I Vbiasp1:I Vinn:I Vinp:I Voutn:O Voutp:O
MM1 Voutp net13 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM9 net13 net13 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Voutn net19 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net19 net19 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Voutp Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA3
MM2 Voutn Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA3
MM5 net17 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM7 net13 Vinn net17 net24 pmos w=WA l=LA nfin=nA5
MM6 net19 Vinp net17 net24 pmos w=WA l=LA nfin=nA5
.ENDS


.SUBCKT LG_pmos Biasn Vbiasp
*.PININFO Biasn:I Vbiasp:O
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR3_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
RR0 net15 gnd! res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasp LG_Vbiasp1 Vinn Vinp Voutn Voutp fully_differential_current_mirror_pmos
xiLG_pmos Biasn LG_Vbiasp LG_pmos
xibCR3_2 Biasn Vbiasp CR3_2
.END