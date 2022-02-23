# spec file for mysql-connector-python
#
# Copyright (c) 2011-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

# Tests only run on manual build --with tests
# Tests rely on MySQL version 5.6
%bcond_without dotests

%define python3_32         /opt/freeware/bin/python3_32
%define python3_64         /opt/freeware/bin/python3_64
%define python3_version    %(%{python3_64} -V | sed "s|\.[0-9]*$||" | sed "s|Python ||")
%define python3_sitelib   %(/opt/freeware/bin/python3_32 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%define python3_minor_version %(/opt/freeware/bin/python3 -c "import sys; print(sys.version.split('.')[1])")

Name:           mysql-connector-python
Version:        8.0.19
Release:        1
Summary:        MySQL Connector for Python 3

License:        GPLv2 with exceptions
URL:            http://dev.mysql.com/doc/connector-python/en/index.html
# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/connector/python/
Source0:        %{name}-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

Patch1:         mysql-connector-python-8.0.19-test.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with dotests}
# for unittest
BuildRequires:  community-mysql-server
BuildRequires:  protobuf-python3
# Beware, mariadb-errmsg must be NOT installed.
%endif

Requires:      python(abi) = %{python3_version}
Provides:      python3-mysql-connector

%description
MySQL Connector/Python is implementing the MySQL Client/Server protocol
completely in Python. No MySQL libraries are needed, and no compilation
is necessary to run this Python DB API v2.0 compliant driver.

Documentation: http://dev.mysql.com/doc/connector-python/en/index.html


%prep
%setup -q -n %{name}-%{version}
chmod -x examples/*py

%patch1 -p1 -b tests

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
# Nothing to build

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
%{python3_64} setup.py install --root ${RPM_BUILD_ROOT} --install-lib %{python3_sitelib}

# cd ../32bit
# %{python3_32} setup.py install --root ${RPM_BUILD_ROOT} --install-lib %{python3_sitelib}


%check
%if %{with dotests}
# known failed tests
# bugs.BugOra14201459.test_error1426

cd 64bit

python3_64 -m venv mysqlTest
. ./mysqlTest/bin/activate
pip3 install dnspython

chown -R mysql:mysql .

(su mysql -c "\
   ulimit -d unlimited; \
   PYTHONPATH=/opt/freeware/lib64/python3.%{python3_minor_version}/site-packages:/opt/freeware/lib/python3/site-packages \
   LIBPATH=/opt/freeware/lib/pthread/ppc64/:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib \
   python3_64 unittests.py \
     --verbosity=10 \
     --with-mysql=/opt/freeware/ \
     --with-mysql-share=/opt/freeware/share/ \
     --skip-install \
" || true)

deactivate

# cd ../32bit
# %{python3_32} unittests.py \
#     --with-mysql=%{_prefix}/bin/mysql \
#     --verbosity=1
%else
: echo test suite disabled, need '--with tests' option
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES.txt 32bit/README* 32bit/docs
%doc 32bit/examples
%doc 32bit/LICENSE.txt
%{python3_sitelib}/mysql/*
%{python3_sitelib}/mysqlx/*
#%{python3_sitelib}/mysql/*
#%{python3_sitelib}/mysqlx/*


%changelog
* Mon Jan 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 8.0.19-1
- First port on AIX

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.16-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.16-4
- Rebuilt for Python 3.8

* Mon Jul 29 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.16-3
- Drop python2-mysql-connector (#1731660)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Honza Horak <hhorak@redhat.com> - 8.0.16-1
- Rebase to 8.0.16
  Resolves: #1390718

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-13
- Rebuilt for Python 3.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.6-11
- Python 2 binary package renamed to python2-mysql-connector
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- version 1.1.6 GA
  http://dev.mysql.com/doc/relnotes/connector-python/en/news-1-1-6.html

* Tue Feb  4 2014 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- version 1.1.5 GA
  http://dev.mysql.com/doc/relnotes/connector-python/en/news-1-1-5.html

* Tue Dec 17 2013 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- version 1.1.4 GA
  http://dev.mysql.com/doc/relnotes/connector-python/en/news-1-1.html
- add link to documentation in package description
- raise dependency on python 2.6

* Mon Aug 26 2013 Remi Collet <remi@fedoraproject.org> - 1.0.12-1
- version 1.0.12 GA

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul  3 2013 Remi Collet <remi@fedoraproject.org> - 1.0.11-1
- version 1.0.11 GA

* Wed May  8 2013 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- version 1.0.10 GA
- archive is now free (no more doc to strip)

* Wed Feb 27 2013 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- version 1.0.9 GA
- disable test suite in mock, fix FTBFS #914203

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 29 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- version 1.0.8 GA

* Wed Oct  3 2012 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- version 1.0.7 GA

* Sat Sep 15 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-2.b2
- version 1.0.6b2

* Fri Sep  7 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-1.b1
- version 1.0.6 (beta)
- remove non GPL documentation
- disable test_network and test_connection on EL-5

* Fri Aug 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- disable test_bugs with MySQL 5.1 (EL-6)

* Wed Aug  8 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- version 1.0.5 (beta)
- move from launchpad (devel) to dev.mysql.com

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.3.2-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 20 2011 Remi Collet <Fedora@famillecollet.com> 0.3.2-2
- run unittest during %%check
- fix License
- add python3 sub package

* Wed Mar 09 2011 Remi Collet <Fedora@famillecollet.com> 0.3.2-1
- first RPM

