# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# compiler default gcc
# To use gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}

%define major_version 8
%define minor_version 6
%define bugfix_version 10

%define majorver %{major_version}.%{minor_version}

Summary: The graphical toolkit for the Tcl scripting language
Name: tk
Version: %{major_version}.%{minor_version}.%{bugfix_version}
Release: 3
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net

Source0: ftp://ftp.tcl.tk/pub/tcl/tcl8_6/%{name}%{version}-src.tar.gz

# Taken from Tk 8.5.19
Source1: libtk8.5.so-aix32
Source2: libtk8.5.so-aix64
# Taken from Tk 8.6.10-2
Source3: libtk8.6.so-aix32
Source4: libtk8.6.so-aix64

Source100: %{name}-%{version}-%{release}.build.log

# Patches from Fedora 32
Patch1: tk-8.6.10-make.patch
# Patch2: tk-8.6.10-conf.patch
Patch3: tk-8.6.7-no-fonts-fix.patch
# https://core.tcl-lang.org/tk/tktview/dccd82bdc70dc25bb6709a6c14880a92104dda43
Patch4: tk-8.6.10-font-sizes-fix.patch

Patch100: tk-8.6.10-configure.patch

# Following is needed, but may cause problems to install if AIX LPP conflict
BuildRequires: tcl-devel = %{version}
BuildRequires: tcl-static = %{version}
BuildRequires: fontconfig-devel >= 2.11.95
# AIX uses an LPP version of X11
# BuildRequires: libX11-devel
BuildRequires: libXft-devel >= 2.3.2
# The AIX find command does not work as expected using findutils find
BuildRequires: findutils sed
Requires: tcl = %{version}
Requires: fontconfig >= 2.11.95
Requires: libXft-devel >= 2.3.2
## Following included due to a dependency in command wish TBC
#Provides: libtk8.6.a(libtk8.6.so) 

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
Requires: %{name}-static = %{version}-%{release}
Requires: tcl-devel = %{version}
# The AIX find command does not work as expected using findutils find
# Requires: libX11-devel
Requires: libXft-devel

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


%package static
Summary: Tk graphical toolkit development files
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel = %{version}

%description static
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the libtkstub static library for tk development.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package oldlibcompat
Summary: Old Tk libraries provided for compatibility purpose only
Group: Development/Languages

%description oldlibcompat
The package contains libtk version 5 and version 6 built before September 2020.
These libraries are made with dangerous flags and are provided only for compatibility.


%prep
echo DISPLAY is set to  "$DISPLAY"
echo ENV is
env

%setup -q -n %{name}%{version}

# Patches from Fedora 32
%patch1 -p1 -b .make
# %patch2 -p1 -b .conf
%patch3 -p1 -b .no-fonts-fix
%patch4 -p1 -b .font-sizes-fix
%patch100 -p1 -b .bexpall

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

echo DISPLAY is set to  "$DISPLAY"
echo ENV is
env



# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar"
export NM="/usr/bin/nm -X32_64"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

# prevent "out of stack space" error
export CFLAGS="-O2 -DTCL_NO_STACK_CHECK"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"



# export LDFLAGS32="-L/opt/freeware/lib -Xlinker -bmaxdata:0x80000000"
export LDFLAGS32="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

# export LDFLAGS64="-L/opt/freeware/lib"
export LDFLAGS64="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

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

build_tk () {
    set -x
    # export DISPLAY="localhost:13.0"

    ./configure \
        --prefix=%{_prefix} \
        --libdir=$1 \
        --enable-shared --disable-static \
        --enable-threads \
        --enable-xft \
        --x-libraries=/opt/freeware/lib \
        --with-x \
        --with-tcl=$1 \
        $2

# TODO old stuff, remove if OK
#sed -e "s|TCL_LIB_FLAG.*=.*|TCL_LIB_FLAG=-ltcl%{majorver}|"                      Makefile     > Makefile.tmp
#sed -e "s|TCL_LIB_SPEC.*=.*|TCL_LIB_SPEC=-L /opt/freeware/lib -ltcl%{majorver}|" Makefile.tmp > Makefile.tmp2

# W/A for missing libtk8.6.a in shared lib build - TODO correction to configure
#   This adds an ar command to build the tk lib for "gcc -ltk -o wish"
#   otherwise build links with system installed libtk and autobuild breaks

#sed -e "/LD_SEARCH_FLAGS}$/s|$|\n      /usr/bin/ar cr libtk%{majorver}.a libtk%{majorver}.so|"                      Makefile.tmp2 > Makefile


#sed -e "s|-L\/opt\/freeware\/lib|-L\/opt\/freeware\/lib64|g" config.status >  config.status.tmp
#mv config.status.tmp config.status
#chmod 755 config.status
#./config.status

    gmake %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver} libtk.so.%{majorver}
    /usr/bin/ar -X32_64 -qc libtk.a libtk.so.%{majorver}
    gmake %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver}
}

# first build the 64-bit version
cd 64bit/unix

# Force using Xft from opt/freeware, as versions from /usr/lib is too old
# 64bit version. libtclstubX.Y.a contains either 32 OR 64bit .o files

export LIBS="/opt/freeware/lib/libXft.a -L/opt/freeware/lib64 -ltclstub"
export LDFLAGS="${LDFLAGS64}"
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

build_tk %{_libdir64} --enable-64bit

cd ../..


# now build the 32-bit version
cd 32bit/unix

# Force using Xft from opt/freeware, as versions from /usr/lib is too old
# 32bit version. libtclstubX.Y.a contains either 32 OR 64bit .o files
export LIBS="/opt/freeware/lib/libXft.a -L/opt/freeware/lib -ltclstub"
export LDFLAGS="${LDFLAGS32}"
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

build_tk %{_libdir}

cd ..
# Now under 32bit directory


# TODO old stuff, remove if OK
# # libtkX.Y.a
# rm    -f      lib%{name}.a
# rm    -f      lib%{name}%{majorver}.a
# ${AR} -X32 -q lib%{name}.a                     unix/lib%{name}%{majorver}.so
# ${AR} -X64 -q lib%{name}.a            ../64bit/unix/lib%{name}%{majorver}.so
# ln -sf        lib%{name}.a                          lib%{name}%{majorver}.a 
# slibclean
# strip -e -X32                                  unix/lib%{name}%{majorver}.so
# strip -e -X64                         ../64bit/unix/lib%{name}%{majorver}.so
# 
# 
# # Compatibility with 8.5 version
# cp %{SOURCE5}                                  lib%{name}8.5.so
# /usr/bin/strip -X32 -e                         lib%{name}8.5.so
# ${AR}          -X32 -q lib%{name}.a            lib%{name}8.5.so
# mv                                             lib%{name}8.5.so          unix/
# cp %{SOURCE6}                                  lib%{name}8.5.so
# /usr/bin/strip -X64 -e                         lib%{name}8.5.so
# ${AR}          -X64 -q lib%{name}.a            lib%{name}8.5.so
# mv                                             lib%{name}8.5.so ../64bit/unix/
# 
# 
# ${AR} -X32 tv lib%{name}.a
# ${AR} -X64 tv lib%{name}.a
# 
# 
# # libtkstubX.Y.a
# mkdir ../tkstub
# cd ../tkstub
# ${AR} -X32 -xv ../32bit/unix/lib%{name}stub%{majorver}.a
# cd -
# rm    -f      lib%{name}stub.a
# rm    -f      lib%{name}stub%{majorver}.a
# ${AR} -X32 -q lib%{name}stub.a                 ../tkstub/*
# cd ../tkstub
# rm -f *
# ${AR} -X64 -xv ../64bit/unix/lib%{name}stub%{majorver}.a
# cd -
# ${AR} -X64 -q lib%{name}stub.a                 ../tkstub/*
# ln -sf        lib%{name}stub.a                 lib%{name}stub%{majorver}.a
# 
# ${AR} -X32 tv lib%{name}stub.a
# ${AR} -X64 tv lib%{name}stub.a


%check
# Running "gmake test" requires an X display
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# TODO: automatize this
# export DISPLAY="localhost:13.0"
export DISPLAY="localhost:16.0"
echo DISPLAY is set to  "$DISPLAY"
if [ X"$DISPLAY" = "X" ]; then
  # Cannot test without a valide DISPLAY
  echo "*** Skipping tests"
  exit 0
fi


# Test the 64 bit version
cd 64bit/unix

(LIBPATH=.:../../32bit:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib gmake -k test || true)

cd ../..

# Test the 32 bit version
cd 32bit/unix

(LIBPATH=.:..:/opt/freeware/lib:/usr/lib:/lib gmake -k test || true)


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar"
export RM="/usr/bin/rm -f"

cd 64bit/unix
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver}_64
cp libtk.a ${RPM_BUILD_ROOT}%{_libdir64}
cd ../..

cd 32bit/unix
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver}_32
cp libtk.a ${RPM_BUILD_ROOT}%{_libdir}


cd ../..

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

ln -sf wish%{majorver}_64            ${RPM_BUILD_ROOT}%{_bindir}/wish
ln -sf wish%{majorver}_32            ${RPM_BUILD_ROOT}%{_bindir}/wish_32
ln -sf wish%{majorver}_64            ${RPM_BUILD_ROOT}%{_bindir}/wish_64

#ln -sf lib%{name}%{majorver}.so      ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
#ln -sf lib%{name}%{majorver}.so      ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

# Compatibility with 8.5 version
#cp                  lib%{name}8.5.so ${RPM_BUILD_ROOT}%{_libdir}/
#cp ../../64bit/unix/lib%{name}8.5.so ${RPM_BUILD_ROOT}%{_libdir64}/

#cd ..
## Now under 32bit directory

# Put current main lib for delivery
#cp              lib%{name}.a                  ${RPM_BUILD_ROOT}%{_libdir}
#cp              lib%{name}stub.a              ${RPM_BUILD_ROOT}%{_libdir}

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f libtk.so.*
    ${AR} -x -X64 libtk.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q -X64 libtk.a ${RPM_BUILD_ROOT}%{_libdir64}/libtk.so.%{majorver}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libtk.so.%{majorver}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/libtk.a libtk.a
)

# # TODO 
# # Old stuff again, remove if OK
# (
#   cd       ${RPM_BUILD_ROOT}%{_libdir}
#   ln -sf /opt/freeware/lib/lib%{name}.a       lib%{name}%{majorver}.a
#   ln -sf /opt/freeware/lib/lib%{name}stub.a   lib%{name}stub%{majorver}.a
# 
#   ${AR} -X32 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a
#   ${AR} -X64 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a
# 
#   ${AR} -X32 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}stub.a
#   ${AR} -X64 tv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}stub.a
# )
# 
# # 64bit symlink for the main archive
# (
#   cd       ${RPM_BUILD_ROOT}%{_libdir64}
#   ln -sf ../lib/lib%{name}.a                  lib%{name}.a
#   ln -sf ../lib/lib%{name}%{majorver}.a       lib%{name}%{majorver}.a
#   ln -sf ../lib/lib%{name}stub%{majorver}.a   lib%{name}stub%{majorver}.a
# )
# 
# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin include lib lib64
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )


# Still under BUILD/tk8.6.10/32bit directory

# Taken from Fedora - deliver tcl internal lib and headers

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/generic/ttk
mkdir -p %{buildroot}/%{_includedir}/%{name}-private/unix

# Following find command does not work as expected using AIX find
cd 64bit
/opt/freeware/bin/find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
cd ..

(
  cd %{buildroot}/%{_includedir}
  for i in *.h ; do
    [ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
  done
)

# remove buildroot traces
# Following sed -i command does not work as expected using AIX sed
cd 32bit
/opt/freeware/bin/sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh
cd ../64bit
/opt/freeware/bin/sed -i -e "s|$PWD/unix|%{_libdir64}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir64}/%{name}Config.sh
cd ..


# Old libs for compatibility
(
  cd %{buildroot}/%{_libdir}
  cp %{SOURCE1} libtk8.5.so
  cp %{SOURCE3} libtk8.6.so
  /usr/bin/strip -X32 -e                     libtk8.5.so
  /usr/bin/strip -X32 -e                     libtk8.6.so

  cd %{buildroot}/%{_libdir64}
  cp %{SOURCE2} libtk8.5.so
  cp %{SOURCE4} libtk8.6.so
  /usr/bin/strip -X64 -e                     libtk8.5.so
  /usr/bin/strip -X64 -e                     libtk8.6.so

  cd %{buildroot}/%{_libdir}
  /usr/bin/ar    -X32 -q libtk8.5.a          libtk8.5.so
  /usr/bin/ar    -X32 -q libtk8.6.a          libtk8.6.so
  /usr/bin/ar    -X64 -q libtk8.5.a ../lib64/libtk8.5.so
  /usr/bin/ar    -X64 -q libtk8.6.a ../lib64/libtk8.6.so

  ln -sf libtk8.6.so libtk.so

  cd %{buildroot}/%{_libdir64}
  ln -sf ../lib/libtk8.5.a .
  ln -sf ../lib/libtk8.6.a

  ln -sf libtk8.6.so libtk.so
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/README.md 32bit/changes 32bit/license.terms
%{_bindir}/wish*
%{_libdir}/lib%{name}.a
#%{_libdir}/lib%{name}%{majorver}.a
#%{_libdir}/lib*.so*
%{_libdir64}/lib%{name}.a
#%{_libdir64}/lib%{name}%{majorver}.a
#%{_libdir64}/lib*.so*
%dir %{_libdir}/%{name}%{majorver}
%dir %{_libdir64}/%{name}%{majorver}
%{_libdir}/%{name}%{majorver}/*
%{_libdir64}/%{name}%{majorver}/*
%dir %{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}%{majorver}/*
%exclude %{_datadir}/%{name}%{majorver}/tkAppInit.c
%{_mandir}/man1/*
%{_mandir}/mann/*


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_libdir}/pkgconfig/tk.pc
%{_mandir}/man3/*
%{_datadir}/%{name}%{majorver}/tkAppInit.c


%files static
%defattr(-,root,system,-)
%{_libdir}/libtkstub*.a
%{_libdir64}/libtkstub*.a


%files oldlibcompat
%defattr(-,root,system,-)
%{_libdir}/libtk8.5.a
%{_libdir}/libtk8.5.so
%{_libdir}/libtk8.6.a
%{_libdir}/libtk8.6.so
%{_libdir}/libtk.so
%{_libdir64}/libtk8.5.a
%{_libdir64}/libtk8.5.so
%{_libdir64}/libtk8.6.a
%{_libdir64}/libtk8.6.so
%{_libdir64}/libtk.so


%changelog
* Fri Nov 06 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 8.6.10-3
- Remove bexpall flag
  So, compatibility with older version is broken
- Clean URL and Source
- Use %{major_version} and %{minor_version}
- Stop provinding libtk.so
- Provide old compatibility library libtk8.{5,6}.{a,so} in a separate subpackage

* Wed Feb 19 2020 Michael Wilson <michael.a.wilson@atos.net> 8.6.10-2
- Correction to 64 bit tkConfig.sh
- Change default wish to 64 bit

* Wed Feb 19 2020 Michael Wilson <michael.a.wilson@atos.net> 8.6.10-1
- Update to 8.6.10 based on Fedora 32
- Include internal header files
- Include Provides libtk8.6.a(libtk8.6.so)
- Add W/A to build libtk8.6.a to link wish and test binaries and execute tests
- Add -blibpath
- Move libtkstub static library to new RPM tk-static
- Add BuildRequires on new RPM tcl-static
- Symbolic links in /usr removed to avoid collision with AIX LPP

* Thu May 24 2018 Tony Reix <tony.reix@bull.net> 8.6.8-1
- Initial port on AIX 6.1

* Wed Sep 20 2017 Pascal Oliva <pascal.olvia@atos.net> 8.6.6-5
- Remove build opton bmaxdata in 64-bit mode

* Tue Feb 21 2017 Tony Reix <tony.reix@bull.net> 8.6.6-4
- Add compatibility with tk 8.5 (.so files)

* Fri Jan 06 2017 Tony Reix <tony.reix@bull.net> 8.6.6-3
- Add .log file

* Fri Jan 06 2017 Tony Reix <tony.reix@bull.net> 8.6.6-2
- Initial port on AIX 6.1

* Wed Jan 04 2017 Tony Reix <tony.reix@bull.net> 8.6.4-2
- Fix issues with 32/64bit and libtclstubX.Y.a .
- No more deliver libtkstubX.Y.a in tk package.
- No more deliver libtkX.Y.a in tk-devel package.
- Create only 1 libtkstubX.Y.a library for both 32 & 64bit.

* Mon Dec 05 2016 Tony Reix <tony.reix@bull.net> 8.6.4-1
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
