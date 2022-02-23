# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

# Current .so version is 2.9.4, but may need to use just 2 TCB
%define soversion 2.9.4


Name:           http-parser
Version:        2.9.4
Release:        1
Summary:        HTTP request/response parser for C

License:        MIT
URL:            https://github.com/nodejs/http-parser
Source0:        https://github.com/nodejs/http-parser/archive/v%{version}/%{name}-%{version}.tar.gz

Source10:       %{name}-%{version}-%{release}.build.log

# https://github.com/nodejs/http-parser/pull/483
Patch0001:      http-parser-0001-url-treat-empty-port-as-default.patch

Patch2:         http-parser-aixbuild.patch
# struct http_parser ends with void *data; 4 or 8 bytes, but 8 byte aligned ?
# https://github.com/nodejs/http-parser/issues/526
#Patch3:         http-parser-aix32build.patch
Patch3:         http-parser-aix-sizeof-voidStar.patch

# BuildRequires:  meson
BuildRequires:  gcc

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).

%package devel
Summary:        Development headers and libraries for http-parser
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Development headers and libraries for http-parser.



%prep
%autosetup -p1


# %%ifarch %{arm}
# # https://github.com/nodejs/http-parser/issues/507
# sed -i -e "/sizeof(http_parser)/d" test.c
# %%endif

# TODO: try to send upstream?
# cat > meson.build << EOF
# project('%{name}', 'c', version : '%{version}')
# install_headers('http_parser.h')
# foreach x : [['http_parser',        ['-DHTTP_PARSER_STRICT=0']],
#              ['http_parser_strict', ['-DHTTP_PARSER_STRICT=1']]]
#   lib = library(x.get(0), 'http_parser.c',
#                 c_args : x.get(1),
#                 version : '%{version}',
#                 install : true)
#   test('test-@0@'.format(x.get(0)),
#        executable('test-@0@'.format(x.get(0)), 'test.c',
#                   c_args : x.get(1),
#                   link_with : lib),
#        timeout : 60)
# endforeach
# EOF

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

# %meson
# %meson_build

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"

export FLAG32="-maix32 -pthread"
export FLAG64="-maix64 -pthread"

# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC__} ${FLAG64}"
export CXX="${CXX__} ${FLAG64}"
# export LDFLAGS=" -Wl,-bbigtoc -L/opt/freeware/lib64:/opt/freeware/lib:/usr/lib "


# There is no configuration phase
#  The Makefile has targets test with HTTP_PARSER_STRICT=1 / 0
#    test: test_g test_fast
#    test_g: http_parser_g.o test_g.o
#    test_fast: http_parser.o test.o http_parser.h
#  And a target library with HTTP_PARSER_STRICT=0
#      But Fedora has meson build to make a library with HTTP_PARSER_STRICT=1
#    library: libhttp_parser.o
#    libhttp_parser.o: http_parser.c http_parser.h Makefile


# This will build and run test      gmake %{?_smp_mflags} test
gmake %{?_smp_mflags} library

# mv libhttp_parser.so libhttp_parser_strict.so


# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC__} ${FLAG32}"
export CXX="${CXX__} ${FLAG32}"
# export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-bbigtoc -L/opt/freeware/lib:/usr/lib"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000"


# This will build and run test      gmake %{?_smp_mflags} test
gmake %{?_smp_mflags} library


# mv libhttp_parser.so libhttp_parser_strict.so




%install

# %meson_install

export AR="/usr/bin/ar"
export LN="/usr/bin/ln -s"
export RM="/usr/bin/rm"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"

export FLAG32="-maix32 -pthread"
export FLAG64="-maix64 -pthread"


[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


cd 64bit
export OBJECT_MODE=64
export CC="${CC__} ${FLAG64}"
export CXX="${CXX__} ${FLAG64}"
export LDFLAGS=" -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


# Target install will rebuild target library
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix}  install

mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


cd ../32bit
export OBJECT_MODE=32
export CC="${CC__} ${FLAG32}"
export CXX="${CXX__} ${FLAG32}"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix}  install


# The 32 bit libraries have been created containing (.2 & 2.9.4 on Fedora)
#     libhttp_parser.a[libhttp_parser.so.2.9.4]  and
#     libhttp_parser_strict.a[libhttp_parser_strict.so.2.9.4]

# Add the 64 bit library member
(
 cd  ${RPM_BUILD_ROOT}
 $AR -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libhttp_parser.a ./%{_libdir}/libhttp_parser.so.%{soversion}
 $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libhttp_parser.a ./%{_libdir64}/libhttp_parser.so.%{soversion}
#  $AR -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libhttp_parser_strict.a ./%{_libdir}/libhttp_parser_strict.so.%{soversion}
#  $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libhttp_parser_strict.a ./%{_libdir64}/libhttp_parser_strict.so.%{soversion}
)

# Create lib64/libhttp_parser.a symlink to lib/libhttp_parser.a
$RM -f ${RPM_BUILD_ROOT}%{_libdir64}/libhttp_parser.a
$LN  ../lib/libhttp_parser.a ${RPM_BUILD_ROOT}%{_libdir64}/libhttp_parser.a





%check

# %meson_test

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"

export FLAG32="-maix32 -pthread"
export FLAG64="-maix64 -pthread"

cd 64bit
export OBJECT_MODE=64
export CC="${CC__} ${FLAG64}"
export CXX="${CXX__} ${FLAG64}"


# This will build and run tests
  (gmake test  || true)


cd ../32bit
export OBJECT_MODE=32
export CC="${CC__} ${FLAG32}"
export CXX="${CXX__} ${FLAG32}"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000"


# This will build and run tests
  (gmake test  || true)



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,system)
%license 32bit/LICENSE-MIT
%doc 32bit/AUTHORS 32bit/README.md
%{_libdir}/libhttp_parser.a
%{_libdir64}/libhttp_parser.a
# %{_libdir}/libhttp_parser_strict.a
# %{_libdir64}/libhttp_parser_strict.a
# %{_libdir}/libhttp_parser.so.*
# %{_libdir}/libhttp_parser_strict.so.*

%files devel
%defattr(-,root,system)
%{_includedir}/http_parser.h
# %{_libdir}/libhttp_parser.so
# %{_libdir}/libhttp_parser_strict.so

%changelog
* Fri Nov 27 2020 Michael Wilson <michael.a.wilson@atos.com> - 2.9.4-1
- Initial port on AIX, based on Fedora 33 without meson build

