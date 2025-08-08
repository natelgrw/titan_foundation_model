************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: fully_differential_folded_cascode_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:03:18 2019
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
* Cell Name:    fully_differential_folded_cascode_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_folded_cascode_pmos Vbiasn1 Vbiasn2 Vbiasp Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM8 Voutn Vbiasn2 net23 gnd! nmos w=WA l=LA nfin=nA1
MM7 Voutp Vbiasn2 net22 gnd! nmos w=WA l=LA nfin=nA1
MM10 net23 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM9 net22 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM0 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM2 net26 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 net24 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM4 net22 Vinn net12 net27 pmos w=WA l=LA nfin=nA5
MM3 net23 Vinp net12 net27 pmos w=WA l=LA nfin=nA5
MM6 Voutn Vbiasp2 net26 vdd! pmos w=WA l=LA nfin=nA6
MM5 Voutp Vbiasp2 net24 vdd! pmos w=WA l=LA nfin=nA6
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR3_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
RR0 net15 gnd! res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp fully_differential_folded_cascode_pmos
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR3_2 Biasn Biasp CR3_2
.END