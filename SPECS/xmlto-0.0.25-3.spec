%global WITH_TEX 0

Summary: A tool for converting XML files to various formats
Name: xmlto
Version: 0.0.25
Release: 3
License: GPLv2+
Group: Applications/System
URL: https://fedorahosted.org/xmlto/
Source0: https://fedorahosted.org/releases/x/m/%{name}/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: docbook-dtds >= 1.0-3
BuildRequires: docbook-style-xsl >= 1.76.1-1
BuildRequires: getopt
BuildRequires: libxml2 >= 2.6.32-2
BuildRequires: libxslt >= 1.1.24

%if %{WITH_TEX}
BuildRequires: passivetex >= 1.11
%endif

# we rely heavily on the DocBook XSL stylesheets!
Requires: docbook-dtds >= 1.0-3
Requires: docbook-style-xsl >= 1.76.1-1
Requires: flex

Requires: bash
Requires: getopt
Requires: coreutils
Requires: findutils
Requires: libxml2 >= 2.6.32-2
Requires: libxslt >= 1.1.24

%description
This is a package for converting XML files to various formats using XSL
stylesheets.


%if %{WITH_TEX}
%package tex
Summary: A set of xmlto backends with TeX requirements
Group: Applications/System
License: GPLv2+
# For full functionality, we need passivetex.
Requires: passivetex >= 1.11
# we require main package
Requires: %{name} = %{version}-%{release}

%description tex
This subpackage contains xmlto backend scripts which do require
PassiveTeX/TeX for functionality.
%endif


%package xhtml
Summary: A set of xmlto backends for xhtml1 source format
Group: Applications/System
License: GPLv2+
# for functionality we need stylesheets xhtml2fo-style-xsl
#Requires: xhtml2fo-style-xsl
# we require main package
Requires: %{name} = %{version}-%{release}

%description xhtml
This subpackage contains xmlto backend scripts for processing
xhtml1 source format.


%prep
%setup -q


%build
export LIBPATH="/opt/freeware/lib:/usr/lib"
# force to use the GNU version of these commands
export BASH=%{_bindir}/bash
export FIND=%{_bindir}/find
export GCP=%{_bindir}/cp
export GETOPT=%{_bindir}/getopt
export MKTEMP=%{_bindir}/mktemp
export PAPER_CONF=%{_bindir}/paperconf
export TAIL=%{_bindir}/tail
export XMLLINT=%{_bindir}/xmllint
export XSLTPROC=%{_bindir}/xsltproc

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc COPYING ChangeLog README AUTHORS NEWS
%{_bindir}/*
%{_mandir}/man?/*
%{_datadir}/%{name}/%{name}.mak
%dir %{_datadir}/%{name}/format
%{_datadir}/%{name}/format/docbook
%{_datadir}/%{name}/format/fo/awt
%{_datadir}/%{name}/format/fo/mif
%{_datadir}/%{name}/format/fo/pcl
%{_datadir}/%{name}/format/fo/svg
%{_datadir}/%{name}/format/fo/txt
/usr/bin/*


%if %{WITH_TEX}
%files tex
%defattr(-,root,system,-)
%{_datadir}/%{name}/format/fo/dvi
%{_datadir}/%{name}/format/fo/ps
%{_datadir}/%{name}/format/fo/pdf
%endif


%files xhtml
%defattr(-,root,system,-)
%dir %{_datadir}/%{name}/format/xhtml1
%{_datadir}/%{name}/format/xhtml1/*


%changelog
* Mon Jul 15 2013 Gerard Visiedo <gerard.visiedo@bull.net> 0.0.25-3
- Initial port on Aix6.1

* Wed Feb 20 2013 Michael Perzl <michael@perzl.org> - 0.0.25-2
- added missing dependencies on bash and getopt

* Tue Apr 03 2012 Michael Perzl <michael@perzl.org> - 0.0.25-1
- updated to version 0.0.25

* Fri Nov 18 2011 Michael Perzl <michael@perzl.org> - 0.0.24-1
- first version for AIX V5.1 and higher
