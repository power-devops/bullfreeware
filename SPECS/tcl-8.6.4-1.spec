%define majorver 8.6

Summary: Tcl scripting language development environment
Name: tcl
Version: %{majorver}.4
Release: 1
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/%{name}/%{name}%{version}-src.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Provides: tcl(abi) = %{majorver}

%define _libdir64 %{_prefix}/lib64

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Tcl scripting language development environment
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q -n %{name}%{version}
chmod -x generic/tclThreadAlloc.c
mkdir -p ../64bit
cp -r * ../64bit/
mv ../64bit .


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# prevent "out of stack space" error


# first build the 64-bit version
export OBJECT_MODE=64
cd 64bit/unix
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static \
	LDFLAGS= libtcl8.6.so \
    CC="gcc -maix64" CXX="g++ -maix64" \
    --enable-threads
gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
cd ../..

# now build the 32-bit version
export OBJECT_MODE=32
cd unix
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static \
	CC="gcc -maix32" CXX="g++ -maix32" \
    --enable-threads
gmake %{?_smp_mflags} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

cd ..
rm -f lib%{name}%{majorver}.a
${AR} -r lib%{name}%{majorver}.a unix/lib%{name}%{majorver}.so 64bit/unix/lib%{name}%{majorver}.so


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
export OBJECT_MODE=64
cd 64bit/unix
make DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh%{majorver}_64
ln -sf tclsh%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/tclsh_64
cd ../..

export OBJECT_MODE=32
cd unix
make DESTDIR=${RPM_BUILD_ROOT} install TCL_LIBRARY=%{_datadir}/%{name}%{majorver}
ln -sf tclsh%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/tclsh

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/%{name}%{majorver}/ldAix

cd ..
cp lib%{name}%{majorver}.a  ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}%{majorver}.a

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
%doc README changes license.terms
%{_bindir}/tclsh*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir64}/lib*.so
%dir %{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}%{majorver}/*
%dir %{_datadir}/%{name}8
%{_datadir}/%{name}8/*
%{_mandir}/man1/*
%{_mandir}/mann/*
/usr/bin/tclsh*
/usr/lib/lib*.a
/usr/lib/lib*.so
/usr/lib64/lib*.so


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/libtclstub*.a
%{_libdir64}/libtclstub*.a
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_mandir}/man3/*
/usr/include/*
/usr/lib/libtclstub*.a
/usr/lib64/libtclstub*.a


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 8.5.9-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jul 28 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-2
- Add librarie libtcl8.5.a with 32 and 64 bits

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-1
- Port on platform Aix5.3
