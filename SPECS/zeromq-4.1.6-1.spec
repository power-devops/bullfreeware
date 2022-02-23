# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}
%{?dotests: %define dotests dotests}

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}


%define _libdir64 %{_prefix}/lib64

# %bcond_without pgm

%define zmq_version 5

Name:           zeromq
Version:        4.1.6
Release:        1
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.zeromq.org
# VCS:          git:http://github.com/zeromq/zeromq2.git
Source0:        https://github.com/zeromq/zeromq4-1/releases/download/v%{version}/zeromq-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/zeromq/cppzmq/master/zmq.hpp
Source2:        https://raw.githubusercontent.com/zeromq/cppzmq/master/zeromq.LICENSE

Source10: %{name}-%{version}-%{release}.build.log

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
# BuildRequires:  libsodium-devel

BuildRequires:  glib2-devel
# %if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
# BuildRequires:  e2fsprogs-devel
# BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# %else
# BuildRequires:  libuuid-devel
# %endif
# %if %{with pgm}
# BuildRequires:  openpgm-devel
# BuildRequires:  krb5-devel
# %endif

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package -n cppzmq-devel
Summary:        Development files for cppzmq
Group:          Development/Libraries
License:        MIT
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}


%description -n cppzmq-devel
The cppzmq-devel package contains libraries and header files for
developing applications that use the C++ header files of %{name}.


%prep
%setup -q

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif

cp -a %{SOURCE2} .

# zeromq.x86_64: W: file-not-utf8 /usr/share/doc/zeromq/ChangeLog
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure

# Sed version number of openpgm into configure
%global openpgm_pc $(basename %{_libdir}/pkgconfig/openpgm*.pc .pc)
sed -i "s/openpgm-[0-9].[0-9]/%{openpgm_pc}/g" \
    configure*


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

# Display build environment and currently installed RPM packages
/usr/bin/env
rpm -qa

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"


# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
# export LDFLAGS="-L./.libs -L/opt/freeware/lib"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export CXX__="xlc_r"
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
# export LDFLAGS="-L./.libs -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"
export CXX32="${CXX__} ${FLAG32} -D_LARGE_FILES"
export CXX64="${CXX__} ${FLAG64} -D_LARGE_FILES"


# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

autoreconf -fi
# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure
%configure \
# %if %{with pgm}
#             --with-pgm \
#             --with-libgssapi_krb5 \
# %endif
#             --disable-static  => does not exist, but is default
gmake %{?_smp_mflags} V=1


# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

autoreconf -fi
# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure
%configure \
# %if %{with pgm}
#             --with-pgm \
#             --with-libgssapi_krb5 \
# %endif
#             --disable-static  => does not exist, but is default
gmake %{?_smp_mflags} V=1


# Archive 32 and 64 bit versions into libzmq.a
rm    -f .libs/libzmq.a
${AR} -r .libs/libzmq.a .libs/libzmq.so.%{zmq_version} ../64bit/.libs/libzmq.so.%{zmq_version}
slibclean
strip -e -X32_64           .libs/libzmq.so.%{zmq_version} ../64bit/.libs/libzmq.so.%{zmq_version}


%install

export AR="/usr/bin/ar -X32_64"

rm -rf %{buildroot}

cd 64bit
export OBJECT_MODE=64

gmake install DESTDIR=%{buildroot} INSTALL="install -p"
install -m 644 -p %{SOURCE1} %{buildroot}%{_includedir}/

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la

# add libzmq.so.5 and libzmq.so (not sure if they are required)
mkdir    ${RPM_BUILD_ROOT}%{_libdir64}
install -p ../64bit/.libs/libzmq.so.%{zmq_version} ${RPM_BUILD_ROOT}%{_libdir64}/libzmq.so.%{zmq_version}
ln -sf  libzmq.so.%{zmq_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libzmq.so

mv ${RPM_BUILD_ROOT}%{_libdir}/libzmq.a ${RPM_BUILD_ROOT}%{_libdir64}/libzmq.a

mv ${RPM_BUILD_ROOT}%{_bindir}/curve_keygen ${RPM_BUILD_ROOT}%{_bindir}/curve_keygen_64


# %check
if [ "%{dotests}" == 1 ]
then
  (gmake check V=1 || true)
fi


cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR=%{buildroot} INSTALL="install -p"
install -m 644 -p %{SOURCE1} %{buildroot}%{_includedir}/

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la

# add libzmq.so.5 and libzmq.so (not sure if they are required)
install -p .libs/libzmq.so.%{zmq_version} ${RPM_BUILD_ROOT}%{_libdir}/libzmq.so.%{zmq_version}
ln -sf  libzmq.so.%{zmq_version}     ${RPM_BUILD_ROOT}%{_libdir}/libzmq.so


# %check
if [ "%{dotests}" == 1 ]
then
  (gmake check V=1 || true)
fi


# %post -p /sbin/ldconfig


# %postun -p /sbin/ldconfig



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/MAINTAINERS 32bit/NEWS
# %license COPYING COPYING.LESSER
%doc 32bit/COPYING 32bit/COPYING.LESSER
%{_bindir}/curve_keygen
%{_bindir}/curve_keygen_64
%{_libdir}/libzmq.a
# %{_libdir64}/libzmq.a
%{_libdir}/libzmq.so.%{zmq_version}
%{_libdir64}/libzmq.so.%{zmq_version}

%files devel
%defattr(-,root,system,-)
%{_libdir}/libzmq.so
%{_libdir64}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
# %{_libdir64}/pkgconfig/libzmq.pc
%{_includedir}/zmq*.h

%files -n cppzmq-devel
%defattr(-,root,system,-)
# %license zeromq.LICENSE
%doc 32bit/zeromq.LICENSE
%{_includedir}/zmq.hpp


%changelog
* Tue Mar 07 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.1.6-1
- Initial version

