Summary: A library of handy utility functions
Name: glib2
Version: 2.30.3
Release: 2
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
# the AIX V3 rpm does not understand ".xz" files, thus converted to bz2
Source0: http://download.gnome.org/sources/glib/2.30/glib-%{version}.tar.bz2
Source1: http://download.gnome.org/sources/glib/2.30/glib-%{version}.sha256sum
Source2: glib2.sh
Source3: glib2.csh
Patch0: glib-%{version}-aix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: pkg-config
BuildRequires: gettext
BuildRequires: libffi-devel >= 3.0.10-1
Requires: gettext
Requires: libffi >= 3.0.10-1

%define _libdir64 %{_prefix}/lib64

%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.

This package provides version 2 of GLib.

The library is available as 32-bit and 64-bit.


%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: pkg-config
Requires: %{name} = %{version}-%{release}
Requires: libffi-devel >= 3.0.10-1

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q -n glib-%{version}
%patch0
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CFLAGS="-I/opt/freeware/include"

export CC="/usr/vac/bin/xlc_r -D_LARGE_FILES"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-threads=posix \
    --enable-regex \
    --with-pcre=internal
make

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-threads=posix \
    --enable-regex \
    --with-pcre=internal
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

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

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
for f in gio glib gmodule gobject gthread ; do
  /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${f}-2.0.a ${RPM_BUILD_ROOT}%{_libdir64}/lib${f}-2.0.so*
done

# glib2.sh and glib2.csh
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cp %{SOURCE2} %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*

(
  for dir in %{_libdir} %{_libdir64} ; do
    cd ${RPM_BUILD_ROOT}${dir}
    for f in lib*so* ; do
      ln -s ${f} `basename ${f} .0` 
    done
  done
)

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
%defattr(-,root,system -)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS
%{_sysconfdir}/profile.d/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%dir %{_libdir}/gio
%dir %{_libdir64}/gio
%dir %{_libdir}/gio/modules
%dir %{_libdir64}/gio/modules
%{_datadir}/locale/*/*/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/glib-2.0
%{_libdir64}/glib-2.0
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*
%{_datadir}/glib-2.0
/usr/bin/*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Wed Jun 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.30.3-2
- Build on Aix6.1

* Wed Apr 11 2012 Michael Perzl <michael@perzl.org> - 2.30.3-1
- updated to version 2.30.3

* Wed Apr 11 2012 Michael Perzl <michael@perzl.org> - 2.28.8-1
- updated to version 2.28.8

* Mon May 02 2011 Michael Perzl <michael@perzl.org> - 2.28.6-1
- updated to version 2.28.6

* Mon May 02 2011 Michael Perzl <michael@perzl.org> - 2.26.1-1
- updated to version 2.26.1

* Mon May 02 2011 Michael Perzl <michael@perzl.org> - 2.24.2-1
- updated to version 2.24.2
- remove dependency on external pcre, use builtin (recommended)

* Tue Jul 06 2010 Michael Perzl <michael@perzl.org> - 2.22.5-2
- removed dependency on gettext >= 0.17

* Mon Mar 29 2010 Michael Perzl <michael@perzl.org> - 2.22.5-1
- updated to version 2.22.5

* Thu Jan 07 2010 Michael Perzl <michael@perzl.org> - 2.22.4-1
- updated to version 2.22.4

* Mon Dec 14 2009 Michael Perzl <michael@perzl.org> - 2.22.3-1
- updated to version 2.22.3

* Fri Nov 20 2009 Michael Perzl <michael@perzl.org> - 2.22.2-1
- updated to version 2.22.2

* Fri Nov 20 2009 Michael Perzl <michael@perzl.org> - 2.20.5-2
- removed the "-D_LINUX_SOURCE_COMPAT" flag during compilation

* Tue Sep 29 2009 Michael Perzl <michael@perzl.org> - 2.20.5-1
- updated to version 2.20.5

* Mon Jun 29 2009 Michael Perzl <michael@perzl.org> - 2.20.4-1
- updated to version 2.20.4

* Mon Jun 29 2009 Michael Perzl <michael@perzl.org> - 2.18.4-1
- updated to version 2.18.4

* Mon Jun 29 2009 Michael Perzl <michael@perzl.org> - 2.18.2-2
- fixed POSIX threads settings

* Wed Oct 22 2008 Michael Perzl <michael@perzl.org> - 2.18.2-1
- updated to version 2.18.2

* Thu Jul 03 2008 Michael Perzl <michael@perzl.org> - 2.16.4-1
- updated to version 2.16.4

* Sat Apr 05 2008 Michael Perzl <michael@perzl.org> - 2.14.6-1
- first version for AIX V5.1 and higher
