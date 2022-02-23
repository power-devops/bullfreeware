%bcond_without dotests

%define python3_32         /opt/freeware/bin/python3_32
%define python3_64         /opt/freeware/bin/python3_64
%define python3_archlib_32   %(/opt/freeware/bin/python3_32 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python3_archlib_64   %(/opt/freeware/bin/python3_64 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python3_minor_version %(/opt/freeware/bin/python3 -c "import sys; print(sys.version.split('.')[1])")
%define AIX_version %(echo "`uname -v`.`uname -r`")


Name:           mariadb-connector-python
Version:        0.9.54
Release:        1beta
Summary:        Mariadb Connector for Python 3

License:        LGPL
URL:            https://dlm.mariadb.com/918887/Connectors/python/connector-python-%{version}/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log


%description
This is the first beta release of MariaDB Connector/Python.

MariaDB Connector/Python enables python programs to access MariaDB
and MySQL databases, using an API which is compliant with the Python
DB API 2.0 (PEP-249). It is written in C and uses MariaDB Connector/C
client library for client server communication.

**This is an beta release of the MariaDB Connector/Python**
**and not intended for production use!**

%package -n %{name}3.%{python3_minor_version}
Summary:        Mariadb Connector for Python 3
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  sed
%if %{with dotests}
BuildRequires:  mariadb-server
%endif
BuildRequires:  mariadb-connector-c-static

Requires:       python(abi) = 3.%{python3_minor_version}

Provides:       python3-mariadb-connector


%description -n %{name}3.%{python3_minor_version}
This is the first beta release of MariaDB Connector/Python.

MariaDB Connector/Python enables python programs to access MariaDB
and MySQL databases, using an API which is compliant with the Python
DB API 2.0 (PEP-249). It is written in C and uses MariaDB Connector/C
client library for client server communication.

**This is an beta release of the MariaDB Connector/Python**
**and not intended for production use!**


%prep
%setup -q -n %{name}-%{version}

find . -name "*.c" | xargs /opt/freeware/bin/sed -i 's|CLOCK_MONOTONIC_RAW|CLOCK_MONOTONIC|g'

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
cd 64bit
export OBJECT_MODE=64
export CPPFLAGS="-maix64"
export LDFLAGS="/opt/freeware/lib64/libmariadbclient.a -lssl -lcrypto -liconv -lz"
%{python3_64} setup.py build --verbose

cd ../32bit
export OBJECT_MODE=32
export CPPFLAGS="-maix32"
export LDFLAGS="/opt/freeware/lib/libmariadbclient.a -lssl -lcrypto -liconv -lz"
%{python3_32} setup.py build --verbose


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
%{python3_64} setup.py install --root ${RPM_BUILD_ROOT} --install-lib %{python3_archlib_64}
cd ../32bit
%{python3_32} setup.py install --root ${RPM_BUILD_ROOT} --install-lib %{python3_archlib_32}

%check
%if %{with dotests}
su mysql -c "ulimit -d unlimited; /opt/freeware/libexec/mysqld --datadir=/opt/freeware/var/lib/mysql/data &"
sleep 5
ln -sf /opt/freeware/var/lib/mysql/mysql.sock /tmp/

ulimit -d unlimited

cd 64bit
#python3_64 -m venv mariadbTest
#. ./mariadbTest/bin/activate
#pip3 install --pre mariadb
(
  export OBEJCT_MODE=64
  PYTHONPATH=`pwd`/build/lib.aix-%{AIX_version}-3.%{python3_minor_version} \
  TEST_DATABASE=test \
  %{python3_64} -m unittest discover -v || true
)
#deactivate

cd ../32bit
(
  export OBEJCT_MODE=32
  PYTHONPATH=`pwd`/build/lib.aix-%{AIX_version}-3.%{python3_minor_version} \
  TEST_DATABASE=test \
  %{python3_32} -m unittest discover -v || true
)

mysqladmin shutdown
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n %{name}3.%{python3_minor_version}
%defattr(-,root,system,-)
%doc 64bit/LICENSE 64bit/README.md
%{python3_archlib_32}/*
%{python3_archlib_64}/*


%changelog
* Fri Mar 27 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> - 0.9.54-1
- First port on AIX
