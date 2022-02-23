# Expected failures in mock, hangs in koji
#%bcond_with tests
# The *.py files we ship are not python scripts, #813651
%global _python_bytecompile_errors_terminate_build 0

Name:           bash-completion
Version:        2.4
Release:        2%{?dist}
Epoch:          1
Summary:        Programmable completion for Bash
Group:		Development/Languages

License:        GPLv2+
URL:            https://github.com/scop/bash-completion
Source0:        https://github.com/scop/bash-completion/releases/download/%{version}/%{name}-%{version}.tar.xz
Source2:        CHANGES.package.old
# https://bugzilla.redhat.com/677446, see also redefine_filedir comments
Patch0:         %{name}-1.99-noblacklist.patch

BuildArch:      noarch
#%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
#%endif
Requires:       bash >= 4.1

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.



%prep
%setup -q
%patch0 -p1
install -pm 644 %{SOURCE2} .


%build
export RM="/usr/bin/rm -f"

%configure
gmake %{?_smp_mflags}

cat <<EOF >redefine_filedir
# This is a copy of the _filedir function in bash_completion, included
# and (re)defined separately here because some versions of Adobe
# Reader, if installed, are known to override this function with an
# incompatible version, causing various problems.
#
# https://bugzilla.redhat.com/677446
# http://forums.adobe.com/thread/745833

EOF
sed -ne '/^_filedir\s*(/,/^}/p' bash_completion >>redefine_filedir


%install
export RM="/usr/bin/rm -f"

gmake install DESTDIR=$RPM_BUILD_ROOT
install -Dpm 644 redefine_filedir \
    $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/redefine_filedir

# Updated completion shipped in cowsay package:
$RM $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/{cowsay,cowthink}

# Copy .pc file in 
cp $RPM_BUILD_ROOT%{_datadir}/pkgconfig/bash-completion.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/


#%if %{with tests}
#%check
# For some tests involving non-ASCII filenames
#	export LANG=en_US.UTF-8
# This stuff borrowed from dejagnu-1.4.4-17 (tests need a terminal)
#	tmpfile=$(mktemp)
#	screen -D -m sh -c '( gmake check ; echo $? ) >'$tmpfile
#	cat $tmpfile
#	result=$(tail -n 1 $tmpfile)
#	rm -f $tmpfile
#	exit $result
#%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS CHANGES CHANGES.package.old CONTRIBUTING.md README.md
%doc doc/bash_completion.txt
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/
%{_datadir}/bash-completion/
%{_datadir}/cmake/
%{_datadir}/pkgconfig/bash-completion.pc
%{_libdir}/pkgconfig/bash-completion.pc


%changelog
* Tue Aug 16 2016 Tony Reix <tony.reix@atos.net> - 2.4-2
- Fix issue with .pc dir .

* Tue Aug 16 2016 Tony Reix <tony.reix@atos.net> - 2.4-1
- Initial port on AIX 6.1

* Tue Aug 16 2016 Tony Reix <tony.reix@atos.net> - 2.3-1
- Initial port on AIX 6.1

* Mon Mar 28 2016 Ville Skyttä <ville.skytta@iki.fi> - 1:2.3-1
- Update to 2.3

* Thu Mar  3 2016 Ville Skyttä <ville.skytta@iki.fi> - 1:2.2-1
- Update to 2.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-9.20150513git1950590
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-8.20150513git1950590
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-7.20150513git1950590
- Autogenerate redefine_filedir (fixes #1171396 in it too)

* Wed May 13 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-6.20150513git1950590
- Update to current upstream git (fixes #1171396)
- Move pre-1.90 %%changelog entries to CHANGES.package.old

* Mon Nov 10 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-6.20141110git52d8316
- Update to current upstream git (fixes #744406, #949479, #1090481, #1015935,
  #1132959, #1135489)
- Clean up no longer needed specfile conditionals
- Mark COPYING as %%license where applicable

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 17 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-4
- Ship bash_completion.txt.
- Make profile.d scriptlet noreplace again.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-2
- Don't install nmcli completion on F-18+ (#950071).

* Mon Apr  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-1
- Update to 2.1 (fixes #860510, #906469, #912113, #919246, #928253).
- Don't ship completions included in util-linux 2.23-rc2 for F-19+.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:2.0-1
- Update to 2.0 (fixes #817902, #831835).
- Don't try to python-bytecompile our non-python *.py (#813651).

* Sun Jan  8 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:1.99-1
- Update to 1.99.

* Fri Nov  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.90-1
- Update to 1.90.
- Specfile cleanups.
- Move pre-1.2 %%changelog entries to CHANGES.package.old.
