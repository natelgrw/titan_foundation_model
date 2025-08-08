************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_current_mirror_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:07:49 2019
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
* Cell Name:    single_ended_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_current_mirror_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM3 Voutp net17 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM2 net17 net17 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM7 net9 Vinn net13 net22 pmos w=WA l=LA nfin=nA2
MM6 net15 Vinp net13 net22 pmos w=WA l=LA nfin=nA2
MM5 net13 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 Voutp net9 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM0 net17 net15 gnd! gnd! nmos w=WA l=LA nfin=nA5
MM9 net9 net9 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM8 net15 net15 gnd! gnd! nmos w=WA l=LA nfin=nA5
.ENDS


.SUBCKT LG_nmos_l1 Biasn Vbiasn Vbiasp
*.PININFO Biasn:I Vbiasn:O Vbiasp:O
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM0 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR11_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
MM1 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net9 net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM2 Vbiasn net9 vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_current_mirror_pmos
xiLG_nmos_l1 Biasn LG_Vbiasn LG_Vbiasp LG_nmos_l1
xibCR11_1 Biasn CR11_1
.END