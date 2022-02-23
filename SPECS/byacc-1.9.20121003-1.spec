%define byaccdate 20121003

Summary: Berkeley Yacc, a parser generator
Name: byacc
Version: 1.9.%{byaccdate}
Release: 1
License: Public Domain
Group: Development/Tools
URL: http://invisible-island.net/byacc/byacc.html
Source0: ftp://invisible-island.net/byacc/%{name}-%{byaccdate}.tgz
Source1: ftp://invisible-island.net/byacc/%{name}-%{byaccdate}.tgz.asc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Byacc (Berkeley Yacc) is a public domain LALR parser generator which
is used by many programs during their build process.

If you are going to do development on your system, you will want to install
this package.


%prep
%setup -q -n %{name}-%{byaccdate}


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}%{_bindir}
mv -f yacc %{name}
cd ${RPM_BUILD_ROOT}%{_mandir}/man1
mv -f yacc.1 %{name}.1

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc ACKNOWLEDGEMENTS CHANGES NEW_FEATURES NOTES NO_WARRANTY README
%defattr(-,root,system,-)
%{_bindir}/*
%{_mandir}/man1/*
/usr/bin/*


%changelog
* Mon Mar 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.9.20121003-1
- Initial port on Aix6.1
