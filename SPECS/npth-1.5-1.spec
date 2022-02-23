# From npth-1.5-1.Perzl.spec

%define _libdir64 %{_prefix}/lib64

Summary:        The New GNU Portable Threads library
Name:           npth
Version:        1.5
Release:        1
# software uses dual licensing (or both in parallel)
License:        LGPLv3+ or GPLv2+ or (LGPLv3+ and GPLv2+)
Group:          System Environment/Libraries
URL:            ftp://ftp.gnupg.org/gcrypt/npth/
Source0:        ftp://ftp.gnupg.org/gcrypt/npth/npth-%{version}.tar.bz2
Source1:        ftp://ftp.gnupg.org/gcrypt/npth/npth-%{version}.tar.bz2.sig
# Manual page is re-used and changed pth-config.1 from pth-devel package
Source2:        npth-config.1

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  AIX-rpm >= 5.3.0.0
Requires:       AIX-rpm >= 5.3.0.0

%description
nPth is a non-preemptive threads implementation using an API very similar
to the one known from GNU Pth.  It has been designed as a replacement of
GNU Pth for non-ancient operating systems.  In contrast to GNU Pth is is
based on the system's standard threads implementation.  Thus nPth allows
the use of libraries which are not compatible to GNU Pth.

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Development headers and libraries for GNU nPth
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc_r -q64" or "gcc -maix64".


%prep
%setup -q
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static 

gmake %{?_smp_mflags}

gmake check

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static 

gmake %{?_smp_mflags}

gmake check


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

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_mandir}/man1/
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so*

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/COPYING.LESSER 32bit/ChangeLog
%doc 32bit/NEWS 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/*/*
%{_datadir}/aclocal/*
/usr/bin/*


%changelog
* Thu Nov 17 2017 Tony Reix <tony.reix@atos.net> - 1.5-1
- Port on AIX 6.1

* Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.5-1
- updated to version 1.5

* Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.4-1
- updated to version 1.4

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 1.3-1
- updated to version 1.3

* Wed Dec 23 2015 Michael Perzl <michael@perzl.org> - 1.2-1
- updated to version 1.2

* Fri Nov 07 2014 Michael Perzl <michael@perzl.org> - 1.1-1
- updated to version 1.1

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 1.0-1
- updated to version 1.0

* Mon Jan 27 2014 Michael Perzl <michael@perzl.org> - 0.91-1
- first version for AIX V5.1 and higher
