%bcond_without dotests

%define meta_name mariadb-connector
%define desc MariaDB Connector/Python enables python programs to access MariaDB \
and MySQL databases, using an API which is compliant with the Python \
DB API 2.0 (PEP-249). It is written in C and uses MariaDB Connector/C \
client library for client server communication.

Name:           python3-mariadb-connector
Version: 1.1.1
Release: 1
Summary:        Mariadb Connector for Python 3
License:        LGPL
URL:            https://www.mariadb.org
Source0:        https://downloads.mariadb.com/Connectors/python/connector-python-%{version}/mariadb-connector-python-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
Patch1:         mariadb-connector-python-1.0.6-arraysize_64.patch

BuildRequires:  python(abi) >= 3.9
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 54.0.0
BuildRequires:  sed
%if %{with dotests}
BuildRequires:  mariadb-server
%endif
BuildRequires:  mariadb-connector-c-static
BuildRequires:  mariadb-connector-c-devel

# For compatibility
Provides: mariadb-connector-python3 = %{version}

%python_meta_requires

%description
%desc

%python_module
%python_module_desc


%prep
%setup -q -n mariadb-connector-python-%{version}

find . -name "*.c" | xargs /opt/freeware/bin/sed -i 's|CLOCK_MONOTONIC_RAW|CLOCK_MONOTONIC|g'

%patch1 -p1 -b .arraysize


%build
export OBJECT_MODE=64
export CPPFLAGS="-maix64"
export LDFLAGS="/opt/freeware/lib64/libmariadbclient.a -lssl -lcrypto -liconv -lz"
%{__python} setup.py build --verbose


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%{__python} setup.py install --root ${RPM_BUILD_ROOT} --install-lib %{python_sitearch64}

%check
%if %{with dotests}
su mysql -c "ulimit -d unlimited; /opt/freeware/libexec/mysqld --datadir=/opt/freeware/var/lib/mysql/data &"
sleep 5
ln -sf /opt/freeware/var/lib/mysql/mysql.sock /tmp/

ulimit -d unlimited

(
  cp build/lib.aix*/mariadb/_mariadb.cpython-%{__python_nodot_version}.so mariadb
  cd testing
  PYTHONPATH=.. \
  TEST_DATABASE=test \
  %{__python} -m unittest discover -v || true
)

mysqladmin shutdown
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %{module_name}
%defattr(-,root,system,-)
%doc LICENSE README.md
%{python_sitearch64}/*


%changelog
* Mon Dec 13 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.1.1-1
- Update to 1.1.1

* Wed Nov 24 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 1.0.8-1
- New version 1.0.8-1
- Add metapackage
- Remove 32 bits support

* Tue Mar 02 2021 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0.6-1
- New version 1.0.6

* Mon Jul 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0.0-1
- New version 1.0.0

* Fri Mar 27 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> - 0.9.54-1
- First port on AIX
