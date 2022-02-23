# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# compiler default xlc
# To use gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}


%define majorver 8.6
%define prevmajorver 8.5

Summary: Tcl scripting language development environment
Name: tcl
Version: %{majorver}.10
Release: 2
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz

# Taken from Tcl 8.5.19
Source1: libtcl8.5.so-aix32
Source2: libtcl8.5.so-aix64

Source100: %{name}-%{version}-%{release}.build.log

# BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# The AIX find command does not work as expected using findutils find
BuildRequires: findutils sed
Provides: tcl(abi) = %{majorver}
Provides: tcl-tcldict = %{version}

%define _libdir64 %{_prefix}/lib64

Patch0: tcl-8.6.10-autopath.patch
# Linux specific ? Patch1: tcl-8.6.10-conf.patch
Patch2: tcl-8.6.10-hidden.patch

Patch3: tcl-8.6.10-tcltests-path-fix.patch

# Patches required for tests requiring package tcltests
# Code copied from tests/fileSystemEncoding.test
# Latest Fedora patch3 corrects this issue
# Patch10: tcl-8.6.10-tcltests.patch


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



%package static
Summary: Tcl scripting language development environment
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description static
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the libtclstub static library for tcl development.

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

echo "dotests=%{dotests}"

%setup -q -n %{name}%{version}

# Not sure why Fedora does this   rm -r compat/zlib
chmod -x generic/tclThreadAlloc.c
chmod -x generic/tclStrToD.c

# Taken from Fedora - deliver tcl internal lib and headers

%patch0 -p1 -b .autopath
# Linux specific ? %patch1 -p1 -b .conf
%patch2 -p1 -b .hidden
%patch3 -p1 -b .tcltests-path-fix

# %patch10 -p1 -b .tcltests


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar"
export NM="/usr/bin/nm -X32_64"


# Choose XLC or GCC
%if %{gcc_compiler} == 1

# prevent "out of stack space" error
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O2 -DTCL_NO_STACK_CHECK"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
# -brtl is required due to:
#   cd unix
#   /opt/freeware/bin/gcc ... tclAppInit.o \
#        -L/opt/freeware/src/packages/BUILD/tcl8.6.6/64bit/unix -ltcl8.6 libtclstub8.6.a \
#        -L/opt/freeware/lib64 -o tclsh
#	ld: 0711-317 ERROR: Undefined symbol: _GLOBAL__AIXI_libtcl8_6_so
#	ld: 0711-317 ERROR: Undefined symbol: _GLOBAL__AIXD_libtcl8_6_so
# ll libtcl8.6*  
#  -rwxr-xr-x 1 root system 3077228 May 24 16:36 libtcl8.6.so
# NO libtcl8.6.a yet !!!
# If an old tcl8.6.6 is installed, it does not find _GLOBAL__AIXI_libtcl8_6_so
# If no tcl8.6.6 installed, gcc does not use libtcl8.6.so .

# Must include -blibath for tclsh 32 and 64 bits

export LDFLAGS32="-Wl,-brtl -Xlinker -bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS64="-Wl,-brtl -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
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
export LDFLAGS32="-Wl,-bmaxdata:0x80000000"
export LDFLAGS64=""
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

export LIBS="-lm"


# first build the 64-bit version
cd 64bit/unix

export OBJECT_MODE=64

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LDFLAGS="${LDFLAGS64}"


./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared \
    --enable-symbols \
    --enable-threads

gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

# %if %{without dotests}
# echo "*** Skipping tests"
# exit 0
# %endif # without dotests

# if [ "%{dotests}" == 1 ]
# then
# 	(gmake -k test || true)
# fi


cd ../..


# now build the 32-bit version
cd 32bit/unix

export OBJECT_MODE=32

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LDFLAGS="${LDFLAGS32}"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static \
    --enable-symbols \
    --enable-threads

gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

# if [ "%{dotests}" == 1 ]
# then
# 	(gmake -k test || true)
# fi


cd ..
# Now under 32bit directory

# libtclX.Y.a
rm    -f      lib%{name}.a
rm    -f      lib%{name}%{majorver}.a
${AR} -X32 -q lib%{name}.a                     unix/lib%{name}%{majorver}.so
${AR} -X64 -q lib%{name}.a            ../64bit/unix/lib%{name}%{majorver}.so
ln -sf        lib%{name}.a                          lib%{name}%{majorver}.a
slibclean
strip -e -X32                                  unix/lib%{name}%{majorver}.so
strip -e -X64                         ../64bit/unix/lib%{name}%{majorver}.so

# libtclstubX.Y.a
mkdir ../tclstub
cd ../tclstub
${AR} -X32 -xv ../32bit/unix/lib%{name}stub%{majorver}.a
cd -
rm    -f      lib%{name}stub.a
rm    -f      lib%{name}stub%{majorver}.a
${AR} -X32 -q lib%{name}stub.a                 ../tclstub/*
cd ../tclstub
rm -f *
${AR} -X64 -xv ../64bit/unix/lib%{name}stub%{majorver}.a
cd -
${AR} -X64 -q lib%{name}stub.a                 ../tclstub/*
ln -sf        lib%{name}stub.a                 lib%{name}stub%{majorver}.a


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# The 64 bit async.test requires ulimit -d unlimited
# because of error "Test file error: unable to realloc 50331648 bytes"
cd 64bit/unix
(
 ulimit -d unlimited
 gmake -k test || true
)
cd ../..

cd 32bit/unix
(gmake -k test || true)


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"


cd 64bit/unix

export OBJECT_MODE=64
export LDFLAGS="${LDFLAGS64}"
gmake DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver}_64

ln -sf tclsh%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/tclsh_64
ln -sf tclsh%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/tclsh

cd ../..


cd 32bit/unix

export OBJECT_MODE=32
export LDFLAGS="${LDFLAGS32}"
gmake DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver}_32
ln -sf tclsh%{majorver}_32 ${RPM_BUILD_ROOT}%{_bindir}/tclsh_32

# Some applications access directly tclsh8.6 (default 64 bit), e.g. expect tests
ln -sf tclsh%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :


ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

cd ..

# Manage compatibility with version 8.5
#  - required:
#        libtcl8.5.a(libtcl8.5.so) is needed by postgresql-pltcl-9.6.0-2
#  - requirement to .so file to be removed in the future:
#        libtcl8.5.so is needed by expect-5.44.1.15-1
#        libtcl8.5.so is needed by tkinter-2.7.12-1
#        libtcl8.5.so is needed by ruby-2.3.1-5

cp %{SOURCE1} libtcl%{prevmajorver}.so
/usr/bin/strip -X32 -e                      libtcl%{prevmajorver}.so
/usr/bin/ar    -X32 -q lib%{name}.a         libtcl%{prevmajorver}.so
mv                                          libtcl%{prevmajorver}.so ${RPM_BUILD_ROOT}%{_libdir}/

cp %{SOURCE2} libtcl%{prevmajorver}.so
/usr/bin/strip -X64 -e                      libtcl%{prevmajorver}.so
/usr/bin/ar    -X64 -q lib%{name}.a         libtcl%{prevmajorver}.so
mv                                          libtcl%{prevmajorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/


chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/%{name}%{majorver}/ldAix


# Put current  main lib for delivery
cp                       lib%{name}.a       ${RPM_BUILD_ROOT}%{_libdir}
cp                       lib%{name}stub.a   ${RPM_BUILD_ROOT}%{_libdir}

(

cd                                          ${RPM_BUILD_ROOT}%{_libdir}
ln -sf /opt/freeware/lib/lib%{name}.a       lib%{name}%{majorver}.a
ln -sf /opt/freeware/lib/lib%{name}stub.a   lib%{name}stub%{majorver}.a

# symlink for the previous main archive
cd                                          ${RPM_BUILD_ROOT}%{_libdir}
ln -sf /opt/freeware/lib/lib%{name}.a       lib%{name}%{prevmajorver}.a
cd                                          ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf /opt/freeware/lib/lib%{name}.a       lib%{name}%{prevmajorver}.a

# 64bit symlink for the main archive
cd                                          ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf ../lib/lib%{name}.a                  lib%{name}.a
ln -sf ../lib/lib%{name}%{majorver}.a       lib%{name}%{majorver}.a
ln -sf ../lib/lib%{name}stub%{majorver}.a   lib%{name}stub%{majorver}.a

)


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



# Taken from Fedora - deliver tcl internal lib and headers

mkdir -p %{buildroot}/%{_libdir}/%{name}%{majorver}
mkdir -p %{buildroot}/%{_libdir64}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/%{name}Config.sh %{buildroot}/%{_libdir}/%{name}%{majorver}/%{name}Config.sh
ln -s %{_libdir64}/%{name}Config.sh %{buildroot}/%{_libdir64}/%{name}%{majorver}/%{name}Config.sh

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/generic
mkdir -p %{buildroot}/%{_includedir}/%{name}-private/unix

# Following find command does not work as expected using AIX find
/opt/freeware/bin/find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
        for i in *.h ; do
                [ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
        done
)

# remove buildroot traces - BUILD/32bit PWD
# Following sed -i command does not work as expected using AIX sed
/opt/freeware/bin/sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh

cd ..
cd 64bit

# remove buildroot traces - BUILD/64bit PWD
/opt/freeware/bin/sed -i -e "s|$PWD/unix|%{_libdir64}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir64}/%{name}Config.sh

# Linux does not need this file   rm -rf %{buildroot}/%{_datadir}/%{name}%{majorver}/ldAix


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/README.md 32bit/changes
%doc 32bit/license.terms
%{_bindir}/tclsh*
%dir %{_datadir}/%{name}%{majorver}
%dir %{_datadir}/%{name}8
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tclAppInit.c
%{_datadir}/%{name}8
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}%{majorver}.a
%{_libdir}/lib%{name}%{prevmajorver}.a
%{_libdir}/lib*.so
%{_libdir64}/lib%{name}.a
%{_libdir64}/lib%{name}%{majorver}.a
%{_libdir64}/lib*.so
%dir %{_libdir}/%{name}%{majorver}
%dir %{_libdir64}/%{name}%{majorver}
%{_mandir}/man1/*
%{_mandir}/mann/*
# Symbolic links in /usr removed to avoid collision with AIX LPP
# /usr/bin/tclsh*
# /usr/lib/lib%{name}.a
# /usr/lib/lib%{name}%{majorver}.a
# /usr/lib/lib*.so
# /usr/lib64/lib%{name}.a
# /usr/lib64/lib%{name}%{majorver}.a
# /usr/lib64/lib*.so


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
# Move static library to separate RPM
# %{_libdir}/libtclstub*.a
# %{_libdir64}/libtclstub*.a
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_libdir}/%{name}ooConfig.sh
%{_libdir}/%{name}%{majorver}/%{name}Config.sh
%{_libdir}/pkgconfig/tcl.pc
%{_datadir}/%{name}%{majorver}/tclAppInit.c
%{_mandir}/man3/*
# Symbolic links in /usr removed to avoid collision with AIX LPP
# /usr/include/*
# /usr/lib/libtclstub*.a
# /usr/lib64/libtclstub*.a


%files static
%defattr(-,root,system,-)
%{_libdir}/libtclstub*.a
%{_libdir64}/libtclstub*.a


%changelog
* Wed Jul 01 2020 Michael Wilson <michael.a.wilson@atos.net> - 8.6.10-2
- Add symlink tclsh8.6 (needed by some apps) to tclsh8.6_64
- Add -blibpath for tclsh 32 and 64 bits
- Correction to 64 bit tclConfig.sh

* Thu Feb 13 2020 Michael Wilson <michael.a.wilson@atos.net> - 8.6.10-1
- Update to 8.6.10 based on Fedora 32
- Add patch10 for test errors - corrected using latest Fedora patch3
- Move libtclstub static library to new RPM tcl-static
- Symbolic links in /usr removed to avoid collision with AIX LPP

* Fri Feb 07 2020 Michael Wilson <michael.a.wilson@atos.net> - 8.6.8-2
- Rebuild on laurel2 for expect 5.45.4
-   Rebuild expect required for dejagnu configure/build of new version

* Thu May 24 2018 Tony Reix <tony.reix@bull.net> 8.6.8-1
- Initial port on AIX 6.1

* Wed Sep 20 2017 Pascal Oliva <pascal.olvia@atos.net> 8.6.6-3
- Remove build opton bmaxdata in 64-bit mode

* Thu Jan 05 2017 Tony Reix <tony.reix@bull.net> 8.6.6-2
- Initial port on AIX 6.1

* Wed Jan 04 2017 Tony Reix <tony.reix@bull.net> 8.6.4-5
- Create only 1 libtclstubX.Y.a library .

* Tue Dec 06 2016 Tony Reix <tony.reix@bull.net> 8.6.4-4
- Change lib%{name}%{majorver}.a to: lib%{name}.a & symlink lib%{name}%{majorver}.a
- Add compatibility for: libtcl8.5.a(libtcl8.5.so) is needed by postgresql-pltcl-9.6.0-2

* Mon Dec 05 2016 Tony Reix <tony.reix@bull.net> 8.6.4-3
- Manage compatibility with version 8.5 .
- Fix issue with libtclstub appearing in tcl RPM in addition to tcl-devel RPM.
- Change tclsh default to 64bit
- Add symlink from /opt/freeware/lib/libtcl...a to /opt/freeware/lib64 .

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
