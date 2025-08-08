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


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR14_1 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM2 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 net010 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
RR0 Vbiasn net010 res=rK
.ENDS


xiota LG_Vbiasn2 LG_Vbiasp Vinn Vinp Voutp single_ended_telescopic_pmos
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR14_1 Biasn Biasp CR14_1
.END