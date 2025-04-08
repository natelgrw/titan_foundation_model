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


.SUBCKT LG_load_biasp Biasn Vbiasp1 Vbiasp2
*.PININFO Biasn:I Vbiasp1:O Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM1 Vbiasp2 Vbiasp2 Vbiasp1 vdd! pmos w=WA l=LA nfin=nA2
MM3 Vbiasp1 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR2_2_wilson Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
RR0 Vbiasn gnd! res=rK
MM2 Vbiasp net12 Vbiasn gnd! nmos w=WA l=LA nfin=nA1
MM0 net12 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM1 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS


xiota LG_Vbiasn LG_Vbiasp2 Vinn Vinp Voutp single_ended_telescopic
xiLG_load_biasp Biasn LG_Vbiasp1 LG_Vbiasp2 LG_load_biasp
xibCR2_2_wilson Biasn Vbiasp CR2_2_wilson
.END