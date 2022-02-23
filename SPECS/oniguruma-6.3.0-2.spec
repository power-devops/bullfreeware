Name:		oniguruma
Version:	6.3.0
Release:	2
Summary:	Regular expressions library

Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/kkos/oniguruma/
Source0:	https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz
# FIXME
# Don't know exactly why, however without Patch0 onig_new returns
# NULL reg variable
Patch0:		oniguruma-5.9.2-onig_new-returns-NULL-reg.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n onig-%{version}
( cd src
%patch0 -p1 -b .nullreg
)
/opt/freeware/bin/sed -i.multilib -e 's|-L@libdir@||' onig-config.in

for f in \
	README.ja \
	doc/API.ja \
	doc/FAQ.ja \
	doc/RE.ja
	do
	iconv -f EUC-JP -t UTF-8 $f > $f.tmp && \
		( touch -r $f $f.tmp ; %{__mv} -f $f.tmp $f ) || \
		%{__rm} -f $f.tmp
done

%build
export RM="/usr/bin/rm -f"

export OBJECT_MODE=32
export CFLAGS="-maix32"

%configure \
    --disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir}
%{__make} %{?_smp_mflags}

%{__make} check


%install
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="/opt/freeware/bin/install -c -p"
/opt/freeware/bin/find $RPM_BUILD_ROOT -name '*.la' \
	-exec %{__rm} -f {} ';'


#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc	AUTHORS
#%license	COPYING
%doc	HISTORY
%doc	README
%doc	index.html
%lang(ja)	%doc	README.ja
%lang(ja)	%doc	index_ja.html

%{_libdir}/libonig.a

%files devel
%defattr(-,root,root,-)
%doc	doc/API
%doc	doc/FAQ
%doc	doc/RE
%lang(ja)	%doc	doc/API.ja
%lang(ja)	%doc	doc/FAQ.ja
%lang(ja)	%doc	doc/RE.ja

%{_bindir}/onig-config

%{_libdir}/libonig.a
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc	

%changelog
* Mon Sep 18 2017 Tony Reix <tony.reix@atos.net> - 6.3.0-2
- Remove ldconfig

* Mon Sep 18 2017 Tony Reix <tony.reix@atos.net> - 6.3.0-1
- First port on AIX

* Tue May 30 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.3.0-1
- 6.3.0
  - CVEs 2017-9226 CVE-2017-9225 CVE-2017-9224 CVE-2017-9227 CVE-2017-9229 CVE-2017-9228

* Wed Apr 26 2017 Nils Philippsen <nils@redhat.com> - 6.2.0-2
- remove unnecessary BR: ruby

* Fri Apr 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Fri Nov 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Sun Oct 30 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Mon Jul 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan  2 2015 <mtasaka@fedoraproject.org> - 5.9.6-1
- 5.9.6

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.3-1
- 5.9.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 5.9.2-3
- F-17: rebuild against gcc47

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging

