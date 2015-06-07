Sometime, if you are in area with very good 2G coverage but average or bad 3G coverage, your 3G modem will stay in 2G network. So, what do you do to force the modem to choose the 3G network as the preferred one?

Yes, you are right, most of modem connection s/w have "band selection" feature like we can find in most 3G handphone. You can force your modem or handphone to stay and looking for 3G coverage forever even there is no coverage at all.

But, not all connection s/w has this menu especially if you are using UNIX environment (FreeBSD, Linux, etc). In unix, normally we are using normal ppp connection no matter what is the "dev" link. In FreeBSD, we should find the modem under /dev/cuaaxx and in linux we should find it under /dev/ttyACMx or /dev/ttyUSBx

So, what can we do in Unix?
Thanks to AT command that provide us access to the modem directly. There is an AT command that very useful for me:
```
AT+COPS
```
As normal AT command, AT+COPS has both read and write command. I put the format for AT+COPS command at the end of this post.
You can try to search the network with this command: at+cops=?
here is the example:
```
at+cops=?
+COPS: (2,"IND INDOSAT","INDOSAT","51001",0),(1,"IND INDOSAT","INDOSAT","51001",2),(3,"IND TELKOMSEL","T-SEL","51010",2),(3,"IND TELKOMSEL","T-SEL","51010",0),(3,"LIPPO TEL","LIPPOTEL","51008",0),(3,"IND XL","XL","51011",0),(1,"3","3","51089",0),,(0,1,3,4),(0,1,2)

OK
```

From the sample above, we can see that I can get more than one operator network coverages. Pay attention to number with bold font above, zero (0) means GSM coverage and two (2) means UMTS (3G) coverage.

Now we know that we have 3G coverage. Our next task is forcing the modem to select the UMTS network instead of GSM. It is the time to use write mode of at+cops command. Here the example how to select the 3G coverage:
```
at+cops? ---> to check what is my network now, which is Indosat GSM network
+COPS: 0,0,"IND INDOSAT",0

OK
at+cops=1,0,"IND XL",2 ---> to force releasing current network
+CME ERROR: no network service
at+cops?
+COPS: 1 --> it is indicated that our manual selection failed

OK
at+cops=1,0,"IND INDOSAT",2 ---> to force/manually select Indosat 3G coverage
OK
at+cops? ---> to verify that we are already in 3G network
+COPS: 1,0,"IND INDOSAT",2

OK
```

You should have a qestion now, why do I use this command several time and use other operator network before choosing the correct one? I force the network selection to another operator first to force the modem to do cell coverage re-selection when I go back to my correct operator network. I found that if I tried to manually select 3G coverage directly using at+cops=1,0,"IND INDOSAT" when I already in GSM coverage, the modem didn't try to change the network from GSM to UMTS, so I tried to force my modem to leave the current network first then go back.

note:this at command is not fully forcing the modem to always attach to 3G like connection client s/w did but this is only a workaround by utilizing manual network search to specific operator and specific radio type.



Finally, here is the AT+COPS description. For full complete AT command description, please refer to 3GPP TS 27.007 specifications.
```
Command:+COPS=[[,[,[,]]]]
Possible response: +CME ERROR:

Command:+COPS?
Possible response:+COPS: [,,[,]]
+CME ERROR:

Command:+COPS=?
Possible response:+COPS: [list of supported (,long alphanumeric ,short alphanumeric ,numeric [,])s][,,(list of supported s),(list of supported s)]
+CME ERROR:

Defined values
:
0 automatic ( field is ignored)
1 manual ( field shall be present, and optionally)
2 deregister from network
3 set only (for read command +COPS?), do not attempt registration/deregistration ( and fields are ignored); this value is not applicable in read command response
4 manual/automatic ( field shall be present); if manual selection fails, automatic mode (=0) is entered
:
0 long format alphanumeric
1 short format alphanumeric
2 numeric
: string type; indicates if the format is alphanumeric or numeric; long alphanumeric format can be upto 16 characters long and short format up to 8 characters (refer GSM MoU SE.13 [9]); numeric format is the GSM Location Area Identification number (refer TS 24.008 [8] subclause 10.5.1.3) which consists of a three BCD digit country code coded as in ITU T E.212 Annex A [10], plus a two BCD digit network code, which is administration specific; returned shall not be in BCD format, but in IRA characters converted from BCD; hence the number has structure: (country code digit 3)(country code digit 2)(country code digit 1)(network code digit 3)(network code digit 2)(network code digit 1)
:
0 unknown
1 available
2 current
3 forbidden
access technology selected:
0 GSM
1 GSM Compact
2 UTRAN
```

