************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: fully_differential_telescopic_pmos
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
* Cell Name:    fully_differential_telescopic_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_telescopic_pmos Vbiasn1 Vbiasn2 Vbiasp Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp:I Vinn:I Vinp:I Voutn:O Voutp:O
MM0 Voutp Vbiasn2 net12 net12 nmos w=WA l=LA nfin=nA1
MM1 Voutn Vbiasn2 net17 net17 nmos w=WA l=LA nfin=nA1
MM8 net17 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM9 net12 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM5 net14 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM7 Voutp Vinn net14 net18 pmos w=WA l=LA nfin=nA4
MM6 Voutn Vinp net14 net18 pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
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


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp Vinn Vinp Voutn Voutp fully_differential_telescopic_pmos
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR5_2 Biasn Biasp CR5_2
.END