#!/bin/ksh

set -x
export U=$(id -nu)
export G=$(id -ng)
[ $U == 'root' ] && {
    echo "Ne doit pas etre lancé sous root";
    exit;
    }

cd  /opt/freeware/src/packages/BUILD/postgresql-9.6.1-1/ || exit;

RPM_SOURCE_DIR="/opt/freeware/src/packages/SOURCES"
RPM_BUILD_DIR="/opt/freeware/src/packages/BUILD"
RPM_OPT_FLAGS="-O2 -fsigned-char"
RPM_ARCH="ppc"
RPM_OS="aix"
export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS
RPM_DOC_DIR="/opt/freeware/doc"
export RPM_DOC_DIR
RPM_PACKAGE_NAME="postgresql"
RPM_PACKAGE_VERSION="9.6.1"
RPM_PACKAGE_RELEASE="2"
export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
RPM_BUILD_ROOT="/var/opt/freeware/tmp/postgresql-9.6.1-2-root"
export RPM_BUILD_ROOT

cd /opt/freeware/src/packages/BUILD
cd postgresql-9.6.1

# This line (use for tracing) sometimes generates the issue: "--trace:  not found" during tests
export MAKE="gmake "
export PATH=/opt/freeware/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java5/jre/bin:/usr/java5/bin
export AR=/usr/bin/ar

export CC__="/usr/vac/bin/xlc"
export CC__="/opt/IBM/xlc/13.1.3/bin/xlc"
export  CC__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export CXX__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export FLAG32="-q32"
export FLAG64="-q64"
export CC64=" ${CC__}  ${FLAG64}"
export CC32=" ${CC__}  ${FLAG32}"
export GLOBAL_CC_OPTIONS="-O2 "


HERE=$PWD
su - root -c "cd $HERE;pwd;echo  chown $U.$G;set -x;find . -type d| xargs chown $U.$G;find . -type f| xargs chown $U.$G;"
cd $HERE

fonct_test()
{
    set -x

    export BITS=$1
    LIB=lib$BITS
    [ $BITS -eq 64 ] && {
	LIB=lib64;
	export LIBPATH=$BUILD/postgresql-9.6.1/"$BITS"bit/tmp_install/opt/freeware/$LIB/:$BUILD/postgresql-9.6.1/"$BITS"bit/tmp_install/opt/freeware/$LIB/postgresql:/opt/freeware/$LIB:/opt/freeware/lib
	export CC="${CC64}   $GLOBAL_CC_OPTIONS"
	export PERL=/opt/freeware/bin/perl_64bit
	export PERL=/opt/freeware/src/packages/SOURCES/postgresql-9.6.1-2.perl_64bit_NoXLC.ksh
	export PYTHON=/opt/freeware/bin/python_64
	
    }
    [ $BITS -eq 32 ] && {
	LIB=lib;
	export LIBPATH=$BUILD/postgresql-9.6.1/"$BITS"bit/tmp_install/opt/freeware/$LIB/:$BUILD/postgresql-9.6.1/"$BITS"bit/tmp_install/opt/freeware/$LIB/postgresql:/opt/freeware/lib
	export CC="${CC32}   $GLOBAL_CC_OPTIONS"
	export PERL=/opt/freeware/bin/perl
	export PYTHON=/opt/freeware/bin/python
	
    }
    
    export OBJECT_MODE="$BITS"
    export LDFLAGS="-L/opt/freeware/lib$BITS -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib$BITS:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lintl"
    REP=/opt/freeware/src/packages/BUILD/postgresql-9.6.1/"$BITS"bit
    export CPPFLAGS="-I$REP/src/include -I$REP/src/interfaces/ecpg/include -I/opt/freeware/include -I/usr/include" ;
    export CFLAGS="-I$REP/src/include -I$REP/src/interfaces/ecpg/include -I/opt/freeware/include -I/usr/include" ;
    
    echo fonct_test "$BITS"bits;

    cd  "$BITS"bit || exit;
    date
    gmake --trace MAX_CONNECTIONS=10 check   2>&1|tee trace.gmakecheck.$D.log

    date
    gmake --trace check-world   2>&1|tee trace.gmakecheck-world.$D.log

    pwd
    RESD=src/test/regress/RESULTATS
    mkdir -p  $RESD

    ALL_EXTRAS=""
    for test in src/test/regress/sql/*.sql;
    do
	tst=$(echo $(basename $test)|sed -e 's;.sql$;;')
	[ -e src/test//regress/expected/$tst.out ] || {
	    echo fichier src/test/regress/expected/$tst.out inexistant SKIP;
	    continue;
	}
	
	grep " $tst .*ok$" trace.gmakecheck-world.$D.log && {
	    echo test $tst OK;
	    continue;
	}
	ALL_EXTRAS="$ALL_EXTRAS $tst"
    done

    echo gmake --trace -k check EXTRA_TESTS="$ALL_EXTRAS"
    gmake --trace -k check EXTRA_TESTS="$ALL_EXTRAS" 2>&1|tee -a trace.gmakeEXTRA_TESTS.ALL_EXTRAS.$D.log
}




export D=$(date +%s)

 fonct_test 32 2>&1| tee trace.fonct_test.32.$D.log
 fonct_test 64 2>&1| tee trace.fonct_test.64.$D.log

 
