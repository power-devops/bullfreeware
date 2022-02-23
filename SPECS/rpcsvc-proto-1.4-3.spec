#
# spec file for package rpcsvc-proto
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           rpcsvc-proto
Version:        1.4
Release:        3%{?dist}
Summary:        RPC protocol definitions
License:        BSD and LGPLv2+
Group:          Applications/Internet
Url:            https://github.com/thkukuk/rpcsvc-proto
Source0:        https://github.com/thkukuk/rpcsvc-proto/releases/v%{version}/%{name}-%{version}.tar.xz

Source10:       %{name}-%{version}-%{release}.build.log

Patch1:         rpcgen-Y.patch
Patch2:         rpcgen-1.4-NoRegister.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Conflicts: glibc-headers < 2.26.9000-36
Conflicts: glibc-common < 2.26.9000-36

BuildRequires:  gcc
#BuildRequires: automake, autoconf

%description
The rpcsvc-proto package includes several rpcsvc header files
and RPC protocol definitions from SunRPC sources (as shipped with
glibc).

%package devel
Summary:        RPC protocol definitions
Group:          Applications/Internet

%description devel
The rpcsvc-proto package includes several rpcsvc header files
and RPC protocol definitions from SunRPC sources (as shipped with
glibc).

%package -n rpcgen
Summary:        RPC protocol compiler
Group:          Applications/Internet
Provides:       rpcgen

%description -n rpcgen
rpcgen is a tool that generates C code to implement an RPC protocol.
The input to rpcgen is a language similar to C known as RPC Language
(Remote Procedure Call Language).

%prep
%setup -q

%patch1 -p1 -b .rpcgen-Y
%patch2 -p1 -b .rpcgen-1.4-NoRegister

%build


LIBS="$LIBS -lintl" CPP="/opt/freeware/bin/cpp " ./configure \
        --prefix=%{_prefix}  --mandir=%{_mandir}

gmake


%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# % make_install
gmake install DESTDIR=${RPM_BUILD_ROOT}

# rquota.x and rquota.h are provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

%files devel
#%license COPYING
%doc COPYING
%{_includedir}/rpcsvc/

%files -n rpcgen
%{_bindir}/rpcgen
%{_mandir}/man1/rpcgen.1*

%changelog
* Thu Jun 27 2019 Tony Reix <tony.reix@atos.net>  1.4-3
- Remove the "register " instruction in generated .c files

* Mon Jun 24 2019 Michael Wilson <michael.a.wilson@atos.net>  1.4-2
- Corrections to .spec file

* Fri Jun 21 2019 Michael Wilson <michael.a.wilson@atos.net>  1.4-1
- Initial version for AIX
- Based on package for Fedora 30

