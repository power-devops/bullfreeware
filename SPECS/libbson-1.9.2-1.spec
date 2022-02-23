Name:       libbson
Version:    1.9.2
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
# Do not install COPYING, install ChangeLog, distribution specific
Patch0:     %{name}-1.5.0-rc3-Install-documentation-according-to-guidelines.patch
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
BuildRequires:  %{_bindir}/sphinx-build
# Modified (with bson allocator and some warning fixes and huge indentation
# refactoring) jsonsl is bundled <https://github.com/mnunberg/jsonsl>.
# jsonsl upstream likes copylib approach and does not plan a release
# <https://github.com/mnunberg/jsonsl/issues/14>.
Provides:       bundled(jsonsl)

%description
This is a library providing useful routines related to building, parsing,
and iterating BSON documents <http://bsonspec.org/>.

%package devel
Summary:    Development files for %{name}
License:    ASL 2.0
Group:     System Environment/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains libraries and header files needed for developing
applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
# Remove pregenerated documentation
rm -rf doc/html/_static doc/html/*.{html,inv,js} doc/man/*.3
# Generate build scripts from sources
autoreconf --force --install

%build
export RM="/usr/bin/rm -f"

# Switching experimental-features support changes ABI (bson_visitor_t type)
%configure \
    --disable-coverage \
    --disable-debug \
    --disable-debug-symbols \
    --enable-examples \
    --enable-extra-align \
    --disable-html-docs \
    --enable-libtool-lock \
    --disable-lto \
    --disable-maintainer-flags \
    --disable-man-pages \
    --disable-optimizations \
    --enable-shared \
    --disable-silent-rules \
    --disable-static \
    --enable-tests
# Explicit man target is needed for generating manual pages.
# If you produced HTML pages be ware doc/conf.py injects tracking JavaScript
# code (search for add_ga_javascript function).
make %{?_smp_mflags} all doc/man

(make -k %{?_smp_mflags} check || true)


%install
[ "${RPM_BUILD_ROOT}" == "" ] && exit 1

echo ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}
find ${RPM_BUILD_ROOT} -name '*.la' -delete
# Install examples here because it's forbidden to use relative %%doc with
# installing into %%_pkgdocdir
install -d -m 0755 ${RPM_BUILD_ROOT}%{_docdir}/%{name}-devel/examples
install -m 0644 -t ${RPM_BUILD_ROOT}%{_docdir}/%{name}-devel/examples examples/*.c


#%check
#make %{?_smp_mflags} check

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
#%license COPYING THIRD_PARTY_NOTICES
# AUTHORS is empty, README etc. are installed by "make install"
#%{_docdir}/%{name}
%{_libdir}/*.a

%files devel
#%{_docdir}/%{name}-devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/cmake
%{_libdir}/pkgconfig
#%{_mandir}/man3/*

%changelog
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
