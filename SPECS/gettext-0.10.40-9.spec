%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define _make %(if test x$MAKE = x ; then echo make; else echo $MAKE; fi)
%define _package_emacs_file %(if test -f %{buildroot}/%{_datadir}/emacs/site-lisp/po-mode.elc ; then echo "%{_datadir}/emacs/site-lisp/po-mode.elc" ; else echo ""; fi)

Summary: 	GNU libraries and utilities for producing multi-lingual messages.
Name: 		gettext
Version: 	0.10.40
Release:	9
License: 	GPL/LGPL
Group: 		Gnome2/Tools
URL: 		http://www.gnu.org/software/gettext/
Source: 	ftp://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.bz2

Patch0:		gettext-0.10.40-aix.patch
Patch1:		gettext-0.10.40-autotools.patch


Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/gettext-0.10.40-aix.patch
$PATCH -p2 -s < %{_sourcedir}/gettext-0.10.40-autotools.patch


%build
PATH=%{_bindir}:$PATH ./configure --disable-shared \
	--with-included-gettext --prefix=%{_prefix}
%{_make}

%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
%{_make} DESTDIR=%{buildroot} install-strip

# make links
cd %{buildroot}
for dir in bin lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%clean

%post
/sbin/install-info %{_infodir}/gettext.info %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gettext.info %{_infodir}/dir
fi

%files
%defattr(-,root,system)
%doc ABOUT-NLS AUTHORS BUGS COPYING DISCLAIM README
%doc NEWS THANKS TODO
%doc %{_prefix}/doc/gettext
%{_bindir}/*
/usr/bin/*
%{_libdir}/*.a
%{_prefix}/64/lib/*.a
/usr/lib/*.a
%{_libdir}/*.la
#%config %{_libdir}/charset.alias
%{_includedir}/*.h
/usr/include/*.h
%{_infodir}/gettext.info*
%{_mandir}/man3/*
%{_datadir}/gettext/intl/*
%{_datadir}/gettext/po/*
%{_datadir}/locale/*/LC_MESSAGES/gettext.mo
%{_datadir}/locale/locale.alias
%{_datadir}/aclocal/*.m4
# if po-mode.elc exists, it is packaged
%{_package_emacs_file}

# These aren't in glibc...
%dir %{_datadir}/locale/en@boldquot
%dir %{_datadir}/locale/en@boldquot/LC_MESSAGES
%dir %{_datadir}/locale/en@quot
%dir %{_datadir}/locale/en@quot/LC_MESSAGES

/usr/share
%changelog
*  Wed Nov 15 2006  BULL
 - Release  9
 - gnome 2.16.1

*  Mon Sep 18 2006  BULL
 - Release  8
 - support 64 bits
 - support 64 bits

*  Tue May 16 2006  BULL
 - Release  7

*  Fri Dec 23 2005  BULL
 - Release 6 
 - Prototype support gtk2 64 bit

*  Wed Nov 16 2005  BULL
 - Release  5
*  Tue Aug 09 2005  BULL
 - Release  4
 - Create symlinks between /usr/share and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  3
 - .o removed from lib
*  Tue Nov 23 2004  BULL
 - Release  2

