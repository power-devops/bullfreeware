# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%{!?gcc_compiler: %define gcc_compiler 1} # Switch to GCC build
%{!?default_bits: %define default_bits 64}

Summary:        Netscape Portable Runtime
Name:           nspr
Version:        4.30
Release:        1
License:        MPLv2.0
URL:            https://www.mozilla.org/projects/nspr/
Group:          System Environment/Libraries

# BuildRoot:      %{_tmppath}/%{name}-%{version}-root

# Sources available at https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-%{release}.build.log

# BuildRequires:  autoconf
# BuildRequires:  sed

Patch1:         nspr-4.28-aixbuild.v2.patch

# Not active by default
%bcond_with dlopen_trace
# Some trace for dlopen. Very useful for finding the name of dlopen(name)
# Needs the same in nss
Patch2:         nspr-4.30-dlopen-name.patch

%description
NSPR provides platform independence for non-GUI operating system
facilities. These facilities include threads, thread synchronization,
normal file and network I/O, interval timing and calendar time, basic
memory management (malloc and free) and shared library linking.

The library is available as 32-bit and 64-bit.

%package devel
Summary:        Development libraries for the Netscape Portable Runtime
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header files for doing development with the Netscape Portable Runtime.

The library is available as 32-bit and 64-bit.

%prep
%setup -q

%patch1 -p1 -b .aixGCCbuild

%if %{with dlopen_trace}
# Some trace for dlopen
%patch2 -p1 -b .dlopen-name
%endif

mkdir 32bit
cp -rp nspr 32bit
cp -rp 32bit 64bit


%build

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# DSO_LDOPTS is set in configure.in (and thus configure) to :
#    -brtl -bnortllib -bM:SRE -bnoentry -bexpall -blibpath:/usr/lib:/lib
# At least bexpall should be removed, also bnortllib and blibpath corrected :
#    -brtl -bM:SRE -bnoentry -blibpath:/opt/freeware/lib:/usr/lib:/lib
# Change added to aixbuild.patch

# setup environment for 32-bit and 64-bit builds

build_nspr() {
    # Need following to display build trace
    set -x
    export AR="/usr/bin/ar -X${OBJECT_MODE}"
    LIBDIR=%{_libdir}
    ENABLE_64=--disable-64bit
    if [ "${OBJECT_MODE}" == "64" ]; then
        LIBDIR=%{_libdir}64
        ENABLE_64=--enable-64bit        
    fi
    if [ "${OBJECT_MODE}" == "32" ]; then
        # Compiling with GCC 32bit build requires linking with libgcc/libgcc_s
        # for 64bit div/mod functions  __divdi3/__moddi3/__udivdi3/__umoddi3
        export LDFLAGS=" -L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 "
        # export LDFLAGS=" -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib "
        # Remove -Wl, options because ld errors, link edit redone later
        export LDFLAGS=" -L/opt/freeware/lib "
    fi
    cd ${OBJECT_MODE}bit/nspr
    # The percent signs are interpreted by RPM, use a simple date stamp
    # echo `date +%Y%m%d_%H%M%S `" : Starting ${OBJECT_MODE}bit build"
    echo `date`" : Starting ${OBJECT_MODE}bit build"
    # export CC="/usr/vac/bin/xlc_r -q${OBJECT_MODE}"
    export CC="gcc -maix${OBJECT_MODE}"
    export CFLAGS=" -maix${OBJECT_MODE}"
    export CXX="g++ "
    export CXXFLAGS=" -maix${OBJECT_MODE}"
    # export DSO_LDOPTS="-brtl -bM:SRE -bnoentry -blibpath:/opt/freeware/lib:/usr/lib:/lib"
    # The configure.in CC test patch requires running autoconf (may be not,
    # because the patch is modified to fix configure as well ?)
    # autoconf

    # sed -i '/-bexpall/s?DSO_LDOPTS.*$?DSO_LDOPTS="-brtl -bM:SRE -bnoentry -blibpath:/opt/freeware/lib:/usr/lib:/lib"?' ./configure

    LDFLAGS=$LDFLAGS LIBS=$LIBS ./configure \
        --prefix=%{_prefix} \
        --libdir=${LIBDIR} \
        --includedir=%{_includedir}/nspr4 \
        ${ENABLE_64} --disable-debug

    gmake %{?_smp_mflags}


    # Re-build shared objects for AIX with libpath and maxdata
    # Initially done just in nspr/dist/lib, but %%install is performed in
    # nspr/lib/ds, nspr/lib/libc/src & nspr/pr/src and -bexpall has been removed

    echo $PWD
    cd dist/lib
    echo $PWD

    export XLCCPATH="/opt/IBM/xlc/13.1.3/bin"

    for lib in nspr4 plc4 plds4
    do
	/usr/bin/dump -X${OBJECT_MODE} -Hv             lib${lib}.so
#	/usr/bin/dump -X${OBJECT_MODE} -Tv             lib${lib}.so
	         ${RM}                     lib${lib}.a
	         ${AR}                 -q  lib${lib}.a lib${lib}.so 
#	         ${AR}                 tv  lib${lib}.a
    done

    cd ../..

    # echo `date +%Y%m%d_%H%M%S `" : ${OBJECT_MODE}bit build completed"
    echo `date`" : ${OBJECT_MODE}bit build completed"
    
    # echo `date +%Y%m%d_%H%M%S `" : Re-Build ${OBJECT_MODE}bit tests"
    echo `date`" : Re-Build ${OBJECT_MODE}bit tests"
    cd pr/tests
    if [ "${OBJECT_MODE}" == "32" ]; then
      export LDFLAGS=" -L/opt/freeware/lib -bmaxdata:0x80000000 "
    fi
    gmake
    cd -
    # echo `date +%Y%m%d_%H%M%S `" : ${OBJECT_MODE}bit tests re-built"
    echo `date`" : ${OBJECT_MODE}bit tests re-built"

    cd ../..
}

export OBJECT_MODE=64
build_nspr

export OBJECT_MODE=32
build_nspr



%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export OBJECT_MODE=64
cd ${OBJECT_MODE}bit
echo `date`" : Starting ${OBJECT_MODE}bit tests"

# Run test suite.
perl ./nspr/pr/tests/runtests.pl 2>&1 | tee output.log

TEST_FAILURES=`grep -c FAILED ./output.log` || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s) - see file ./output.log"
  exit 1
fi
echo `date`" : ${OBJECT_MODE}bit tests completed"
cd ..


export OBJECT_MODE=32
cd ${OBJECT_MODE}bit
echo `date`" : Starting ${OBJECT_MODE}bit tests"

# Run test suite.
perl ./nspr/pr/tests/runtests.pl 2>&1 | tee output.log

TEST_FAILURES=`grep -c FAILED ./output.log` || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s) - see file ./output.log"
  exit 1
fi
echo `date`" : ${OBJECT_MODE}bit tests completed"
cd ..




%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit/nspr
gmake install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
mv ${RPM_BUILD_ROOT}%{_bindir}/nspr-config ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_64


cd 32bit/nspr
gmake install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
mv ${RPM_BUILD_ROOT}%{_bindir}/nspr-config ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_32

chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_64
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_32

DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi
ln -sf nspr-config_${DEFAULT_BITS} ${RPM_BUILD_ROOT}%{_bindir}/nspr-config

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar"

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64

# add the shared objects to the libraries already containing
# the 32-bit objects
for file in libnspr4 libplc4 libplds4
do
	# First, remove lib*.a(<FILES>.o) before adding lib*.so files
	${RM}         ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${RPM_BUILD_ROOT}%{_libdir}64/${file}.a

	${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${RPM_BUILD_ROOT}%{_libdir}64/${file}.so
	${AR} -q -X32 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${RPM_BUILD_ROOT}%{_libdir}/${file}.so

	# Check made for stripped .so files
	strip -e -X32 ${RPM_BUILD_ROOT}%{_libdir}/${file}.so
	strip -e -X64 ${RPM_BUILD_ROOT}%{_libdir}64/${file}.so
done


#	# add the 64-bit objects to the libraries already containing
#	# the 32-bit objects and shared objects
#	for file in libnspr4 libplc4 libplds4
#	do
#	    mkdir $file
#	    cd $file
#		${AR} -x -X64 ${RPM_BUILD_ROOT}%{_libdir}64/${file}.a
#		${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a *.o
#	done


(
  cd ${RPM_BUILD_ROOT}%{_libdir}64

  for file in libnspr4 libplc4 libplds4
  do
    # ln -sf %{_libdir}/${file}.a .
    # Check made for link ../lib/libxxx.a
    ln -sf ../lib/${file}.a .
  done
)

# No more
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


%files
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir}64/*.a
%{_libdir}64/*.so*
# No more
#	# /usr/lib/*.a
#	# /usr/lib/*.so*
#	# /usr/lib64/*.a
#	# /usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_bindir}/nspr-config*
%{_includedir}/*
%{_datadir}/aclocal/*
#	/usr/bin/nspr-config*
#	/usr/include/*


%changelog
* Mon Apr 19 2021 Tony Reix <tony.reix@atos.net> - 4.30-1
- Update to version 4.30
- Clean the mess in lib*.a

* Wed Sep 16 2020 Michael Wilson <michael.a.wilson@atos.net> - 4.28-1
- Update to version 4.28
- Correction to DSO_LDOPTS in configure.in/configure for libpath/expall/nortllib
- Apply an export list to .so libs installed from nspr/lib/ds,
-   nspr/lib/libc/src, nspr/pr/src to replace the removed -bexpall
- Remove call to autoconf
- Exclude links in /usr

* Tue Jun 25 2019 Michael Wilson <michael.a.wilson@atos.net> - 4.21-2
- Switch to GCC build
- Add library libgcc_s (libgcc) to ld command for 64 bit div/mod functions
-       __divdi3/__moddi3/__udivdi3/__umoddi3  generated in 32 bit build
- Switch to RPM version 4 build environment

* Tue Apr 09 2019 Michael Wilson <michael.a.wilson@atos.net> - 4.21-1
- Update to version 4.21

* Fri Oct 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 4.13-1
- Update to version 4.13

* Wed Jun 29 2016 Tony Reix <tony.reix@bull.net> 4.12-1
- Update to 4.12 version
- Add symlink from lib to lib64 for .a files
- No tests are available

* Fri Feb 22 2013 Gerard Visiedo <gerard.visiedo@bul.net> 4.9.5-1
- update to 4.9.5 version

* Mon Mar 26 2012 Patricia Cugny <patricia.cugny@bull.net> 4.9-1
- update to 4.9

* Wed Feb 18 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.7.3
- Initial port for AIX

