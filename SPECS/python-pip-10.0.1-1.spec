%define name python-pip
%define srcname pip
%define version 10.0.1
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

Summary: Tool for installing and managing Python packages.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{srcname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Url: https://pypi.python.org/pypi/pip/9.0.1

BuildRequires: python, python-devel
BuildRequires: python-setuptools >= 0.9.8-2
Requires: python-setuptools >= 0.9.8-2
Requires: python

%description
Tool for installing and managing Python packages.

%prep
%setup -q -n %{srcname}-%{version}

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
cd 64bit
python_64 setup.py build

cd ../32bit
python setup.py build

# Building docs.
cd docs
gmake

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

mkdir %{buildroot}%{_libdir}64
mv ${RPM_BUILD_ROOT}%{_libdir}/* ${RPM_BUILD_ROOT}%{_libdir}64/

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in *
  do
    mv ${f} ${f}_64
  done
)

cd ../32bit
#cd 32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Create links into /usr/bin 
(
    cd $RPM_BUILD_ROOT
    mkdir -p usr/bin
    cd usr/bin
    ln -sf ../..%{prefix}/bin/* .
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE.txt 32bit/PKG-INFO 32bit/README.rst 
%{python_sitelib}/*
%{python_sitelib64}/*
%{_prefix}/bin/*
/usr/bin/*

%changelog
* Tue May 21 2019 Tony Reix <tony.reix@atos.net> - 10.0.1-1
- Port on BullFreeware

* Wed Jun 13 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 10.0.1-1
- Updated to 10.0.1

* Wed Feb 22 2017 Sangamesh Mallayya <smallayy@in.ibm.com> 9.0.1-1
- Initial port to AIX.
