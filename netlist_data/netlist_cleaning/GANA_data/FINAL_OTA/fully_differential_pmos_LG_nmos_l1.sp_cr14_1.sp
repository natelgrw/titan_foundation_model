************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: fully_differential_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:06:01 2019
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
* Cell Name:    fully_differential_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_pmos Vbiasn Vbiasp Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:O Vbiasp:I Vinn:I Vinp:I Voutn:O Voutp:O
MM7 Voutp Vinn net12 net16 pmos w=WA l=LA nfin=nA1
MM6 Voutn Vinp net12 net16 pmos w=WA l=LA nfin=nA1
MM5 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM9 Voutp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM8 Voutn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA3
.ENDS


.SUBCKT LG_nmos_l1 Biasn Vbiasn Vbiasp
*.PININFO Biasn:I Vbiasn:O Vbiasp:O
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM0 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR14_1 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 net010 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
RR0 Vbiasn net010 res=rK
.ENDS


xiota LG_Vbiasn LG_Vbiasp Vinn Vinp Voutn Voutp fully_differential_pmos
xiLG_nmos_l1 Biasn LG_Vbiasn LG_Vbiasp LG_nmos_l1
xibCR14_1 Biasn Vbiasp CR14_1
.END