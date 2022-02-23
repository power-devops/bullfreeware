%bcond_without dotests

Name:           Cython
Version:        0.29.20
Release:        1
Summary:        Language for writing Python extension modules

License:        ASL 2.0
URL:            http://www.cython.org
Source0:        https://github.com/cython/cython/archive/%{upver}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-%{release}.build.log


%define _libdir64 %{_libdir}64

%define python3_sitearch32 %(python3_32 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python3_sitearch64 %(python3_64 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python3_minor_version %(/opt/freeware/bin/python3 -c "import sys; print(sys.version.split('.')[1])")


%description
Cython is an optimising static compiler for both the Python
programming language and the extended Cython programming language
(based on Pyrex).
It makes writing C extensions for Python as easy as Python itself.


%package -n python3.%{python3_minor_version}-Cython
Summary:        Language for writing Python extension modules
License:        ASL 2.0

BuildRequires: gcc
BuildRequires: python3-devel >= 3.8
BuildRequires: python3-pip
BuildRequires: python3-setuptools

Requires:      python3 >= 3.8

Provides:      Cython = %{version}-%{release}

%description -n python3.%{python3_minor_version}-Cython
Cython is an optimising static compiler for both the Python
programming language and the extended Cython programming language
(based on Pyrex).
It makes writing C extensions for Python as easy as Python itself.


%prep
%autosetup -n %{name}-%{version} -p1

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
build_cython () {
  set -ex
  export OBJECT_MODE=$1
  export LFALGS="-lpthread"
  export CC="gcc -lpthread -maix${OBJECT_MODE} %{optflags}"
  export FC="gfortran -lpthread -maix${OBJECT_MODE} %{optflags}"
  python3_${OBJECT_MODE} setup.py build
}

cd 32bit
export OBJECT_MODE=32
export LDFLAGS="-lpthread -Wl,-bmaxdata:0x80000000"
build_cython 32

cd ../64bit
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
  python3_${OBJECT_MODE} setup.py install --root %{buildroot}
}

cd 32bit
export LDFLAGS="-lpthread -Wl,-bmaxdata:0x80000000"
install_cython 32

cd ../64bit
export LDFLAGS="-lpthread"
install_cython 64


%check
%if %{with dotests}
# Avoid ld warnings
export LDFLAGS="-Wl,-bnoerrmsg"

# We cannot run all test in the same run.
# Flags are
# --no-unit --no-file --no-examples

cd 64bit
python3_64 -m venv python_venv
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

cd ../32bit
python3_32 -m venv python_venv
. ./python_venv/bin/activate
pip3 install pytest
ulimit -d unlimited
# ulimit -s unlimited
ulimit -n unlimited
ulimit -m unlimited
# ulimit -f unlimited
export CC="gcc -maix32"
export CXX="g++ -maix32"

( python runtests.py -3 -v            --no-file --no-examples || true )
( python runtests.py -3 -v --no-unit            --no-examples || true )
( python runtests.py -3 -v --no-unit  --no-file               || true )

deactivate
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python3.%{python3_minor_version}-Cython
%defattr(-,root,system,-)
%doc 64bit/LICENSE.txt
%doc 64bit/*.txt 64bit/Demos 64bit/Tools

# 64 bits only
%{_bindir}/cython
%{_bindir}/cygdb
%{_bindir}/cythonize

%{python3_sitearch64}/%{name}-*.egg-info
%{python3_sitearch64}/%{name}
%{python3_sitearch64}/pyximport
%{python3_sitearch64}/cython.py

%{python3_sitearch32}/%{name}-*.egg-info
%{python3_sitearch32}/%{name}
%{python3_sitearch32}/pyximport
%{python3_sitearch32}/cython.py


%changelog
* Wed Jul 01 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.29.20-1
- First port on AIX
