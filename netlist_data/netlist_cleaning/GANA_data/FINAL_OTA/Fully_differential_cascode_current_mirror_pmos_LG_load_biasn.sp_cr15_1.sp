************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: fully_differential_cascode_current_mirror_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:02:31 2019
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
* Cell Name:    fully_differential_cascode_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_cascode_current_mirror_pmos Vbiasn1 Vbiasn2 Vbiasp Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM1 Voutp Vbiasn2 net37 gnd! nmos w=WA l=LA nfin=nA1
MM0 Voutn Vbiasn2 net29 gnd! nmos w=WA l=LA nfin=nA2
MM9 net35 Vbiasn2 net34 gnd! nmos w=WA l=LA nfin=nA1
MM8 net31 Vbiasn2 net30 gnd! nmos w=WA l=LA nfin=nA2
MM12 net37 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM11 net29 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM10 net34 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM4 net30 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM14 net36 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM13 net28 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM3 Voutp Vbiasp2 net36 vdd! pmos w=WA l=LA nfin=nA6
MM2 Voutn Vbiasp2 net28 vdd! pmos w=WA l=LA nfin=nA6
MM5 net17 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA7
MM7 net35 Vinn net17 net32 pmos w=WA l=LA nfin=nA8
MM6 net31 Vinp net17 net32 pmos w=WA l=LA nfin=nA8
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR15_1 Vbiasp
*.PININFO Vbiasp:O
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp fully_differential_cascode_current_mirror_pmos
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR15_1 Biasp CR15_1
.END