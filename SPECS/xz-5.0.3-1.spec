Summary:	LZMA compression utilities
Name:		xz
Version:	5.0.3
Release:	1
License:	LGPLv2+
Group:		Applications/File
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-aixconf.patch
URL:		http://tukaani.org/%{name}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	make, gettext, pkg-config, bash
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bash, gettext

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:		System Environment/Libraries
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkg-config

%description  devel
Devel libraries and headers for liblzma.

%prep
%setup -q
%patch0 -p1 -b .aixconf

%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"


export CFLAGS="$CFLAGS -qlanglvl=extc99 -qcpluscmt -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

cp src/liblzma/.libs/liblzma.so.5 .
gmake distclean

# now build the 32-bit version
export OBJECT_MODE="32"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X32_64 -q src/liblzma/.libs/liblzma.a ./liblzma.so.5

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -rf ${RPM_BUILD_ROOT}%{_docdir}/%{name}

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
%doc AUTHORS README THANKS COPYING.* ChangeLog 
%{_bindir}/*xz*
%{_mandir}/man1/*xz*
/usr/bin/*xz*


%files libs
%defattr(-,root,system,-)
%doc COPYING.*
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc doc/faq.txt doc/lzma-file-format.txt
%doc doc/xz-file-format.txt doc/history.txt
%{_includedir}/lzma*
%{_libdir}/*.la
%{_libdir}/pkgconfig/liblzma.pc
/usr/include/*
/usr/lib/*.la

%changelog
* Fri Feb 10 2012 Patricia Cugny <patricia.cugny@bull.net> - 5.0.3-1
- initial version for AIX 6.1
