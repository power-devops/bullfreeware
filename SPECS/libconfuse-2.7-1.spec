Name:           libconfuse
Version:        2.7
Release:        1
Summary:        A configuration file parser library

Group:          System Environment/Libraries
License:        LGPL
URL:            http://www.nongnu.org/confuse/
Source0:        http://download.savannah.nongnu.org/releases/confuse/confuse-%{version}.tar.gz
Source1:        http://download.savannah.nongnu.org/releases/confuse/confuse-%{version}.tar.gz.sig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  pkg-config, flex

%description
libConfuse is a configuration file parser library, licensed 
under the terms of the LGPL, and written in C. It supports 
sections and (lists of) values (strings, integers, floats, 
booleans or other sections), as well as some other features 
(such as single/double-quoted strings, environment variable 
expansion, functions and nested include statements). It 
makes it very easy to add configuration file capability to 
a program using a simple API.

The goal of libConfuse is not to be the configuration file 
parser library with a gazillion of features. Instead, it 
aims to be easy to use and quick to integrate with your code. 

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
Development files for %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q -n confuse-%{version}


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-nls
make

cp src/.libs/libconfuse.so.0 .
make distclean

# now build the 32-bit version
export CC=/usr/vac/bin/xlc_r
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-nls
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libconfuse.a ./libconfuse.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

# Install man pages
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3/
cp -p doc/man/man3/*.3 ${RPM_BUILD_ROOT}%{_mandir}/man3/
chmod 644 ${RPM_BUILD_ROOT}%{_mandir}/man3/*

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
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
%doc ABOUT-NLS AUTHORS NEWS README
%doc doc/html
%{_libdir}/*.a
%{_mandir}/man?/*.*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc examples/ftpconf.c examples/ftp.conf
%doc examples/simple.c examples/simple.conf
%doc examples/reread.c examples/reread.conf
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/libconfuse.pc
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Mar 23 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.7-1
- Initial port on Aix6.1
