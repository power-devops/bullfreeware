%define libarchive_version 13
%define libarchive_fullversion 13.4.2
# The full version is significant as each new version may add symbols

%define name libarchive
%define version 3.4.2
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%bcond_without dotests

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %global gcc_compiler 1}


%define _libdir64 %{_prefix}/lib64


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A library for handling streaming archive formats
Group:          System Environment/Libraries

License:        BSD
URL:            https://www.libarchive.org/
Source0:        https://www.libarchive.org/downloads/%{name}-%{version}.tar.gz


Source10: %{name}-%{version}-%{release}.build.log

Patch1:         libarchive-3.3.3-dirfd.patch

BuildRequires:  libtool
BuildRequires:  libxml2-devel >= 2.9.10-1
BuildRequires:  xz-devel      >= 5.2.4-1
BuildRequires:  zlib-devel    >= 1.2.11-3
Requires:       libxml2 >= 2.9.10-1
Requires:       xz      >= 5.2.4-1
Requires:       zlib    >= 1.2.11-3

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

The library is available as 32-bit and 64-bit.

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

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif



%package -n bsdtar
Summary:        Manipulate tape archives
Group:          Development/Utility
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n bsdcpio
Summary:        Copy files to and from archives
Group:          Development/Utility
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.


%package -n bsdcat
Summary:        Expand files to standard output
Group:          Development/Utility
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcat
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe.  In both cases decompressed data it written to
standard output.


%prep
# %autosetup -p1
%setup -q
%patch1 -p1 -b .Dirfd

echo "dotests=%{with dotests}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif



# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

/usr/bin/env | /usr/bin/sort

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
# export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/usr/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export LDFLAGS=" -lpthreads -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"


# %configure --disable-static --disable-rpath

./configure -v --prefix=%{_prefix} \
               --infodir=%{_infodir} \
               --localedir=%{_datadir}/locale \
               --mandir=%{_mandir} \
               --disable-static \
               --enable-shared \
               --disable-rpath


# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

gmake %{?_smp_mflags} --trace



# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -lpthreads -Wl,-blibpath:/opt/freeware/lib:/usr/lib"

./configure -v --prefix=%{_prefix} \
               --infodir=%{_infodir} \
               --localedir=%{_datadir}/locale \
               --mandir=%{_mandir} \
               --disable-static \
               --enable-shared \
               --disable-rpath

# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

gmake %{?_smp_mflags} --trace


# Archive 64 bit shared object in 32 bit shared library

slibclean
${AR} -q .libs/libarchive.a ../64bit/.libs/libarchive.so.%{libarchive_version}

slibclean

strip -e -X32_64     .libs/libarchive.so.%{libarchive_version} ../64bit/.libs/libarchive.so.%{libarchive_version}


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"
# export RM="/usr/bin/rm -f"

# Install 64 bit
cd 64bit
export OBJECT_MODE=64


gmake install DESTDIR=$RPM_BUILD_ROOT


# Add libarchive.so.13 and libarchive.so & .so.13.3.3 - they may be required
mkdir    ${RPM_BUILD_ROOT}%{_libdir64}
install -p .libs/libarchive.so.%{libarchive_version} ${RPM_BUILD_ROOT}%{_libdir64}/libarchive.so.%{libarchive_version}
ln -sf  libarchive.so.%{libarchive_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libarchive.so
ln -sf  libarchive.so.%{libarchive_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libarchive.so.%{libarchive_fullversion}



find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f "$RPM_BUILD_ROOT%{_libdir}"/*.la

# Move lib to lib64 - lib64 has already been created above
mv  ${RPM_BUILD_ROOT}/%{_libdir}/*  ${RPM_BUILD_ROOT}/%{_libdir64}


# Install 32 bit
cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR="$RPM_BUILD_ROOT"


# Add libarchive.so.13 and libarchive.so & .so.13.3.3 - they may be required
install -p .libs/libarchive.so.%{libarchive_version} ${RPM_BUILD_ROOT}%{_libdir}/libarchive.so.%{libarchive_version}
ln -sf  libarchive.so.%{libarchive_version}     ${RPM_BUILD_ROOT}%{_libdir}/libarchive.so
ln -sf  libarchive.so.%{libarchive_version}     ${RPM_BUILD_ROOT}%{_libdir}/libarchive.so.%{libarchive_fullversion}

# Following is done in case a future version is incompatible
mv    ${RPM_BUILD_ROOT}%{_libdir}/libarchive.a ${RPM_BUILD_ROOT}%{_libdir}/libarchive-%{libarchive_fullversion}.a
ln -s libarchive-%{libarchive_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libarchive.a


# Remove the 64 bit libarchive.a, because it will be a link to lib/libarchive.a
rm    ${RPM_BUILD_ROOT}%{_libdir64}/libarchive.a
ln -s ../lib/libarchive.a ${RPM_BUILD_ROOT}%{_libdir64}/libarchive.a


find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



# rhbz#1294252 - this function relies onbash features
replace ()
{
    filename=$1
    file=`basename "$filename"`
    binary=${file%%.*}
    pattern=${binary##bsd}

    awk "
        {
            pat = \"${pattern}\" ;
            bin = \"${binary}\" ;
            PAT = toupper(pat) ;
            BIN = toupper(bin) ;
        }
        # replace the .Dt topic to .Dt bsdtopic
        # ksh does not recognise  ${pattern^^}  (uppercase)
        /^.Dt .* 1/ {
            print \".Dt \"BIN\" 1\";
            next;
        }
        # replace the first occurence of \"$pattern\" by \"$binary\"
        !stop && /^.Nm $pattern/ {
            print \".Nm $binary\" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    " "$filename" > "$filename.new"
    mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
    installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
    # replace "$installed_manpage"
    echo "$installed_manpage"

    case $manpage in
    bsdtar.1)
      pat=tar;
      bin=bsdtar;
      PAT=TAR;
      BIN=BSDTAR;
      ;;
    bsdcpio.1)
      pat=cpio;
      bin=bsdcpio;
      PAT=CPIO;
      BIN=BSDCPIO;
      ;;
    esac

    awk "
        # replace the .Dt topic to .Dt bsdtopic
        /^.Dt $PAT 1/ {
            print \".Dt $BIN 1\";
            next;
        }
        # replace the first occurence of tar by bsdtar
        !stop && /^.Nm $pat/ {
            print \".Nm $bin\" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    " "$installed_manpage" > "$installed_manpage.new"
    mv "$installed_manpage".new "$installed_manpage"
done


%check
# Currently there are XXX tests
%if %{with dotests}

logfiles ()
{
    find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
    cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
    for i in `logfiles`
    do
        echo "=== $i ==="
        cat "$i"
    done
}

run_testsuite ()
{
    rc=0
    LIBPATH=`pwd`/.libs gmake check -j1 || {
        # error happened - try to extract in koji as much info as possible
        cat_logs

        for i in `tempdirs`; do
            if test -d "$i" ; then
                find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
                cat $i/*.log
            fi
        done
        return 1
    }
    cat_logs
}

# On a ppc/ppc64 is some race condition causing 'make check' fail on ppc
# when both 32 and 64 builds are done in parallel on the same machine in
# koji.  Try to run once again if failed.

# On AIX, too space consuming to run it 4 times.
# Morevoer, logs are too long and verbose on AIX (500 Mo for 64 bit only).
# Just run gmake check by default.
cd 64bit
export OBJECT_MODE=64
# run_testsuite
(gmake -k check || true)
cd ../32bit
export OBJECT_MODE=32
# run_testsuite
(gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/COPYING
%doc 32bit/NEWS 32bit/README.md
%{_libdir}/libarchive.a
%{_libdir}/libarchive-%{libarchive_fullversion}.a
%{_libdir64}/libarchive.a
# %{_libdir}/libarchive.so.13*
# %{_libdir64}/libarchive.so.13*
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*

%files devel
%defattr(-,root,system,-)
%{_includedir}/*.h
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*
# %{_libdir}/libarchive.so
%{_libdir}/pkgconfig/libarchive.pc
# %{_libdir64}/libarchive.so
%{_libdir64}/pkgconfig/libarchive.pc

%files -n bsdtar
%defattr(-,root,system,-)
%doc 32bit/COPYING
%doc 32bit/NEWS 32bit/README.md
%{_bindir}/bsdtar
%{_mandir}/*/bsdtar*

%files -n bsdcpio
%defattr(-,root,system,-)
%doc 32bit/COPYING
%doc 32bit/NEWS 32bit/README.md
%{_bindir}/bsdcpio
%{_mandir}/*/bsdcpio*

%files -n bsdcat
%defattr(-,root,system,-)
%doc 32bit/COPYING
%doc 32bit/NEWS 32bit/README.md
%{_bindir}/bsdcat
%{_mandir}/*/bsdcat*


%changelog
* Tue Apr 21 2020 ??tienne Guesnet <etienne.guesnet.external@atos.net> - 3.4.2-1
- New version 3.4.2
- Stop providing .so
- Add requires

* Thu Apr 16 2020 ??tienne Guesnet <etienne.guesnet.external@atos.net> - 3.3.3-2
- Bullfreeware OpenSSL removal
- Activate check by default

* Wed Jan 02 2019 Michael Wilson <michael.a.wilson@atos.com> - 3.3.3-1
- Initial port on AIX, inspired by Fedora

