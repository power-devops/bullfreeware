# In:
#	                === libstdc++ Summary ===
#	
#	# of expected passes            8035
#	# of unexpected failures        22
#	# of expected failures          44
#	# of unexpected successes	10
#	# of unresolved testcases       9
#	# of unsupported tests          584


# Out:
#       Tests            EP       UF       EF       US       UC       UT
#	------------------------------------------------------------------
#	gfortran      41046       32       75        1        0       82
#	g++           95030       33      268        0        2     3785
#	gcc           97017      524      282       20        1     2108
#	------------------------------------------------------------------
#	Total        233093      589      625       21        3     5975


FILE=$1

cat $FILE | awk '
BEGIN {
f = 0;
}
{
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

	F1="        %-10s %8s %8s %8s %8s %8s %8s\n";
	F2="	------------------------------------------------------------------\n";
		printf(F1,"Tests", "EP", "UF", "EF", "US", "UC", "UT");
		printf(F2);
	for(n in N)
	{
		printf("	%-10s %8d %8d %8d %8d %8d %8d\n", n, EP[n,0], UF[n,0], EF[n,0], US[n,0], UC[n,0], UT[n,0]);
		ep += EP[n,0];
		uf += UF[n,0];
		ef += EF[n,0];
		us += US[n,0];
		uc += UC[n,0];
		ut += UT[n,0];
	}
		printf("	------------------------------------------------------------------\n");
		printf("	%-10s %8d %8d %8d %8d %8d %8d\n", "Total", ep, uf, ef, us, uc, ut);
        GT=ep+uf+ef+us+uc+ut;
		printf("\n	%-10s %8d\n", "GrandTotal: ", GT);
		printf("\n	%-10s %8g%\n", "UF/GT     : ", (uf/GT)*100);
}
}'
