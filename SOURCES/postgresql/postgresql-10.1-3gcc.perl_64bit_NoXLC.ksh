#!/bin/ksh

PERLVERSION=`/usr/bin/rpm -qa | grep perl-`
PERLV=`echo $PERLVERSION | awk -F- '{print $2}'`
PERLVV=`echo $PERLV | awk -F. '{print $1}'`
PERLVERSION="perl$PERLVV/$PERLV"

echo $* | grep ldopts > /dev/null
if [ $? -eq 0 ]
then
	echo "-Wl,-bE:/opt/freeware/lib/$PERLVERSION/ppc-aix-thread-multi-64all/CORE/perl.exp -s -L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -Wl,-brtl -Wl,-bdynamic -L/usr/local/lib -Wl,-b64 -L/opt/freeware/lib/$PERLVERSION/ppc-aix-thread-multi-64all/CORE -lperl -lpthread -lbind -lnsl -ldl -lld -lm -lcrypt -lpthreads -lc"
else
	/opt/freeware/bin/perl_64bit "$@"
fi
