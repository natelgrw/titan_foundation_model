************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_folded_cascode
* View Name:     schematic
* Netlisted on:  Sep 11 21:03:06 2019
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
* Cell Name:    Fully_differential_folded_cascode
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_folded_cascode Vbiasn Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutn
*.PININFO Vbiasn:I Vbiasn1:I Vbiasn2:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O
MM6 net26 Vbiasp2 net23 vdd! pmos w=WA l=LA nfin=nA
MM5 Voutn Vbiasp2 net24 vdd! pmos w=WA l=LA nfin=nA
MM2 net23 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net24 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM8 net26 Vbiasn2 net27 gnd! nmos w=WA l=LA nfin=nA
MM7 Voutn Vbiasn2 net25 gnd! nmos w=WA l=LA nfin=nA
MM3 net24 Vinp net13 gnd! nmos w=WA l=LA nfin=nA
MM0 net23 Vinn net13 gnd! nmos w=WA l=LA nfin=nA
MM10 net27 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM9 net25 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM4 net13 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR16_1 Vbiasp
*.PININFO Vbiasp:O
RR0 vdd! net6 res=rK
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp net6 vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Fully_differential_folded_cascode
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR16_1 Biasp CR16_1
.END