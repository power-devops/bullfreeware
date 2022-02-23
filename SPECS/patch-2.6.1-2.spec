Summary:	The GNU patch command, for modifying/upgrading files
Name:		patch
Version:	2.6.1
Release:	2
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/directory/GNU/%{name}.html
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2.sig
Source2:	%{name}-%{version}-strnlen.c
Patch0:		%{name}-%{version}-aix.patch
Buildroot:	/var/tmp/%{name}-%{version}-%{release}-buildroot

BuildRequires:	make, bash

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.


%prep
%setup -q
%patch0 -p1 -b .aix

cp %{SOURCE2} gl/lib/strnlen.c

# fake a <stdbool.h> as AIX5L V5.1 and XLC/C++ V7 doesn't have one
cat > stdbool.h << EOF
#ifndef stdbool_h_wrapper
#define stdbool_h_wrapper

typedef enum {false = 0, true = 1} bool;

#endif
EOF


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
	install
       

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -sf ../../..%{_prefix}/bin/* .
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc NEWS README AUTHORS ChangeLog
%{_prefix}/bin/*
%{_prefix}/man/man1/*
/usr/linux/bin/*


%changelog
* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.1-2
- Port on platform Aix6.1

* Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.1-1
- Port on platform Aix5.3

