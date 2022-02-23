# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# compiler default xlc
# To use gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}


%define majorver 8.5

Summary: Tcl scripting language development environment
Name: tcl
Version: %{majorver}.19
Release: 2
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/%{name}/%{name}%{version}-src.tar.gz
Source1: %{name}-%{version}-%{release}.build.log

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: tcl(abi) = %{majorver}

%define _libdir64 %{_prefix}/lib64


%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif



%package devel
Summary: Tcl scripting language development environment
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
%setup -q -n %{name}%{version}
chmod -x generic/tclThreadAlloc.c

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# Choose XLC or GCC
%if %{gcc_compiler} == 1

# prevent "out of stack space" error
export CFLAGS="               -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O2 -DTCL_NO_STACK_CHECK"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export LDFLAGS="-Wl,-brtl"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# prevent "out of stack space" error
export CFLAGS="-qmaxmem=16384 -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O2 -DTCL_NO_STACK_CHECK"

export CC__="xlc_r"
export CXX__="xlc_r"
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



# first build the 64-bit version
cd 64bit/unix

export OBJECT_MODE=64

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static \
    --enable-threads

gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver} -j16

if [ "%{dotests}" == 1 ]
then
	(gmake -k test || true)
fi


cd ../..


# now build the 32-bit version
cd 32bit/unix

export OBJECT_MODE=32

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static \
    --enable-threads

gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver} -j16

if [ "%{dotests}" == 1 ]
then
	(gmake -k test || true)
fi


cd ..
rm    -f lib%{name}%{majorver}.a
${AR} -r lib%{name}%{majorver}.a unix/lib%{name}%{majorver}.so ../64bit/unix/lib%{name}%{majorver}.so
slibclean
strip -e -X32_64                 unix/lib%{name}%{majorver}.so ../64bit/unix/lib%{name}%{majorver}.so


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"


cd 64bit/unix

export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver}_64
ln -sf tclsh%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/tclsh_64

cd ../..


cd 32bit/unix

export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
ln -sf tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :


ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/%{name}%{majorver}/ldAix

cd ..
cp lib%{name}%{majorver}.a  ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}%{majorver}.a

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
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
%doc 32bit/README 32bit/changes 32bit/license.terms
%{_bindir}/tclsh*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir64}/lib*.so
%dir %{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}%{majorver}/*
%dir %{_datadir}/%{name}8
%{_datadir}/%{name}8/*
%{_mandir}/man1/*
%{_mandir}/mann/*
/usr/bin/tclsh*
/usr/lib/lib*.a
/usr/lib/lib*.so
/usr/lib64/lib*.so


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/libtclstub*.a
%{_libdir64}/libtclstub*.a
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_mandir}/man3/*
/usr/include/*
/usr/lib/libtclstub*.a
/usr/lib64/libtclstub*.a


%changelog
* Fri May 25 2018 Tony Reix <tony.reix@bull.net> 8.5.19-2
- Rebuild without BullFreeware libx11

* Thu Dec 01 2016 Tony Reix <tony.reix@bull.net> 8.5.19-1
- Initial port on AIX 6.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 8.5.9-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jul 28 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-2
- Add librarie libtcl8.5.a with 32 and 64 bits

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-1
- Port on platform Aix5.3
