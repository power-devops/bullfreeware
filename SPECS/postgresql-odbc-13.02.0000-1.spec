# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64
%global upstream_name psqlodbc

Name: postgresql-odbc
Summary: PostgreSQL ODBC driver
Version: 13.02.0000
Release: 1
License: LGPLv2+
URL: https://odbc.postgresql.org/

# Don't use %{upstream_name} for our jenkins.
Source0: http://ftp.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

BuildRequires: unixODBC-devel
BuildRequires: postgresql-devel
BuildRequires: sed

# For libpgcommon.a
BuildRequires: postgresql-static

Provides: %upstream_name = %version-%release

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n %{upstream_name}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_COMMON="-O1"

export LIBS=-lpgcommon

build_psqlodbc(){
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \
	--with-unixodbc

	gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_psqlodbc %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_psqlodbc %{_libdir}

# %configure --with-unixodbc --disable-dependency-tracking

# # GCC 10 defaults to -fno-common
# # https://gcc.gnu.org/gcc-10/changes.html (see C section)
# make %{?_smp_mflags} CFLAGS="%{optflags} -fcommon"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

(
    # Libraries aren't versionned for now.
    for name in psqlodbca psqlodbcw; do
	# Extract .so from 64bit .a libraries
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x ${name}.a

	# Create 32 bits libraries with 32/64bit members
	cd ${RPM_BUILD_ROOT}%{_libdir}
	${AR} -q ${name}.a ${RPM_BUILD_ROOT}%{_libdir64}/${name}.so
	rm ${RPM_BUILD_ROOT}%{_libdir64}/${name}.so

	# Create links for 64 bits libraries
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	rm -f ${name}.a
	ln -sf ../lib/${name}.a ${name}.a
    done
)

(
    cd ${RPM_BUILD_ROOT}%{_libdir}
    rm psqlodbcw.la psqlodbca.la
)

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Tests needs to be done manually with a running postgresql server.
# $ cd tests && make installcheck

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_libdir}/psqlodbca.a
%{_libdir}/psqlodbcw.a
%{_libdir64}/psqlodbca.a
%{_libdir64}/psqlodbcw.a
%doc 64bit/license.txt 64bit/readme.txt 64bit/docs/*


%changelog
* Sat Oct 02 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 13.02.0000-1
- Update to 13.02.0000

* Fri Jul 23 2021 Clément Chigot <clement.chigot@atos.net> - 13.01.0000-1
- First port for AIX

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.02.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Ondrej Dubaj <odubaj@redhat.com> - 12.02.0000-1
- Rebase to upstream release 12.02.0000

* Mon Mar 09 2020 Patrik Novotný <panovotn@redhat.com> - 12.01.0000-1
- Rebase to upstream release 12.01.0000

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Pavel Raiskup <praiskup@redhat.com> - 10.03.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20180519131632.8E59CB40E51%40winpg.jp

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 10.02.0000-2
- BR postgresql-test-rpm-macros
- add %%bcond for check section

* Mon Apr 02 2018 Pavel Raiskup <praiskup@redhat.com> - 10.02.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20180330143925.88CEDB40E51%40winpg.jp

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.01.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Pavel Raiskup <praiskup@redhat.com> - 10.01.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20171227144219.0ABC4B4C417%40winpg.jp

* Mon Oct 23 2017 Pavel Raiskup <praiskup@redhat.com> - 10.00.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20171013143455.9D0E5B4C412%40winpg.jp

* Tue Sep 05 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0500-1
- update to new upstream release, per:
  https://www.postgresql.org/message-id/20170905143318.95448B4C411@winpg.jp

* Thu Jul 27 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0410-1
  https://odbc.postgresql.org/docs/release.html

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 09.06.0310-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0310-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Tue May 09 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0300-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon Mar 13 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0200-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon Feb 06 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0100-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Thu Oct 20 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0400-4
- provide 'psqlodbc', we possibly should rename the package in future

* Wed Oct 05 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0400-3
- depend on postgresql-setup 5.0 (in postgresql-devel package)

* Mon Aug 29 2016 Petr Kubat <pkubat@redhat.com> - 09.05.0400-2
- once again revert upstream commit d5374bcc4d
- also revert its accompanying testsuite commit eb480e19ee

* Thu Aug 11 2016 Petr Kubat <pkubat@redhat.com> - 09.05.0400-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Tue Jul 26 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0300-2
- backport upstream fixes for testsuite failures (rhbz#1350486)

* Sat Jun 18 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0300-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon May 02 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0210-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html
- revert one upstream commit to fix testsuite issues
- disable one armv7hl related issue during self-testing (rhbz#1330031)

* Thu Apr 14 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0200-2
- enable testsuite during build

* Tue Apr 12 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0200-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 09.05.0100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0100-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0400-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-3
- fix testsuite requirements

* Wed Nov 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-2
- install the testsuite

* Wed Oct 29 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0300-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0300-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0300-2
- run upstream testsuite when '%%runselftest' defined

* Mon May 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0300-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Wed Apr 23 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0210-1
- rebase to latest upstream version (#1090345), per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Thu Dec 19 2013 Pavel Raiskup <praiskup@redhat.com> - 09.03.0100-1
- rebase to latest upstream version

* Mon Nov 18 2013 Pavel Raiskup <praiskup@redhat.com> - 09.02.0100-1
- rebase to latest upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Tom Lane <tgl@redhat.com> 09.01.0200-2
- Update tarball URL in specfile (no actual package change)

* Mon Aug 20 2012 Tom Lane <tgl@redhat.com> 09.01.0200-1
- Update to version 09.01.0200
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 09.01.0100-1
- Update to version 09.01.0100

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.00.0200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 09.00.0200-1
- Update to version 09.00.0200

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 08.04.0200-2
- Correct Source0: tag and comment to reflect how to get the tarball

* Wed Dec 30 2009 Tom Lane <tgl@redhat.com> 08.04.0200-1
- Update to version 08.04.0200

* Fri Aug 28 2009 Tom Lane <tgl@redhat.com> 08.04.0100-2
- Rebuild with new openssl

* Tue Aug 18 2009 Tom Lane <tgl@redhat.com> 08.04.0100-1
- Update to version 08.04.0100

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 08.03.0200-2
- Rebuild for unixODBC 2.2.14.

* Tue Aug  5 2008 Tom Lane <tgl@redhat.com> 08.03.0200-1
- Update to version 08.03.0200

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 08.03.0100-1
- Update to version 08.03.0100
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.

* Fri Nov  2 2007 Tom Lane <tgl@redhat.com> 08.02.0500-1
- Update to version 08.02.0500

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 08.02.0200-2
- Update License tag to match code.

* Wed Apr 25 2007 Tom Lane <tgl@redhat.com> 08.02.0200-1
- Update to version 08.02.0200

* Mon Dec 11 2006 Tom Lane <tgl@redhat.com> 08.01.0200-4
- Rebuild for new Postgres libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-3.1
- rebuild

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 08.01.0200-3
- Fix BuildRequires: for mock build environment

* Wed Mar 22 2006 Tom Lane <tgl@redhat.com> 08.01.0200-2
- Change library name back to psqlodbc.so, because it appears that upstream
  will revert to that name in next release; no point in thrashing the name.
- Include documentation files unaccountably omitted before (bug #184158)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tom Lane <tgl@redhat.com> 08.01.0200-1
- Update to version 08.01.0200.
- Upstream now calls the library psqlodbcw.so ... add a symlink to avoid
  breaking existing odbc configuration files.

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 08.01.0102-1
- Update to version 08.01.0102.
- Add buildrequires postgresql-devel (bz #174505)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 08.01.0100-1
- Update to version 08.01.0100.

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 08.00.0100-1
- Update to version 08.00.0100.

* Fri Nov 12 2004 Tom Lane <tgl@redhat.com> 7.3-9
- back-port 64-bit fixes from current upstream (bug #139004)

* Tue Sep 21 2004 Tom Lane <tgl@redhat.com> 7.3-8
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com>
- Correct License: annotation.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 21 2003 David Jee <djee@redhat.com> 7.3-5
- rebuild

* Wed Nov 05 2003 David Jee <djee@redhat.com> 7.3-4
- import new community version 07.03.0200

* Mon Sep 15 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- autotools fixes (courtesy Alex Oliva <aoliva@redhat.com> and
  Owen Taylor <otaylor@redhat.com>)

* Tue Jul 08 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- allow use with unixODBC (courtesy Troels Arvin) [Bug #97998]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 02 2003 Andrew Overholt <overholt@redhat.com> 7.3-1
- sync to new community version (07.03.0100 => v7.3, r1)

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 1-2
- rebuild

* Tue Jan 14 2003 Andrew Overholt <overholt@redhat.com>
- 1-1
- initial build (just took old package sections)
