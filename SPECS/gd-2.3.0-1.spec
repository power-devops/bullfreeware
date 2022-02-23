# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, 64 bit versions of utilities
%define default_bits 64


# requested by https://bugzilla.redhat.com/1468338
# this break gdimagefile/gdnametest:
#   gdimagefile/gdnametest.c:122: 255 pixels different on /tmp/gdtest.CrpdIb/img.gif
#   gdimagefile/gdnametest.c:122: 255 pixels different on /tmp/gdtest.CrpdIb/img.GIF
#   FAIL gdimagefile/gdnametest (exit status: 2)


Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.3.0
Release:       1
License:       MIT
URL:           http://libgd.github.io/
Source0:       https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz

# Missing, temporary workaround, fixed upstream for next version
# Source1:     https://raw.githubusercontent.com/libgd/libgd/gd-%{version}/config/getlib.sh
Source1:       gd-%{version}-getlib.sh

%define _libdir64 %{_prefix}/lib64

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: freetype2-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
#BuildRequires: libwebp-devel     - Not available on AIX
#BuildRequires: libimagequant-devel   - Not available on AIX
#BuildRequires: libraqm-devel     - Not available on AIX
# AIX provides LPPs for X11
#BuildRequires: libX11-devel
#BuildRequires: libXpm-devel      - AIX has an LPP version /usr/lpp/X11/lib/R7
BuildRequires: zlib-devel
BuildRequires: pkg-config
BuildRequires: libtool
#BuildRequires: perl-interpreter
#BuildRequires: perl-generators
BuildRequires: perl(perl)
# for fontconfig/basic test       - Not available on AIX
#BuildRequires: liberation-sans-fonts


%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.

The library is available as 32-bit and 64-bit.
This version has been compiled with GCC.


%package progs
Requires:       %{name} = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.


%package devel
Summary:  The development libraries and header files for gd
Requires: %{name} = %{version}-%{release}
Requires: freetype2-devel
Requires: fontconfig-devel
Requires: libjpeg-devel
Requires: libpng-devel
Requires: libtiff-devel
#Requires: libwebp-devel            - Not available on AIX
# AIX provides LPPs for X11
#Requires: libX11-devel
#Requires: libXpm-devel             - Not available on AIX
Requires: zlib-devel
#Requires: libimagequant-devel      - Not available on AIX
#Requires: libraqm-devel            - Not available on AIX

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.


%prep

echo "dotests=%{dotests}"

%setup -q -n libgd-%{version}

install -m 0755 %{SOURCE1} config/getlib.sh

# brpm displays ERROR for /usr/bin/perl in bdftogd - should be a patch ?
sed -i '1s/perl/env perl/' ./src/bdftogd

# : $(perl config/getver.pl)

# : regenerate autotool stuff
# if [ -f configure ]; then
#    libtoolize --copy --force
#    autoreconf -vif
# else
#    ./bootstrap.sh
# fi

# Duplicate source for 32 & 64 bits
rm -rf /tmp/libgd-%{version}-32bit
mkdir  /tmp/libgd-%{version}-32bit
mv *   /tmp/libgd-%{version}-32bit
mkdir 32bit
mv     /tmp/libgd-%{version}-32bit/* 32bit
rm -rf /tmp/libgd-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/



%build

# Provide a correct default font search path
#CFLAGS="$RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"\
#/usr/share/fonts/bitstream-vera:\
#/usr/share/fonts/dejavu:\
#/usr/share/fonts/default/Type1:\
#/usr/share/X11/fonts/Type1:\
#/usr/share/fonts/liberation\"'"

# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1359680
# Not sure Linux only TBC   export CFLAGS="$CFLAGS -ffp-contract=off"
# This is a W/A for FAIL in gdimagecopyresampled/bug00201 - fail also in AIX


# setup environment for 32-bit and 64-bit builds only using GCC
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS=" -O2 -ffp-contract=off"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"


export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.

# first build the 64-bit version
export OBJECT_MODE=64
cd 64bit

export CC="${CC64}"
export LDFLAGS="-pthread"

./bootstrap.sh

# options --enable-shared & --enable-static are by default
# Fedora includes --disable-rpath

./configure \
  --prefix=/opt/freeware \
  --with-tiff=/opt/freeware \
  --with-webp=no

gmake %{?_smp_mflags}


# now build the 32-bit version
export OBJECT_MODE=32
cd ../32bit

export CC="${CC32}"
export LDFLAGS="-pthread -Wl,-bmaxdata:0x80000000"

./bootstrap.sh

./configure \
  --prefix=/opt/freeware \
  --with-tiff=/opt/freeware \
  --with-webp=no

gmake %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libgd.a ../64bit/src/.libs/libgd.so.3




%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit

gmake install DESTDIR="$RPM_BUILD_ROOT"

rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.a
mv $RPM_BUILD_ROOT/%{_libdir} $RPM_BUILD_ROOT/%{_libdir64}

(

  cd ${RPM_BUILD_ROOT}/%{_bindir}

  # strip and move 64 bit binaries
  for file in *
  do
    /usr/bin/strip -X64 $file > /dev/null 2>&1 || true
    mv $file "$file"_64
  done
  cd -

)

cd ../32bit

gmake install DESTDIR="$RPM_BUILD_ROOT"

(

  cd ${RPM_BUILD_ROOT}/%{_bindir}

  # strip and move 32 bit binaries
  for file in `ls * | grep -v '_64'`
  do
    /usr/bin/strip -X32 $file > /dev/null 2>&1 || true
    mv $file "$file"_32
  done
  cd -
)

# Add symlinks for commands without _32/_64 suffix
DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi

(
  cd ${RPM_BUILD_ROOT}%{_bindir}

  for file in `ls *_${DEFAULT_BITS}`
  do
    ln -s ${file} `echo ${file} | sed -e "s/_${DEFAULT_BITS}$//"`
  done
  cd -
)

# Add symlinks in _libdir64 and /usr
(
  cd ${RPM_BUILD_ROOT}/%{_libdir64}
  ln -s ../lib/libgd* .
  cd -

  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -s ../..%{_prefix}/${dir}/* .
    cd -
  done

  # may not be in RPM
  mkdir -p usr/lib64
  cd usr/lib64
  ln -s ../../%{_libdir64}/* .
  cd -

)




%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Test freetype/bug00132 fails in 32 & 64 bit runs  - To be analysed
#   freetype/bug00132.c:34: Total pixels changed: 9 with a maximum channel
#                                                       difference of 255.
#   freetype/bug00132.c:36: Reference image and destination differ
#
#
# Test gdimageline/gdimageline_bug5 fails in 32 & 64 bit run with core sigsegv
#      due to resource limit ==> needs ulimit -d 195000
#      32 bit version was completing ok with default 131072, if the value
#      is not changed (increased then decreased)
#
# Tests
#    gdimagestring16/gdimagestring16
#    gdimagestringup16/gdimagestringup16
# fail in 64 bit run but pass in 32 bits due to wchar_t == short/int 32/64 bits
#
# Fedora labels these 2 tests, plus gdimagestringft/gdimagestringft_bbox
# as XFAIL, but the latter passes on AIX 6.1 :
# # minor diff in size
# XFAIL_TESTS="gdimagestringft/gdimagestringft_bbox"
# %ifarch s390x
# XFAIL_TESTS="gdimagestring16/gdimagestring16 gdimagestringup16/gdimagestringup16 $XFAIL_TESTS"
# %endif


ulimit -d 195000
for testdir in 64bit  32bit
do
    cd $testdir
    ( gmake  check || true )
    /usr/sbin/slibclean
    cd ..
done


# : Check content of pkgconfig  - Fedora specific ?
# grep %{version} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdlib.pc


# %ldconfig_scriptlets


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
# %{!?_licensedir:%global license %%doc}
%license 32bit/COPYING
# %{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir64}/*.a
/usr/lib/*.a
/usr/lib64/*.a

%files progs
%defattr(-,root,system)
%{_bindir}/*
# %exclude %{_bindir}/gdlib-config*
# List from Bull 2.1.1
# %{_bindir}/bdftogd
# %{_bindir}/gd2copypal
# %{_bindir}/gd2togif
# %{_bindir}/gd2topng
# %{_bindir}/gdcmpgif
# %{_bindir}/gdparttopng
# %{_bindir}/gdtopng
# %{_bindir}/giftogd2
# %{_bindir}/pngtogd
# %{_bindir}/pngtogd2
# %{_bindir}/webpng
# /usr/bin/bdftogd
# /usr/bin/gd2copypal
# /usr/bin/gd2togif
# /usr/bin/gd2topng
# /usr/bin/gdcmpgif
# /usr/bin/gdparttopng
# /usr/bin/gdtopng
# /usr/bin/giftogd2
# /usr/bin/pngtogd
# /usr/bin/pngtogd2
# /usr/bin/webpng
# List on Linux 2.2.5
# /usr/bin/annotate
# /usr/bin/bdftogd
# /usr/bin/gd2copypal
# /usr/bin/gd2togif
# /usr/bin/gd2topng
# /usr/bin/gdcmpgif
# /usr/bin/gdparttopng
# /usr/bin/gdtopng
# /usr/bin/giftogd2
# /usr/bin/pngtogd
# /usr/bin/pngtogd2
# /usr/bin/webpng



%files devel
%defattr(-,root,system)
# %{_bindir}/gdlib-config*
# /usr/bin/gdlib-config
# /usr/include/*
# %{_libdir}/*.la
# /usr/lib/*.la
%{_includedir}/*
# %{_libdir}/*.so
# %{_libdir}/pkgconfig/gdlib.pc


%changelog
* Wed Apr 08 2020 Michael Wilson <michael.a.wilson@atos.net> - 2.3.0-1
- Update to 2.3.0 based on Fedora 32
- gdlib-config is deprecated in favour of pkg-config (AIX ?)

* Thu Apr 02 2020 Michael Wilson <michael.a.wilson@atos.net> - 2.2.5-1
- Update to 2.2.5
- Rebuild on laurel2, RPM v4 with brpm, exclusively GCC
- Modifications based on Fedora 2.2.5-12.fc32

* Thu Feb 25 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.1.1-1
- Updated to version 2.1.1

* Thu May 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.0.35-6
- Build on Aix6.1

* Tue Apr 27 2010 Michael Perzl <michael@perzl.org> - 2.0.35-5
- recompiled thread-safe with cc_r

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 2.0.35-4
- some minor spec file fixes

* Sat Mar 29 2008 Michael Perzl <michael@perzl.org> - 2.0.35-3
- changed to FreeType version 2

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 2.0.35-2
- included both 32-bit and 64-bit shared objects

* Fri Sep 28 2007 Michael Perzl <michael@perzl.org> - 2.0.35-1
- first version for AIX V5.1 and higher

