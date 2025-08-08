************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_cascode_current_mirror
* View Name:     schematic
* Netlisted on:  Sep 11 21:41:11 2019
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
* Cell Name:    single_ended_cascode_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_cascode_current_mirror Vbiasn Vbiasn2 Vbiasp2 Vinn Vinp Voutn
*.PININFO Vbiasn:I Vbiasn2:I Vbiasp2:I Vinn:I Vinp:I Voutn:O
MM12 net12 Vbiasp2 net37 vdd! pmos w=WA l=LA nfin=nA1
MM11 net23 Vbiasp2 net36 vdd! pmos w=WA l=LA nfin=nA2
MM10 net10 Vbiasp2 net35 vdd! pmos w=WA l=LA nfin=nA1
MM9 Voutn Vbiasp2 net34 vdd! pmos w=WA l=LA nfin=nA2
MM2 net37 net12 vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 net36 net23 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM6 net35 net12 vdd! vdd! pmos w=WA l=LA nfin=nA3
MM5 net34 net23 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM14 net10 Vbiasn2 net33 gnd! nmos w=WA l=LA nfin=nA5
MM13 Voutn Vbiasn2 net31 gnd! nmos w=WA l=LA nfin=nA5
MM3 net23 Vinp net17 gnd! nmos w=WA l=LA nfin=nA6
MM0 net12 Vinn net17 gnd! nmos w=WA l=LA nfin=nA6
MM4 net17 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA7
MM8 net33 net10 gnd! gnd! nmos w=WA l=LA nfin=nA8
MM7 net31 net10 gnd! gnd! nmos w=WA l=LA nfin=nA8
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR6_2 Vbiasn1 Vbiasn2 Vbiasp
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp:O
MM2 Vbiasp Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn2 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM4 Vbiasn1 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM5 net15 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn2 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM6 net15 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA5
.ENDS


xiota LG_Vbiasn LG_Vbiasn2 LG_Vbiasp2 Vinn Vinp Voutn single_ended_cascode_current_mirror
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR6_2 Biasn1 Biasn2 Biasp CR6_2
.END