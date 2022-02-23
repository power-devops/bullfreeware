Summary: 	LZMA utils
Name: 		lzma
Version: 	4.32.7
Release: 	1
License: 	GPLv2+
Group:		Applications/File
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-aix.patch
URL:		http://tukaani.org/%{name}/
BuildRoot: 	/var/tmp/%{name}-%{version}-%{release}-root
Requires:	%{name}-libs = %{version}-%{release}

%description
LZMA provides very high compression ratio and fast decompression. The
core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual
LZMA encoder/decoder. LZMA utils add a few scripts which provide
gzip-like command line interface and a couple of other LZMA related
tools. 


%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding LZMA compression.


%package 	devel
Summary:	Devel libraries & headers for liblzmadec
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}

%description  devel
Devel libraries and headers for liblzmadec.


%prep
%setup -q
%patch0 -p1 -b .aix

%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

export CC="/usr/vac/bin/xlc_r -qlanglvl=extc99"
export CXX="/usr/vacpp/bin/xlC_r -qlanglvl=extc99"

export CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

make

cp src/liblzmadec/.libs/liblzmadec.so.0 .
make distclean

# now build the 32-bit version
export OBJECT_MODE="32"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X32_64 -q src/liblzmadec/.libs/liblzmadec.a ./liblzmadec.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* »||

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
%doc README THANKS COPYING.* ChangeLog AUTHORS
%{_bindir}/*
%{_mandir}/man1/*
/usr/bin/*


%files libs
%defattr(-,root,system,-)
%doc COPYING.*
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Sep 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 4.32.7-1
- Initial port on Aix6.1

