Name:          imake
Version:       1.0.5
Release:       1
Summary:       X.Org imake build tool
Group:         System/X11
URL:           http://x.org
Source:        ftp://x.org/pub/individual/util/imake-%{version}.tar.bz2
License:       MIT
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
## AUTOBUILDREQ-BEGIN
#BuildRequires: glibc-devel
#BuildRequires: xorg-cf-files
## AUTOBUILDREQ-END
#BuildRequires: xorg-proto-devel
#Requires:      xorg-cf-files >= 1.0.2

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
X.Org imake build tool.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--host=%{buildhost} \
	--target=%{buildhost} \
	--build=%{buildhost}

make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=${RPM_BUILD_ROOT} install

(
 cd $RPM_BUILD_ROOT
 for dir in bin 
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
%defattr(-,root,system)
%{_bindir}/ccmakedep
%{_bindir}/cleanlinks
%{_bindir}/imake
%{_bindir}/makeg
%{_bindir}/mergelib
%{_bindir}/mkdirhier
%{_bindir}/mkhtmlindex
%{_bindir}/revpath
%{_bindir}/xmkmf
/usr/bin/ccmakedep
/usr/bin/cleanlinks
/usr/bin/imake
/usr/bin/makeg
/usr/bin/mergelib
/usr/bin/mkdirhier
/usr/bin/mkhtmlindex
/usr/bin/revpath
/usr/bin/xmkmf
%{_datadir}/man/man1/ccmakedep.1
%{_datadir}/man/man1/cleanlinks.1
%{_datadir}/man/man1/imake.1
%{_datadir}/man/man1/makeg.1
%{_datadir}/man/man1/mergelib.1
%{_datadir}/man/man1/mkdirhier.1
%{_datadir}/man/man1/mkhtmlindex.1
%{_datadir}/man/man1/revpath.1
%{_datadir}/man/man1/xmkmf.1
%doc COPYING ChangeLog README

%changelog
* Tue Jun 18 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.5-1
- Initial port on Aix6.1
