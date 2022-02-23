%bcond_without dotests

%define meta_name Cython
%define desc Cython is an optimising static compiler for both the Python \
programming language and the extended Cython programming language \
(based on Pyrex). \
It makes writing C extensions for Python as easy as Python itself.

Name:           python3-Cython
Version:        0.29.24
Release:        1
Summary:        Language for writing Python extension modules

License:        ASL 2.0
URL:            http://www.cython.org
Source0:        https://github.com/cython/cython/archive/%{version}/%{meta_name}-%{version}.tar.gz
Source1:        %{name}-%{version}-%{release}.build.log

BuildRequires: gcc
BuildRequires: python(abi) >= 3.9
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools

Provides:      Cython = %{version}-%{release}

%python_meta_requires

%description
%desc

%python_module
%python_module_desc


%prep
%setup -q -n %{meta_name}-%{version}


%build
build_cython () {
  set -ex
  export OBJECT_MODE=$1
  export LFALGS="-lpthread"
  export CC="gcc -lpthread -maix${OBJECT_MODE} %{optflags}"
  export FC="gfortran -lpthread -maix${OBJECT_MODE} %{optflags}"
  %{__python} setup.py build
}

export LDFLAGS="-lpthread"
build_cython 64


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

install_cython () {
  set -ex
  export OBJECT_MODE=$1
  export LFALGS="-lpthread"
  export CC="gcc -lpthread -maix${OBJECT_MODE} %{optflags}"
  export FC="gfortran -lpthread -maix${OBJECT_MODE} %{optflags}"
  %{__python} setup.py install --root %{buildroot}
}

export LDFLAGS="-lpthread"
install_cython 64


%check
%if %{with dotests}
# Avoid ld warnings
export LDFLAGS="-Wl,-bnoerrmsg"

# We cannot run all test in the same run.
# Flags are
# --no-unit --no-file --no-examples

%{__python} -m venv python_venv
. ./python_venv/bin/activate
pip3 install pytest
ulimit -d unlimited
# ulimit -s unlimited
ulimit -n unlimited
ulimit -m unlimited
# ulimit -f unlimited
export CC="gcc -maix64"
export CXX="g++ -maix64"

( python runtests.py -3 -v            --no-file --no-examples || true )
( python runtests.py -3 -v --no-unit            --no-examples || true )
( python runtests.py -3 -v --no-unit  --no-file               || true )

deactivate
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)

%files -n %{module_name}
%defattr(-,root,system,-)
%doc LICENSE.txt
%doc *.txt Demos Tools

# 64 bits only
%{_bindir}/cython
%{_bindir}/cygdb
%{_bindir}/cythonize

%{python_sitearch64}/Cython-*.egg-info
%{python_sitearch64}/Cython
%{python_sitearch64}/pyximport
%{python_sitearch64}/cython.py


%changelog
* Wed Nov 24 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 0.29.24-1
- New version 0.29.24
- Add metapackage
- Drop 32 bits support

* Wed Jul 01 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.29.20-1
- First port on AIX
