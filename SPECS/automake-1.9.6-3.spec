%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

%define api_version 1.9

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.9.6

Release: 3 
License: GPL
Group: Development/Tools
Source0: ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2

Patch0:		automake-1.9.6-aix.patch

URL: http://sources.redhat.com/automake
Requires: perl, autoconf >= 2.58
Buildrequires: autoconf >= 2.58, flex, bison
Prereq: /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Automake is an experimental Makefile generator. Automake was inspired
by the 4.4BSD make and include files, but aims to be portable and to
conform to the GNU standards for Makefile variables and targets.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles. If you install Automake, you will also need to install
GNU's Autoconf package.

%prep
%setup -q -n automake-%{version}
perl -pi -e's,^tar.test ,,' tests/Makefile.am

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/automake-1.9.6-aix.patch



%build
PATH=%{_bindir}:$PATH ./configure
%{_make}
%{_make} check 

%install
if test "%{buildroot}" != "/"; then
  rm -rf %{buildroot}
fi

# make links
cd %{buildroot}
for dir in bin share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%makeinstall
rm -f %{buildroot}%{_infodir}/dir

# create this dir empty so we can own it
mkdir -p %{buildroot}%{_datadir}/aclocal

%clean
#rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/info/*.info*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
/usr/share
/usr/bin/*
%changelog
*  Tue May 16 2006  BULL
 - Release  3

*  Tue Nov 15 2005  BULL
 - Release  2

*  Mon Nov 14 2005  BULL
 - Release  1
 - New version  version: 1.9.6

