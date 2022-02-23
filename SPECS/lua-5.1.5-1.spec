%define _libdir64 %{_prefix}/lib64

Name:           lua
Version:        5.1.5
Release:        1
Summary:        Powerful light-weight programming language
Group:          Development/Languages
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-aix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  coreutils
BuildRequires:  readline-devel >= 5.2
Requires:       readline >= 5.2

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
Requires:       readline-devel >= 5.2
Requires:       pkg-config

%description devel
This package contains development files for %{name}.


%prep
%setup -q

%patch0 -p1 -b .aix

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)

%build
export CC="/usr/vac/bin/xlc_r"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
make aix
cd src
/usr/vac/bin/CreateExportList -X64 lib%{name}.exp lib%{name}.a
${CC} -q64 -qmkshrobj lib%{name}.a -o lib%{name}-5.1.so -bE:lib%{name}.exp -lm
rm -f lib%{name}.a
/usr/bin/ar -X64 -rc lib%{name}.a lib%{name}-5.1.so
rm -f %{name}.exp lua luac
make all CC="/usr/vac/bin/xlc_r" CFLAGS="-O -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-L. -L/opt/freeware/lib64 -L/opt/freeware/lib -lreadline -Wl,-blibpath:/opt/freware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
cd ..

# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
make aix
cd src
/usr/vac/bin/CreateExportList -X32 lib%{name}.exp lib%{name}.a
${CC} -q32 -qmkshrobj lib%{name}.a -o lib%{name}-5.1.so -bE:lib%{name}.exp -lm
rm -f lib%{name}.a
/usr/bin/ar -X32 -rc lib%{name}.a lib%{name}-5.1.so
rm -f %{name}.exp lua luac
make all CC="/usr/vac/bin/xlc_r" CFLAGS="-O -DLUA_USE_LINUX" MYLIBS="" MYLDFLAGS="-L. -L/opt/freeware/lib -lreadline -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH

cd 64bit
export OBJECT_MODE=64
make install INSTALL_TOP=${RPM_BUILD_ROOT}%{_prefix}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

mv ${RPM_BUILD_ROOT}%{_libdir} ${RPM_BUILD_ROOT}%{_libdir64} 

cd ../32bit
export OBJECT_MODE=32
make install INSTALL_TOP=${RPM_BUILD_ROOT}%{_prefix}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}/5.1
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/5.1

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

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig
cat etc/%{name}.pc | \
    grep -v '^#' | \
    grep -v INSTALL_ | \
    sed 's|/usr/local|/opt/freeware|' \
      > ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/%{name}.pc
cp ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/%{name}.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/

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
%doc 32bit/README 32bit/doc/*.html
%doc 32bit/doc/*.css 32bit/doc/*.gif 32bit/doc/*.png
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man1/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/5.1
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/5.1
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/include/*


%changelog
* Mon Mar 26 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.1.5-1
- update to version - 5.1.5

* Wed Feb 11 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.1.4
- Initial port for AIX
