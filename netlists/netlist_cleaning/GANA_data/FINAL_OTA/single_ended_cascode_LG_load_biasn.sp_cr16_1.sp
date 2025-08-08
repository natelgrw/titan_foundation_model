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


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR16_1 Vbiasp
*.PININFO Vbiasp:O
RR0 vdd! net6 res=rK
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp net6 vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn single_ended_cascode
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR16_1 Biasp CR16_1
.END