%define name python-pygments
%define srcname Pygments
%define version 2.0rc1
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

Summary: Syntax highlighting engine written in Python
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/P/%{srcname}/%{srcname}-%{version}.tar.gz
Url:     http://pygments.org
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-setuptools
BuildRequires: python-nose
BuildArch:     noarch

%description

Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!

    The `Pygments tip`_ is installable with ``easy_install Pygments==dev``.

    .. _Pygments tip:
       http://bitbucket.org/birkenfeld/pygments-main/get/default.zip#egg=Pygments-dev

    :copyright: Copyright 2006-2013 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details

%prep
%setup -q -n %{srcname}-%{version}

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

install -d %{buildroot}%{_mandir}/man1

pwd

mv ../64bit/doc/pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

#%check
## make check

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/CHANGES 32bit/doc 32bit/LICENSE 32bit/TODO
/usr/bin/*
%{_bindir}/pygmentize
%{python_sitelib}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.0rc1-1
- first version for AIX V6.1 and higher
