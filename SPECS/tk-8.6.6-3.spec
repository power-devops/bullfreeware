# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# compiler default gcc
# To use gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}


%define majorver 8.6

Summary: The graphical toolkit for the Tcl scripting language
Name: tk
Version: %{majorver}.6
Release: 3
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net

Source0: http://download.sourceforge.net/tcl/%{name}%{version}-src.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: tcl-devel = %{version}
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: libXft-devel >= 2.1.14
Requires: tcl = %{version}
Requires: fontconfig >= 2.5.0
Requires: libXft >= 2.1.14

%define _libdir64 %{_prefix}/lib64

%description
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary: Tk graphical toolkit development files
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel = %{version}

%description devel
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the development files and man pages for tk.

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
export CFLAGS="               -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O2 -DTCL_NO_STACK_CHECK"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export LDFLAGS="-L/opt/freeware/lib"
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

# Force using Xft from opt/freeware, as versions from /usr/lib is too old
# 64bit version. libtclstubX.Y.a contains either 32 OR 64bit .o files
export LIBS="/opt/freeware/lib/libXft.a -L/opt/freeware/lib64 -ltclstub%{majorver} "

export OBJECT_MODE=64

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-64bit \
    --enable-shared --disable-static \
    --enable-threads \
    --enable-xft \
    --x-libraries=/opt/freeware/lib \
    --with-x \
    --with-tcl=%{_libdir64}

sed -e "s|TCL_LIB_FLAG.*=.*|TCL_LIB_FLAG=-ltcl%{majorver}|"                      Makefile     > Makefile.tmp
sed -e "s|TCL_LIB_SPEC.*=.*|TCL_LIB_SPEC=-L /opt/freeware/lib -ltcl%{majorver}|" Makefile.tmp > Makefile

#sed -e "s|-L\/opt\/freeware\/lib|-L\/opt\/freeware\/lib64|g" config.status >  config.status.tmp
#mv config.status.tmp config.status
#chmod 755 config.status
#./config.status

gmake %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver}

if [ "%{dotests}" == 1 ]
then
        (gmake -k test || true)
fi


cd ../..


# now build the 32-bit version
cd 32bit/unix

# Force using Xft from opt/freeware, as versions from /usr/lib is too old
# 32bit version. libtclstubX.Y.a contains either 32 OR 64bit .o files
export LIBS="/opt/freeware/lib/libXft.a -L/opt/freeware/lib -ltclstub%{majorver} "

export OBJECT_MODE=32

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static \
    --enable-threads \
    --enable-xft \
    --with-x \
    --with-tcl=%{_libdir}

sed -e "s|TCL_LIB_FLAG.*=.*|TCL_LIB_FLAG=-ltcl%{majorver}|"                      Makefile     > Makefile.tmp
sed -e "s|TCL_LIB_SPEC.*=.*|TCL_LIB_SPEC=-L /opt/freeware/lib -ltcl%{majorver}|" Makefile.tmp > Makefile

gmake %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver}

if [ "%{dotests}" == 1 ]
then
        (gmake -k test || true)
fi


cd ..
# Now under 32bit directory

# libtkX.Y.a
rm    -f      lib%{name}.a
rm    -f      lib%{name}%{majorver}.a
${AR} -X32 -q lib%{name}.a                     unix/lib%{name}%{majorver}.so
${AR} -X64 -q lib%{name}.a            ../64bit/unix/lib%{name}%{majorver}.so
ln -sf        lib%{name}.a                          lib%{name}%{majorver}.a
slibclean
strip -e -X32                                  unix/lib%{name}%{majorver}.so
strip -e -X64                         ../64bit/unix/lib%{name}%{majorver}.so

${AR} -X32 tv lib%{name}.a
${AR} -X64 tv lib%{name}.a


# libtkstubX.Y.a
mkdir ../tkstub
cd ../tkstub
${AR} -X32 -xv ../32bit/unix/lib%{name}stub%{majorver}.a
cd -
rm    -f      lib%{name}stub.a
rm    -f      lib%{name}stub%{majorver}.a
${AR} -X32 -q lib%{name}stub.a                 ../tkstub/*
cd ../tkstub
rm -f *
${AR} -X64 -xv ../64bit/unix/lib%{name}stub%{majorver}.a
cd -
${AR} -X64 -q lib%{name}stub.a                 ../tkstub/*
ln -sf        lib%{name}stub.a                 lib%{name}stub%{majorver}.a

${AR} -X32 tv lib%{name}stub.a
${AR} -X64 tv lib%{name}stub.a


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit/unix
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver}_64

cd ../..

cd 32bit/unix
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

ln -sf wish%{majorver}    ${RPM_BUILD_ROOT}%{_bindir}/wish
ln -sf wish%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/wish_64

ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

cd ..
# Now under 32bit directory

# Put current main lib for delivery
cp                       lib%{name}.a                  ${RPM_BUILD_ROOT}%{_libdir}
cp                       lib%{name}stub.a              ${RPM_BUILD_ROOT}%{_libdir}
cd                                                     ${RPM_BUILD_ROOT}%{_libdir}
ln -sf /opt/freeware/lib/lib%{name}.a                  lib%{name}%{majorver}.a
ln -sf /opt/freeware/lib/lib%{name}stub.a              lib%{name}stub%{majorver}.a

${AR} -X32 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a
${AR} -X64 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a

${AR} -X32 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}stub.a
${AR} -X64 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}stub.a

# 64bit symlink for the main archive
cd                                                     ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf /opt/freeware/lib/lib%{name}.a                  .
ln -sf /opt/freeware/lib/lib%{name}%{majorver}.a       .
ln -sf /opt/freeware/lib/lib%{name}stub%{majorver}.a   .

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
%{_bindir}/wish*
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}%{majorver}.a
%{_libdir}/lib*.so*
%{_libdir64}/lib%{name}.a
%{_libdir64}/lib%{name}%{majorver}.a
%{_libdir64}/lib*.so*
%dir %{_libdir}/%{name}%{majorver}
%dir %{_libdir64}/%{name}%{majorver}
%{_libdir}/%{name}%{majorver}/*
%{_libdir64}/%{name}%{majorver}/*
%dir %{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}%{majorver}/*
%{_mandir}/man1/*
%{_mandir}/mann/*
/usr/bin/wish*
/usr/lib/lib%{name}.a
/usr/lib/lib%{name}%{majorver}.a
/usr/lib/lib*.so*
/usr/lib64/lib*.so*


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/lib%{name}stub*.a
%{_libdir64}/lib%{name}stub*.a
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_mandir}/man3/*
/usr/include/*
/usr/lib/lib%{name}stub*.a
/usr/lib64/lib%{name}stub*.a


%changelog
* Fri Jan 06 2017 Tony Reix <tony.reix@bull.net> 8.6.6-3
- Add .log file

* Fri Jan 06 2017 Tony Reix <tony.reix@bull.net> 8.6.6-2
- Initial port on AIX 6.1

* Wed Jan 04 2017 Tony Reix <tony.reix@bull.net> 8.6.4-2
- Fix issues with 32/64bit and libtclstubX.Y.a .
- No more deliver libtkstubX.Y.a in tk package.
- No more deliver libtkX.Y.a in tk-devel package.
- Create only 1 libtkstubX.Y.a library for both 32 & 64bit.

* Thu Dec 05 2016 Tony Reix <tony.reix@bull.net> 8.6.4-1
- Initial port on AIX 6.1

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
