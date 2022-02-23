Summary: A terminal handling library
Name: ncurses
Version: 5.9
Release: 3
License: MIT
Group: System Environment/Libraries
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/%{name}-%{version}.tar.gz
Source1: ftp://invisible-island.net/ncurses/%{name}-%{version}.tar.gz.asc

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

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
%setup -q


%build
export RM="/usr/bin/rm -f"
# hack to get shared libraries working on AIX
find . -name Makefile.in -exec /opt/freeware/bin/sed -i 's/@OBJEXT@/lo/' {} \;

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc -q64"
export CXX="/usr/vacpp/bin/xlC -q64"

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
    $*
}

configurencurses
make 

(
  for library in libncurses libpanel libmenu libform libncurses++
  do
	cp ./lib/.libs/${library}.so.5 .
  done
)
make clean
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc"
export CXX="/usr/vacpp/bin/xlC"

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
    $*
}

configurencurses
make


%install
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  for library in libncurses libpanel libmenu libform libncurses++
  do
	rm -f ./lib/.libs/${library}.a
	${AR} -rv ./lib/.libs/${library}.a ./lib/.libs/${library}.so.5 ${library}.so.5 
	rm -f ${RPM_BUILD_ROOT}/%{_libdir}/${library}.a
	cp ./lib/.libs/${library}.a  ${RPM_BUILD_ROOT}%{_libdir}
  done
)

(cd $RPM_BUILD_ROOT

 for dir in bin lib include share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/share
 cd usr/share
 ln -sf ../..%{_datadir}/* .
 cd -

 mkdir -p usr/linux/include
 cd usr/linux/include
 ln -sf ../../..%{_includedir}/ncurses .
 cd -

 mkdir -p usr/linux/bin
 cd usr/bin
 mv captoinfo clear infocmp infotocap reset tic tput tset ../../usr/linux/bin
 cd -

 mkdir -p usr/linux/lib
 cd usr/linux/lib
 ln -sf ../../..%{_libdir}/* .
)


%files
%defattr(-,root,system)
%doc ANNOUNCE AUTHORS README TO-DO
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
%doc doc/html/hackguide.html doc/html/ncurses-intro.html c++/README*
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
* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 13 2011 Gerard Visiedo <gerard.visiedo@bull.net - 5.9-1
- Initial port on Aix 5.3

