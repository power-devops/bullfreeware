#!/bin/ksh

PERLVERSION=`/usr/bin/rpm -qa | grep "^perl-5"`
PERLV=`echo $PERLVERSION | awk -F- '{print $2}'`
PERLVV=`echo $PERLV | awk -F. '{print $1}'`
PERLV2=`echo $PERLV | awk -F. '{print $1 "." $2}'`
PERLVERSION="perl$PERLVV/$PERLV"
PERLVERSION2="perl$PERLVV/$PERLV2"

echo $* | grep ldopts > /dev/null
if [ $? -eq 0 ]
then
	echo "-Wl,-bE:/opt/freeware/lib/$PERLVERSION2/CORE/perl.exp -s -L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -Wl,-brtl -Wl,-bdynamic -L/usr/local/lib -Wl,-b64 -L/opt/freeware/lib/$PERLVERSION2/CORE -lperl -lpthread -lbind -lnsl -ldl -lld -lm -lcrypt -lpthreads -lc"
else
	/opt/freeware/bin/perl_64 "$@"
fi
