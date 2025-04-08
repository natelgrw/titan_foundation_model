************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_cascode
* View Name:     schematic
* Netlisted on:  Sep 11 21:06:28 2019
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
* Cell Name:    single_ended_cascode
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_cascode Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutn
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O
MM10 net27 net12 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM9 net21 net12 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM8 net12 Vbiasn2 net27 gnd! nmos w=WA l=LA nfin=nA2
MM7 Voutn Vbiasn2 net21 gnd! nmos w=WA l=LA nfin=nA2
MM3 net32 Vinp net10 gnd! nmos w=WA l=LA nfin=nA3
MM0 net26 Vinn net10 gnd! nmos w=WA l=LA nfin=nA3
MM4 net10 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM6 net12 Vbiasp2 net26 vdd! pmos w=WA l=LA nfin=nA5
MM5 Voutn Vbiasp2 net32 vdd! pmos w=WA l=LA nfin=nA5
MM1 net32 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA6
MM2 net26 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA6
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR14_1 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 net010 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
RR0 Vbiasn net010 res=rK
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn single_ended_cascode
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR14_1 Biasn Biasp CR14_1
.END