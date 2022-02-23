Name:           scons
Version:        2.2.0
Release:        1
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT, freely distributable
URL:            http://www.scons.org
Source0:        %{name}-%{version}.tar.gz
Patch0: 	%{name}-%{version}-env_python.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Prefix: 	%{_prefix}
BuildRequires:  python-devel >= 2.4, sed
Requires:       python >= 2.4
BuildArchitectures: noarch


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
%patch0 -p1 -b .env_python

%build
export RM="/usr/bin/rm -f"
/usr/bin/python setup.py build

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

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
* Thu Aug 30 2012 Patricia Cugny <patricia.cugny@bull.net> - 2.2.0-1
- initial version built on AIX 6.1
