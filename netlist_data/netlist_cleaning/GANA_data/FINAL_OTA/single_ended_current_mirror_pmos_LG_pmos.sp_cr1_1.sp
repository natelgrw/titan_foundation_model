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


.SUBCKT LG_pmos Biasn Vbiasp
*.PININFO Biasn:I Vbiasp:O
MM10 Vbiasp Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR1_1 Vbiasn
*.PININFO Vbiasn:O
RRF vdd! Vbiasn res=rK
RR0 vdd! net02 res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM1 net02 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_current_mirror_pmos
xiLG_pmos Biasn LG_Vbiasp LG_pmos
xibCR1_1 Biasn CR1_1
.END