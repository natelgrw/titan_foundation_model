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


.SUBCKT LG_load_biasp Biasn Vbiasp1 Vbiasp2
*.PININFO Biasn:I Vbiasp1:O Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM1 Vbiasp2 Vbiasp2 Vbiasp1 vdd! pmos w=WA l=LA nfin=nA2
MM3 Vbiasp1 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR1_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
RR0 vdd! net02 res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM1 net02 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasp LG_Vbiasp1 Vinn Vinp Voutn Voutp fully_differential_current_mirror_pmos
xiLG_load_biasp Biasn LG_Vbiasp1 LG_Vbiasp2 LG_load_biasp
xibCR1_1 Biasn CR1_1
.END