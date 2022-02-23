%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define libxml2_version 2.6.23
%define _make %(if test x$MAKE = x ; then echo make ; else echo $MAKE ; fi)

Name: 		docbookx
Version: 	4.1.2
Release: 	7
Group: 		Applications/Text
Summary: 	XML document type definition for DocBook 4.1.2
License: 	IBM_ILA
URL: 		http://www.oasis-open.org/docbook/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
# BuildArch:	noarch
Source:         http://www.oasis-open.org/docbook/xml/4.1.2/%{name}-%{version}.tar.bz2

Patch0:		docbookx-4.1.2-aix.patch

PreReq: libxml2 >= %{libxml2_version}

# PreReq: xml-common fileutils
# PreReq: textutils grep perl

%description
DocBookX is an XML version of the DocBook DTD.
DocBook is an SGML DTD (document type definition). DTDs define how the
markup tags in SGML documents should be interpreted. DocBook is well
suited for the creation of books and papers about computer hardware
and software.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/docbookx-4.1.2-aix.patch


%build

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
%{_make} INSTALL_PATH=%{buildroot}%{_prefix} install-dtd
PATH=%{_bindir}:$PATH DATADIR=%{buildroot}%{_datadir}/xml/ \
SYSCONFDIR=%{buildroot}%{_sysconfdir}/xml/ ./buildDocBookCatalog
mkdir -p %{buildroot}%{_bindir}
cp -f buildDocBookCatalog %{buildroot}%{_bindir}

# Make the links
cd %{buildroot}
for dir in bin share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr (-,root,system)
%doc *.txt ChangeLog LICENSE
%{_datadir}/xml/docbook/xml-dtd-%{version}/*
%attr (755, root, root) %{_bindir}/*

%attr (755, root, root) /usr/bin/*
/usr/share

%post
export PATH=%{_bindir}:$PATH
DATADIR=%{_prefix}/share/xml SYSCONFDIR=%{_prefix}/etc/xml ${SHELL} %{_bindir}/buildDocBookCatalog >/dev/null

%changelog
*  Thu Nov 17 2005  BULL
 - Release  7
*  Tue Aug 09 2005  BULL
 - Release  6
 - Create symlinks between /usr/share and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  5
 - .o removed from lib
*  Tue Nov 23 2004  BULL
 - Release  4

*  Fri Jul 02 2004  BULL
 - Release  3

