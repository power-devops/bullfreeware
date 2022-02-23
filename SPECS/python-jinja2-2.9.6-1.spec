%define name python-jinja2
%define srcname Jinja2
%define version 2.9.6
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



%global with_python3 0
%global with_async 1

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 1


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        General purpose template engine for python2
Group:          Development/Languages
License:        BSD
URL:            http://jinja.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-markupsafe
BuildRequires:  python-pytest
%if 0%{?with_docs}
BuildRequires:  python-sphinx
%endif # with_docs

# %if 0%{?with_python3}
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# BuildRequires:  python3-markupsafe
# #BuildRequires:  python3-pytest
# %endif # with_python3


%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.


Requires:       python-babel >= 0.8
Requires:       python-markupsafe
Requires:       python-setuptools
Provides:       python-jinja2



# %if 0%{?with_python3}
# %package -n python3-jinja2
# Summary:        General purpose template engine for python3
# Group:          Development/Languages
# Requires:       python3-markupsafe
# Requires:       python3-setuptools
# babel isn't py3k ready yet, and is only a weak dependency
#Requires:       python3-babel >= 0.8
# %{?python_provide:%python_provide python3-jinja2}
# 
# %description -n python3-jinja2
# Jinja2 is a template engine written in pure Python.  It provides a
# Django inspired non-XML syntax but supports inline expressions and an
# optional sandboxed environment.
# 
# If you have any exposure to other text-based template languages, such
# as Smarty or Django, you should feel right at home with Jinja2. It's
# both designer and developer friendly by sticking to Python's
# principles and adding functionality useful for templating
# environments.
# %endif # with_python3


%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -exec rm {} \;

# fix EOL
sed -i 's|\r$||g' LICENSE

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# %if 0%{?_with_python3}
# rm -rf %{py3dir}
# cp -a . %{py3dir}
# %endif # with_python3


# A python3 build/install is not yet supported

%build

cd 64bit
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64  setup.py build

cd ../32bit
export OBJECT_MODE=32
/opt/freeware/bin/python2.7  setup.py build


# Build docs under Python 2.7 32bit
%if 0%{?with_docs}
make -C docs html PYTHONPATH=$(pwd)
%endif # with_docs

# %if 0%{?with_python3}
# cd 64bit
# export OBJECT_MODE=64
# /opt/freeware/bin/python3.5_64  setup.py build
#
# cd ../32bit
# export OBJECT_MODE=32
# /opt/freeware/bin/python3.5  setup.py build
#
# %endif # with_python3


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Remove hidden file
rm -rf docs/_build/html/.buildinfo

# Remove files valid only on Python 3.6+
rm %{buildroot}%{python_sitelib}/jinja2/asyncsupport.py
rm %{buildroot}%{python_sitelib}/jinja2/asyncfilters.py


# %check
# Currently no tests in jinja2 (2.9.6)
# make test
# if [ "%{dotests}" == 1 ]
# then
#  (/opt/freeware/bin/python2.7_64 -m tornado.test.runtests --verbose || true)
# fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Remove hidden file
rm -rf docs/_build/html/.buildinfo

# Remove files valid only on Python 3.6+
rm %{buildroot}%{python_sitelib}/jinja2/asyncsupport.py
rm %{buildroot}%{python_sitelib}/jinja2/asyncfilters.py


# %check
# Currently no tests in jinja2 (2.9.6)
# make test
# if [ "%{dotests}" == 1 ]
# then
#  (/opt/freeware/bin/python2.7 -m tornado.test.runtests --verbose || true)
# fi




# %if 0%{?with_python3}
# cd 64bit
# /opt/freeware/bin/python3.5_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# 
# Remove hidden file
# rm -rf docs/_build/html/.buildinfo
# 
# 
# %if ! 0%{?with_async}
# rm %{buildroot}%{python3_sitelib}/jinja2/asyncsupport.py
# rm %{buildroot}%{python3_sitelib}/jinja2/asyncfilters.py
# %endif
# %endif # with_python3

# %if 0%{?with_python3}
# Currently no tests in jinja2 (2.9.6)
# make test
# if [ "%{dotests}" == 1 ]
# then
#  (/opt/freeware/bin/python3.5_64 -m tornado.test.runtests --verbose || true)
# fi
# %endif # with_python3


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files -n python-jinja2
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/CHANGES
# %license LICENSE
%doc 32bit/LICENSE
%if 0%{?with_docs}
%doc 32bit/docs/_build/html
%endif # with_docs
%doc 32bit/ext
%doc 32bit/examples
%{python_sitelib}/jinja2
%{python_sitelib}/Jinja2-%{version}-py?.?.egg-info
%{python_sitelib64}/jinja2
%{python_sitelib64}/Jinja2-%{version}-py?.?.egg-info
# %exclude %{python_sitelib}/jinja2/_debugsupport.c
# %exclude %{python_sitelib64}/jinja2/_debugsupport.c


# %if 0%{?with_python3}
# %defattr(-,root,system,-)
# %files -n python3-jinja2
# %doc AUTHORS CHANGES
# %license LICENSE
# %doc 32bit/LICENSE
# %if 0%{?with_docs}
# docs are built with python2
# %doc docs/_build/html
# %endif # with_docs
# %doc ext
# %doc examples
# %{python3_sitelib}/jinja2
# %{python3_sitelib}/Jinja2-%{version}-py?.?.egg-info
# %{python3_sitelib64}/jinja2
# %{python3_sitelib64}/Jinja2-%{version}-py?.?.egg-info
# %exclude %{python3_sitelib}/jinja2/_debugsupport.c
# %exclude %{python3_sitelib64}/jinja2/_debugsupport.c
# %endif # with_python3


%changelog
* Wed May 24 2017 Michael Wilson <michael.a.wilson@atos.net> - 2.9.6-1
- Update to 2.9.6

* Thu Jul 16 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 2.7-1
- - first version for AIX V6.1 and higher

