************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_cascode_current_mirror_pmos
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
* Cell Name:    Fully_differential_cascode_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_cascode_current_mirror_pmos Vbiasn1 Vbiasn2 Vbiasp Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasn2:I Vbiasp:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM1 Voutp Vbiasn2 net37 gnd! nmos w=WA l=LA nfin=nA
MM0 Voutn Vbiasn2 net29 gnd! nmos w=WA l=LA nfin=nA
MM9 net35 Vbiasn2 net34 gnd! nmos w=WA l=LA nfin=nA
MM8 net31 Vbiasn2 net30 gnd! nmos w=WA l=LA nfin=nA
MM12 net37 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM11 net29 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM10 net34 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM4 net30 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM14 net36 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM13 net28 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Voutp Vbiasp2 net36 vdd! pmos w=WA l=LA nfin=nA
MM2 Voutn Vbiasp2 net28 vdd! pmos w=WA l=LA nfin=nA
MM5 net17 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM7 net35 Vinn net17 net32 pmos w=WA l=LA nfin=nA
MM6 net31 Vinp net17 net32 pmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR16_1 Vbiasp
*.PININFO Vbiasp:O
RR0 vdd! net6 res=rK
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp net6 vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp Fully_differential_cascode_current_mirror_pmos
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR16_1 Biasp CR16_1
.END