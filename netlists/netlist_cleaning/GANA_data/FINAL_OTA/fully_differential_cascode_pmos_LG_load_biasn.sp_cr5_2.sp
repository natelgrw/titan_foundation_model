************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: fully_differential_cascode_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:05:09 2019
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
* Cell Name:    fully_differential_cascode_pmos
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_cascode_pmos Vbiasn1 Vbiasn2 Vbiasp Vinn Vinp Voutp1 Voutp2
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp:I Vinn:I Vinp:I Voutp1:O Voutp2:O
MM1 Voutp2 Vbiasn2 net17 gnd! nmos w=WA l=LA nfin=nA1
MM0 Voutp1 Vbiasn2 net18 gnd! nmos w=WA l=LA nfin=nA1
MM9 net18 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net17 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM5 net13 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM7 Voutp1 Vinn net13 net20 pmos w=WA l=LA nfin=nA4
MM6 Voutp2 Vinp net13 net20 pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR5_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM5 net014 net014 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM4 net15 net014 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM6 net014 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp Vinn Vinp Voutp1 Voutp2 fully_differential_cascode_pmos
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR5_2 Biasn Biasp CR5_2
.END