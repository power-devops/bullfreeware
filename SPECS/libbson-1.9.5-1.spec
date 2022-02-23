
%{!?gcc_compiler: %define gcc_compiler 0}
%{!?dotests: %define dotests 1}

%define gcc_compiler 1


%define _libdir64 %{_prefix}/lib64


%if 0%{?__isa_bits} == 64
%global with_tests   1
%global with_tests   0%{!?_without_tests:1}
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   1
%global with_tests   0%{?_with_tests:1}
%endif



Name:       libbson
Version:    1.9.5
Release:    1%{?dist}
Summary:    Building, parsing, and iterating BSON documents
Group:     System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root




## Installed:
# COPYING:                              ASL 2.0
# THIRD_PARTY_NOTICES:                  other license texts
# src/bson/b64_ntop.h:                  ISC and MIT
# src/bson/b64_pton.h:                  ISC and MIT
# src/bson/bson-md5.h:                  zlib
# src/jsonsl:                           MIT (LICENSE file exists in git)
## Not installed:
# configure:                            FSFUL and GPLv2+ with exceptions
# aclocal.m4:                           FSFULLR
# Makefile.in:                          FSFULLR
# build/autotools/compile:              GPLv2+ with exceptions
# build/autotools/config.guess:         GPLv3+ with exceptions
# build/autotools/config.sub:           GPLv3+ with exceptions
# build/autotools/depcomp:              GPLv2+ with exceptions
# build/autotools/install-sh:           MIT
# build/autotools/ltmain.sh:            GPLv2+ with exceptions
# build/autotools/m4/ax_pthread.m4:     GPLv3+ with exceptions
# build/autotools/m4/ax_check_compile_flag.m4:  GPLv3+ with exceptions
# build/autotools/m4/ax_check_link_flag.m4:     GPLv3+ with exceptions
# build/autotools/m4/libtool.m4:        FSFUL and FSFULLR and GPLv2+ with exceptions
# build/autotools/m4/lt~obsolete.m4:    FSFULLR
# build/autotools/m4/ltoptions.m4:      FSFULLR
# build/autotools/m4/ltsugar.m4:        FSFULLR
# build/autotools/m4/ltversion.m4:      FSFULLR
# build/autotools/missing:              GPLv2+ with exceptions
# build/autotools/install-sh:           MIT and Public Domain
# doc/html/_static/basic.css:           BSD
# doc/html/_static/doctools.js:         BSD
# doc/html/_static/jquery.js:           MIT
# doc/html/_static/jquery-3.1.0.js:     MIT
# doc/html/_static/mongoc.css:          MIT
# doc/html/_static/searchtools.js:      BSD
# doc/html/_static/underscore.js:       MIT
# doc/html/_static/underscore-1.3.1.js: MIT
# doc/html/_static/websupport.js:       BSD
# doc/mongoc-theme/static/mongoc.css_t: MIT
# doc/taglist.py:                       MIT
# src/bson/bson-stdint-win32.h:         BSD


License:    ASL 2.0 and ISC and MIT and zlib
# Upstream GIT will be moved to mongo-c-driver's src/libbson subdirectory
# <https://github.com/mongodb/mongo-c-driver/tree/master/src/libbson>,
# but upstream releses reamins on
# <https://github.com/mongodb/libbson/releases>.
URL:        https://github.com/mongodb/%{name}
Source0:    %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz


# 32bit and 64bit versions of bson-config.h differs about:
#   #define BSON_HAVE_ATOMIC_64_ADD_AND_FETCH  0 or 1
# This is handled by bson-config.h wrapper who includes a 32bit or 64bit version
Source1: bson-config.h

Source1000: %{name}-%{version}-%{release}.build.log


# Do not install COPYING, install ChangeLog, distribution specific
Patch0:     %{name}-1.5.0-rc3-Install-documentation-according-to-guidelines.patch

# Print message when no more memory
Patch1:     %{name}-1.9.4-memory.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
# sphinx-build is executed from a build script. Depend on the executable name
# instead of a package name not to be disturbed by transition to a different
# Python version.
#   /opt/freeware/bin/sphinx-build is provided by python-sphinx on AIX
BuildRequires:  python-sphinx python-pygments python-jinja2 python-docutils
BuildRequires:  %{_bindir}/sphinx-build
# Modified (with bson allocator and some warning fixes and huge indentation
# refactoring) jsonsl is bundled <https://github.com/mnunberg/jsonsl>.
# jsonsl upstream likes copylib approach and does not plan a release
# <https://github.com/mnunberg/jsonsl/issues/14>.

Provides:       bundled(jsonsl)

%description
This is a library providing useful routines related to building, parsing,
and iterating BSON documents <http://bsonspec.org/>.

The database is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary:    Development files for %{name}
License:    ASL 2.0
Group:     System Environment/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains libraries and header files needed for developing
applications that use %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


##################################################################
#                                                                #

#                           %prep                                #
#                                                                #
##################################################################





%prep
# Use BullFreeware patch command !
export PATH=/opt/freeware/bin/:$PATH
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1

# Remove pregenerated documentation
rm -rf doc/html/_static doc/html/*.{html,inv,js} doc/man/*.3

# Generate build scripts from sources
autoreconf --force --install

# ChangeLog file missing in 1.9.5 and required by Makefile
touch ChangeLog

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


############################################################################
#                                                                          #
#                                %build                                    #
#                                                                          #
############################################################################

%build
env

export PATH=/opt/freeware/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java5/jre/bin:/usr/java5/bin

export RM="/usr/bin/rm -f"
export AR=/usr/bin/ar


# Chose GCC or XLC

echo "CC: %{gcc_compiler}"

%if %{gcc_compiler} == 1

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
#export CC__="/usr/vac/bin/xlc"
#export  CC__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export CC__="/opt/IBM/xlc/13.1.3/bin/xlc"       #  13.01.0003.0004

#export CXX__="/usr/vacpp/bin/xlC"
#export CXX__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export CXX__="/opt/IBM/xlC/13.1.0/bin/xlC"     #  13.01.0003.0004

export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

export GLOBAL_CC_OPTIONS="-O2"


############################### 64-bit BEGIN ##############################
# first build the 64-bit version

env

cd 64bit
export LIBPATH=/opt/freeware/lib64:/opt/freeware/lib

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lintl"
export CFLAGS="-I/usr/include -I/opt/freeware/include"

# Switching experimental-features support changes ABI (bson_visitor_t type)
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --disable-coverage \
    --disable-debug \
    --disable-debug-symbols \
    --disable-examples \
    --enable-extra-align \
    --disable-html-docs \
    --disable-man-pages \
    --enable-libtool-lock \
    --disable-lto \
    --disable-maintainer-flags \
    --disable-optimizations \
    --enable-shared \
    --disable-static \
    --disable-silent-rules \
    --enable-tests


# Explicit man target is needed for generating manual pages.
# If you produced HTML pages be ware doc/conf.py injects tracking JavaScript
# code (search for add_ga_javascript function).
make %{?_smp_mflags} all

# This is required for tests since they are launched as:
#	$BUILD/libbson-1.9.4/64bit/.libs/lt-test-libbson --threads --no-fork
#		implying threads
#	There is a recursivity:
#		_bson_iter_validate_document()
#		unnamed block in bson_iter_visit_all()
#		bson_iter_visit_all()
#	which is greater than 39 times and
#	which consumes the stack of threads and generates a weird and random core.
export AIXTHREAD_STK=500000
(make -k %{?_smp_mflags} check || true)

############################### 64-bit END ##############################


############################### 32-bit BEGIN ##############################
# now build the 32-bit version

cd ../32bit
export LIBPATH=/opt/freeware/lib

export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

%if %{gcc_compiler} == 1
        export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib                          -lintl"
%else
        export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lintl"
%endif

export CFLAGS="-I/usr/include -I/opt/freeware/include"

# Switching experimental-features support changes ABI (bson_visitor_t type)
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-coverage \
    --disable-debug \
    --disable-debug-symbols \
    --disable-examples \
    --enable-extra-align \
    --disable-html-docs \
    --disable-man-pages \
    --enable-libtool-lock \
    --disable-lto \
    --disable-maintainer-flags \
    --disable-optimizations \
    --enable-shared \
    --disable-static \
    --disable-silent-rules \
    --enable-tests


# Explicit man target is needed for generating manual pages.
# If you produced HTML pages be ware doc/conf.py injects tracking JavaScript
# code (search for add_ga_javascript function).
make %{?_smp_mflags} all

export AIXTHREAD_STK=500000
(make -k %{?_smp_mflags} check || true)

############################### 32-bit END ##############################


############################################################################
#                                                                          #
#                                %install                                  #
#                                                                          #
############################################################################

%install

# Use BullFreeware find command !
export PATH=/opt/freeware/bin/:$PATH

[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#export MAKE="gmake --trace"
export MAKE="gmake -j14"

echo ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
$MAKE install DESTDIR=${RPM_BUILD_ROOT}
mv ${RPM_BUILD_ROOT}%{_includedir}/libbson-1.0/bson-config.h ${RPM_BUILD_ROOT}%{_includedir}/libbson-1.0/bson-config-ppc${OBJECT_MODE}.h

find ${RPM_BUILD_ROOT} -name '*.la' -delete

# Install examples here because it's forbidden to use relative %%doc with
# installing into %%_pkgdocdir
#install -d -m 0755 ${RPM_BUILD_ROOT}%{_docdir}/%{name}-devel/examples
#install -m 0644 -t ${RPM_BUILD_ROOT}%{_docdir}/%{name}-devel/examples examples/*.c

cd ../32bit
export OBJECT_MODE=32
$MAKE install DESTDIR=${RPM_BUILD_ROOT}
mv ${RPM_BUILD_ROOT}%{_includedir}/libbson-1.0/bson-config.h ${RPM_BUILD_ROOT}%{_includedir}/libbson-1.0/bson-config-ppc${OBJECT_MODE}.h

find ${RPM_BUILD_ROOT} -name '*.la' -delete


cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/libbson-1.0/bson-config.h


cd ..
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libbson-1.0.a
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libbson-1.0.a libbson-1.0.so.0
(
  rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/libbson-1.0.a
  cd        ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s                      %{_libdir}/libbson-1.0.a .
)


#%check
#make %{?_smp_mflags} check

# create link from /usr/bin to /opt/freeware/bin
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


%files
%defattr(-,root,system)
#%license COPYING THIRD_PARTY_NOTICES
# AUTHORS is empty, README etc. are installed by "make install"
#%{_docdir}/%{name}
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
#%{_docdir}/%{name}-devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/cmake
%{_libdir}/pkgconfig
#%{_mandir}/man3/*


%changelog
* Wed May 02 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.9.5-1
- First port on AIX

* Tue Apr 17 2018 Tony Reix <tony.reix@atos.net> - 1.9.4-2
- Add error messages when no more memory

* Thu Apr 12 2018 Tony Reix <tony.reix@atos.net> - 1.9.4-1
- New version

* Wed Apr 11 2018 Tony Reix <tony.reix@atos.net> - 1.9.3-2
- Manage 32/64bit for bson-config.h file

* Wed Apr 04 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.9.3-1
- First port on AIX

* Wed Jan 17 2018 Tony Reix <tony.reix@atos.net> - 1.9.2-1
- First port on AIX

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 1.9.2-1
- 1.9.2 bump

* Wed Jan 10 2018 Petr Pisar <ppisar@redhat.com> - 1.9.1-2
- Fix BSON_STATIC_ASSERT() definition

* Wed Jan 10 2018 Petr Pisar <ppisar@redhat.com> - 1.9.1-1
- 1.9.1 bump

* Thu Dec 21 2017 Petr Pisar <ppisar@redhat.com> - 1.9.0-1
- 1.9.0 bump

* Mon Nov 20 2017 Petr Pisar <ppisar@redhat.com> - 1.8.2-1
- 1.8.2 bump

* Thu Nov 02 2017 Petr Pisar <ppisar@redhat.com> - 1.8.1-1
- 1.8.1 bump

* Fri Sep 15 2017 Petr Pisar <ppisar@redhat.com> - 1.8.0-1
- 1.8.0 bump

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 1.7.0-1
- 1.7.0 bump

* Mon Jul 31 2017 Petr Pisar <ppisar@redhat.com> - 1.7.0-0.5.rc2
- 1.7.0-rc2 bump

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.7.0-0.4.rc1
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Petr Pisar <ppisar@redhat.com> - 1.7.0-0.2.rc1
- 1.7.0-rc1 bump

* Fri Jul 07 2017 Petr Pisar <ppisar@redhat.com> - 1.7.0-0.1.rc0
- 1.7.0-rc0 bump

* Wed May 24 2017 Petr Pisar <ppisar@redhat.com> - 1.6.3-1
- 1.6.3 bump

* Tue Mar 28 2017 Petr Pisar <ppisar@redhat.com> - 1.6.2-1
- 1.6.2 bump

* Tue Mar 07 2017 Petr Pisar <ppisar@redhat.com> - 1.6.1-1
- 1.6.1 bump

* Thu Feb 09 2017 Petr Pisar <ppisar@redhat.com> - 1.6.0-1
- 1.6.0 bump

* Wed Feb 08 2017 Petr Pisar <ppisar@redhat.com> - 1.5.3-2
- Fix undefined behavior exhibiting with GCC 7 (bug #1420440)

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 1.5.3-1
- 1.5.3 bump

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- 1.5.2 bump

* Mon Dec 19 2016 Petr Pisar <ppisar@redhat.com> - 1.5.1-1
- 1.5.1 bump

* Thu Dec 01 2016 Petr Pisar <ppisar@redhat.com> - 1.5.0-1
- 1.5.0 bump

* Fri Nov 18 2016 Petr Pisar <ppisar@redhat.com> - 1.5.0-0.4.rc6
- 1.5.0-rc6 bump

* Fri Nov 04 2016 Petr Pisar <ppisar@redhat.com> - 1.5.0-0.3.rc4
- 1.5.0-rc4 bump

* Thu Oct 20 2016 Petr Pisar <ppisar@redhat.com> - 1.5.0-0.2.rc3
- 1.5.0-rc3 bump

* Thu Oct 13 2016 Petr Pisar <ppisar@redhat.com> - 1.5.0-0.1.rc2
- 1.5.0-rc2 bump

* Wed Sep 21 2016 Petr Pisar <ppisar@redhat.com> - 1.4.1-1
- 1.4.1 bump

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 1.4.0-1
- 1.4.0 bump

* Thu Mar 31 2016 Petr Pisar <ppisar@redhat.com> - 1.3.5-1
- 1.3.5 bump

* Tue Mar 15 2016 Petr Pisar <ppisar@redhat.com> - 1.3.4-1
- 1.3.4 bump

* Mon Feb 15 2016 Petr Pisar <ppisar@redhat.com> - 1.3.3-1
- 1.3.3 bump

* Fri Jan 22 2016 Petr Pisar <ppisar@redhat.com> - 1.3.1-1
- Packaged
