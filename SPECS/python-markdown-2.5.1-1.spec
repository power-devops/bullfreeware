%define name python-markdown
%define srcname Markdown
%define version 2.5.1
%define release 1

%define is_python %(test -e /usr/bin/python && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /usr/bin/python_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Summary: Template engine and code generator
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz
Url:     http://packages.python.org/%{srcname}/
License: BSD
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildArch:     noarch
BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: PyYAML
Requires: python >= 2.4

%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%prep
%setup -q -n %{srcname}-%{version}
# remove shebangs
find markdown -type f -name '*.py' \
  -exec sed -i -e '/^#!/{1D}' {} \;

# fix line-ending
find bin docs -type f \
  -exec sed -i 's/\r//' {} \;


mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
cd 64bit
export OBJECT_MODE=64
python_64 setup.py build

cd ../32bit
export OBJECT_MODE=32
python setup.py build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
python_64 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

# 2.X binary is called by default for now
#ln -s markdown_py-%{python_version} %{buildroot}%{_bindir}/markdown_py

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

#%check
#python run-tests.py

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/build/docs/*
/usr/bin/*
%{_bindir}/*
%{python_sitelib}/*
#%{python_sitelib64}/*

%changelog
* Fri Nov 07 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.5.1-1
- first version for AIX V6.1 and higher
