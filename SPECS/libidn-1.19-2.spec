Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.19
Release: 2
URL: http://www.gnu.org/software/libidn
License: LGPLv2+
Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkg-config, gettext
Requires: info, gettext
Requires: /sbin/install-info

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.


%package devel
Summary: Development files for the libidn library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static
make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/%{name}.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

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

cd examples
make clean
rm -rf .deps


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc ChangeLog NEWS FAQ README THANKS COPYING*
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/*.a
%{_infodir}/libidn*
%{_datadir}/locale/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc doc/libidn.html examples
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Mar 04 2011 Patricia Cugny <patricia.cugny@bull.net> - 1.19-2
- first version for AIX V5.3 and higher
