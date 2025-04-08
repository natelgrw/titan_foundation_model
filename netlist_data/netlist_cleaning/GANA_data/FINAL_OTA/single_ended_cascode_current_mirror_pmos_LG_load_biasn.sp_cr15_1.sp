************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: single_ended_cascode_current_mirror_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:41:22 2019
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
* Cell Name:    single_ended_cascode_current_mirror_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_cascode_current_mirror_pmos Vbiasn2 Vbiasp Vbiasp2 Vinn Vinp Voutp
*.PININFO Vbiasn2:I Vbiasp:I Vbiasp2:I Vinn:I Vinp:I Voutp:O
MM14 net025 net012 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM13 net024 net012 vdd! vdd! pmos w=WA l=LA nfin=nA1
MM3 Voutp Vbiasp2 net025 vdd! pmos w=WA l=LA nfin=nA2
MM2 net012 Vbiasp2 net024 vdd! pmos w=WA l=LA nfin=nA2
MM7 net11 Vinn net14 net27 pmos w=WA l=LA nfin=nA3
MM6 net16 Vinp net14 net27 pmos w=WA l=LA nfin=nA3
MM5 net14 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM12 net29 net11 gnd! gnd! nmos w=WA l=LA nfin=nA5
MM11 net32 net16 gnd! gnd! nmos w=WA l=LA nfin=nA6
MM10 net33 net11 gnd! gnd! nmos w=WA l=LA nfin=nA5
MM4 net26 net16 gnd! gnd! nmos w=WA l=LA nfin=nA6
MM1 Voutp Vbiasn2 net29 gnd! nmos w=WA l=LA nfin=nA7
MM0 net012 Vbiasn2 net32 gnd! nmos w=WA l=LA nfin=nA8
MM9 net11 Vbiasn2 net33 gnd! nmos w=WA l=LA nfin=nA7
MM8 net16 Vbiasn2 net26 gnd! nmos w=WA l=LA nfin=nA8
.ENDS


.SUBCKT LG_load_biasn Vbiasn1 Vbiasn2 Biasp
*.PININFO Vbiasn1:O Vbiasn2:O Biasp:I 
MM15 Vbiasn2 Vbiasn2 Vbiasn1 gnd! nmos w=WA l=LA nfin=nA1
MM13 Vbiasn1 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR15_1 Vbiasp
*.PININFO Vbiasp:O
RR1 Vbiasp gnd! res=rK
MM2 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasn2 LG_Vbiasp LG_Vbiasp2 Vinn Vinp Voutp single_ended_cascode_current_mirror_pmos
xiLG_load_biasn LG_Vbiasn1 LG_Vbiasn2 Biasp LG_load_biasn
xibCR15_1 Biasp CR15_1
.END