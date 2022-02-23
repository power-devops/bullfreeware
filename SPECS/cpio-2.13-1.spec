
%bcond_without dotests

# compiler default gcc
# NO MORE SUPPORTED
# To use gcc : --define 'gcc_compiler 1'
# To use xlc : --define 'gcc_compiler 0'
# 
# %{?gcc_compiler:%define gcc_compiler 0}
# %{!?gcc_compiler:%define gcc_compiler 1}

%{!?optimize:%define optimize 2}

Summary: A GNU archiving program
Name: cpio
Version: 2.13
Release: 1
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2.sig
Source2: %{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64

BuildRequires: info

Requires: gettext
Requires: /sbin/install-info, info

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following arch*ive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

# %if %{gcc_compiler} == 1
# This version has been compiled with GCC.
# %else
# This version has been compiled with XLC.
# %endif



%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "optimize=%{optimize}"

%setup -q

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export MAKE="gmake --trace"
export GLOBAL_CC_OPTIONS=" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

# Choose XLC or GCC
# %if %{gcc_compiler} == 1
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

# %else
# 
# # XLC specific (do NOT compile yet...)
# export CC__="/usr/vac/bin/xlc"
# 
# export CXX__="/usr/vacpp/bin/xlC"
# export FLAG32="-q32 -qcpluscmt"
# export FLAG64="-q64 -qcpluscmt"
# 
# echo "CC Version:"
# $CC__ -qversion
# 
# %endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-bnoipath"

./configure \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-largefile \
    --disable-mt

$MAKE %{?_smp_mflags}
cd ..
# END : build on 64bit mode

# build on 32bit mode
cd 32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-bnoipath"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-largefile \
    --disable-mt

$MAKE %{?_smp_mflags}
cd ..
# END : build on 64bit mode


%install
export MAKE="gmake --trace"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# gzip --best ${RPM_BUILD_ROOT}%{_infodir}/%{name}*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)

cd -

cd 32bit
export OBJECT_MODE=32
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/%{name}*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -s "$fic"_64 $fic
    done
)

cd -

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
cd usr/linux/bin
ln -sf ../../..%{_bindir}/* .

%check
export MAKE="gmake --trace"
%if %{with dotests}
cd 64bit
$MAKE -k check || true
cd ../32bit
$MAKE -k check || true
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/NEWS 32bit/README 32bit/THANKS 32bit/TODO 32bit/COPYING
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*info*


%changelog
* Fri Jan 31 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.13-1
- New version 2.13

* Mon Nov 21 2016 Jean Girardet <jean.girardet@atos.net> - 2.12-2
- updated to version 2.12 from perzl version 2.11-2

* Thu Jul 01 2010 Michael Perzl <michael@perzl.org> - 2.11-2
- removed dependency on gettext >= 0.17

* Thu Apr 22 2010 Michael Perzl <michael@perzl.org> - 2.11-1
- updated to version 2.11

* Tue Jul 14 2009 Michael Perzl <michael@perzl.org> - 2.10-1
- updated to version 2.10

* Wed Mar 26 2008 Michael Perzl <michael@perzl.org> - 2.9-1
- first version for AIX V5.1 and higher
