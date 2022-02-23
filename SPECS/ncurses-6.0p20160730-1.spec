%define ncurses_version 6.0
%define ncurses_patch_date 20160730
%global MY_ABI 6

Summary: A terminal handling library
Name: ncurses
Version: %{ncurses_version}p%{ncurses_patch_date}
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/%{name}-%{ncurses_version}.tar.gz
Source1: %{name}-%{version}-%{release}.build.log
Source2: ftp://invisible-island.net/ncurses/%{version}/%{name}-%{ncurses_version}-20160423-patch.sh.bz2
Source3: ftp://invisible-island.net/ncurses/%{version}/%{name}-%{ncurses_version}-20160423-patch.sh.bz2.asc
Source4: %{name}-%{ncurses_version}-librairies.tar.gz
Patch20160507:    %{name}-%{ncurses_version}-20160507.patch
Patch20160514:    %{name}-%{ncurses_version}-20160514.patch
Patch20160521:    %{name}-%{ncurses_version}-20160521.patch
Patch20160528:    %{name}-%{ncurses_version}-20160528.patch
Patch20160604:    %{name}-%{ncurses_version}-20160604.patch
Patch20160611:    %{name}-%{ncurses_version}-20160611.patch
Patch20160618:    %{name}-%{ncurses_version}-20160618.patch
Patch20160625:    %{name}-%{ncurses_version}-20160625.patch
Patch20160702:    %{name}-%{ncurses_version}-20160702.patch
Patch20160709:    %{name}-%{ncurses_version}-20160709.patch
Patch20160723:    %{name}-%{ncurses_version}-20160723.patch
Patch20160730:    %{name}-%{ncurses_version}-20160730.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

# Build does not work for now with libtool > 1.5.26-4
BuildRequires: libtool = 1.5.26-4

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.


%package devel
Summary: Development files for the ncurses library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.


%prep
echo "###########
# WARNING #
###########
 Some libraries from this package will be built agains the currently installed libncurses.a !
 To ensure the libraries in the final package are properly linked, you must build a first version of the package, install it and then build again !
###########
# WARNING #
###########"
sleep 30

%setup -q -n %{name}-%{ncurses_version}

export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.

# first cumulative patch is a shell script
/bin/bzip2 -dc  %SOURCE2 > patch.%{name}-%{ncurses_version}.tmp.$$.sh
chmod +x  patch.%{name}-%{ncurses_version}.tmp.$$.sh
./patch.%{name}-%{ncurses_version}.tmp.$$.sh
rm -f ./patch.%{name}-%{ncurses_version}.tmp.$$.sh
 
%patch20160507 -p1
%patch20160514 -p1
%patch20160521 -p1
%patch20160528 -p1
%patch20160604 -p1
%patch20160611 -p1
%patch20160618 -p1
%patch20160625 -p1
%patch20160702 -p1
%patch20160709 -p1
%patch20160723 -p1
%patch20160730 -p1

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/
# */

# Extract old shared objects, to be added to new archive
mkdir lib_so_5
cd lib_so_5
cp %SOURCE4 .
gzip -d *.tar.gz
tar -xf $(basename *.tar)
/usr/bin/strip -X32 -e *.so.5.aix32
/usr/bin/strip -X64 -e *.so.5.aix64
cd -

%build
export PATH=/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export RM="/usr/bin/rm -f"
# hack to get shared libraries working on AIX
find . -name Makefile.in -exec /opt/freeware/bin/sed -i 's/@OBJEXT@/lo/' {} \;

# setup environment for 32-bit and 64-bit builds
export CONFIG_SHELL=/bin/sh
export CONFIGURE_ENV_ARGS=/bin/sh

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"

# shell function to configure ncurses
configurencurses() {
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --without-ada \
    --without-normal \
    --without-debug \
    --with-shared \
    --with-libtool \
    --enable-hard-tabs \
    --enable-xmc-glitch \
    --enable-colorfgbg \
    --disable-static \
    $*
}

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CFLAGS="-maix64"
export CXXFLAGS=${CFLAGS}

configurencurses
make 
cd ..

# now build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CFLAGS=""
export CXXFLAGS=${CFLAGS}

configurencurses
make
cd ..

%install
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# first install the 64 bit version
cd 64bit
export OBJECT_MODE=64
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

# Rename binary files to _64
for file in `ls -1 ${RPM_BUILD_ROOT}%{_bindir}`; do
    mv ${RPM_BUILD_ROOT}%{_bindir}/${file} ${RPM_BUILD_ROOT}%{_bindir}/${file}_64
done

# Extract shared 64 bits shared objects from archives
for library in libncurses libpanel libmenu libform libncurses++; do
    /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir}/${library}.a ${library}.so.6 
done

# now install the 32 bits version
# first install the 64 bit version
cd 32bit
export OBJECT_MODE=32
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

# Add the 64 bits shared objects and older versions to archives
for library in libncurses libpanel libmenu libform libncurses++; do
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/${library}.a ${library}.so.6
    mv lib_so_5/${library}.so.5.aix64 ${library}.so.5
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/${library}.a ${library}.so.5
    mv lib_so_5/${library}.so.5.aix32 ${library}.so.5
    /usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/${library}.a ${library}.so.5
done

# strip binaries
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || true
# */

(cd $RPM_BUILD_ROOT

 for dir in bin lib include share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    # */
    cd -
 done

 mkdir -p usr/share
 cd usr/share
 ln -sf ../..%{_datadir}/* .
 # */
 cd -

 mkdir -p usr/linux/include
 cd usr/linux/include
 ln -sf ../../..%{_includedir}/ncurses .
 cd -

 mkdir -p usr/linux/bin
 cd usr/bin
 mv captoinfo clear infocmp infotocap reset tic tput tset tabs ../../usr/linux/bin
 cd -

 mkdir -p usr/linux/lib
 cd usr/linux/lib
 ln -sf ../../..%{_libdir}/* .
 # */
)

%files
%defattr(-,root,system)
%doc 32bit/ANNOUNCE 32bit/AUTHORS 32bit/README 32bit/TO-DO
%{_bindir}/[cirt]*
%{_libdir}/*.a
%{_libdir}/terminfo
%{_datadir}/terminfo
%{_datadir}/tabset
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
/usr/bin/*
/usr/lib/*.a
/usr/share/tabset
/usr/share/terminfo
/usr/linux/bin/*
/usr/linux/lib/*.a


%files devel
%defattr(-,root,system)
%doc 32bit/doc/html/hackguide.html 32bit/doc/html/ncurses-intro.html 32bit/c++/README*
%{_bindir}/ncurses*-config
%dir %{_includedir}/ncurses
%{_includedir}/ncurses/*.h
%{_libdir}/*.la
%{_mandir}/man3/*
/usr/lib/*.la
/usr/include/ncurses
/usr/linux/include/*
/usr/linux/lib/*.la


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Aug 01 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> -6.0p2016O730-1
- updated with all patches until 20160730

* Wed Jun 01 2016 Reshma V Kumar <reskumar@in.ibm.com> -6.0-1
- updated to latest version

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 13 2011 Gerard Visiedo <gerard.visiedo@bull.net - 5.9-1
- Initial port on Aix 5.3

