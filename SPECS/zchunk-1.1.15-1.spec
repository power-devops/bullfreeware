# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:           zchunk
Version:        1.1.15
Release:        1
Summary:        Compressed file format that allows easy deltas
License:        BSD and MIT
URL:            https://github.com/zchunk/zchunk
Source0:        https://github.com/zchunk/zchunk/archive/%{version}/%{name}-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

Patch0:		%{name}-1.1.15-meson-adapt-to-AIX.patch
Patch1:		%{name}-1.1.15-python3-path.patch
Patch2:		%{name}-1.1.15-lib-remove-endian.h-for-AIX.patch
Patch3:		%{name}-1.1.15-zck_gen_zdict-remove-stdout-as-variable-name.patch

BuildRequires:  gcc
BuildRequires:  libzstd-devel
BuildRequires:  curl-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:	argp-standalone-devel

Requires:       %{name}-libs = %{version}-%{release}
Provides:       bundled(buzhash-urlblock) = 0.1
Requires:	curl >= 7.65.1
Requires:	argp-standalone

%description
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

%package libs
Summary: Zchunk library

%description libs
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the zchunk library, libzck.

%package devel
Summary: Headers for building against zchunk
Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description devel
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the headers necessary for building against the zchunk
library, libzck.

%prep

# echo "##########################################################"
# echo " This might needs to be built as root user due to nina posix spawn failure" 
# echo "##########################################################"
# # TODO: Need to analyse why ninja fails with no root user

%autosetup -p1
# Remove bundled sha libraries
rm -rf src/lib/hash/sha*

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
# export AR="/usr/bin/ar -X32_64"
# export NM="/usr/bin/nm -X32_64"

export CFLAGS_COMMON="-I/opt/freeware/include"

build_zchunk(){
    meson setup builddir \
	  --prefix=/opt/freeware \
	  --libdir=$1 \
	  -Dwith-openssl=enabled \
	  -Dwith-zstd=enabled

    ninja -v -C builddir
}

cd 64bit
# first build the 64-bit version
export CC="gcc"
export CFLAGS="-maix64 $CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -L/usr/lib -L/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_zchunk %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc"
export CFLAGS="-maix32 $CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-L/opt/freeware/lib -L/usr/lib -L/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_zchunk %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
DESTDIR=${RPM_BUILD_ROOT} ninja -v -C builddir install

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)

cd ../32bit
export OBJECT_MODE=32
DESTDIR=${RPM_BUILD_ROOT} ninja -v -C builddir install
cd ..

# Only provide 64bit version for commands.
(
    # Replace 32bit command by 64bit version
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _64)
    do
	mv ${f}_64 ${f}
    done
)

mkdir -p %{buildroot}%{_libexecdir}
install 64bit/contrib/gen_xml_dictionary %{buildroot}%{_libexecdir}/zck_gen_xml_dictionary

(
    %define libsoversion 1
    %define libname libzck

    # Install only provide .so for now.
    # Moreover, the binaries are linked with libzck.so.1.1.15. Thus, it must
    # be kept until either meson or ninja is fixed. Only the 64bit version.
    # TODO: fix it

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{libname}.a ${RPM_BUILD_ROOT}%{_libdir}/%{libname}.so.%{libsoversion}
    ${AR} -q %{libname}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir}/%{libname}.so*
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.1

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/%{libname}.a %{libname}.a
)

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(ninja -v -C builddir test|| true)

cd ../32bit
(ninja -v -C builddir test|| true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 64bit/README.md 64bit/contrib
%{_bindir}/zck*
%{_bindir}/unzck
%{_libexecdir}/zck_gen_xml_dictionary

%files libs
%defattr(-,root,system,-)
%license 64bit/LICENSE
%doc 64bit/README.md
%{_libdir}/libzck.a
%{_libdir64}/libzck.a
%{_libdir64}/libzck.so.%{version}

%files devel
%defattr(-,root,system,-)
%doc 64bit/zchunk_format.txt
%{_includedir}/zck.h

%changelog
* Wed Aug 11 2021 Clément Chigot <clement.chigot@atos.net> - 1.1.15-1
- Update to vrsion 1.1.15
- BullFreeware Compatibility Improvements

* Mon Jan 20 2020 Sangamesh Mallayya <smallayy@in.ibm.com> - 1.1.4-1
- Initial port to AIX.

* Sat Jan 18 2020 Jonathan Dieter <jdieter@gmail.com> - 1.1.5-1
- Fix small bug in corner case when handling write failures

* Wed Nov 13 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.4-1
- Fix download failure when web server doesn't include content-type with each
  range

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 19 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.2-2
- Fix multipart range handling to work with quotes, fixes #1706627
- Fix file creation permissions so they respect umask
- Actually push new sources

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.1.1-3
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.1-2
- Fix compilation on GCC 4.4.7 so it builds on EL6
- Add missing sources
- Also, zchunk will now automatically do all your taxes

* Sat Mar 23 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.0-1
- Optimize chunk matching while downloading, significantly reducing CPU usage

* Sat Mar 16 2019 Jonathan Dieter <jdieter@gmail.com> - 1.0.4-1
- Fix multipart boundary bug when dealing with lighttpd servers

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jonathan Dieter <jdieter@gmail.com> - 1.0.3-1
- Fix several memory leaks and use-after-frees

* Fri Dec 28 2018 Jonathan Dieter <jdieter@gmail.com> - 1.0.2-1
- Use hash table for finding identical chunks, speeding up process considerably
- Add test case to verify that identical chunk checking is working

* Sat Dec 22 2018 Jonathan Dieter <jdieter@gmail.com> - 1.0.0-1
- 1.0 release.  API/ABI stability is now guaranteed

* Sun Dec 09 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.17-1
- Turn off some tests for big-endian architectures since zstd isn't
  deterministic on them

* Sat Dec 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.16-1
- Add zck_gen_zdict binary to generate optimal zdict for a zchunk file
- Add functions to API to simplify extracting a single chunk
- Change default zstd compression to 9 for a 6x speed increase in compression
  speed for a 5% increase in compression size

* Tue Nov 13 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.15-1
- Switch from optional flags to more robust optional elements

* Thu Nov 01 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.14-1
- Sanity check hex hashes passed in as an option

* Mon Oct 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.13-1
- Add read support for zchunk files with optional flags
- Fix tests for zstd-1.3.6

* Fri Sep 28 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.11-1
- Fix small bug where creating a zck_dl context fails when zck context is NULL

* Tue Sep 18 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.10-1
- Update to 0.9.10
- Fixes security bugs found by Coverity

* Fri Aug 10 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.7-2
- Add contrib scripts to docs
- Fix test failures for zstd <= 1.3.4
- Add gen_xml_dictionary to libexecdir with zck_ prefix

* Wed Aug 01 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.5-1.1
- Update to 0.9.4
- Fix failing tests on ppc64, ppc64le, arm7, and s390x
- Fix intermittent parallel test failures
- Add upstream patch to fix tests against zstd-1.3.4

* Tue Jul 31 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.3-1
- Update to 0.9.3
- Fix intermittent bug where auto-chunking wasn't deterministic

* Mon Jul 30 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.2-1
- Update to 0.9.2
- Set minimum and maximum chunk sizes for both automatic and
  manual chunking
- New tests
- ABI (but not API change) - Use bool from stdbool.h
- Allow specification of output file in zck

* Wed Jul 25 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.1-1
- Update to 0.9.1
- New error handling functions
- File format changes
- API changes
- Proposed permanent stable ABI
- Fix Rawhide build error

* Thu Jul 12 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.6-1
- Update to 0.7.6
- SHA-512 and SHA-512/128 support
- New default chunk checksum type SHA-512/128
- Automatic chunking moved into libzck and is now default
- New option to disable automatic chunking
- Bugfixes

* Wed Jul 04 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.5-4
- Fix ldconfig scriptlets to run on libs package
- Rename zchunk-libs-devel to zchunk-devel
- Add BR: gcc
- Explicitly enable zstd and openssl support
- Simplify file globs

* Tue Jul 03 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.5-1
- Split libs into separate package
- Fix license
- Provide bundled buzhash
- Fix punctuation
- Simplify source0 using url macro
- Remove bundled sha library and add dependency on OpenSSL

* Mon Jul 02 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.4-2
- Add zchunk format definition to -devel documentation

* Fri Jun 22 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.4-1
- Add --stdout argument to unzck
- Use meson native versioning rather than manual header and fix
  pkgconfig output

* Tue Jun 12 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.2-1
- Rename zck_get_dl_range to zck_get_missing_range because it
  was too similar to the unrelated zck_dl_get_range function

* Mon Jun 11 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.1-1
- New functions in the library

* Fri Jun 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.0-1
- Massive API rework in preparation for ABI stability guarantee

* Wed Jun 06 2018 Jonathan Dieter <jdieter@gmail.com> - 0.6.2-1
- Header and API cleanup
- Fix warnings

* Tue Jun 05 2018 Jonathan Dieter <jdieter@gmail.com> - 0.6.0-1
- Massive rework of zckdl utility
- Main library no longer depends on curl, only zckdl utility
- Rework API
- Support for servers that have different maximum ranges in a request

* Thu May 10 2018 Jonathan Dieter <jdieter@gmail.com> - 0.5.2-1
- Add new zck_get_range() function
- Add tests
- Range functions are no longer prefixed with "Range: bytes="

* Wed May 09 2018 Jonathan Dieter <jdieter@gmail.com> - 0.5.0-1
- Command line utilities now provide help and usage examples and take
  proper flags
- Reading a zchunk header no longer automatically reads the dictionary

* Sun Apr 29 2018 Jonathan Dieter <jdieter@gmail.com> - 0.4.0-1
- Next release with incompatible file format changes
- File format has been reworked to allow checking of the header checksum
  without reading full header into memory at once
- Terminology changes for the header

* Fri Apr 20 2018 Jonathan Dieter <jdieter@gmail.com> - 0.3.0-1
- Next release with incompatible file format changes
- File format now supports streams and signatures

* Tue Apr 17 2018 Jonathan Dieter <jdieter@gmail.com> - 0.2.2-1
- First release
- Fix build on EL7
