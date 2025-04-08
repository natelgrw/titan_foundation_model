************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: fully_differential_cascode_current_mirror
* View Name:     schematic
* Netlisted on:  Sep 11 21:02:16 2019
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
* Cell Name:    fully_differential_cascode_current_mirror
* View Name:    schematic
************************************************************************

.SUBCKT fully_differential_cascode_current_mirror Vbiasn Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutn Voutp
*.PININFO Vbiasn:I Vbiasn1:I Vbiasn2:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O Voutp:O
MM3 net22 Vinp net9 gnd! nmos w=WA l=LA nfin=nA1
MM0 net31 Vinn net9 gnd! nmos w=WA l=LA nfin=nA1
MM4 net9 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM14 Voutp Vbiasn2 net34 gnd! nmos w=WA l=LA nfin=nA3
MM13 Voutn Vbiasn2 net21 gnd! nmos w=WA l=LA nfin=nA3
MM8 net34 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM7 net21 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA4
MM2 net32 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM1 net23 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA6
MM6 net33 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA5
MM5 net20 Vbiasp2 vdd! vdd! pmos w=WA l=LA nfin=nA6
MM12 net31 Vbiasp1 net32 vdd! pmos w=WA l=LA nfin=nA7
MM11 net22 Vbiasp1 net23 vdd! pmos w=WA l=LA nfin=nA8
MM10 Voutp Vbiasp1 net33 vdd! pmos w=WA l=LA nfin=nA7
MM9 Voutn Vbiasp1 net20 vdd! pmos w=WA l=LA nfin=nA8
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA2
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS

.SUBCKT CR4_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM11 net023 net024 Vbiasn gnd! nmos w=27.0n l=LA nfin=nA1
MM8 net025 net010 net023 gnd! nmos w=27.0n l=LA nfin=nA2
MM9 net024 net024 net023 gnd! nmos w=27.0n l=LA nfin=nA3
MM7 net010 net010 net025 gnd! nmos w=WA l=LA nfin=nA4
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA5
MM0 Vbiasp net025 gnd! gnd! nmos w=WA l=LA nfin=nA6
MM10 net024 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA7
MM4 net010 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA8
MM3 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA7
MM1 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA9
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Voutp fully_differential_cascode_current_mirror
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR4_2 Biasn Biasp CR4_2
.END