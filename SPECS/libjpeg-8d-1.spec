Summary:       A library for manipulating JPEG image format files
Name:          libjpeg
Version:       8d
Release:       1
License:       IJG
Group:         System Environment/Libraries
URL:           http://www.ijg.org/
Source0:       http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz
Source1:       %{name}.so.62-aix32
Source2:       %{name}.so.62-aix64
Source3:       %{name}.so.7-aix32
Source4:       %{name}.so.7-aix64
Patch0:        %{name}-%{version}-aix.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: patch

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

The library is available as 32-bit and 64-bit.


%package devel
Summary:  Development tools for programs which will use the libjpeg library
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q -n jpeg-%{version}
%patch0


%build
# setup environment for 32-bit and 64-bit builds
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make 

cp ./.libs/%{name}.so.8 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ./.libs/%{name}.a ./%{name}.so.8

# Add the older version 6b shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} %{name}.so.62
/usr/bin/strip -X32 -e %{name}.so.62
/usr/bin/ar -X32 -q ./.libs/%{name}.a %{name}.so.62
cp %{SOURCE2} %{name}.so.62
/usr/bin/strip -X64 -e %{name}.so.62
/usr/bin/ar -X64 -q ./.libs/%{name}.a %{name}.so.62

cp %{SOURCE3} %{name}.so.7
/usr/bin/strip -X32 -e %{name}.so.7
/usr/bin/ar -X32 -q ./.libs/%{name}.a %{name}.so.7
cp %{SOURCE4} %{name}.so.7
/usr/bin/strip -X64 -e %{name}.so.7
/usr/bin/ar -X64 -q ./.libs/%{name}.a %{name}.so.7


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
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
%defattr(-,root,system)
%doc README usage.txt
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man?/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc example.c %{name}.txt structure.txt
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 8d-1
- Update to version 8d

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 8c-2
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 8c-1
- Initial port on Aix5.3
