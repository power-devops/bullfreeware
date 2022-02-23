
# XFAIL: g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++98 broken -feliminate-dwarf2-dups (test for bogus messages, line 1)
# PASS:  g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++98 (test for excess errors)
# XFAIL: g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++11 broken -feliminate-dwarf2-dups (test for bogus messages, line 1)
# PASS:  g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++11 (test for excess errors)
# XFAIL: g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++14 broken -feliminate-dwarf2-dups (test for bogus messages, line 1)
# PASS:  g++.dg/debug/dwarf2/dwarf2-1.C  -std=gnu++14 (test for excess errors)




FILEA=$1
FILEB=$2

echo "A= " $FILEA
echo "B= " $FILEB
echo ""

cat $FILEA >  /tmp/AB
echo "@@"  >> /tmp/AB
cat $FILEB >> /tmp/AB



cat /tmp/AB | awk '
BEGIN {
f = 0;
}
{
if($0=="@@") { f++; next }

if($1=="PASS:" || $1=="XPASS:" || $1=="FAIL:" || $1=="XFAIL:" || $1=="UNSUPPORTED:" || $1=="ERROR:" || $1=="WARNING:" )
{
TEST="";
for(i=2;i<=NF;i++) TEST= TEST " " $i;
n	= TEST
}

if($1=="PASS:")        { ep[f]++; EP[n,f] = n; N[n] = n; next; }
if($1=="XPASS:")       { us[f]++; US[n,f] = n; N[n] = n; next; }
if($1=="FAIL:")        { uf[f]++; UF[n,f] = n; N[n] = n; next; }
if($1=="XFAIL:")       { ef[f]++; EF[n,f] = n; N[n] = n; next; }
if($1=="UNSUPPORTED:") { ut[f]++; UT[n,f] = n; N[n] = n; next; }
if($1=="ERROR:")       { ue[f]++; UE[n,f] = n; N[n] = n; next; }
if($1=="WARNING:")     { uw[f]++; UW[n,f] = n; N[n] = n; next; }
} END {
for(n in N)
{
	US0=""; if(US[n,0]!="") US0="US";
	US1=""; if(US[n,1]!="") US1="US";
	if(US0 != US1) { printf("%2s %2s | %-80s\n", US0, US1, n); }

	UF0=""; if(UF[n,0]!="") UF0="UF";
	UF1=""; if(UF[n,1]!="") UF1="UF";
	if(UF0 != UF1) { printf("%2s %2s | %-80s\n", UF0, UF1, n); }

#	if(US[n,0] != "" || US[n,1] != "") { printf(US[n,f]); }
#	if(UF[n,f] != "") { print(UF[n,f]); }
	if(UE[n,f] != "") { print(UE[n,f]); }
	if(UW[n,f] != "") { print(UW[n,f]); }
}
}'

exit

F=2
if(F==1)
{
	for(n in N)
	{
		printf("	%s\n", n);
		printf("		Expected Passes		%8d\n", EP[n,0]);
		printf("		Unexpected Failures	%8d\n", UF[n,0]);
		printf("		Expected Failures	%8d\n", EF[n,0]);
		printf("		Unexpected Successes	%8d\n", US[n,0]);
		printf("		Unresolved TestCases	%8d\n", UC[n,0]);
		printf("		Unsupported Tests	%8d\n", UT[n,0]);
	}
}
else
{
	print("EP: Expected Passes");
	print("UF: Unexpected Failures");
	print("EF: Expected Failures");
	print("US: Unexpected Successes");
	print("UC: Unresolved TestCases");
	print("UT: Unsupported Tests");
	print("");

	F2="  -------------------------------------------------------------------------------------------------------------------\n";
	printf("                              A                                  B                             Delta(A,B)   \n");
	printf(F2);
	F1="  %-10s | %6s %4s %4s %4s %4s %5s | %6s %4s %4s %4s %4s %5s | %6s %4s %4s %4s %4s %5s\n";
	printf(F1,"Tests", "EP", "UF", "EF", "US", "UC", "UT", "EP", "UF", "EF", "US", "UC", "UT", "EP", "UF", "EF", "US", "UC", "UT");
	printf(F2);
	F3="  %-10s | %6d %4d %4d %4d %4d %5d | %6d %4d %4d %4d %4d %5d | %6d %4d %4d %4d %4d %5d\n";
	for(n in N)
	{
		ep0 += EP[n,0]; ep1 += EP[n,1]; DEP = EP[n,1] - EP[n,0]; dep += DEP;
		uf0 += UF[n,0]; uf1 += UF[n,1]; DUF = UF[n,1] - UF[n,0]; duf += DUF;
		ef0 += EF[n,0]; ef1 += EF[n,1]; DEF = EF[n,1] - EF[n,0]; def += DEF;
		us0 += US[n,0]; us1 += US[n,1]; DUS = US[n,1] - US[n,0]; dus += DUS;
		uc0 += UC[n,0]; uc1 += UC[n,1]; DUC = UC[n,1] - UC[n,0]; duc += DUC;
		ut0 += UT[n,0]; ut1 += UT[n,1]; DUT = UT[n,1] - UT[n,0]; dut += DUT;
		printf(F3, n, EP[n,0], UF[n,0], EF[n,0], US[n,0], UC[n,0], UT[n,0], EP[n,1], UF[n,1], EF[n,1], US[n,1], UC[n,1], UT[n,1], DEP, DUF, DEF, DUS, DUC, DUT);
	}
	printf(F2);
	printf(F3, "Total", ep0, uf0, ef0, us0, uc0, ut0, ep1, uf1, ef1, us1, uc1, ut1, dep, duf, def, dus, duc, dut);
}
}'
exit
		Flag=""; D="";
		if( ep0!=0 && ep1!=0 ) { Dep=ep1-ep0 ; if(Dep>0) { Flag="   "; TBD+=D} else { D=-D; TAD+=D} }
