Summary: A perfect hash function generator
Name: gperf
Version: 3.0.4
Release: 1
License: GPLv2+
Source: ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Group: Development/Tools
URL: http://www.gnu.org/software/%{name}/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: /sbin/install-info, info

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
exit 0


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi
exit 0


%files
%defattr(-,root,system)
%doc README NEWS doc/%{name}.html
%{_bindir}/*
%{_mandir}/man1/%{name}.1
%{_infodir}/%{name}.info*
/usr/bin/*


%changelog
* Thu Aug 06 2015 Hamza.sellami <hamza.sellami@atos.net> - 3.0.4-1
- Building with new GCC

* Wed Mar 11 2009 Michael Perzl <michael@perzl.org> - 3.0.4-1
- updated to version 3.0.4

* Tue Jun 17 2008 Michael Perzl <michael@perzl.org> - 3.0.3-1
- first version for AIX V5.1 and higher
