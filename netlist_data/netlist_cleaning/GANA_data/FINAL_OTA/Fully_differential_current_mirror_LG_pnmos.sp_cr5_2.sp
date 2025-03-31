************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_current_mirror
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
* Cell Name:    Fully_differential_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_current_mirror Vbiasn Vbiasn1 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasn1:I Vinn:I Vinp:I Voutn:O Voutp:O
MM3 net23 Vinp net19 gnd! nmos w=WA l=LA nfin=nA
MM0 net15 Vinn net19 gnd! nmos w=WA l=LA nfin=nA
MM4 net19 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM8 Voutp Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM7 Voutn Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM6 Voutp net15 vdd! vdd! pmos w=WA l=LA nfin=nA
MM5 Voutn net23 vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net23 net23 vdd! vdd! pmos w=WA l=LA nfin=nA
MM2 net15 net15 vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_pnmos Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM1 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasp net6 gnd! gnd! nmos w=WA l=LA nfin=nA
MM8 net6 net6 gnd! gnd! nmos w=WA l=LA nfin=nA
MM2 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM10 net6 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR5_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM5 net014 net014 gnd! gnd! nmos w=WA l=LA nfin=nA
MM4 net15 net014 gnd! gnd! nmos w=WA l=LA nfin=nA
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM6 net014 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 Vinn Vinp Voutn Voutp Fully_differential_current_mirror
xiLG_pnmos Biasp LG_Vbiasn LG_Vbiasp LG_pnmos
xibCR5_2 Biasn Biasp CR5_2
.END