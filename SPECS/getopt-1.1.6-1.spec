Summary:        Parse command-line parameters
Name:           getopt
Version:        1.1.6
Release:        1
License:        GPLv2
Group:          System Environment/Base 
URL:            http://software.frodo.looijaard.name/getopt/
Source0:        http://software.frodo.looijaard.name/getopt/files/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-aix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  coreutils, make, gettext
Requires:       gettext, bash, tcsh

%description
Getopt(1) is a program to help shell scripts parse command-line parameters. 


%prep
%setup -q
%patch0


%build
export LIBPATH="/opt/freeware/lib:/usr/lib"

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} prefix=%{_prefix} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
cd usr/linux/bin
ln -sf ../../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc README
%doc getopt-parse.bash getopt-parse.tcsh
%doc getopt-test.bash getopt-test.tcsh
%{_bindir}/*
%{_mandir}/man1/*
/usr/linux/bin/*


%changelog
* Tue Aug 23 2016 Tony Reix <tony.reix@bull.net> 1.1.6-1
- Initial port on AIX 6.1

* Mon Jul 15 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.1.4-4
- Initial port on Aix6.1

* Thu Dec 16 2010 Michael Perzl <michael@perzl.org> - 1.1.4-3
- fixed dependency issue with tcsh

* Mon Jul 05 2010 Michael Perzl <michael@perzl.org> - 1.1.4-2
- removed dependency on gettext >= 0.17

* Thu Sep 04 2008 Michael Perzl <michael@perzl.org> - 1.1.4-1
- first version for AIX V5.1 and higher
