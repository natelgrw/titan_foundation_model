************************************************************************
* auCdl Netlist:
*
* Library Name:  OTA_class
* Top Cell Name: single_ended_miller_compensated_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:09:34 2019
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
* Cell Name:    single_ended_miller_compensated_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_miller_compensated_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM13 Voutp net38 gnd! gnd! nmos w=WA l=LA nfin=nA1
MM9 net38 net35 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net35 net35 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM12 Voutp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM11 net33 Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM10 net38 Vinn net33 net39 pmos w=WA l=LA nfin=nA4
MM7 net35 Vinp net33 net39 pmos w=WA l=LA nfin=nA4
CC2 Voutp net38 1p
.ENDS


.SUBCKT LG_npmos Biasn Vbiasn Vbiasp
*.PININFO Biasn:I Vbiasn:O Vbiasp:O
MM4 Vbiasp Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM2 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM10 neta Biasn gnd! gnd! nmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA4
MM1 Vbiasn neta vdd! vdd! pmos w=WA l=LA nfin=nA5
MM0 neta neta vdd! vdd! pmos w=WA l=LA nfin=nA5
.ENDS

.SUBCKT CR7_1 Vbiasn
*.PININFO Vbiasn:O
RR1 Vbiasn net7 res=rK
RR0 vdd! net7 res=rK
RRF vdd! Vbiasn res=rK
MM1 net7 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_miller_compensated_pmos
xiLG_npmos Biasn LG_Vbiasn LG_Vbiasp LG_npmos
xibCR7_1 Biasn CR7_1
.END