Name:           scons
Version:        2.3.6
Release:        1
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            http://www.scons.org
Source0:        http://prdownloads.sourceforge.net/scons/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  python-devel >= 2.6.2, sed
Requires:       python >= 2.6.2


%description
SCons is an Open Source software construction tool--that is, a build
tool; an improved substitute for the classic Make utility; a better way
to build software.  SCons is based on the design which won the Software
Carpentry build tool design competition in August 2000.

SCons "configuration files" are Python scripts, eliminating the need
to learn a new build tool syntax.  SCons maintains a global view of
all dependencies in a tree, and can scan source (or other) files for
implicit dependencies, such as files specified on #include lines.  SCons
uses MD5 signatures to rebuild only when the contents of a file have
really changed, not just when the timestamp has been touched.  SCons
supports side-by-side variant builds, and is easily extended with user-
defined Builder and/or Scanner objects.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
sed -i 's|/usr/bin/env python|/usr/bin/python|' script/*


%build
export RM="/usr/bin/rm -f"

/usr/bin/python setup.py build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

/usr/bin/python setup.py install \
    --root=${RPM_BUILD_ROOT} \
    --record=INSTALLED_FILES \
    --install-lib=%{_libdir}/%{name} \
    --install-scripts=%{_bindir}

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc CHANGES.txt LICENSE.txt README.txt RELEASE.txt
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man?/*
/usr/bin/*


%changelog
* Fri Nov 18 2016 Tony Reix <tony.reix@bull.net> - 2.3.6-1
- Initial port on AIX 6.1

* Fri Nov 18 2016 Tony Reix <tony.reix@bull.net> - 2.3.4-1
- Initial port

* Wed Oct 15 2014 Michael Perzl <michael@perzl.org> - 2.3.4-1
- updated to version 2.3.4

* Mon Aug 25 2014 Michael Perzl <michael@perzl.org> - 2.3.3-1
- updated to version 2.3.3

* Mon Aug 25 2014 Michael Perzl <michael@perzl.org> - 2.3.2-1
- updated to version 2.3.2

* Thu Mar 27 2014 Michael Perzl <michael@perzl.org> - 2.3.1-1
- updated to version 2.3.1

* Mon Feb 10 2014 Michael Perzl <michael@perzl.org> - 2.3.0-1
- updated to version 2.3.0

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 2.2.0-1
- updated to version 2.2.0

* Wed Jul 18 2012 Michael Perzl <michael@perzl.org> - 2.1.0-1
- updated to version 2.1.0

* Mon Nov 22 2010 Michael Perzl <michael@perzl.org> - 2.0.1-1
- updated to version 2.0.1

* Mon Nov 22 2010 Michael Perzl <michael@perzl.org> - 1.3.1-1
- updated to version 1.3.1

* Mon Mar 29 2010 Michael Perzl <michael@perzl.org> - 1.3.0-1
- first version for AIX V5.1 and higher
