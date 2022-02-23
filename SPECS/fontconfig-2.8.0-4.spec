%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define freetype_version 2.0.9

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.8.0
Release:	4
License:	MIT
Group:		System Environment/Libraries
Source:		http://cgit.freedesktop.org/fontconfig/snapshot/fontconfig-2.8.0.tar.gz
URL:		http://fontconfig.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
PreReq:		freetype2 >= %{freetype_version}
BuildRequires:	freetype2-devel >= %{freetype_version}

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.

%package devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	freetype2-devel >= %{freetype_version}

%description devel
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.
Install fontconfig-devel if you want to develop programs which will use
fontconfig.

%prep
%setup -q

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"
CC_prev="$CC"
export CC="$CC -q64"

./configure     --enable-shared --disable-static --prefix=%{_prefix}
make

cp src/.libs/lib%{name}.so.1 .
make distclean

# now build the 32-bit version
export CC="$CC_prev"
./configure     --enable-shared --disable-static --prefix=%{_prefix}
make
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/lib%{name}.a ./lib%{name}.so.1


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
make DESTDIR=$RPM_BUILD_ROOT install
(
  cd $RPM_BUILD_ROOT
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%post
# Force regeneration of all fontconfig cache files.
%{_bindir}/fc-cache -f >/dev/null 2>&1

%files
%defattr(-, root, system)
%doc README AUTHORS COPYING
%{_prefix}/etc/fonts/*
%{_bindir}/fc*
%{_libdir}/libfontconfig.a
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
/usr/bin/fc*
/usr/lib/libfontconfig.a

%files devel
%defattr(-, root, system)
%{_libdir}/*.la
/usr/lib/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig/*.h
/usr/include/*
%{_datadir}/doc/fontconfig*
%{_datadir}/man/man3/*

%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  2.8.0-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.8.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo àbull.net> 2.8.0-2
 - Compiling on 3é and 64 bits

*  Wed Nov 26 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.8.0-1
 - Update to version 2.8.0

*  Wed Nov 15 2006  BULL
 - Release 7 
 - gnome 2.16.1

*  Tue Sep 19 2006  BULL
 - Release 6
 - support 64 bit
*  Fri Dec 23 2005  BULL
 - Release 5
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  4
*  Mon May 30 2005  BULL
 - Release  3
 - .o removed from lib
*  Fri Sep 24 2004  BULL
 - Release  2
 - Package the directories /opt/freeware/etc/fonts, /opt/freeware/include/fontconfig and /usr/include/fontconfig along with their contents

