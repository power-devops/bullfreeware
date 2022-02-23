%define majorver 8.5

Summary: The graphical toolkit for the Tcl scripting language
Name: tk
Version: %{majorver}.9
Release: 4
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net
Source0: http://download.sourceforge.net/tcl/%{name}%{version}-src.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: tcl-devel = %{version}
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: libXft-devel >= 2.1.14
Requires: tcl = %{version}
Requires: fontconfig >= 2.5.0
Requires: libXft >= 2.1.14

%define _libdir64 %{_prefix}/lib64

%description
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Tk graphical toolkit development files
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel = %{version}

%description devel
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the development files and man pages for tk.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q -n %{name}%{version}
mkdir -p ../64bit
cp -r * ../64bit/
mv ../64bit .


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC="/usr/vac/bin/xlc_r"

# first build the 64-bit version
export OBJECT_MODE=64
cd 64bit/unix
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-64bit \
    --enable-shared --disable-static \
    --enable-threads \
    --enable-xft \
    --with-x \
    --with-tcl=%{_libdir64}
sed -e "s|-L\/opt\/freeware\/lib|-L\/opt\/freeware\/lib64|g" config.status >  config.status.tmp
mv config.status.tmp config.status
chmod 755 config.status
./config.status
make %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver}
cd ../..

# now build the 32-bit version
export OBJECT_MODE=32
cd unix
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static \
    --enable-threads \
    --enable-xft \
    --with-x
make %{?_smp_mflags} TK_LIBRARY=%{_datadir}/%{name}%{majorver}

cd ..
rm -f lib%{name}%{majorver}.a
${AR} -r lib%{name}%{majorver}.a unix/lib%{name}%{majorver}.so 64bit/unix/lib%{name}%{majorver}.so


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
export OBJECT_MODE=64
cd 64bit/unix
make DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}
mv ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/wish%{majorver}_64
cd ../..

export OBJECT_MODE=32
cd unix
make DESTDIR=${RPM_BUILD_ROOT} install TK_LIBRARY=%{_datadir}/%{name}%{majorver}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

ln -sf wish%{majorver} ${RPM_BUILD_ROOT}%{_bindir}/wish
ln -sf wish%{majorver}_64 ${RPM_BUILD_ROOT}%{_bindir}/wish_64

ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so
ln -sf lib%{name}%{majorver}.so ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so

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
%{_bindir}/wish*
%{_libdir}/lib*.a
%{_libdir}/lib*.so*
%{_libdir64}/lib*.so*
%dir %{_libdir}/%{name}%{majorver}
%dir %{_libdir64}/%{name}%{majorver}
%{_libdir}/%{name}%{majorver}/*
%{_libdir64}/%{name}%{majorver}/*
%dir %{_datadir}/%{name}%{majorver}
%{_datadir}/%{name}%{majorver}/*
%{_mandir}/man1/*
%{_mandir}/mann/*
/usr/bin/wish*
/usr/lib/lib*.a
/usr/lib/lib*.so*
/usr/lib64/lib*.so*


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/libtkstub*.a
%{_libdir64}/libtkstub*.a
%{_libdir}/%{name}Config.sh
%{_libdir64}/%{name}Config.sh
%{_mandir}/man3/*
/usr/include/*
/usr/lib/lib*.a
/usr/lib64/lib*.a


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 8.5.9-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jul 28 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-2
- Add librarie libtcl8.5.a with 32 and 64 bits

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.5.9-1
- Port on platform Aix5.3
