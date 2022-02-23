Name:		libpaper
Version:	1.1.24
Release:	2
Summary:	Library and tools for handling papersize
Group:		System Environment/Libraries
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
Source0:	http://ftp.debian.org/debian/pool/main/libp/%{name}/%{name}_%{version}.tar.gz
Patch0:		%{name}-%{version}-aix.patch
# Upstream bug:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=475683
Patch1:         %{name}-1.1.23-debianbug475683.patch
Patch2:         %{name}-%{version}-aixplatform.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	make, gawk, patch

%define _libdir64 %{_prefix}/lib64

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH

%patch0
%patch1 -p1 -b .dlfix
%patch2 -p1 -b .aixplatform
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export CC="xlc_r"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > ${RPM_BUILD_ROOT}%{_sysconfdir}/papersize
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/libpaper.d


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(- root,system,-)
%doc 32bit/COPYING 32bit/ChangeLog 32bit/README
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
/usr/bin/*
/usr/sbin/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Wed Mar 18 2015 Gerard Visiedo <gerard.visido@bull.net> 1.1.24-2
- Initial port on Aix6.1

* Tue Jan 25 2011 Michael Perzl <michael@perzl.org> - 1.1.24-1 
- updated to version 1.1.24

* Fri Oct 23 2009 Michael Perzl <michael@perzl.org> - 1.1.23-3 
- adapted the paper.h include file for AIX

* Tue Sep 15 2009 Michael Perzl <michael@perzl.org> - 1.1.23-2 
- fixed some minor SPEC file issues

* Tue Jul 28 2009 Michael Perzl <michael@perzl.org> - 1.1.23-1
- first version for AIX5L v5.1 and higher
