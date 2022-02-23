Summary:    Non-interactive SSH authentication utility
Name:       sshpass
Version:    1.06
Release:    3
License:    GPLv2
Group:      Applications/Internet
Url:        http://sshpass.sourceforge.net/
Source0:    http://downloads.sourceforge.net/sshpass/sshpass-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Patch1:	sshpass-1.06-usleep-fork-son.patch

%description
Tool for non-interactively performing password authentication with so called
"interactive keyboard password authentication" of SSH. Most users should use
more secure public key authentication of SSH instead.

%prep
%setup -q

%patch1 -p1

%build
export ac_cv_func_malloc_0_nonnull=yes
export PATH="/opt/freeware/bin:$PATH"
#export CC="/usr/vac/bin/xlc_r"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/sshpass
/usr/bin/sshpass*
%{_prefix}/man/man1/sshpass.*
%doc AUTHORS COPYING ChangeLog NEWS

%changelog
* Tue Oct 24 2017 Tony Reix <tony.reix@atos.net> 1.06-3
- Fix issue with fork(): son started before father

* Tue May 09 2017 Ravi Hirekurabar <rhirekur@in.ibm.com> 1.06-2
- First port to AIX 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Kevin Fenzi <kevin@scrye.com> - 1.06-1
- Update to 1.06. Fixes bug #1414699

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild


* Tue Aug 23 2011 Martin Cermak <mcermak@redhat.com> 1.05-1
- Packaged for Fedora 

