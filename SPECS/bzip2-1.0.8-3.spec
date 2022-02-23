%bcond_without dotests

Summary: A file compression utility
Name: bzip2
Version: 1.0.8
Release: 3
License: BSD
Group: Applications/File
URL: https://sourceware.org/bzip2/
Source0: https://sourceware.org/pub/bzip2/%{name}-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

#Source1: %{name}-Makefile-aix
#Patch1: %{name}-1.0.8-aix.patch
Patch2: bzip2-1.0.8-Makefile-so.patch

Requires: libgcc >= 8.4.0

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Header files developing apps which will use bzip2
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files of bzip2 functions, for developing apps which will
use the library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q 

#%patch1 -p0
#cp %{SOURCE1} Makefile-aix

%patch2 -p1 -b .Makefile_so

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# don't allow -I/opt/freeware/include
export CFLAGS="-qmaxmem=16384 -DSYSV -D_AIX -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I."

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"


build_bzip2 () {
	set -x
	gmake -f Makefile-libbz2_so CC="$CC $LDFLAGS" AR="$AR"
	gmake CC="$CC" AR="$AR" LDFLAGS="$LDFLAGS"
	ln -s libbz2.so.1.0 libbz2.so.1
	# Contains static lib
	rm libbz2.a
	$AR qc libbz2.a libbz2.so.1
	
	# make -f Makefile-aix
	# 
	# /usr/vac/bin/CreateExportList -X64 libbz2.exp libbz2.a
	# ${CC} -shared libbz2.a -o libbz2.so.1 -Wl,-bE:libbz2.exp
	# rm -f libbz2.exp
	# ${AR} -rv tmp_libbz2.a libbz2.so.1
	# 
	# mv tmp_libbz2.a libbz2.a
}

# first build the 64-bit version
cd 64bit 

export CC="gcc -maix64"
export OBJECT_MODE=64
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
build_bzip2

# now build the 32-bit version
cd ../32bit

export CC="gcc -maix32"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_bzip2
# Add 64 bits
$AR qc libbz2.a ../64bit/libbz2.so.1

#make CC="${CC}" CFLAGS="-O2 -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES" LDFLAGS="-Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib" \
#     %{?_smp_mflags} all


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install CFLAGS="-maix64" LDFLAGS="$LDFLAGS"

mv $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}64

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install LDFLAGS="$LDFLAGS"

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)

(
	cd ${RPM_BUILD_ROOT}/%{_libdir}64
	ln -sf ../lib/libbz2.a .
)

# These binaries are just link
# Create it correctly (by defaut, use build root)
(
        cd ${RPM_BUILD_ROOT}/%{_bindir}
        ln -sf bzdiff_32 bzcmp_32
        ln -sf bzdiff_64 bzcmp_64
        ln -sf bzgrep_32 bzegrep_32
        ln -sf bzgrep_64 bzegrep_64
        ln -sf bzgrep_32 bzfgrep_32
        ln -sf bzgrep_64 bzfgrep_64
        ln -sf bzmore_32 bzless_32
        ln -sf bzmore_64 bzless_64
)

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/CHANGES 32bit/README 
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}64/*.a
%{_mandir}/man?/*

%files devel
%defattr(-,root,system,-)
%docdir /opt/freeware/doc/bzip2-1.0.6
%doc 32bit/manual.html 32bit/manual.pdf
%{_includedir}/*


%changelog
* Fri Oct 09 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.0.8-3
- Update to 1.0.8

* Fri Oct 09 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0.8-2
- Port on Bullfreeware
- Use upstream Makefile
- Create lib without CreateExportList
- Provide all binaries
- Add %check section
- Correct URL
- Add link for bzless, bzegrep, bzfgrep and bzcmp

* Wed Sep 4 2019 Baanu Tumma <btumma15@in.ibm.com> - 1.0.8-1
- Update to latest version to fix CVE-2019-12900 

* Mon Jan 1 2018 Sangamesh Mallayya <smallayy@in.ibm.com> 1.0.6-3
- Rebuilt to ship the original wrapper scripts.
- Some commands are shipped as wrapper script on top of gzip command to pass -d option.
- Rebuilt with -DLARGE_FILE support option.

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.0.6-2
- Initial port on Aix6.1

* Fri Jun 10 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.0.6
- Update to 1.0.6

* Fri Jun 4 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.0.5
- Update to 1.0.5

* Tue Mar 08 2005 David Clissold <cliss@austin.ibm.com> 1.0.2-3
- Clean up; build 64-bit libbz.a member

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri Apr 19 2002 David Clissold <cliss@austin.ibm.com>
- Update to version 1.0.2.

* Thu Mar 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Build both 32- and 64-bit libraries

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI
