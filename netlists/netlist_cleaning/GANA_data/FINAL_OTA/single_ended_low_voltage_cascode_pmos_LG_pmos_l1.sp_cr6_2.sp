************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_low_voltage_cascode_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:08:22 2019
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
* Cell Name:    single_ended_low_voltage_cascode_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_low_voltage_cascode_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM7 Voutp Vinn net11 net18 pmos w=WA l=LA nfin=nA1
MM6 net13 Vinp net11 net18 pmos w=WA l=LA nfin=nA1
MM5 net11 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM1 Voutp net17 net20 gnd! nmos w=WA l=LA nfin=nA3
MM0 net13 net17 net19 gnd! nmos w=WA l=LA nfin=nA3
MM9 net20 net13 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM8 net19 net13 gnd! gnd! nmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_pmos_l1 Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM0 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM8 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
MM10 Vbiasn Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR6_2 Vbiasn1 Vbiasn2 Vbiasp
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp:O
MM2 Vbiasp Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn2 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM4 Vbiasn1 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM5 net15 net15 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn2 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM6 net15 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA5
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_low_voltage_cascode_pmos
xiLG_pmos_l1 Biasp LG_Vbiasn LG_Vbiasp LG_pmos_l1
xibCR6_2 Biasn1 Biasn2 Biasp CR6_2
.END