%define name python-cherrypy
%define srcname CherryPy
%define version 3.6.0
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

Summary: Pythonic, object-oriented web development framework
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://download.cherrypy.org/%{srcname}-%{version}.tar.gz
# Don't ship the tests or tutorials in the python module directroy,
# tutorial will be shipped as doc instead
Patch0:         python-cherrypy-tutorial-doc.patch

Url:     http://www.cherrypy.org
License: MIT
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-setuptools
BuildRequires: python-nose
BuildArch:     noarch

%description
CherryPy allows developers to build web applications in much the same way
they would build any other object-oriented Python program. This usually
results in smaller source code developed in less time.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1
sed -i 's/\r//' README.txt cherrypy/tutorial/README.txt cherrypy/tutorial/tutorial.conf

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
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

(
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .
)
#%check
#cd cherrypy/test
## These two tests hang in the buildsystem so we have to disable them.
## The third fails in cherrypy 3.2.2.
#PYTHONPATH='../../' nosetests -s ./ -e 'test_SIGTERM' -e \
#  'test_SIGHUP_tty' -e 'test_file_stream'

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/README.txt
%doc 32bit/cherrypy/tutorial
%{_bindir}/cherryd
/usr/bin/cherryd
%{python_sitelib}/*


%changelog
* Fri Nov 21 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 3.6.0-1
- First version for AIX V6.1 and higher
