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


.SUBCKT LG_pnmos_4 Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM1 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasp net6 gnd! gnd! nmos w=WA l=LA nfin=nA
MM8 net6 net6 gnd! gnd! nmos w=WA l=LA nfin=nA
MM2 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM10 net6 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR2_2_wilson Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
RR0 Vbiasn gnd! res=rK
MM2 Vbiasp net12 Vbiasn gnd! nmos w=WA l=LA nfin=nA
MM0 net12 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasp LG_Vbiasp1 Vinn Vinp Voutn Voutp Fully_differential_current_mirror_pmos
xiLG_pnmos_4 Biasp LG_Vbiasn LG_Vbiasp LG_pnmos_4
xibCR2_2_wilson Biasn Biasp CR2_2_wilson
.END