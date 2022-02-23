%bcond_without dotests

%define         git b737f60
%define         perl  %{_bindir}/perl_64

Summary:        A top clone for MySQL
Name:           mytop
Version:        1.7
Release:        19_%{git}
License:        GPLv2
URL:            https://github.com/jzawodn/mytop
# http://jeremy.zawodny.com/mysql/mytopis the old 1.6 => MySQL 4 version.
# Tarball created by
# $ git clone git://github.com/jzawodn/mytop.git
# $ cd mytop
# $ git archive --format=tar --prefix=mytop-1.7/ %{git} | xz > mytop-1.7-%{git}.tar.xz
Source0:        mytop-%{version}-%{git}.tar.xz
Source1000:     %{name}-%{version}-%{release}.build.log

Patch01:        mytop-1.7-long.patch
Patch02:        mytop-1.7-undef-resolv.patch

Requires:       perl
Requires:       perl(DBD::mysql) >= 1
Requires:       perl(DBI) >= 1.13
Requires:       perl(Term::ReadKey) >= 2.1
Requires:       perl(Term::ANSIColor)
Requires:       perl(Time::HiRes)

BuildRequires:  perl(DBD::mysql) >= 1
BuildRequires:  perl(DBI) >= 1.13
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Term::ReadKey) >= 2.1

BuildArch:      noarch


%description 
mytop is a console-based tool for monitoring the threads and overall
performance of MySQL servers. The user interface is modeled after
familiar top application.


%prep
%setup -q
%patch1 -p1
%patch2 -p1


%build
%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake
sed -i 's|#!/usr/bin/perl|#!/usr/bin/env perl|g' mytop


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
INSTALL=/opt/freeware/bin/install

$INSTALL -D -m 0644 blib/man1/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
$INSTALL -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with dotests}
gmake -k test TEST_VERBOSE=1
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc Changes README
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}


%changelog
* Fri Oct 11 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.7-18.b737f60
- First port on AIX

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-18.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-17.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-16.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-15.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-14.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-13.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-12.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-11.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-10.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-9.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.7-8.b737f60
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-7.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4.b737f60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 09 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-3.b737f60
- add patch to fix #589366

* Mon May 03 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-2.b737f60
- add patch to fix #584602

* Sat Mar 27 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.7-1.b737f60
- 1.7 (from github), fixing bz #577528

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 30 2007 Terje Rosten <terje.rosten@ntnu.no> - 1.6-2
- remove explicit req on dbi, let rpm to the job

* Wed Dec 26 2007 Terje Rosten <terje.rosten@ntnu.no> - 1.6-1
- initial package
