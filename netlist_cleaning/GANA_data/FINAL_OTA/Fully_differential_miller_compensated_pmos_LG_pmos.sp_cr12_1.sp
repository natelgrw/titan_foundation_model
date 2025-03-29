************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_miller_compensated_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:03:30 2019
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
* Cell Name:    Fully_differential_miller_compensated_pmos
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_miller_compensated_pmos Vbiasn1 Vbiasp Vinn Vinp Voutn Voutp
*.PININFO Vbiasn1:I Vbiasp:I Vinn:I Vinp:I Voutn:O Voutp:O
MM1 Voutn net21 gnd! gnd! nmos w=WA l=LA nfin=nA
MM13 Voutp net25 gnd! gnd! nmos w=WA l=LA nfin=nA
MM9 net25 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM8 net21 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Voutn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM12 Voutp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM11 net17 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM10 net25 Vinn net17 net28 pmos w=WA l=LA nfin=nA
MM7 net21 Vinp net17 net28 pmos w=WA l=LA nfin=nA
CC0 Voutn net21 1p
CC2 Voutp net25 1p
.ENDS


.SUBCKT LG_pmos Biasn Vbiasp
*.PININFO Biasn:I Vbiasp:O
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR12_1 Vbiasn
*.PININFO Vbiasn:O
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM1 net10 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM2 Vbiasn net10 vdd! vdd! pmos w=WA l=LA nfin=nA
RRF vdd! Vbiasn res=rK
RR0 vdd! net10 res=rK
.ENDS


xiota LG_Vbiasn1 LG_Vbiasp Vinn Vinp Voutn Voutp Fully_differential_miller_compensated_pmos
xiLG_pmos Biasn LG_Vbiasp LG_pmos
xibCR12_1 Biasn CR12_1
.END