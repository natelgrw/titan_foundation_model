************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_telescopic_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:04:07 2019
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
* Cell Name:    Fully_differential_telescopic_pmos
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_telescopic_pmos Vbiasn1 Vbiasn2 Vbiasp Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp:I Vinn:I Vinp:I Voutn:O Voutp:O
MM0 Voutp Vbiasn2 net12 net12 nmos w=WA l=LA nfin=nA
MM1 Voutn Vbiasn2 net17 net17 nmos w=WA l=LA nfin=nA
MM8 net17 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM9 net12 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM5 net14 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM7 Voutp Vinn net14 net18 pmos w=WA l=LA nfin=nA
MM6 Voutn Vinp net14 net18 pmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR6_3 Vbiasn1 Vbiasn2 Vbiasp
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp:O
MM2 Vbiasp Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasn2 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM4 Vbiasn1 net15 gnd! gnd! nmos w=WA l=LA nfin=nA
MM5 net15 net15 gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 Vbiasn2 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM6 net15 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp Vinn Vinp Voutn Voutp Fully_differential_telescopic_pmos
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR6_3 Biasn1 Biasn2 Biasp CR6_3
.END