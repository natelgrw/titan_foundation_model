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


.SUBCKT LG_npmos Biasn Vbiasn Vbiasp
*.PININFO Biasn:I Vbiasn:O Vbiasp:O
MM4 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM10 neta Biasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn neta vdd! vdd! pmos w=WA l=LA nfin=nA5
MM0 neta neta vdd! vdd! pmos w=WA l=LA nfin=nA5
.ENDS

.SUBCKT CR11_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
MM1 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net9 net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM2 Vbiasn net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 Vinn Vinp Voutn Voutp fully_differential_current_mirror
xiLG_npmos Biasn LG_Vbiasn LG_Vbiasp LG_npmos
xibCR11_1 Biasn CR11_1
.END