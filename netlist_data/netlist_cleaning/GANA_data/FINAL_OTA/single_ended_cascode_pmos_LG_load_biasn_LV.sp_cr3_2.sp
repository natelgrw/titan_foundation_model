************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: single_ended_cascode_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:07:21 2019
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
* Cell Name:    single_ended_cascode_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_cascode_pmos Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutp
*.PININFO Vbiasn1:O Vbiasn2:O Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutp:O
MM4 net28 Vinn net12 net22 pmos w=WA l=LA nfin=nA1
MM3 net29 Vinp net12 net22 pmos w=WA l=LA nfin=nA1
MM0 net12 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM6 net16 Vbiasp2 net25 vdd! pmos w=WA l=LA nfin=nA3
MM5 Voutp Vbiasp2 net24 vdd! pmos w=WA l=LA nfin=nA3
MM2 net25 net16 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 net24 net16 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM10 net29 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA5
MM9 net28 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA5
MM8 net16 Vbiasn2 net29 gnd! nmos w=WA l=LA nfin=nA6
MM7 Voutp Vbiasn2 net28 gnd! nmos w=WA l=LA nfin=nA6
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR3_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
RR0 net15 gnd! res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutp single_ended_cascode_pmos
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR3_2 Biasn Biasp CR3_2
.END