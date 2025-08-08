************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: fully_differential_current_mirror
* View Name:     schematic
* Netlisted on:  Sep 11 21:01:53 2019
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
* Cell Name:    fully_differential_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_current_mirror Vbiasn Vbiasn1 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasn1:I Vinn:I Vinp:I Voutn:O Voutp:O
MM3 net23 Vinp net19 gnd! nmos w=WA l=LA nfin=nA1
MM0 net15 Vinn net19 gnd! nmos w=WA l=LA nfin=nA1
MM4 net19 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 Voutp Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM7 Voutn Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM6 Voutp net15 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM5 Voutn net23 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM1 net23 net23 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM2 net15 net15 vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_nmos Biasp Vbiasn
*.PININFO Biasp:I Vbiasn:O
MM8 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM10 Vbiasn Biasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR15_1 Vbiasp
*.PININFO Vbiasp:O
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 Vinn Vinp Voutn Voutp fully_differential_current_mirror
xiLG_nmos Biasp LG_Vbiasn LG_nmos
xibCR15_1 Biasp CR15_1
.END