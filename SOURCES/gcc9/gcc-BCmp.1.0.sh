#	                === libstdc++ Summary ===
#	
#	# of expected passes            8035
#	# of unexpected failures        22
#	# of expected failures          44
#	# of unexpected successes	10
#	# of unresolved testcases       9
#	# of unsupported tests          584

#       Tests           EP     UF       EF       US       UC       UT
#	------------------------------------------------------------------
#	gfortran     41046     32       75        1        0       82
#	g++          95030     33      268        0        2     3785
#	gcc          97017    524      282       20        1     2108
#	------------------------------------------------------------------
#	Total       233093    589      625       21        3     5975



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
if($1=="===" && $3=="Summary" && $4=="===")
{
	Sum	= 1;
	n	= $2;
	N[n]	= n;
	next;
}
if(Sum==1)
{
	if($0!="" && $1!="#")	Sum	= 0;
	if($1=="#")
	{
		if($3$4=="expectedpasses") 	EP[n,f]= $5;
		if($3$4=="unexpectedfailures")	UF[n,f]= $5;
		if($3$4=="expectedfailures")	EF[n,f]= $5;
		if($3$4=="unexpectedsuccesses")	US[n,f]= $5;
		if($3$4=="unresolvedtestcases")	UC[n,f]= $5;
		if($3$4=="unsupportedtests")	UT[n,f]= $5;
	}
}
} END {
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
