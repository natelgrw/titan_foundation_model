************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_two_stage
* View Name:     schematic
* Netlisted on:  Sep 11 21:10:37 2019
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
* Cell Name:    single_ended_two_stage
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_two_stage Vbiasn Vinn Vinp Voutp
*.PININFO Vbiasn:I Vinn:I Vinp:I Voutp:O
MM1 net16 net20 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM2 net12 net20 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM9 net9 net12 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM5 Voutp net16 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM7 net9 net9 gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 net16 Vinp net15 gnd! nmos w=WA l=LA nfin=nA4
MM0 net12 Vinn net15 gnd! nmos w=WA l=LA nfin=nA4
MM4 net15 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA5
MM6 Voutp net9 gnd! gnd! nmos w=WA l=LA nfin=nA3
.ENDS


.SUBCKT LG_nmos Biasp Vbiasn
*.PININFO Biasp:I Vbiasn:O
MM8 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM10 Vbiasn Biasp vdd! vdd! pmos w=WA l=LA nfin=nA2
.ENDS

.SUBCKT CR16_1 Vbiasp
*.PININFO Vbiasp:O
RR0 vdd! net6 res=rK
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp net6 vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn Vinn Vinp Voutp single_ended_two_stage
xiLG_nmos Biasp LG_Vbiasn LG_nmos
xibCR16_1 Biasp CR16_1
.END