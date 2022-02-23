Name:           intltool
#BuildRequires:  perl-XML-Parser
Summary:        Internationalization Tool Collection
Version:        0.41.1
Release:        1
Group:          Development/Tools/Other
BuildArch:      noarch
#Requires:       gettext-tools
#Requires:       perl-XML-Parser
Provides:       xml-i18n-tools
Obsoletes:      xml-i18n-tools
License:        GPLv2+
Url:            https://edge.launchpad.net/intltool/
Source:         http://edge.launchpad.net/intltool/trunk/0.41.0/+download/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
Some scripts to support translators working on GNOME and similar
programs. Data available in XML files (.oaf, .desktop, .sheet, and
more) can be extracted into PO files. After translation, the new
information is written back into the XML files.

%prep
%setup -q

%build
./configure
make 
#make check

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
* Thu May 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.41.1
- Initial port on Aix6.1
