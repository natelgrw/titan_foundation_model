************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_current_mirror_pmos
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
* Cell Name:    Fully_differential_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_current_mirror_pmos Vbiasp Vbiasp1 Vinn Vinp Voutn Voutp
*.PININFO Vbiasp:I Vbiasp1:I Vinn:I Vinp:I Voutn:O Voutp:O
MM1 Voutp net13 gnd! gnd! nmos w=WA l=LA nfin=nA
MM9 net13 net13 gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Voutn net19 gnd! gnd! nmos w=WA l=LA nfin=nA
MM8 net19 net19 gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Voutp Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM2 Voutn Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM5 net17 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM7 net13 Vinn net17 net24 pmos w=WA l=LA nfin=nA
MM6 net19 Vinp net17 net24 pmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasp Biasn Vbiasp1 Vbiasp2
*.PININFO Biasn:I Vbiasp1:O Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM1 Vbiasp2 Vbiasp2 Vbiasp1 vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasp1 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR7_1 Vbiasn
*.PININFO Vbiasn:O
RR1 Vbiasn net7 res=rK
RR0 vdd! net7 res=rK
RRF vdd! Vbiasn res=rK
MM1 net7 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasp LG_Vbiasp1 Vinn Vinp Voutn Voutp Fully_differential_current_mirror_pmos
xiLG_load_biasp Biasn LG_Vbiasp1 LG_Vbiasp2 LG_load_biasp
xibCR7_1 Biasn CR7_1
.END