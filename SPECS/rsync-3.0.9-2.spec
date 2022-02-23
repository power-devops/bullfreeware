Summary: A program for synchronizing files over a network.
Name: rsync
Version: 3.0.9
Release: 2
Group: Applications/Internet
URL: http://rsync.samba.org
Source0: ftp://rsync.samba.org/pub/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://rsync.samba.org/pub/%{name}/%{name}-%{version}.tar.gz.asc
Source2: ftp://rsync.samba.org/pub/%{name}/%{name}-patches-%{version}.tar.gz
Source3: ftp://rsync.samba.org/pub/%{name}/%{name}-patches-%{version}.tar.gz.asc
Patch0:  %{name}-%{version}-aix_plat.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
License: GPLv3+

BuildRequires: patch make
Requires: popt

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -b 2

# Needed for compatibility with previous patched rsync versions
patch -p1 -i patches/acls.diff
patch -p1 -i patches/xattrs.diff

%patch0 -p1 -b .aix_plat

%build
export CC="/usr/vac/bin/xlc_r  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-largefile \
    --enable-acl-support

# manually remove MKSTEMP from config.h
perl -i.bak -pe 's/#define HAVE_SECURE_MKSTEMP 1/\/* #undef HAVE_SECURE_MKSTEMP *\//' config.h

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc COPYING README tech_report.tex
%{_bindir}/*
%{_mandir}/man?/*
/usr/bin/*


%changelog
* Tue Mar 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 3.0.9-1
- Initial port on Aix6.1
