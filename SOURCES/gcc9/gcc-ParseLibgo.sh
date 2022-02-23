cat $1 | awk '\
BEGIN {
f = "";
s = "";
}
function clean()
{
	t = 0;
	r = "";
	rr= 0;
	f = "";
	s = "";
	fe= "";
}

{
# _testmain.go:14:43: ...
#trace_stack_test.go:10:16: error: import file 'internal/trace' not found
n = split($0, a, ":")
if( n != 0 && ( a[1] == "_testmain.go" || a[4] == " error" ) )
{
	t = 1;
	tm= $0;
}

# "=== RUN" appears only if -test.v 
if( $1$2 == "===RUN" )
{
	r = $3;
	rr= 1;
	rrr=1;
	next;
}
if( rr == 1 )
{
#                              tab !                    blank !
	if( substr($0,1,1) != "	" && substr($0,1,1) != " " && $1 != "---" && $0 != "PASS" )
	{
		cr= $0;
		rr= 0;
	}
}
if( $1$2 == "---FAIL:" )
{
	f = f $3 " ";
	next;
}
if( $1 == "SIGILL:" || $1 == "SIGABRT:" || $1 == "SIGTRAP:" || $1$2 == "[signalSIGSEGV:" || $1 == "panic:" || $1$2 == "timedout" )
{
	s = $0;
	next;
}
#=== RUN   TestHugeWriteFails
#fatal error: runtime: out of memory
if( $1$2 == "fatalerror:" )
{
	fe = $0;
	next;
}
if( $1 == "FAIL:" )
{
	if(f != "")
	{
		printf("  %-25s : %s\n", $2, f);
	}
	if( t == 1 && s == "" )
	{
		printf("  %-25s : %s\n", $2, tm);
		clean();
		next;
	}
	if(s != "")
	{
		if( rrr == 1 )	printf("  %-25s : %s : %s\n", $2, r, s);
		else		printf("  %-25s : %s\n", $2, s);
		clean();
		next;
	}
	if(fe != "")
	{
		if( rrr == 1 )	printf("  %-25s : %s : %s\n", $2, r, fe);
		else		printf("  %-25s : %s\n", $2, fe);
		clean();
		next;
	}
	if( f == "" && s == "" )
	{
		if( rrr == 1 )	printf("  %-25s : %s : %s\n", $2, r, cr);
		else		printf("  %-25s : %s\n", $2, cr);
		clean();
		next;
	}
	clean();
}
}' | sort
