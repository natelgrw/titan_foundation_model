************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended
* View Name:     schematic
* Netlisted on:  Sep 11 21:06:14 2019
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
* Cell Name:    single_ended
* View Name:    schematic
************************************************************************

.SUBCKT single_ended Vbiasn Vinn Vinp Voutp
*.PININFO Vbiasn:I Vinn:I Vinp:I Voutp:O
MM3 Voutp Vinp net16 gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasp Vinn net16 gnd! nmos w=WA l=LA nfin=nA1
MM4 net16 Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM1 Voutp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM2 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
.ENDS


.SUBCKT LG_pnmos Biasp Vbiasn Vbiasp
*.PININFO Biasp:I Vbiasn:O Vbiasp:O
MM1 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA1
MM0 Vbiasp net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM8 net6 net6 gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA3
MM10 net6 Biasp vdd! vdd! pmos w=WA l=LA nfin=nA4
.ENDS

.SUBCKT CR3_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM3 Vbiasp Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
MM1 Vbiasn Vbiasp vdd! vdd! pmos w=WA l=LA nfin=nA1
RR0 net15 gnd! res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos w=WA l=LA nfin=nA2
MM2 Vbiasp Vbiasn net15 gnd! nmos w=WA l=LA nfin=nA2
.ENDS


xiota LG_Vbiasn Vinn Vinp Voutp single_ended
xiLG_pnmos Biasp LG_Vbiasn LG_Vbiasp LG_pnmos
xibCR3_2 Biasn Biasp CR3_2
.END