************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_telescopic
* View Name:     schematic
* Netlisted on:  Sep 11 21:39:36 2019
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
* Cell Name:    single_ended_telescopic
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_telescopic Vbiasn Vbiasp2 Vinn Vinp Voutp
*.PININFO Vbiasn:I Vbiasp2:I Vinn:I Vinp:I Voutp:O
MM3 Voutp Vinp net11 gnd! nmos w=WA l=LA nfin=nA1
MM0 net13 Vinn net11 gnd! nmos w=WA l=LA nfin=nA1
MM4 net11 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM6 net13 Vbiasp2 net016 vdd! pmos w=WA l=LA nfin=nA3
MM5 Voutp Vbiasp2 net014 vdd! pmos w=WA l=LA nfin=nA3
MM1 net014 net13 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM2 net016 net13 vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_load_biasp_LV Biasn Vbiasp2
*.PININFO Biasn:I Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net8 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM1 Vbiasp2 Vbiasp2 net8 vdd! pmos w=WA l=LA nfin=nA3
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


xiota LG_Vbiasn LG_Vbiasp2 Vinn Vinp Voutp single_ended_telescopic
xiLG_load_biasp_LV Biasn LG_Vbiasp2 LG_load_biasp_LV
xibCR5_2 Biasn Vbiasp CR5_2
.END