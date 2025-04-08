************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: fully_differential_miller_compensated
* View Name:     schematic
* Netlisted on:  Sep 11 21:05:48 2019
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
* Cell Name:    fully_differential_miller_compensated
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_miller_compensated Vbiasn Vbiasp Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasp:I Vinn:I Vinp:I Voutn:O Voutp:O
MM7 Voutp net15 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM1 net22 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM2 net15 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM5 Voutn net22 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM8 Voutp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 net22 Vinp net21 gnd! nmos w=WA l=LA nfin=nA4
MM0 net15 Vinn net21 gnd! nmos w=WA l=LA nfin=nA4
MM4 net21 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM6 Voutn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA5
CC1 Voutp net15 1p
CC0 Voutn net22 1p
.ENDS


.SUBCKT LG_pmos Biasn Vbiasp
*.PININFO Biasn:I Vbiasp:O
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR11_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
MM1 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net9 net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM2 Vbiasn net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasn LG_Vbiasp Vinn Vinp Voutn Voutp fully_differential_miller_compensated
xiLG_pmos Biasn LG_Vbiasp LG_pmos
xibCR11_1 Biasn CR11_1
.END