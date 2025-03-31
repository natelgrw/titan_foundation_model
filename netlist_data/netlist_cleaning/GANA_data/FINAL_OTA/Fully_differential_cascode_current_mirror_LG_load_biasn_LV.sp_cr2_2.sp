************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_cascode_current_mirror
* View Name:     schematic
* Netlisted on:  Sep 11 21:02:16 2019
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
* Cell Name:    Fully_differential_cascode_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_cascode_current_mirror Vbiasn Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasn1:I Vbiasn2:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM3 net22 Vinp net9 gnd! nmos w=WA l=LA nfin=nA
MM0 net31 Vinn net9 gnd! nmos w=WA l=LA nfin=nA
MM4 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM14 Voutp Vbiasn2 net34 gnd! nmos w=WA l=LA nfin=nA
MM13 Voutn Vbiasn2 net21 gnd! nmos w=WA l=LA nfin=nA
MM8 net34 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM7 net21 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM2 net32 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net23 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA
MM6 net33 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA
MM5 net20 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA
MM12 net31 Vbiasp1 net32 vdd! pmos w=WA l=LA nfin=nA
MM11 net22 Vbiasp1 net23 vdd! pmos w=WA l=LA nfin=nA
MM10 Voutp Vbiasp1 net33 vdd! pmos w=WA l=LA nfin=nA
MM9 Voutn Vbiasp1 net20 vdd! pmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR2_2_wilson Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
RR0 Vbiasn gnd! res=rK
MM2 Vbiasp net12 Vbiasn gnd! nmos w=WA l=LA nfin=nA
MM0 net12 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp Fully_differential_cascode_current_mirror
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR2_2_wilson Biasn Biasp CR2_2_wilson
.END