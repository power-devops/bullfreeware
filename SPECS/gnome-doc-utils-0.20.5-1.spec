%define        majver      %(echo %version | cut -d. -f 1-2)
%define        group       desktop
%define        pkgname     gnome-doc-utils

Name:          gnome-doc-utils
Version:       0.20.5
Release:       1
Summary:       A collection of documentation utilities for the Gnome project
Group:         System/Tools
URL:           ftp://ftp.gnome.org
# bugfixes: http://ftp.gnome.org/pub/GNOME/sources/%{pkgname}
Source:        http://ftp.gnome.org/pub/GNOME/sources/gnome-doc-utils/%{majver}/gnome-doc-utils-%{version}.tar.bz2
License:       GPL
BuildRequires: gettext-devel
BuildRequires: perl
BuildRequires: pkg-config
BuildRequires: python-devel
BuildRequires: libxslt-devel
BuildRequires: libxml2-python
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
Gnome-doc-utils is a collection of documentation utilities for the Gnome project.  Notably, it contains utilities for building documentation and all auxiliary files in your source tree, and it contains the DocBook XSLT stylesheets that were once distributed with Yelp. Starting with Gnome 2.8, Yelp will require gnome-doc-utils for the XSLT.

Gnome documentation utilities.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}

%description devel
gnome-doc-utils is a collection of documentation utilities for the Gnome project.  Notably, it contains utilities for building documentation and all auxiliary files in your source tree, and it contains the DocBook XSLT stylesheets that were once distributed with Yelp. Starting with Gnome 2.8, Yelp will require gnome-doc-utils for the XSLT.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
export CONFIG_SHELL=/usr/bin/sh
export RM="/usr/bin/rm -f"

export CC="/usr/vac/bin/xlc_r"

./configure \
	--prefix=%{_prefix} \
	--disable-scrollkeeper \
	--disable-silent-rules
make

%install
[ "${RPM_BUILD_ROOT}" != / ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
  mkdir -p ${RPM_BUILD_ROOT}/usr/bin
  cd ${RPM_BUILD_ROOT}/usr/bin
  ln -s ../..%{_bindir}/* .
)

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
mv ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig/*.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig


%clean
[ "${RPM_BUILD_ROOT}" != / ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_bindir}/gnome-doc-prepare
%{_bindir}/gnome-doc-tool
%{_bindir}/xml2po
/usr/bin/gnome-doc-prepare
/usr/bin/gnome-doc-tool
/usr/bin/xml2po
%{_datadir}/gnome/help/gnome-doc-make/
%{_datadir}/gnome/help/gnome-doc-xslt/
%{_datadir}/gnome-doc-utils/*
%{_datadir}/omf/gnome-doc-make/*
%{_datadir}/omf/gnome-doc-xslt/*
%{_datadir}/xml/gnome/xslt/docbook/common/*
%{_datadir}/xml/gnome/xslt/docbook/html/*
%{_datadir}/xml/gnome/xslt/docbook/omf/*
%{_datadir}/xml/gnome/xslt/docbook/utils/*
%{_datadir}/xml/gnome/xslt/gettext/*
%{_datadir}/xml/gnome/xslt/common/theme.xsl
%{_datadir}/xml/gnome/xslt/common/utils.xsl
%{_datadir}/xml/gnome/xslt/mallard
%{_datadir}/xml/mallard/1.0/mallard.rnc
%{_datadir}/xml/mallard/1.0/mallard.rng
#%{python_sitearch}/xml2po
%{_libdir}/python*/site-packages/xml2po
#%{_datadir}/xml/gnome/xslt/xsldoc/*
#%{_datadir}/xml2po/*
%{_datadir}//man/man1/xml2po.*
%doc AUTHORS COPYING ChangeLog NEWS README

%files devel
%defattr(-,root,system)
%{_datadir}/aclocal/gnome-doc-utils.m4
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jul 27 2012 Gerard Visiedo <gerard.visiedo@bull.net> 0.20.5-1
- Initial port on Aix6.1

