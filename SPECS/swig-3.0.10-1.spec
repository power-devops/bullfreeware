#!/usr/bin/bash

# You can build the package from SVN using something like:
# tar -czf swig-1.3.39.tar.gz swig-1.3.39 && rpmbuild -tb swig-1.3.39.tar.gz
# swig.spec.  Generated from swig.spec.in by configure.

%define ver          3.0.10
%define rel          1
# %define prefix       /usr
%define home_page    http://www.swig.org
%define docprefix    %{_prefix}/share

######################################################################
# Usually, nothing needs to be changed below here between releases
######################################################################
Summary: Simplified Wrapper and Interface Generator
Name: swig
Version: %{ver}
Release: %{rel}
URL: %{home_page}
Source0: %{name}-%{version}.tar.gz
License: BSD
Group: Development/Tools
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildPrereq: perl, python-devel

%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
SWIG is a software development tool that connects programs written in C and C++
with a variety of high-level programming languages. SWIG is primarily used with
common scripting languages such as Perl, Python, Tcl/Tk, and Ruby, however the
list of supported languages also includes non-scripting languages such as Java,
OCAML and C#. Also several interpreted and compiled Scheme implementations
(Guile, MzScheme, Chicken) are supported. SWIG is most commonly used to create
high-level interpreted or compiled programming environments, user interfaces,
and as a tool for testing and prototyping C/C++ software. SWIG can also export
its parse tree in the form of XML and Lisp s-expressions. 

%prep
%setup -q -n %{name}-%{version}


%build

# so we can build package from SVN source too
[ ! -r configure ] && ./autogen.sh

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`

export CC=/usr/vac/bin/xlc_r
export CXX=/usr/vacpp/bin/xlC_r

CFLAGS="-O2" \
CXXFLAGS="-O2" \
LIBCFLAGS="-O2" \
./configure \
	--prefix=%{_prefix} \
	--build=powerpc-ibm-aix6.1.0.0 \
	--host=powerpc-ibm-aix6.1.0.0 \
	--target=powerpc-ibm-aix6.1.0.0
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc ANNOUNCE CHANGES COPYRIGHT INSTALL LICENSE LICENSE-GPL LICENSE-UNIVERSITIES RELEASENOTES
%doc Doc/*
%{_bindir}/*
%{_datadir}/*
/usr/bin/*

%changelog
* Wed Jun 29 2016 Laurent GAY <laurent.gay@atos.net> - 3.0.10-1
- Update to 3.0.10 on Aix

* Wed Jul 03 2013 Gerard.Visiedo <gerard.visiedo@bull.net> - 2.0.10-2
- Update to 2.0.10 on Aix5.3

* Wed Jun 19 2013 Gerard.Visiedo <gerard.visiedo@bull.net> - 2.0.10-1
- Initial port on Aix6.1

* Tue Jun 28 2011 Gerard.Visiedo <gerard.visiedo@bull.net> - 2.0.4-1
- Update to 2.0.4

* Thu Jul 30 2009 BULL  1.3.39
- Integrate in Aix 5.3 toolbox packages
