%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define libxml2_version 2.6.23

Summary: 	Library providing the Gnome XSLT engine
Name: 		libxslt
Version: 	1.1.15
Release: 	1
License: 	MIT
Group: 		Development/Libraries
Source: 	ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.bz2

Patch0:		libxslt-1.1.15-aix.patch
Patch1:		libxslt-1.1.15-autotools.patch

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
URL: 		http://xmlsoft.org/XSLT/
Requires: 	libxml2 >= %{libxml2_version}	
BuildRequires: libxml2-devel >= %{libxml2_version}
#BuildRequires: python python-devel
#BuildRequires: libxml2-python
Prefix: %{_prefix}
Docdir: %{_docdir}

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.3.8
installed. The xsltproc command is a command line interface to the XSLT engine

%package devel
Summary:	Libraries, includes, etc. to embed the Gnome XSLT engine
Group: 		Development/Libraries
Requires: 	libxslt = %{version}
Requires: 	libxml2-devel >= %{libxml2_version}

%description devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.3.8
installed.

#%package python
#Summary: Python bindings for the libxslt library
#Group: Development/Libraries
#Requires: libxslt = %{version}
#Requires: libxml2 >= 2.4.17
#Requires: python

#%description python
#The libxslt-python package contains a module that permits applications
#written in the Python programming language to use the interface
#supplied by the libxslt library to apply XSLT transformations.

#This library allows to parse sytlesheets, uses the libxml2-python
#to load and save XML and HTML files. Direct access to XPath and
#the XSLT transformation context are possible to extend the XSLT language
#with XPath functions written in Python.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/libxslt-1.1.15-aix.patch
$PATCH -p2 -s < %{_sourcedir}/libxslt-1.1.15-autotools.patch


%build
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix}
PATH=%{_bindir}:$PATH make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# Make the links
cd %{buildroot}
for dir in bin lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files

%defattr(-, root, system)
%doc AUTHORS ChangeLog NEWS README Copyright TODO FEATURES
%doc doc/*.html doc/html doc/tutorial doc/*.gif doc/*.png
%doc %{_mandir}/man1/xsltproc.1*
%{_libdir}/lib*.a
%{_bindir}/xsltproc

/usr/lib/lib*.a
/usr/bin/xsltproc

%files devel

%defattr(-, root, system)
%doc AUTHORS ChangeLog NEWS README Copyright TODO FEATURES
%{_libdir}/lib*a
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*.pc
%{_bindir}/xslt-config
%{_includedir}/*
%{_datadir}/aclocal/*.m4
%doc %{_mandir}/man3/libxslt.3*
%doc %{_mandir}/man3/libexslt.3*

/usr/bin/xslt-config
/usr/lib/*
/usr/include/*
/usr/share/*

#%files python

#%defattr(-, root, system)
#%doc AUTHORS ChangeLog NEWS README Copyright FEATURES
#
# ??? @faur1d
# Many pbs with this package: to do soon
#
# %{_libdir}/python*/site-packages/libxslt.py
# %{_libdir}/python*/site-packages/libxsltmod.so
#%doc python/TODO
#%doc python/libxsltclass.txt
#%doc python/tests/*.py
#%doc python/tests/*.xml
#%doc python/tests/*.xsl
%changelog
*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.1.15

*  Wed Aug 10 2005  BULL
 - Release  3
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Wed May 11 2005  BULL
 - Release  1
 - New version  version: 1.1.12

