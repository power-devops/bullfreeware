%define name python-pytest
%define srcname pytest
%define version 3.0.7
%define release 1

# The (old) Bull version of RPM python-docutls left ".py" suffix on rst2* tools
%define RST2HTML rst2html.py

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

# The test in this specfile use pytest-timeout
# When building pytest for the first time with new Python version
# that is not possible as it depends on pytest
%global timeout 0

%global pylib_version 1.4.29

Name:        %{name}
Version:     %{version}
Release:     %{release}
Summary:     Simple powerful testing with Python

License:     MIT
Group:       Development/Libraries
URL:         http://pytest.org
Source0:     https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-py >= %{pylib_version}
BuildRequires:  python-sphinx
BuildRequires:  python-docutils
BuildRequires:  python-hypothesis
%if %{timeout}
BuildRequires:  python-pytest-timeout
%endif
BuildRequires:  python-mock
BuildRequires:  python-twisted

BuildRequires:  python-jinja2

BuildRequires:  python-nose
BuildRequires:  python-argcomplete
BuildRequires:  python-decorator

%description
py.test provides simple, yet powerful testing for Python.


Requires:       python-setuptools
Requires:       python-py >= %{pylib_version}
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < 2.8.7-3


# A python3 build/install is not yet supported

# %package -n python3-%{name}
# Summary:        Simple powerful testing with Python
# Requires:       python3-setuptools
# Requires:       python3-py >= %{pylib_version}
# %{?python_provide:%python_provide python3-%{name}}
# 
# %description -n python3-%{name}
# py.test provides simple, yet powerful testing for Python.

# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# BuildRequires:  python3-py >= %{pylib_version}
# BuildRequires:  python3-hypothesis

# %if %{with timeout}
# BuildRequires:  python3-pytest-timeout
# %endif
# BuildRequires:  python3-mock

#BuildRequires:  python3-twisted
# BuildRequires:  python3-jinja2
# BuildRequires:  python3-nose
# BuildRequires:  python3-argcomplete
# BuildRequires:  python3-decorator


%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * .coveragerc
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


for l in doc/* ; do
  make -C $l html PYTHONPATH=$(pwd)
done
for f in README CHANGELOG CONTRIBUTING ; do
  %{RST2HTML} ${f}.rst > ${f}.html
done

# %if 0%{?_with_python3}
# %{py3_build}
# for l in doc/* ; do
#   make -C $l html PYTHONPATH=$(pwd)
# done
# for f in README CHANGELOG CONTRIBUTING ; do
#   rst2html ${f}.rst > ${f}.html
# done
# %endif


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-2.7_64
ln -snf pytest-2.7_64 %{buildroot}%{_bindir}/pytest-2_64
ln -snf pytest-2.7_64 %{buildroot}%{_bindir}/pytest_64
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-2.7_64
ln -snf py.test-2.7_64 %{buildroot}%{_bindir}/py.test-2_64
ln -snf py.test-2.7_64 %{buildroot}%{_bindir}/py.test_64


# %if 0%{?_with_python3}
# %{py3_install}
# mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python3_version}
# ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest-3
# mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python3_version}
# ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test-3
# 
# mkdir -p _htmldocs/html
# for l in doc/* ; do
  # remove hidden file
#   rm ${l}/_build/html/.buildinfo
#   mv ${l}/_build/html _htmldocs/html/${l##doc/}
# done

# remove shebangs from all scripts
find %{buildroot}%{python_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

# find %{buildroot}%{python3_sitelib} \
#      -name '*.py' \
#      -exec sed -i -e '1{/^#!/d}' {} \;


# %check
if [ "%{dotests}" == 1 ]
then

 (PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python_sitelib} \
  %{buildroot}%{_bindir}/pytest-2_64 -r s testing \
  %if %{timeout}
  --timeout=20
  %endif
           || true)
fi


# pushd python3
# PATH=%{buildroot}%{_bindir}:${PATH} \
# PYTHONPATH=%{buildroot}%{python3_sitelib} \
#   %{buildroot}%{_bindir}/pytest-3 -r s testing \
#   %if %{with timeout}
#   --timeout=20
#   %endif
# 
# popd

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-2.7
ln -snf pytest-2.7 %{buildroot}%{_bindir}/pytest-2
ln -snf pytest-2.7 %{buildroot}%{_bindir}/pytest
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-2.7
ln -snf py.test-2.7 %{buildroot}%{_bindir}/py.test-2
ln -snf py.test-2.7 %{buildroot}%{_bindir}/py.test

mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done

# remove shebangs from all scripts
find %{buildroot}%{python_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

# %check
if [ "%{dotests}" == 1 ]
then

 (PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python_sitelib} \
  %{buildroot}%{_bindir}/pytest-2 -r s testing \
  %if %{timeout}
  --timeout=20
  %endif
           || true)
fi


cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{srcname}
%defattr(-,root,system,-)
%doc 32bit/CHANGELOG.html 32bit/README.html 32bit/CONTRIBUTING.html
%doc 32bit/_htmldocs/html
# %license python2/LICENSE
%doc 32bit/LICENSE
%{_bindir}/pytest
%{_bindir}/pytest-2
%{_bindir}/pytest-2.7
%{_bindir}/pytest_64
%{_bindir}/pytest-2_64
%{_bindir}/pytest-2.7_64
%{_bindir}/py.test
%{_bindir}/py.test-2
%{_bindir}/py.test-2.7
%{_bindir}/py.test_64
%{_bindir}/py.test-2_64
%{_bindir}/py.test-2.7_64
/usr/bin/*
%{python_sitelib}/*
%{python_sitelib64}/*


# %files -n python3-%{srcname}
# %defattr(-,root,system,-)
# %doc python3/CHANGELOG.html python3/README.html python3/CONTRIBUTING.html
# %doc python3/_htmldocs/html
# %license python3/LICENSE
# %{_bindir}/pytest-3
# %{_bindir}/pytest-%{python3_version}
# %{_bindir}/py.test-3
# %{_bindir}/py.test-%{python3_version}
# %{python3_sitelib}/*
# %exclude %dir %{python3_sitelib}/__pycache__


%changelog
* Wed May 10 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.0.7-1
- Update to version 3.0.7

* Thu Jun 11 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 2.3.5-1
- first version for AIX V6.1 and higher

