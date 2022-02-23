# rpm -ba --define 'dotests 0' guile-*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 1}

%define _libdir64 %{_prefix}/lib64

%define mver 1.8

Summary: A GNU implementation of Scheme for application extensibility
Name: guile
Version: 1.8.8
Release: 2
URL: http://www.gnu.org/software/guile/
Source0: ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz.sig
Source2: %{name}-1.8.8-libtool-64bits.patch
License: GPLv2+ and LGPLv2+ and GFDL and OFSFDL
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: coreutils
BuildRequires: gettext
BuildRequires: gmp-devel >= 4.3.2-2
BuildRequires: readline-devel >= 5.2-3

Requires: info, /sbin/install-info
Requires: coreutils
Requires: gettext
Requires: gmp-devel >= 4.3.2-2
Requires: readline-devel >= 5.2-3

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the guile package if you'd like to add extensibility to programs
that you are developing.

Guile is available as 32-bit and 64-bit.


%package devel
Summary: Libraries and header files for the GUILE extensibility library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel >= 4.3.2-2
Requires: pkg-config
Requires: readline-devel >= 5.2-3

%description devel
The guile-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the guile-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to
install the guile package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export CC="xlc_r"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export  CFLAGS="-q64 -O2"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-error-on-warning

# Put /opt/freeware/lib64 BEFORE /opt/freeware/lib
patch -p0 < %{SOURCE2}

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export  CFLAGS="-q32 -O2"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-error-on-warning

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

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

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

# compress large documentation
bzip2 NEWS

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
for i in "" -srfi-srfi-1-v-3 -srfi-srfi-13-14-v-3 -srfi-srfi-4-v-3 -srfi-srfi-60-v-2 readline-v-17 ; do
  /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}${i}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}${i}.so*
done

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


%post
for i in guile r5rs goops guile-tut ; do
    /sbin/install-info %{_infodir}/${i}.info.gz %{_infodir}/dir &> /dev/null
done
:


%preun
if [ "$1" = 0 ]; then
    for i in guile r5rs goops guile-tut ; do
        /sbin/install-info --delete %{_infodir}/${i}.info.gz \
            %{_infodir}/dir &> /dev/null
    done
fi
:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING* 32bit/ChangeLog 32bit/HACKING 32bit/NEWS.bz2
%doc 32bit/README 32bit/THANKS
%{_bindir}/guile
%{_bindir}/guile_64
%{_bindir}/guile-tools*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man1/guile.1*
%{_infodir}/*info*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{mver}
%{_datadir}/%{name}/%{mver}/guile-procedures.txt
%{_datadir}/%{name}/%{mver}/ice-9
%{_datadir}/%{name}/%{mver}/lang
%{_datadir}/%{name}/%{mver}/oop
%{_datadir}/%{name}/%{mver}/scripts
%{_datadir}/%{name}/%{mver}/srfi
/usr/bin/guile
/usr/bin/guile_64
/usr/bin/guile-tools*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_bindir}/guile-config*
%{_bindir}/guile-snarf*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_datadir}/aclocal/*
/usr/bin/guile-config*
/usr/bin/guile-snarf*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Tue May 17 2016 Tony Reix <tony.reix@bull.net> - 1.8.8-1
- First version for AIX V6.1

* Wed Sep 12 2012 Michael Perzl <michael@perzl.org> - 1.8.8-1
- first version for AIX V5.1 and higher
