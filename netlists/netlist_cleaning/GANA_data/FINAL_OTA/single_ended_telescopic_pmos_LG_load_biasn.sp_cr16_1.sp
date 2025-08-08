************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_telescopic_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:39:52 2019
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
* Cell Name:    single_ended_telescopic_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_telescopic_pmos Vbiasn2 Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasn2:I Vbiasp:I Vinn:I Vinp:I Voutp:O
MM1 net14 Vbiasn2 net013 gnd! nmos w=WA l=LA nfin=nA1
MM0 Voutp Vbiasn2 net10 gnd! nmos w=WA l=LA nfin=nA1
MM9 net10 net14 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net013 net14 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM5 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM7 Voutp Vinn net12 net19 pmos w=WA l=LA nfin=nA4
MM6 net14 Vinp net12 net19 pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR16_1 Vbiasp
*.PININFO Vbiasp:O
RR0 vdd! net6 res=rK
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp net6 vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn2 LG_Vbiasp Vinn Vinp Voutp single_ended_telescopic_pmos
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR16_1 Biasp CR16_1
.END