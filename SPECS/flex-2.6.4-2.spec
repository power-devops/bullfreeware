%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.6.4
Release: 2
License: BSD
Group: Development/Tools
URL: http://flex.sourceforge.net/
Source0: %{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log
Patch0: %{name}-%{version}-aix.patch

BuildRequires: gettext-devel >= 0.19.7
BuildRequires: make >= 4.1, texinfo
# We must use the same version during build and use.
BuildRequires: m4 = 1.4.18
Requires: m4 = 1.4.18
# Require itself to build on 64 bit. To bootstrap,
# Compile it on 64 only, and use this executable to produces
# 32 and 64 bitsz version.
# Compilation on 32 and 64 seems different...
BuildRequires: flex
BuildRequires: bison
# Configure searches the version and want the EXACT 1.15
BuildRequires: automake = 1.15
%if %{with dotests}
BuildRequires: sed
%endif
Requires: /sbin/install-info, info
Requires: gettext >= 0.19.7
Requires: libgcc >= 6.3.0-1


%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.


%prep
%setup -q
%patch0
find . -exec touch {} \;
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export PATH=/opt/freeware/bin:$PATH

# first build the 64-bit version
export CC="gcc -maix64 "
export CXX="g++ -maix64 "
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib  -Wl,-bnoipath"
cd 64bit
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-static

gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32 -D_LARGE_FILES "
export CXX="g++ -maix32 -D_LARGE_FILES "
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -Wl,-bnoipath"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

gmake %{?_smp_mflags}


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for fic in * ; do
    mv -f ${fic} ${fic}_64
#     ln -sf "$fic"_64 $fic
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
    mv $fic "$fic"_32
    ln -sf "$fic"_64 $fic
    done
) 
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/%{name}.info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  rm *.la
  ar -x  -X64 ../lib64/libfl.a libfl.so.2
  ar -qc -X64          libfl.a libfl.so.2
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  rm *.la
  ln -sf      ../lib/libfl.a   libfl.a
)

%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
(gmake -k check %{?_smp_mflags} || true)
cd ../32bit
sed -i 's|#define malloc rpl_malloc|/* #undef malloc */|' src/config.h
sed -i 's|#define realloc rpl_realloc|/* #undef realloc */|' src/config.h
export OBJECT_MODE=32
(gmake -k check %{?_smp_mflags} || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/%{name}.info.gz --dir-file=%{_infodir}/dir ||:


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir ||:
fi


%files
%defattr(-,root,system)
%doc 64bit/COPYING 64bit/NEWS 64bit/README.md
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_includedir}/*
%{_infodir}/*
%{_datadir}/locale/*/*/*


%changelog
* Mon Mar 02 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.6.4-2
- Add a BuildRequires on itself


* Mon Jul 30 2018 Harshita Jain <harjain9@in.ibm.com> - 2.6.4-1
- updated to version 2.6.4

* Fri Mar 16 2012 Gerard Visiedo <gerard.visiedo@bull.net> -- 2.5.35-2
-  Add lib64 libraries

* Tue May 25 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net>
- Update to version 2.5.35

* Thu Jul 10 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM VAC compiler for better size and performance.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Mar 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler

* Wed Feb 28 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Fix minor error in install section of previous patch

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI
