# rpm -ba --define 'dotests 0' libmpc....spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: C library for multiple precision complex arithmetic
Name: libmpc
Version: 1.0.3
Release: 2
License: LGPLv2+
Group: Development/Tools
URL: http://www.multiprecision.org/
Source0: http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
Source1: http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz.sig
Source2: %{name}.so.2-aix32
Source3: %{name}.so.2-aix64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gmp-devel >= 4.3.2-1
BuildRequires: mpfr-devel >= 3.1.2-1
Requires: gmp >= 4.3.2-1
Requires: mpfr >= 3.1.2-1

%define _libdir64 %{_prefix}/lib64

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Header and shared development libraries for MPC
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel >= 4.3.2-1
Requires: mpfr-devel >= 3.1.2-1
Requires: info, /sbin/install-info

%description devel
Header files and other files required for developing programs using MPC.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q -n mpc-%{version}

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/



%build
export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/sbin:.

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC="gcc -maix64 "
export CXX="g++ -maix64 "

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
        (gmake -k check || true)
fi


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC="gcc -maix32 "
export CXX="g++ -maix32 "

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
        (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/sbin:.

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
# What does this message mean ??
# libtool: warning: remember to run 'libtool --finish /opt/freeware/lib64'

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
# What does this message mean ??
# libtool: warning: remember to run 'libtool --finish /opt/freeware/lib'


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

rm -f   ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*.info*

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*


# Add a link from lib64/libmpc.a to lib/libmpc.a
(
  cd    ${RPM_BUILD_ROOT}%{_libdir64}/
  rm -f %{name}.a
  ln -s %{_libdir}/%{name}.a .
)


# Add the older libmpc.so.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
# 32bits
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/%{name}.so.2
cp %{SOURCE2} %{name}.so.2
/usr/bin/strip -X32 -e %{name}.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.2
# 64bits
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2
cp %{SOURCE3} %{name}.so.2
/usr/bin/strip -X64 -e %{name}.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.2


# Add symlinks from /usr to /opt/freeware
( 
  cd ${RPM_BUILD_ROOT}
  for dir in include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%post devel
if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
   /sbin/install-info %{_infodir}/mpc.info.gz %{_infodir}/dir || :
fi


%preun devel
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
      /sbin/install-info --delete %{_infodir}/mpc.info.gz %{_infodir}/dir || :
   fi
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/README 32bit/NEWS 32bit/COPYING.LESSER
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_infodir}/*.info*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Tue May 31 2016 Tony Reix <tony.reix@atos.net> - 1.0.3-2
- Compile version 1.0.3 for AIX 6.1 using GCC 4.8.4
- Improve .spec file

* Thu Aug 06 2015 Hamza Sellami <hamza.sellami@atos.net> - 1.0.3-1
- Compile version 1.0.3 for AIX 6.1 using GCC 4.8.4

* Sat Feb 21 2015 Michael Perzl <michael@perzl.org> - 1.0.3-1
- updated to version 1.0.3

* Wed Jan 15 2014 Michael Perzl <michael@perzl.org> - 1.0.2-1
- updated to version 1.0.2

* Tue Oct 09 2012 Michael Perzl <michael@perzl.org> - 1.0.1-2
- added missing older compatibility shared members

* Thu Sep 06 2012 Michael Perzl <michael@perzl.org> - 1.0.1-1
- updated to version 1.0.1

* Thu Mar 10 2011 Michael Perzl <michael@perzl.org> - 0.9-1
- updated to version 0.9, added RTL-style shared libraries

* Thu Nov 04 2010 Michael Perzl <michael@perzl.org> - 0.8.2-1
- updated to version 0.8.2

* Mon Dec 14 2009 Michael Perzl <michael@perzl.org> - 0.8.1-1
- first version for AIX V5.1 and higher
