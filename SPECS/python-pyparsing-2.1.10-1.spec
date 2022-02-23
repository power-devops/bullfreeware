%define name python-pyparsing
%define srcname pyparsing
%define version 2.1.10
%define release 1

# %global build_wheel 1
# 
# %global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
# %global python3_wheelname %python2_wheelname

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

%global with_python3 0

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   Python package with an object-oriented approach to text processing

Group:    Development/Libraries
License:  MIT
URL:      http://pyparsing.wikispaces.com/
Source0:  http://downloads.sourceforge.net/pyparsing/pyparsing-%{version}.tar.gz

BuildArch:   noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:      %{_prefix}

BuildRequires:  dos2unix
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# %if 0%{?with_python3}
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# %endif

# %if 0%{?build_wheel}
# BuildRequires:  python2-pip
# BuildRequires:  python-wheel
# BuildRequires:  python%{python3_pkgversion}-pip
# BuildRequires:  python%{python3_pkgversion}-wheel
# %endif

Requires:      python-%{srcname} = %{version}-%{release}
%{?python_provide:%python_provide python-%{srcname}}

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.


%package        doc
Summary:        Documentation for pyparsing python package
Group:          Documentation

%description    doc
The package contains documentation for pyparsing.



# A python3 build/install is not yet supported

# %if 0%{?with_python3}
# %package -n python3-pyparsing
# Summary:        %{sum}
# %{?python_provide:%python_provide python3-%{srcname}}
# 
# %description -n python3-pyparsing
# pyparsing is a module that can be used to easily and directly configure syntax
# definitions for any number of text parsing applications.
# 
# This is the Python 3 version.
# %endif # with_python3


%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"

mv docs/pyparsingClassDiagram.PNG docs/pyparsingClassDiagram.png
rm docs/pyparsingClassDiagram.JPG
# dos2unix -k CHANGES LICENSE README

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * .coveragerc
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

cd 64bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7_64  setup.py build
# %endif

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6_64  setup.py build
# %endif


cd ../32bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7  setup.py build
# %endif

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6  setup.py build
# %endif



%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
 echo No tests defined
fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

cd ../32bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
 echo No tests defined
fi


# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files -n python-pyparsing
%doc 32bit/LICENSE
%doc 32bit/CHANGES 32bit/README
%{python_sitelib}/pyparsing.py*
%{python_sitelib}/pyparsing-*egg-info/
%{python_sitelib64}/pyparsing.py*
%{python_sitelib64}/pyparsing-*egg-info/

# %files -n python3-pyparsing
# %doc 32bit/LICENSE
# %doc 32bit/CHANGES 32bit/README 32bit/LICENSE
# %{python3_sitelib}/pyparsing.py
# %{python3_sitelib}/__pycache__/*
# %{python3_sitelib}/pyparsing-*egg-info/
# %{python3_sitelib64}/pyparsing.py
# %{python3_sitelib64}/__pycache__/*
# %{python3_sitelib64}/pyparsing-*egg-info/


%files doc
%doc 32bit/LICENSE
%doc 32bit/CHANGES 32bit/README 32bit/HowToUsePyparsing.html 32bit/docs 32bit/examples 32bit/htmldoc


%changelog
* Fri Jan 12 2018 Michael Wilson <michael.a.wilson@atos.net> - 2.1.10-1
- Update to version 2.1.10 for setuptools/rrdtools
- Add separate package python-pyparsing-doc and provision for Python 3

* Thu Jun 27 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 1.5.7-1
- first version for AIX V6.1 and higher

