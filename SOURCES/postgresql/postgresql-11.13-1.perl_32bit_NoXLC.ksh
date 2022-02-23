#!/bin/ksh

PERLVERSION=`/usr/bin/rpm -qa | grep "^perl-"`
PERLV=`echo $PERLVERSION | awk -F- '{print $2}' | awk -F. '{print $1 "." $2}'`
PERLVV=`echo $PERLV | awk -F. '{print $1}'`
PERLVERSION="perl$PERLVV/$PERLV"

echo $* | grep ldopts > /dev/null
if [ $? -eq 0 ]
then
	echo "-Wl,-bE:/opt/freeware/lib/$PERLVERSION/CORE/perl.exp -s -L/opt/freeware/lib -Wl,-brtl -Wl,-bdynamic -L/usr/local/lib -L/opt/freeware/lib/$PERLVERSION/CORE -lperl -lpthread -lbind -lnsl -ldl -lld -lm -lcrypt -lpthreads -lc"
else
	/opt/freeware/bin/perl_32 "$@"
fi
