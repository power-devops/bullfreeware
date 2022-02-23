Name:    libassuan
Summary: GnuPG IPC library
Group: System Environment/Base
Version: 2.4.3
Release: 1

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
Source0: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
URL:     http://www.gnupg.org/

Patch1:  libassuan-2.1.0-multilib.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages.

%package devel 
Summary: GnuPG IPC library 
Group: System Environment/Base
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.


%prep
%setup -q

%patch1 -p1 -b .multilib


%build
export RM="/usr/bin/rm -f"
export CC="gcc -O2 -maix32"

%configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir}/libassuan2

gmake

gmake check


%install
export RM="/usr/bin/rm -f"

export CC="gcc -O2 -maix32"

gmake install DESTDIR=${RPM_BUILD_ROOT}

## Unpackaged files
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/lib*.la


#%check
#make check


#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig


%post devel 
/sbin/install-info %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :

%preun devel 
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :
fi


%files
#%license COPYING COPYING.LIB
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libassuan.a

%files devel 
%{_bindir}/libassuan-config
%{_includedir}/libassuan2/
%{_libdir}/libassuan.a
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 2.4.3-1
- Port on AIX

* Mon Aug 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.4.3-6
- .spec cosmetics, update source URLs

* Mon Aug 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.3-5
- Drop unneeded pth-devel dependencies

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Tomáš Mráz <tmraz@redhat.com> 2.4.3-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec  3 2015 Tomáš Mráz <tmraz@redhat.com> 2.4.2-1
- new upstream release

* Tue Nov 24 2015 Tomáš Mráz <tmraz@redhat.com> 2.4.1-1
- new upstream release

* Wed Sep  2 2015 Tomáš Mráz <tmraz@redhat.com> 2.3.0-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Tomáš Mráz <tmraz@redhat.com> 2.2.0-1
- new upstream release

* Thu Sep 11 2014 Tomáš Mráz <tmraz@redhat.com> 2.1.2-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.0-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Tomáš Mráz <tmraz@redhat.com> 2.1.0-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-4
- multilib conflict in libassuan-config fixed

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-2
- add missing requires of base package

* Wed Apr 18 2012 Tomáš Mráz <tmraz@redhat.com> 2.0.3-1
- new upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Tomáš Mráz <tmraz@redhat.com> 2.0.1-1
- new upstream release

* Thu Apr 14 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- Missing ldconfig calls (#696787)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-2
- -devel: Provides: libassuan2-devel

* Tue Jul 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-1
- libassuan-2.0.0 (#573796)

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-4
- better versioning for Obsoletes
- better (upstreamable) multilib patch

* Thu Dec 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.5-3
- Fix license tag - the documentation is GPLv3+

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.5-1
- libassuan-1.0.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-3
- multiarch conflicts (#341911)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-2
- respin (gcc43)

* Wed Dec 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.4-1
- libassuan-1.0.4
- License: LGPLv2+
- disable useless -debuginfo (static libs only)

* Sun Aug 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-2
- BR: gawk (to reenable pth support)

* Fri Aug 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.3-1
- libassuan-1.0.3
- License: LGPLv2

* Thu Aug 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-2
- License: LGPLv3 (clarification, changed from LGPLv2 1.0.1 -> 1.0.2)

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.0.2-1
- libassuan-1.0.2
- rename -static -> -devel

* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.1-1
- libassuan-1.0.1

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.0.0-1
- libassuan-1.0.0
- rename -devel -> -static (+Obsoletes/Provides: %%name-devel)

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-2
- another libassuan.m4 patch

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.3-1
- 0.9.3
- BR: pth-devel, -devel: Requires: pth-devel

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.9.2-1
- 0.9.2

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.ne> - 0.9.0-3
- respin

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net - 0.9.0-2
- -devel: Provides: %%name-static
- 0.9.0

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.10-3
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Mon Jul  4 2005 Michael Schwendt <mschwendt[at]users.sf.net> - 0.6.10-2
- Build PIC only for x86_64.

* Fri Jul  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.10-1
- 0.6.10, macro patch no longer needed (#162262).

* Sun May  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-4
- rebuilt

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.9-3
- Fix FC4 build and source URLs.

* Thu Feb  3 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.9-2
- Build PIC to fix x86_64 linking.

* Thu Jan 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.9-1
- 0.6.9

* Sat Oct 23 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.3
- *really* fix description this time.

* Fri Oct 22 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.2
- remove "We decided..." part of description
- remove hard-coded .gz info references
- Req(preun)->Preq(postun): /sbin/install-info

* Thu Oct 21 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.1
- cleanup, make presentable.

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> - 0.6.7-0.fdr.0
- first try
