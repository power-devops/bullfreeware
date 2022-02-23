
# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

# compiler defauft xlc
# To use gcc : --define 'gcc_compiler=x'

%{?gcc_compiler:%define gcc_compiler 1}
%{!?gcc_compiler:%define gcc_compiler 0}

%if %{gcc_compiler} == 1
%define sub_release 
%else
%define sub_release xlc
%endif


Summary: A garbage collector for C and C++ 
Name:    gc	
Version: 7.6.0
Release: 4%{?sub_release}
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/	
#Source0: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz
Source0: http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
Source1: libatomic_ops-7.4.4.tar.gz
Source2: %{name}-%{version}-%{release}.build.log

%if %{gcc_compiler} == 1
Source3: %{name}-%{version}.libgc.la
Source4: %{name}-%{version}.libgc.lai
Source5: %{name}-%{version}.libstaticrootslib_test.la
%endif
Patch0:  %{name}-%{version}-3_powerpc_h.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _libdir64 %{_prefix}/lib64


%description
The Boehm-Demers-Weiser conservative garbage collector can be 
used as a garbage collecting replacement for C malloc or C++ new.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif



%package devel
Summary: Libraries and header files for %{name} development 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.
%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
echo "DO_TESTS=%{DO_TESTS}"
echo "gcc_compiler=%{gcc_compiler}"
echo "sub_release=%{?sub_release}"
%setup -q -n %{name}-%{version}

tar xf %{SOURCE1}
mv libatomic_ops-7.4.4 libatomic_ops

%if !%{gcc_compiler} == 1
# Avec compilateur xlc
    cp -p  ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h  ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h.save
    cp -p  ./libatomic_ops/src/atomic_ops/sysdeps/gcc/powerpc.h   ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h

%else
%patch0
%endif


# Modifie le type (ulong) (inconnu du compilateur xlc) par (unsigned long) : include/private/gcconfig.h include/gc.h
find . -type f  -name '*.h' |  while read f;
do
# <sys/types.h>
    grep -l ulong $f || continue;
    sed -e 's|(ulong)|(unsigned long)|g' <$f >$f.tmp.$$
    rm -f $f
    mv $f.tmp.$$ $f
done

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

# see bugzilla.redhat.com/689877
export CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN"

export RM="/usr/bin/rm -f"

GLOBAL_CC_OPTIONS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "

# Choose XLC or GCC
%if %{gcc_compiler} == 1

# compil assembler : Wall -Xextra
# -Wa,<options>            Pass comma-separated <options> on to the assembler
# -Wp,<options>            Pass comma-separated <options> on to the preprocessor
# -Wl,<options>            Pass comma-separated <options> on to the linker
# -Xassembler <arg>        Pass <arg> on to the assembler
# -Xpreprocessor <arg>     Pass <arg> on to the preprocessor
# -Xlinker <arg>           Pass <arg> on to the linker


# -E                       Preprocess only; do not compile, assemble or link
# -S                       Compile only; do not assemble or link
# -c                       Compile and assemble, but do not link
# -x <language>            Specify the language of the following input files
#       		   Permissible languages include: c c++ assembler none
# 		           'none' means revert to the default behavior of
#                          guessing the language based on the file's extension

# 1/ compile not assemble <-S> : ./libatomic_ops/src/atomic_ops.c   => atomic_ops.s
# gcc -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES -maix64 -DHAVE_CONFIG_H -I./include -I./libatomic_ops/src -DUSE_GET_STACKBASE_FOR_MAIN -fexceptions -DGC_NO_VISIBILITY -Wall -Wextra -fno-strict-aliasing -MT libatomic_ops/src/atomic_ops.lo -MD -MP -MF libatomic_ops/src/.deps/atomic_ops.Tpo -S ./libatomic_ops/src/atomic_ops.c -fPIC -DPIC
#
# ......  -Wall -Wextra .....  -S 
#
# => -rw-r--r-- 1 root system 20106 Aug 29 09:45 ./atomic_ops.s
#
# assemble :   /usr/bin/as -u -a64 -mppc64 -many -o libatomic_ops/src/.libs/atomic_ops.o atomic_ops.s
# :  /usr/bin/as -v -u -a64 -mppc64 -many -o libatomic_ops/src/.libs/atomic_ops.o atomic_ops.s
# as V6.1
# Assembler:
# atomic_ops.s: line 168: Error In Syntax
# ......  atomic_ops.s: line 249: Error In Syntax

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export LDFLAGS=""
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export CC__="/usr/vac/bin/xlc"
export CXX__="/usr/vacpp/bin/xlC"
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__
type $CXX__


export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

export CFLAGS="-O2"


# ****** DEBUT fontion configure_GC ******

configure_GC()
{
    set -x
    # $1 64 32
    [ $1 == "32" ] && {
	libdir=%{_libdir};
	lib="lib";
	slib="";
	bpT="0x10000000";
	bpD="0x30000000";

    }
    [ $1 == "64" ] && {
	libdir=%{_libdir64}
	lib="lib64";
	slib="_64";
    	bpT="0x100000000";
	bpD="0x110000000";
    }
    bmaxdata="0x80000000";
    
    echo configure_GC configure_GC $@
    echo configure_GC libdir=$libdir
    echo configure_GC lib=$lib
    echo configure_GC slib=$slib
    
    autoreconf -vif
    automake --add-missing

    CONFIG_SHELL=/bin/bash ./configure \
		--prefix=%{_prefix} \
		--libdir=$libdir \
		--enable-threads=aix \
		--enable-shared --disable-static \
		--with-libatomic-ops=no

    %if %{gcc_compiler} == 1

        gmake %{?_smp_mflags} || true

	sed  -e "s|lib64|$lib|" %{SOURCE3} >libgc.la
	sed  -e "s|lib64|$lib|" %{SOURCE4} >.libs/libgc.lai

	(cd ".libs" && rm -f "libgc.la" && ln -s "../libgc.la" "libgc.la" )
	/usr/bin/ld -b"$1" /lib/crt0"$slib".o -bpT:"$bpT" -bpD:"$bpD" -bM:SRE -o .libs/libgc.a.d/libgc.so.1 .libs/allchblk.o .libs/alloc.o .libs/blacklst.o .libs/checksums.o .libs/dbg_mlc.o .libs/dyn_load.o .libs/finalize.o .libs/gc_dlopen.o .libs/gcj_mlc.o .libs/headers.o .libs/mach_dep.o .libs/malloc.o .libs/mallocx.o .libs/mark.o .libs/mark_rts.o .libs/misc.o .libs/new_hblk.o .libs/obj_map.o .libs/os_dep.o .libs/pcr_interface.o .libs/ptr_chck.o .libs/real_malloc.o .libs/reclaim.o .libs/specific.o .libs/stubborn.o .libs/thread_local_alloc.o .libs/typd_mlc.o .libs/pthread_start.o .libs/pthread_support.o .libs/pthread_stop_world.o .libs/fnlz_mlc.o libatomic_ops/src/.libs/atomic_ops.o -lpthread -ldl -lc -bnoentry -bmaxdata:"$bmaxdata" -bE:.libs/libgc.exp -bernotok -L/usr/vac/lib -lxlopt -lxlipa -lxl -lc
	/usr/bin/ar  -q -X"$1" ./.libs/libgc.a ./.libs/libgc.a.d/libgc.so.1
    %endif

    gmake %{?_smp_mflags}

    %if %{gcc_compiler} == 1
        if [ "%{DO_TESTS}" == 1 ]
	then
            (gmake check || true)
             sed -e  "s|64bit|"$1"bit|g" -e "s|-q64|-q$1|g" -e "s|bmaxdata:0x80000000|bmaxdata:$bmaxdata|g" %{SOURCE5} >libstaticrootslib_test.la
            (cd ".libs" && /usr/bin/rm -f "libstaticrootslib_test.la" && ln -s "../libstaticrootslib_test.la" "libstaticrootslib_test.la" ;cd - )

            /usr/bin/ld -b"$1" /lib/crt0"$slib".o -bpT:"$bpT" -bpD:"$bpD" -bM:SRE -o .libs/libstaticrootslib_test.a.d/libstaticrootslib_test.so.1 tests/.libs/staticrootslib.o -blibpath:.libs:/opt/freeware/lib64:/usr/vac/lib:/usr/lib:/lib -L./.libs -lgc -lpthread -ldl -lc -bnoentry -bmaxdata:"$bmaxdata" -bE:.libs/libstaticrootslib_test.exp -bernotok -L/usr/vac/lib -lxlopt -lxlipa -lxl -lc
            /usr/bin/ar -X"$1" cru .libs/libstaticrootslib_test.a .libs/libstaticrootslib_test.a.d/libstaticrootslib_test.so.1

	fi

    %endif

    if [ "%{DO_TESTS}" == 1 ]
    then
	(gmake -k check || true)
    fi

}    # ****** END fontion configure_GC ******

    # first build the 64-bit version

export M4=/usr/linux/bin/m4 

    
cd 64bit

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export OBJECT_MODE=64

export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export STRIP="/usr/bin/strip -X64"

configure_GC 64

# EXPLICATION !!
#    Compilation mode gcc:
#    En mode gcc, le compilateur n'arrive pas a creer la librairie libgc.so.1 
# ld: 0711-317 ERROR: Undefined symbol: _end
# ld: 0711-317 ERROR: Undefined symbol: _data
# _data et _end sont des variables predefinies, respectivement le début des datas et le premier caractere apres la fin des datas
# Pour une raison inconnue la compile libtool+gcc même a cette erreur il est donc necessaire de se passer de libtoll pour produire libgc.a
# Un autre problème : libtool génère d'autres fichiers indispensables : .la et .lai
# Ces 2 fichiers sont de simples fichiers texte contenant quelques infos sur la librairie
# Nous avons donc produit et sourcé ces fichiers pour permettre à la compile de continuer
#    
#     1: premier gmake : Production des points .o, .lo. 
#     2: recopie des sources
#     3: Création du liens ".libs/libgc.la-> "../libgc.la""
#     4: Link (/usr/bin/ld -> libgc.so.1)
#     5: Construction librairie -> libgc.a
#     6: Continuation du make si necessaire
#    
#    En mode xlc seule la phase 6 est executée
#    
#    Passage des tests demandé:
#    
#        même problème, même solution, la librairie est : libstaticrootslib_test.a
#        Un seul source est necessaire (Pas de .lai necessaire)
#        
#        


# now build the 32-bit version
cd ../32bit

#export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export OBJECT_MODE=32

export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"
export STRIP="/usr/bin/strip -X32"

configure_GC 32


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
gmake install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
gmake install DESTDIR=${RPM_BUILD_ROOT}

# Extraction des .so 64 puis 32
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
echo "%{name}   1   "   > input.lib.$$.tmp
echo "cord      1   "  >> input.lib.$$.tmp

cat input.lib.$$.tmp | while read lib number pad;
do
    SEP=".";
     [ $number == "NULL" ] && { number="";SEP=""; }
    # add the 64-bit shared object to the shared library containing already the
    # 32-bit shared object
    $AR -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
    $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a lib"$lib".so"$SEP$number"
    (
	# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
	$RM ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
	cd  ${RPM_BUILD_ROOT}%{_libdir64}
	ln -s ../lib/lib"$lib".a lib"$lib".a
    )
done
rm -f input.lib.$$.tmp

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
cp doc/gc.man ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,system,-)
%doc 32bit/README.md
%doc 32bit/README.QUICK
%doc 32bit/doc/README.linux
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/*.html
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_mandir}/man?/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Fri Sep 02 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-4
- Improve .spec file

* Fri Sep 02 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-3
- Improve .spec file

* Thu Aug 25 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-2
- Add gcc/xlc.

* Tue Aug 23 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-1
- Update to version 7.6.0

* Fri Aug 05 2016 Tony Reix <tony.reix@atos.net> - 7.4.4-1
- Update to version 7.4.4

* Fri Aug 05 2016 Tony Reix <tony.reix@atos.net> - 7.4.2-2
- Add .pc files
- Fix issues with README files

* Fri Sep 18 2015 Pascal Oliva <pascal.oliva@atos.net> - 7.4.2-1
- Update to version 7.4.2

* Thu Nov 04 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 6.8-1
- First port on Aix6.1
