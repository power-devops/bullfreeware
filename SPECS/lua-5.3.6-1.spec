# Create a test package in ANY case, but test only if with dotests.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:           lua
Version:        5.3.6
Release:        1
Summary:        Powerful light-weight programming language
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:        lib%{name}-5.1.so-aix32
Source2:        lib%{name}-5.1.so-aix64
Source3:        lib%{name}-5.2.so-aix32
Source4:        lib%{name}-5.2.so-aix64

Patch0:         %{name}-%{version}-aix.patch
Patch1:         lua-5.3.5-Makefile-CC.patch

#	BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Source1000:     %{name}-%{version}-%{release}.build.log


BuildRequires:  coreutils
BuildRequires:  readline-devel >= 7.0-1
Requires:       readline >= 7.0-1

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.


%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       readline-devel >= 7.0-1
Requires:       pkg-config

%description devel
This package contains development files for %{name}.


%prep
%setup -q
%patch0
%patch1

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit

cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)


%build
export CC=gcc
export AR=/usr/bin/ar

# $BUILD/%{name}-%{version}/XXbit added to -Wl,-blibpath in order to be able to test without RPMs installed.
# (note that the tests does very silly testing...)

# first build the 64-bit version

cd 64bit
export OBJECT_MODE=64

export LDFLAGS=-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib

# -DLUA_USE_POSIX alread defined in luaconf.h
# Removed by patch -Makefile-CC.patch
gmake aix CC="gcc" CFLAGS="-maix64 -O2 -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-maix64 -L. -L/opt/freeware/lib64 -L/opt/freeware/lib -lreadline -Wl,-blibpath:$BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src:/opt/freware/lib64:/opt/freeware/lib:/usr/lib:/lib"

cd src
  mkdir tmp_obj
  cd tmp_obj
  ${AR} -x ../lib%{name}.a
  cd ..
  ${CC} -maix64 -shared tmp_obj/*.o -o lib%{name}-5.3.so -lm $LDFLAGS
#CreateExportList -X64 lib%{name}.exp lib%{name}.a
#${CC} -maix64 -shared lib%{name}.a -o lib%{name}-5.3.so -Wl,-bE:lib%{name}.exp -lm $LDFLAGS
rm -f lib%{name}.a
/usr/bin/ar -X64 -rc lib%{name}.a lib%{name}-5.3.so
rm -f %{name}.exp lua luac
gmake all CC="gcc" CFLAGS="-O2 -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-maix64 -L. -L/opt/freeware/lib64 -L/opt/freeware/lib -lreadline -Wl,-blibpath:$BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src:/opt/freware/lib64:/opt/freeware/lib:/usr/lib:/lib $LDFLAGS"
cd ..

# now build the 32-bit version

cd ../32bit
export OBJECT_MODE=32

export LDFLAGS=-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib

gmake aix CC="gcc" CFLAGS="-maix32 -O2 -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-maix32 -L. -L/opt/freeware/lib -lreadline -Wl,-blibpath:$BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

cd src
  mkdir tmp_obj
  cd tmp_obj
  ${AR} -x ../lib%{name}.a
  cd ..
  ${CC} -maix32 -shared tmp_obj/*.o -o lib%{name}-5.3.so -lm $LDFLAGS
#CreateExportList -X32 lib%{name}.exp lib%{name}.a
#${CC} -maix32 -shared lib%{name}.a -o lib%{name}-5.3.so -Wl,-bE:lib%{name}.exp -lm $LDFLAGS
rm -f lib%{name}.a
/usr/bin/ar -X32 -rc lib%{name}.a lib%{name}-5.3.so
rm -f %{name}.exp lua luac
gmake all CC="gcc" CFLAGS="-O2 -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-maix32 -L. -L/opt/freeware/lib -lreadline -Wl,-blibpath:$BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 $LDFLAGS"
cd ..


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
( gmake test || true )

cd ..

cd 32bit
( gmake test || true )


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH

cd 64bit
export OBJECT_MODE=64
gmake install INSTALL_TOP=${RPM_BUILD_ROOT}%{_prefix}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

mv ${RPM_BUILD_ROOT}%{_libdir} ${RPM_BUILD_ROOT}%{_libdir64} 

cd ../32bit
export OBJECT_MODE=32
gmake install INSTALL_TOP=${RPM_BUILD_ROOT}%{_prefix}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Move 64bit binaries to *_64
# Make 64 the default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in lua luac ; do
    mv -f ${f} ${f}_32
    ln -s ${f}_64 ${f}
  done
)

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}/5.3
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/5.3

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
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}*.so*
# Create a symlink from lib to lib64 for liblua.a
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -sf ../lib/lib%{name}.a .
)

# Add the older 5.1 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} lib%{name}-5.1.so
/usr/bin/strip -X32 -e lib%{name}-5.1.so
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}-5.1.so
cp %{SOURCE2} lib%{name}-5.1.so
/usr/bin/strip -X64 -e lib%{name}-5.1.so
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}-5.1.so

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-5.1.so
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-5.1.so

# Add the older 5.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} lib%{name}-5.2.so
/usr/bin/strip -X32 -e lib%{name}-5.2.so
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}-5.2.so
cp %{SOURCE4} lib%{name}-5.2.so
/usr/bin/strip -X64 -e lib%{name}-5.2.so
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}-5.2.so

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-5.2.so
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-5.2.so

# Seems that the file lua.pc no more exists
#	mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
#	mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig
#	cat etc/%{name}.pc | \
#	    grep -v '^#' | \
#	    grep -v INSTALL_ | \
#	    sed 's|/usr/local|/opt/freeware|' \
#	      > ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/%{name}.pc
#	cp ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/%{name}.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/

# No more deliver files in /usr
#	(
#	  cd ${RPM_BUILD_ROOT}
#	  for dir in bin include lib lib64
#	  do
#	    mkdir -p usr/${dir}
#	    cd usr/${dir}
#	    ln -sf ../..%{_prefix}/${dir}/* .
#	    cd -
#	  done
#	)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


# No more deliver .so files
# No more deliver files under /usr
%files
%defattr(-,root,system,-)
%doc 32bit/README 32bit/doc/*.html
%doc 32bit/doc/*.css 32bit/doc/*.gif 32bit/doc/*.png
%{_bindir}/*
%{_libdir}/*.a
#	%{_libdir}/*.so*
%{_libdir64}/*.a
#	%{_libdir64}/*.so*
%{_mandir}/man1/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/5.3
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/5.3
#	/usr/bin/*
#	/usr/lib/*.a
#	/usr/lib/*.so*
#	/usr/lib64/*.so*


# No more deliver files under /usr
%files devel
%defattr(-,root,system,-)
%{_includedir}/*
#	%{_libdir}/pkgconfig/*.pc
#	%{_libdir64}/pkgconfig/*.pc
#	/usr/include/*


%changelog
* Thu Jan 14 2021 Tony Reix <tony.reix@atos.net> - 5.3.6-1
- Move to 5.3.6
- Suppress /usr files
- Add a symlink for lib64 for liblua.a

* Mon Apr 08 2019 Tony Reix <tony.reix@atos.net> - 5.3.5-1
- Port it on AIX 6.1 .
- Use gcc instead of xlc.
- Add test (lua -v).
- Remove no more existant lua.pc file

* Wed Sep 19 2018 Michael Perzl <michael@perzl.org> - 5.3.5-1
- updated to version 5.3.5

* Tue Jan 31 2017 Michael Perzl <michael@perzl.org> - 5.3.4-1
- updated to version 5.3.4

* Thu Jul 07 2016 Michael Perzl <michael@perzl.org> - 5.3.3-1
- updated to version 5.3.3

* Mon Dec 28 2015 Michael Perzl <michael@perzl.org> - 5.3.2-1
- updated to version 5.3.2

* Fri Sep 25 2015 Michael Perzl <michael@perzl.org> - 5.3.1-1
- updated to version 5.3.1

* Tue Jan 20 2015 Michael Perzl <michael@perzl.org> - 5.3.0-1
- updated to version 5.3.0

* Thu Dec 26 2013 Michael Perzl <michael@perzl.org> - 5.2.3-1
- updated to version 5.2.3

* Tue Jun 04 2013 Michael Perzl <michael@perzl.org> - 5.2.2-1
- updated to version 5.2.2

* Sun Jun 17 2012 Michael Perzl <michael@perzl.org> - 5.2.1-1
- updated to version 5.2.1

* Wed May 30 2012 Michael Perzl <michael@perzl.org> - 5.2.0-3
- fixed missing compatibility with lua version 5.1.X

* Sun May 13 2012 Michael Perzl <michael@perzl.org> - 5.2.0-2
- added a missing compatibility symbolic link

* Mon Feb 20 2012 Michael Perzl <michael@perzl.org> - 5.2.0-1
- updated to version 5.2.0

* Mon Feb 20 2012 Michael Perzl <michael@perzl.org> - 5.1.5-1
- updated to version 5.1.5
- removed the GNU autotools patch, added RTL-style shared libraries

* Thu Aug 25 2011 Michael Perzl <michael@perzl.org> - 5.1.4-3
- updated to latest 5.1.4-3 patch

* Wed Oct 06 2010 Michael Perzl <michael@perzl.org> - 5.1.4-2
- fixed some dependency problems

* Wed Nov 11 2009 Michael Perzl <michael@perzl.org> - 5.1.4-1
- first version for AIX V5.1 and higher
