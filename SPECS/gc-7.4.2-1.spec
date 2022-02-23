
%define _libdir64 %{_prefix}/lib64

Summary: A garbage collector for C and C++ 
Name:    gc	
Version: 7.4.2
Release: 1
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/	
Source0: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Boehm-Demers-Weiser conservative garbage collector can be 
used as a garbage collecting replacement for C malloc or C++ new.


%package devel
Summary: Libraries and header files for %{name} development 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)

%build
# see bugzilla.redhat.com/689877
export CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN"

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export STRIP="i/usr/bin/strip -X64"

export CC="/usr/vac/bin/xlc -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
export CXX="/usr/vacpp/bin/xlC -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "

cd 64bit
# first build the 64-bit version
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=64
export M4=/usr/linux/bin/m4 
autoreconf -vif
automake --add-missing 
CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-threads=aix \
    --enable-shared --disable-static \
    --with-libatomic-ops=no
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version

# see bugzilla.redhat.com/689877
export CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN"

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"
export STRIP="/usr/bin/strip -X32"

export CC="/usr/vac/bin/xlc  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX="/usr/vacpp/bin/xlC  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

#export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
export M4=/usr/linux/bin/m4
autoreconf -vif
automake --add-missing

CONFIG_SHELL=/bin/bash /bin/bash -x ./configure \
    --prefix=%{_prefix} \
    --enable-threads=aix \
    --enable-shared --disable-static \
    --with-libatomic-ops=no
gmake %{?_smp_mflags}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
make install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
touch .libs/libcord.aU libcord.aU
touch .libs/libcord.aT libcord.aT
make install DESTDIR=${RPM_BUILD_ROOT}

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
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so*

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
cp doc/gc.man ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3

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

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,system,-)
%doc 32bit/doc/README
%doc 32bit/doc/README.changes 32bit/doc/README.contributors
%doc 32bit/doc/README.environment 32bit/doc/README.linux
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*

%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/*.html
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_mandir}/man?/*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la

%changelog
* Fri Sep 18 2015 Pascal Oliva <pascal.oliva@atos.net> - 7.4.2-1
- Update to version 7.4.2

* Thu Nov 04 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 6.8-1
- First port on Aix6.1
