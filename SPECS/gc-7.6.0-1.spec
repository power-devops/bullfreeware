# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}


Summary: A garbage collector for C and C++ 
Name:    gc	
Version: 7.6.0
Release: 1
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/	
#Source0: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz
Source0: http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
Source1: libatomic_ops-7.4.4.tar.gz
Source2: %{name}-%{version}-%{release}.build.log

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _libdir64 %{_prefix}/lib64


%description
The Boehm-Demers-Weiser conservative garbage collector can be 
used as a garbage collecting replacement for C malloc or C++ new.


%package devel
Summary: Libraries and header files for %{name} development 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.


%prep
echo "DO_TESTS=%{DO_TESTS}"
%setup -q -n %{name}-%{version}

tar xf %{SOURCE1}
mv libatomic_ops-7.4.4 libatomic_ops

cp -p  ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h  ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h.save
cp -p  ./libatomic_ops/src/atomic_ops/sysdeps/gcc/powerpc.h   ./libatomic_ops/src/atomic_ops/sysdeps/ibmc/powerpc.h

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

export CC__="/usr/vac/bin/xlc     -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX__="/usr/vacpp/bin/xlC  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CFLAGS="-O2"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

# first build the 64-bit version
cd 64bit

#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC="$CC__   -q64 "
export CXX="$CXX__ -q64 "
export OBJECT_MODE=64

export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export STRIP="/usr/bin/strip -X64"

export M4=/usr/linux/bin/m4 
autoreconf -vif
automake --add-missing 

CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-threads=aix \
    --enable-shared --disable-static \
    --with-libatomic-ops=no

gmake %{?_smp_mflags}


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi


# now build the 32-bit version
cd ../32bit

#export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC="$CC__   -q32 "
export CXX="$CXX__ -q32 "
export OBJECT_MODE=32

export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"
export STRIP="/usr/bin/strip -X32"

export M4=/usr/linux/bin/m4
autoreconf -vif
automake --add-missing

CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-threads=aix \
    --enable-shared --disable-static \
    --with-libatomic-ops=no

gmake %{?_smp_mflags}


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
make install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
make install DESTDIR=${RPM_BUILD_ROOT}

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
