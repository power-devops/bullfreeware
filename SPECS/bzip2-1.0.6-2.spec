Summary: A file compression utility
Name: bzip2
Version: 1.0.6
Release: 2
License: BSD
Group: Applications/File
URL: http://www.bzip.org/
Source0: http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Source1: %{name}-Makefile-aix
Patch0: %{name}-%{version}-bzip2recover.patch
Patch1: %{name}-%{version}-aix.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

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
%patch0 -p 1
%patch1
cp %{SOURCE1} Makefile-aix


%build
# don't allow -I/opt/freeware/include
export CFLAGS="-qmaxmem=16384 -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I."

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"

# first build the 64-bit version
CC_prev="$CC"
export CC="$CC -q64"
make -f Makefile-aix

/usr/vac/bin/CreateExportList -X64 libbz2.exp libbz2.a
${CC} -qmkshrobj libbz2.a -o libbz2.so.1 -bE:libbz2.exp
rm -f libbz2.exp
${AR} -rv tmp_libbz2.a libbz2.so.1

make -f Makefile-aix clean

# now build the 32-bit version
export CC="$CC_prev"
make -f Makefile-aix

/usr/vac/bin/CreateExportList -X32 libbz2.exp libbz2.a
${CC} -qmkshrobj libbz2.a -o libbz2.so.1 -bE:libbz2.exp
rm -f libbz2.exp
${AR} -q tmp_libbz2.a libbz2.so.1

mv tmp_libbz2.a libbz2.a

make CC="${CC}" CFLAGS="-O2 -D_FILE_OFFSET_BITS=64" \
     %{?_smp_mflags} all


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}/
mv $RPM_BUILD_ROOT/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1/
mv $RPM_BUILD_ROOT/lib/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/include/* $RPM_BUILD_ROOT%{_includedir}

rm -f $RPM_BUILD_ROOT%{_bindir}/bzcmp
rm -f $RPM_BUILD_ROOT%{_bindir}/bzegrep
rm -f $RPM_BUILD_ROOT%{_bindir}/bzfgrep
rm -f $RPM_BUILD_ROOT%{_bindir}/bzless

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}%{_bindir}
ln -s bzdiff bzcmp
ln -s bzgrep bzegrep
ln -s bzgrep bzfgrep
ln -s bzmore bzless
cd -

( cd $RPM_BUILD_ROOT
  for dir in bin lib include
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc LICENSE CHANGES README 
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man?/*
/usr/bin/*
/usr/lib/*


%files devel
%defattr(-,root,system,-)
%doc manual.html manual.pdf
%{_includedir}/*
/usr/include/*


%changelog
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
