************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: Fully_differential_folded_cascode
* View Name:     schematic
* Netlisted on:  Sep 11 21:03:06 2019
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
* Cell Name:    Fully_differential_folded_cascode
* View Name:    schematic
************************************************************************

.SUBCKT Fully_differential_folded_cascode Vbiasn Vbiasn1 Vbiasn2 Vbiasp1 Vbiasp2 Vinn Vinp Voutn
*.PININFO Vbiasn:I Vbiasn1:I Vbiasn2:I Vbiasp1:I Vbiasp2:I Vinn:I Vinp:I Voutn:O
MM6 net26 Vbiasp2 net23 vdd! pmos w=WA l=LA nfin=nA
MM5 Voutn Vbiasp2 net24 vdd! pmos w=WA l=LA nfin=nA
MM2 net23 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 net24 Vbiasp1 vdd! vdd! pmos w=WA l=LA nfin=nA
MM8 net26 Vbiasn2 net27 gnd! nmos w=WA l=LA nfin=nA
MM7 Voutn Vbiasn2 net25 gnd! nmos w=WA l=LA nfin=nA
MM3 net24 Vinp net13 gnd! nmos w=WA l=LA nfin=nA
MM0 net23 Vinn net13 gnd! nmos w=WA l=LA nfin=nA
MM10 net27 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM9 net25 Vbiasn1 gnd! gnd! nmos w=WA l=LA nfin=nA
MM4 net13 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_load_biasn_LV Vbiasn2 Biasp
*.PININFO Vbiasn2:O Biasp:I 
MM13 net9 Vbiasn2 gnd! gnd! nmos w=WA l=LA nfin=nA
MM15 Vbiasn2 Vbiasn2 net9 gnd! nmos w=WA l=LA nfin=nA
MM14 Vbiasn2 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR4_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM11 net023 net024 Vbiasn gnd! nmos w=27.0n l=LA nfin=nA
MM8 net025 net010 net023 gnd! nmos w=27.0n l=LA nfin=nA
MM9 net024 net024 net023 gnd! nmos w=27.0n l=LA nfin=nA
MM7 net010 net010 net025 gnd! nmos w=WA l=LA nfin=nA
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA
MM0 Vbiasp net025 gnd! gnd! nmos w=WA l=LA nfin=nA
MM10 net024 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM4 net010 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM3 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
MM1 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasn LG_Vbiasn1 LG_Vbiasn2 LG_Vbiasp1 LG_Vbiasp2 Vinn Vinp Voutn Fully_differential_folded_cascode
xiLG_load_biasn_LV LG_Vbiasn2 Biasp LG_load_biasn_LV
xibCR4_2 Biasn Biasp CR4_2
.END