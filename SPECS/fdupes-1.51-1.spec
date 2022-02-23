Summary:	Finds duplicate files in a given set of directories
Name:		fdupes
Version:	1.51
Release:	1
License:	MIT
Group:		Applications/File
URL:		http://netdial.caribe.net/~adrian2/fdupes.html
Source0:	http://netdial.caribe.net/~adrian2/programs/fdupes/%{name}-%{version}.tar.gz

Patch0:		%{name}-%{version}-destdir.patch
# http://bugs.debian.org/353789
Patch1:		%{name}-%{version}-typo.patch
# Fix CVE
Patch2:		%{name}-%{version}-check-permissions.patch
# Apply proper LDFLAGS
Patch3:		%{name}-%{version}-obey-ldflags.patch

Patch10:	%{name}-%{version}-aix.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	patch, coreutils, make

%description
FDUPES is a program for identifying duplicate files residing within specified
directories.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch2 -p1 -b .cve
%patch0 -p1 -b .destdir
%patch1 -p1 -b .typo
%patch3 -p1 -b .ldflags
%patch10


%build
gmake %{?_smp_mflags} COMPILER_OPTIONS="${CFLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install INSTALL="/opt/freeware/bin/install -p" BIN_DIR=%{_bindir} \
  MAN_BASE_DIR=%{_mandir} DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc CHANGES CONTRIBUTORS README TODO
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
/usr/bin/%{name}


%changelog
* Mon Jun 23 2014 Michael Perzl <michael@perzl.org> - 1.51-1
- updated to version 1.51

* Wed Apr 13 2011 Michael Perzl <michael@perzl.org> - 1.50-1.PR2
- first version for AIX5L v5.1 and higher
