Name:           jbigkit
Version:        2.0
Release:        3
Summary:        JBIG1 lossless image compression tools

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:        http://www.cl.cam.ac.uk/~mgk25/download/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-aix.patch
BuildRoot:      /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires:  make
Requires:       %{name}-libs = %{version}-%{release}

%description
The jbigkit package contains tools for converting between PBM and JBIG1
formats.


%package libs
Summary:        JBIG1 lossless image compression library
Group:          Applications/Multimedia

%description libs
JBIG-KIT provides a portable library of compression and decompression
functions with a documented interface that you can include very easily
into your image or document processing software. In addition, JBIG-KIT
provides ready-to-use compression and decompression programs with a
simple command line interface (similar to the converters found in
netpbm).

JBIG-KIT implements the specification:
    ISO/IEC 11544:1993 and ITU-T Recommendation T.82(1993):
     Information technology — Coded representation of picture and audio
     information — Progressive bi-level image compression 

which is commonly referred to as the “JBIG1 standard”


%package devel
Summary:        JBIG1 lossless image compression library -- development files
Group:          Applications/Multimedia
Requires:       %{name}-libs = %{version}-%{release}

%description devel
The jbigkit-devel package contains files needed for development using 
the JBIG-KIT image compression library.


%prep
%setup -q -n jbigkit
%patch0

%build
export AR="/usr/bin/ar -X32_64"

cd libjbig

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=64
export LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib"

make 
make libjbig85.a
/usr/vac/bin/CreateExportList -X64 libjbig.exp   libjbig.a
/usr/vac/bin/CreateExportList -X64 libjbig85.exp libjbig85.a
${CC} -qmkshrobj libjbig.a   -o shr64-libjbig.so   -bE:libjbig.exp
${CC} -qmkshrobj libjbig85.a -o shr64-libjbig85.so -bE:libjbig85.exp
rm -f libjbig.exp libjbig85.exp

make clean
rm -f libjbig.a libjbig85.a *.o

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export OBJECT_MODE=32
export LIBPATH="%{_libdir}:/usr/lib"

make
make libjbig85.a
/usr/vac/bin/CreateExportList -X32 libjbig.exp   libjbig.a
/usr/vac/bin/CreateExportList -X32 libjbig85.exp libjbig85.a

${CC} -qmkshrobj libjbig.a -o shr.o -bE:libjbig.exp
rm -f libjbig.exp libjbig.a
${AR} -rv libjbig.a shr.o
rm -f shr.o

${CC} -qmkshrobj libjbig85.a -o shr.o -bE:libjbig85.exp
rm -f libjbig85.exp libjbig85.a
${AR} -rv libjbig85.a shr.o
rm -f shr.o


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
mv shr64-libjbig.so shr64.o
${AR} -q libjbig.a shr64.o
rm -f shr64.o

mv shr64-libjbig85.so shr64.o
${AR} -q libjbig85.a shr64.o
rm -f shr64.o

# now build the rest
export PATH=/opt/freeware/bin:$PATH
cd ..
make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1

cp libjbig/libjbig.a   ${RPM_BUILD_ROOT}%{_libdir}
cp libjbig/libjbig85.a ${RPM_BUILD_ROOT}%{_libdir}
chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/*

cp libjbig/jbig.h    ${RPM_BUILD_ROOT}%{_includedir}
cp libjbig/jbig85.h  ${RPM_BUILD_ROOT}%{_includedir}
cp libjbig/jbig_ar.h ${RPM_BUILD_ROOT}%{_includedir}
chmod 0644 ${RPM_BUILD_ROOT}%{_includedir}/*

cp pbmtools/???to???   ${RPM_BUILD_ROOT}%{_bindir}
cp pbmtools/???to???85 ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

cp pbmtools/*.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
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
%{_bindir}/*
%{_mandir}/man1/*
/usr/bin/*


%files libs
%defattr(-,root,system,-)
%doc COPYING ANNOUNCE TODO INSTALL CHANGES
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
/usr/include*


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.0-3
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Sep 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.0-1
- Initial port on Aix5.3

