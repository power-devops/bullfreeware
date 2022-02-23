%define _libdir64 %{_prefix}/lib64

Summary:	Automated text file generator
Name:		autogen
Version:	5.12
Release:	2
# Some files are licensed under GPLv2+.
# We redistribute them under GPLv3+.
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/autogen/
Source0:	ftp://ftp.gnu.org/gnu/autogen/rel5.12/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	guile-devel < 2
BuildRequires:	libtool
BuildRequires:	libxml2-devel

Requires:	guile < 2

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

%package libopts
Summary:	Automated option processing library based on %{name}
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser consisting of a set of
AutoGen templates and a run time library that nearly eliminates the hassle of
parsing and documenting command line options.

%package libopts-devel
Summary:	Development files for libopts
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		Development/Libraries

Requires:	automake
Requires:	%{name}-libopts = %{version}-%{release}
Requires:	pkgconfig

%description libopts-devel
This package contains development files for libopts.

%prep
%setup -q -n %{name}-%{version}
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)

%build
#export LDFLAGS="-lguile"

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export STRIP="i/usr/bin/strip -X64"

export CC="/usr/vac/bin/xlc -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
export CXX="/usr/vacpp/bin/xlC -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "

#first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export M4=/usr/linux/bin/m4
CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} 

gmake #%{?_smp_mflags}

( gmake -k check || true )


cd ../32bit
# now build the 32-bit version

export OBJECT_MODE=32
export M4=/usr/linux/bin/m4
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"
export STRIP="/usr/bin/strip -X32"

export CC="/usr/vac/bin/xlc  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX="/usr/vacpp/bin/xlC  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} 

gmake #%{?_smp_mflags}

( gmake -k check || true )


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake install INSTALL="/opt/freeware/%{__install} -p" DESTDIR=$RPM_BUILD_ROOT


cd ../32bit
gmake install INSTALL="/opt/freeware/%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libopts.a ${RPM_BUILD_ROOT}%{_libdir64}/libopts.so*

%clean
/usr/bin/rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/%{name}.info %{_prefix}/share/info/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_prefix}/share/info/%{name}.info \
  %{_prefix}/share/info/dir >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc 32bit/AUTHORS
%doc 32bit/ChangeLog
%doc 32bit/COPYING
%doc 32bit/NEWS
%doc 32bit/README
%doc 32bit/THANKS
%doc 32bit/pkg/libopts/COPYING.gplv3

%{_bindir}/columns
%{_bindir}/getdefs
%{_bindir}/%{name}
%{_bindir}/xml2ag
%{_prefix}/share/info/autogen.info
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files libopts
%defattr(-,root,root,-)
%doc 32bit/pkg/libopts/COPYING.mbsd
%doc 32bit/pkg/libopts/COPYING.lgplv3
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so*
%{_libdir64}/*.so*

%files libopts-devel
%defattr(-,root,root,-)
%{_bindir}/autoopts-config
%{_datadir}/aclocal/autoopts.m4
#%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_datadir}/pkgconfig/autoopts.pc

%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h

%changelog
* Fri Sep 02 2016 Tony Reix - <tony.reix@atos.net> - 5.12-2
- make --> gmake
- /opt/freeware/bin/install !!  for -p option.
- Add  gmake -k check
- Add BuildRequires and Requires on guile version < 2 . Version 1.8.8 works.

* Tue Sep 29 2015 Pascal OLIVA - <pascal.oliva@atos.net>  - 5.12-1
- Porting for AIX
