%define name python-hypothesis
%define srcname hypothesis
%define version 3.4.0
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}


# Needs care because default command python may be linked to 32 or 64 bit python
# and compiler/loader options are not the same, e.g. -maix32/-maix64
# Also, although
#     /usr/bin/python_64 eventually links to /opt/freeware/bin/python2.7_64
#     /usr/bin/python_32 links to inexistant /opt/freeware/bin/python2_32
# So, use /opt/freeware/bin/python2.7 and /opt/freeware/bin/python2.7_64

%define is_python %(test -e /opt/freeware/bin/python2.7 && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(/opt/freeware/bin/python2.7 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /opt/freeware/bin/python2.7_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(/opt/freeware/bin/python2.7_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif


Name:           %{name}
Version:        %{version}
Release:        %{release}
Group:          Development/Libraries
Summary:        A library for property based testing

License:        MPLv2.0
URL:            https://github.com/DRMacIver/hypothesis
Source0:        https://github.com/DRMacIver/hypothesis/archive/%{version}.tar.gz#/hypothesis-%{version}.tar.gz

# disable Sphinx extensions that require Internet access
# Patch0:         %{srcname}-2.0.0-offline.patch

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python-enum34

# BuildRequires:  python3-devel

Provides:       python-hypothesis = %{version}-%{release}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log


%description
Hypothesis is a library for testing your Python code against a much
larger range of examples than you would ever want to write by
hand. It’s based on the Haskell library, Quickcheck, and is designed
to integrate seamlessly into your existing Python unit testing work
flow.



# %package     -n python3-%{srcname}
# Summary:        A library for property based testing
# Provides:       python3-hypothesis = %{version}-%{release}
# 
# Suggests:       python3-numpy
# Suggests:       python3-pytz
# 
# %description -n python3-%{srcname}
# Hypothesis is a library for testing your Python code against a much
# larger range of examples than you would ever want to write by
# hand. It’s based on the Haskell library, Quickcheck, and is designed
# to integrate seamlessly into your existing Python unit testing work
# flow.


%prep
# %autosetup -n %{srcname}-python-%{version}
%setup -n %{srcname}-python-%{version}

echo "dotests=%{dotests}"

# %patch1 -p1

# remove shebang, mergedbs gets installed in sitelib
# sed has to be /opt/freeware because of "-i" option
sed -i -e 1,2d src/hypothesis/tools/mergedbs.py

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * ./.[cgt]*
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build

# First build the 64-bit version
cd 64bit
/opt/freeware/bin/python2.7_64 setup.py build
# Pb inline in sphinx/docutils
# READTHEDOCS=True sphinx-build -b man docs docs/_build/man

# Build the 32-bit version
cd ../32bit
/opt/freeware/bin/python2.7 setup.py build
# READTHEDOCS=True sphinx-build -b man docs docs/_build/man


# %py3_build

# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --prefix=%{_prefix} --root ${RPM_BUILD_ROOT}

# Currently there are no tests
if [ "%{dotests}" == 1 ]
then
  (PYTHONPATH=%{buildroot}%{python_sitelib} /opt/freeware/bin/python2.7_64 -m pytest tests/cover tests/py2 || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --prefix=%{_prefix} --root ${RPM_BUILD_ROOT}

# %{__install} -Dp -m 644 docs/_build/man/hypothesis.1 \
#              $RPM_BUILD_ROOT%{_mandir}/man1/hypothesis.1

# Currently there are no tests
if [ "%{dotests}" == 1 ]
then
  (PYTHONPATH=%{buildroot}%{python_sitelib} /opt/freeware/bin/python2.7 -m pytest tests/cover tests/py2 || true)
fi


# %py3_install


%files -n python-%{srcname}
# %license LICENSE.txt
%doc 32bit/LICENSE.txt 32bit/README.rst
%{python_sitelib}/*
%{python_sitelib64}/*
# %{_mandir}/man1/hypothesis.1*

# %files -n python3-%{srcname}
# %license LICENSE.txt
# %doc 32bit/LICENSE.txt 32bit/README.rst
# %{python3_sitelib}/*
# %{python3_sitelib64}/*
# %{_mandir}/man1/hypothesis.1*

%changelog
* Mon May 15 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.4.0-1
- Initial version

