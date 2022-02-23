#!/bin/sh
set -x
#!/bin/sh


usr=$(id -u)
[ $usr == 0 ] && { echo "Ne pas lancer sous root";exit 0; }


export nb="32 64"

[ "$1"  == 64 ] && { nb=64; }
[ "$1"  == 32 ] && { nb=32; }
[ "$nb" == 00 ] && { echo Erreur;exit 1; }





fct()
{
    export nbits=$1
    echo nbits=$nbits

    RPM_SOURCE_DIR="/opt/freeware/src/packages/SOURCES"
    RPM_BUILD_DIR="/opt/freeware/src/packages/BUILD"
    RPM_OPT_FLAGS="-O2 -fsigned-char"
    RPM_ARCH="ppc"
    RPM_OS="aix"
    export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS
    RPM_DOC_DIR="/opt/freeware/doc"
    export RPM_DOC_DIR
    RPM_PACKAGE_NAME="cups"
    RPM_PACKAGE_VERSION="2.2.1"
    RPM_PACKAGE_RELEASE="2"
    export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
    RPM_BUILD_ROOT="/var/opt/freeware/tmp/cups-2.2.1-2-root"
    export RPM_BUILD_ROOT
    
    set -x
    umask 022
    cd /opt/freeware/src/packages/BUILD || exit 1
    cd cups-2.2.1 || exit 1
    
    export CFLAGS=""
    export CXXFLAGS=""
    
    export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
    export MAKE="gmake --print-directory -k "
    export AR=/usr/bin/ar
    export AWK=/opt/freeware/bin/gawk
    
    
    find . -name '*.sh' | while read fic;
    do
	[  -e $fic.sauve ] && break;
	cp -p $fic $fic.sauve
	head -1 $fic.sauve > $fic
	echo "set -x" >> $fic
	cat  $fic.sauve >> $fic
    done
    
    
    cd "$nbits"bit/test || exit 1
    
    export CC="/opt/freeware/bin/gcc -maix$nbits -D_DBUS_GNUC_EXTENSION=__extension__" 
    export CXX="/opt/freeware/bin/g++ -maix$nbits -D_DBUS_GNUC_EXTENSION=__extension__ "
    export OBJECT_MODE=$nbits
    export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
    export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
    export LDFLAGS="-L/opt/freeware/lib"
    export LIBRARY_PATH=/opt/freeware/lib:/opt/freeware/lib/gcc/powerpc-ibm-aix6.1.0.0/4.8.4/:/lib/:/usr/lib/
    
    
    make clean
    make
    
    # arguments positionel :
    #  
    #  1 : testype 0-4  (*=1)
    #  2 : ssltype 0-2  (*=0)      0 pas SSL/TLS 1 pas d'encryption, 2 : encryp
    #  3 : usevalgrind Y (*=N)
    #  4 : usedebugprintfs 0-9 Y=5 (*=N)    Log files in $BASE/log BASE=/tmp/cups-$user
    #  5 : junk (*=Scheduler is PID $cupsd.)
    
    
    export u=girardet
    export BS=/tmp/cups-$u
    
    for testype in 0 1 2 3 4;
    do
	for ssltype in 0 1 2;
	do
	    for usevalgrind in N;
	    do
		for usedebugprintfs in 9;
		do
		    for junk in N;  # Scheduler is PID $cupsd
		    do
			
			DAT=$(date +%s)
			SF=$testype.$ssltype.$usevalgrind.$usedebugprintfs.$junk.$DAT
			
			echo ./run-stp-tests.sh $testype $ssltype $usevalgrind $usedebugprintfs $junk  ...... tee traces.run-stp-tests-all.sh.$SF.log
			./run-stp-tests.sh $testype $ssltype $usevalgrind $usedebugprintfs $junk  2>&1 | tee traces.run-stp-tests-all.sh.$SF.log
			mv $BS $BD.$SF
			
			mkdir S_"$DAT"
			mv "*girardet*" S_"$DAT"

			mv /tmp/cups-girardet /tmp/cups-girardet.$DAT
			sleep 30
			
		    done
		done
	    done
	done
    done
    
}



# lancement 32/64
for n in $nb
do
    fct $n
done

