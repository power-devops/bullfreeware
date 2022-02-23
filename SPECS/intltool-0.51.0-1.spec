Name:           intltool
#BuildRequires:  perl-XML-Parser
Summary:        Internationalization Tool Collection
Version:        0.51.0
Release:        1
Group:          Development/Tools/Other
BuildArch:      noarch
#Requires:       gettext-tools
#Requires:       perl-XML-Parser
Provides:       xml-i18n-tools
Obsoletes:      xml-i18n-tools
License:        GPLv2+
Url:            https://edge.launchpad.net/intltool/
Source:         http://edge.launchpad.net/intltool/trunk/0.51.0/+download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
Some scripts to support translators working on GNOME and similar
programs. Data available in XML files (.oaf, .desktop, .sheet, and
more) can be extracted into PO files. After translation, the new
information is written back into the XML files.

%prep
%setup -q

%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export PERL="/usr/bin/perl"
./configure
gmake 
gmake check

%install
%makeinstall


cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%doc AUTHORS COPYING README TODO
%defattr(-, root, system)
%{_bindir}/*
/usr/bin/*
%{_datadir}/aclocal/*.m4
%{_datadir}/%{name}
%doc %{_mandir}/man8/*.*

%changelog
* Tue Apr 26 2016 Tony Reix <tony.reix@bull.net> - 0.51.0
- Initial port on AIX 6.1

* Thu May 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.41.1
- Initial port on Aix6.1
