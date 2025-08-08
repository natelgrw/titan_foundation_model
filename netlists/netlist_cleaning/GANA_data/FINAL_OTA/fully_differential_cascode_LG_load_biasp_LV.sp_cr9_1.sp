************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: fully_differential_cascode
* View Name:     schematic
* Netlisted on:  Sep 11 21:04:46 2019
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
* Cell Name:    fully_differential_cascode
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_cascode Vbiasn Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM3 Voutn Vinp net16 gnd! nmos w=WA l=LA nfin=nA1
MM0 Voutp Vinn net16 gnd! nmos w=WA l=LA nfin=nA1
MM4 net16 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM6 Voutp Vbiasp2 net22 vdd! pmos w=WA l=LA nfin=nA3
MM5 Voutn Vbiasp2 net21 vdd! pmos w=WA l=LA nfin=nA3
MM1 net21 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA4
MM2 net22 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS


.SUBCKT LG_load_biasp_LV Biasn Vbiasp2
*.PININFO Biasn:I Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM3 net8 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA2
MM1 Vbiasp2 Vbiasp2 net8 vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR9_1 Vbiasn
*.PININFO Vbiasn:O
RR0 vdd! net02 res=rK
RR1 net05 gnd! res=rK
RRF vdd! Vbiasn res=rK
MM0 Vbiasn Vbiasn net05 gnd! nmos w=WA l=LA nfin=nA1
MM1 net02 Vbiasn net05 gnd! nmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp fully_differential_cascode
xiLG_load_biasp_LV Biasn LG_Vbiasp2 LG_load_biasp_LV
xibCR9_1 Biasn CR9_1
.END