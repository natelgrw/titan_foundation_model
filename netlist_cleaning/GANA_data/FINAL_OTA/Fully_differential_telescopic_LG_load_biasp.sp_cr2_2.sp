************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_telescopic
* View Name:     schematic
* Netlisted on:  Sep 11 21:03:54 2019
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
* Cell Name:    Fully_differential_telescopic
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_telescopic Vbiasn Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM5 Voutp Vbiasp2 net18 net18 pmos w=WA l=LA nfin=nA
MM6 Voutn Vbiasp2 net13 net13 pmos w=WA l=LA nfin=nA
MM1 net18 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM2 net13 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Voutp Vinp net16 gnd! nmos w=WA l=LA nfin=nA
MM0 Voutn Vinn net16 gnd! nmos w=WA l=LA nfin=nA
MM4 net16 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasp Biasn Vbiasp1 Vbiasp2
*.PININFO Biasn:I Vbiasp1:O Vbiasp2:O
MM0 Vbiasp2 Biasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM1 Vbiasp2 Vbiasp2 Vbiasp1 vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasp1 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR2_2_wilson Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
RR0 Vbiasn gnd! res=rK
MM2 Vbiasp net12 Vbiasn gnd! nmos w=WA l=LA nfin=nA
MM0 net12 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net12 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp Fully_differential_telescopic
xiLG_load_biasp Biasn LG_Vbiasp1 LG_Vbiasp2 LG_load_biasp
xibCR2_2_wilson Biasn Vbiasp CR2_2_wilson
.END