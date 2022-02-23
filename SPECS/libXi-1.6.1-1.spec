Name:          libXi
Version:       1.6.1
Release:       1
Summary:       X.Org input library
Group:         System/Libraries
URL:           http://x.org
Source:        ftp://ftp.freedesktop.org/pub/individual/lib/libXi-%{version}.tar.bz2
#Patch0:        %{name}-1.4.3-Handle-unknown-device-classes.patch
License:       MIT
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
## AUTOBUILDREQ-BEGIN
#BuildRequires: glibc-devel
#BuildRequires: inputproto-devel
#BuildRequires: libpthread-stubs-devel
#BuildRequires: libX11-devel
#BuildRequires: libXau-devel
#BuildRequires: libxcb-devel
#BuildRequires: libXdmcp-devel
##BuildRequires: libXext-devel
#BuildRequires: pkg-config
## AUTOBUILDREQ-END
#BuildRequires: inputproto-devel >= 2.2
Obsoletes:     libXorg

%description
X.Org input library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xi library.

This package contains static libraries and header files need for development.

%prep
%setup -q
#%patch0 -p1

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"

./configure \
        --prefix=%{_prefix} \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules

make

cp src/.libs/%{name}.so.6 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"

./configure \
        --prefix=%{_prefix} \
        --enable-shared \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.6


%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
%makeinstall

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,system)
%{_libdir}/libXi.a
%doc COPYING

%files devel
%defattr(-,root,system)
%{_includedir}/X11/extensions/XInput.h
%{_includedir}/X11/extensions/XInput2.h
%{_libdir}/libXi.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%dir %{_datadir}/doc/libXi
%{_datadir}/doc/libXi/*
%doc ChangeLog

%changelog
* Thu Apr 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.6.1-1
- Initial port on Aix6.1

* Fri Jul 06 2012 Automatic Build System <autodist@...> 1.6.1-1mamba
- automatic version update by autodist

* Sat Oct 01 2011 Silvan Calarco <silvan.calarco@...> 1.4.3-2mamba
- added Handle-unknown-device-classes patch to fix application crash on resume (i.e. nm-applet 0.9.0)

* Sun Jun 19 2011 Automatic Build System <autodist@...> 1.4.3-1mamba
- automatic update by autodist

* Tue Mar 29 2011 Automatic Build System <autodist@...> 1.4.2-1mamba
- automatic update by autodist

* Mon Jan 31 2011 Automatic Build System <autodist@...> 1.4.1-1mamba
- automatic update by autodist

* Sat Nov 20 2010 Automatic Build System <autodist@...> 1.4.0-1mamba
- automatic update by autodist

* Sun Aug 15 2010 Automatic Build System <autodist@...> 1.3.2-1mamba
- automatic update by autodist
