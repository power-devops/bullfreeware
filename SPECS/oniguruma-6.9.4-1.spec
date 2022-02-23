# By default run tests
# To build without tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# The .so version was 4 for 6.3.0
%define soname 5

%define _libdir64 %{_prefix}/lib64


Name:		oniguruma
Version:	6.9.4
Release:	1
Summary:	Regular expressions library

License:	BSD
URL:		https://github.com/kkos/oniguruma/
Source0:	https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz

Source10:	%{name}-%{version}-%{release}.build.log

BuildRequires: gcc
BuildRequires: sed

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep

%setup -q -n onig-%{version}

export SED="/opt/freeware/bin/sed"

# %{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in
${SED} -i.multilib -e 's|-L@libdir@||' onig-config.in

%if 0
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
%endif

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

export AR="/usr/bin/ar -X32_64"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

%configure \
	--disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir}
gmake %{?_smp_mflags}

# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32"

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

%configure \
	--disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir}
gmake %{?_smp_mflags}




%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

# shared object not installed
cp src/.libs/libonig.so.%{soname} ${RPM_BUILD_ROOT}/%{_libdir}
%{__ln_s} libonig.so.%{soname} ${RPM_BUILD_ROOT}/%{_libdir}/libonig.so

# move 64 bit library, libonig.so.5.0.0, libonig.so.5
mv ${RPM_BUILD_ROOT}/%{_libdir} ${RPM_BUILD_ROOT}/%{_libdir64}

cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

# shared object not installed
cp src/.libs/libonig.so.%{soname} ${RPM_BUILD_ROOT}/%{_libdir}
%{__ln_s} libonig.so.%{soname} ${RPM_BUILD_ROOT}/%{_libdir}/libonig.so



# add 64 bit libonig.so.5 to library
${AR} -q ${RPM_BUILD_ROOT}/%{_libdir}/libonig.a   ${RPM_BUILD_ROOT}/%{_libdir64}/libonig.so.%{soname}

cd $RPM_BUILD_ROOT/%{_prefix}/lib64
rm -f *.a
%{__ln_s}  ../lib/*.a .



# %{__make} install \
# 	DESTDIR=$RPM_BUILD_ROOT \
# 	INSTALL="%{__install} -c -p"

find $RPM_BUILD_ROOT -name '*.la' \
	-exec %{__rm} -f {} ';'

ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib
ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib64



%check

%if %{with dotests}

#% {__make} check

cd 64bit
(gmake -k check || true)

slibclean

cd ../32bit
(gmake -k check || true)

%endif



# %ldconfig_scriptlets

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc	32bit/AUTHORS
%license	32bit/COPYING
%doc	32bit/HISTORY
%doc	32bit/README.md
%doc	32bit/index.html
%lang(ja)	%doc	32bit/README_japanese
%lang(ja)	%doc	32bit/index_ja.html

%{_libdir}/libonig.a
%{_libdir64}/libonig.a
# %{_libdir}/libonig.so.5*
# %{_libdir64}/libonig.so.5*

%files devel
%defattr(-,root,system,-)
%doc	32bit/doc/API
%doc	32bit/doc/CALLOUTS.API
%doc	32bit/doc/CALLOUTS.BUILTIN
%doc	32bit/doc/FAQ
%doc	32bit/doc/RE
%doc	32bit/doc/SYNTAX.md
%doc	32bit/doc/UNICODE_PROPERTIES
%lang(ja)	%doc	32bit/doc/API.ja
%lang(ja)	%doc	32bit/doc/CALLOUTS.API.ja
%lang(ja)	%doc	32bit/doc/CALLOUTS.BUILTIN.ja
%lang(ja)	%doc	32bit/doc/FAQ.ja
%lang(ja)	%doc	32bit/doc/RE.ja

%{_bindir}/onig-config

# %{_libdir}/libonig.so
# %{_libdir64}/libonig.so
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc	

%changelog
* Thu Jan 30 2020 Michael Wilson <michael.a.wilson@atos.net> - 6.9.4-1
- Update to 6.9.4 on AIX using RPM version 4 and brpm on laurel2
- Build in 64 and 32 bits

* Fri Nov 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-1
- 6.9.4 final

* Fri Nov 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-0.2.rc3
- 6.9.4 rc3 (CVE-2019-19204 CVE-2019-19203 CVE-2019-19012)

* Sat Nov  9 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.9.4-0.1.rc1
- 6.9.4 rc1 (CVE-2019-19246)
- ...
- ...
- ...

* Mon Sep 18 2017 Tony Reix <tony.reix@atos.net> - 6.3.0-2
- Remove ldconfig

* Mon Sep 18 2017 Tony Reix <tony.reix@atos.net> - 6.3.0-1
- First port on AIX

* Tue May 30 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.3.0-1
- 6.3.0
  - CVEs 2017-9226 CVE-2017-9225 CVE-2017-9224 CVE-2017-9227 CVE-2017-9229 CVE-2017-9228

