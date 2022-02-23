# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define macro_location /usr/opt/rpm/lib/rpm/macros.d

%global version     3.9
%global pyshortver  39

Summary: The Python interpreter
Name: python3
Version: %{version}
Release: 1
License: Modified CNRI Open Source License
Group: Development/Languages
URL: http://www.python.org/
Source1:  macros.python
Source10: %{name}-%{version}-%{release}.build.log

Requires: python%{version}

Provides: python(abi) = %{version}

Obsoletes: python3-docs < 3.9

%description
Python is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The python package provides the python executable: the reference
interpreter for the Python language, version 3 and majority of its standard library.
The remaining parts of the Python standard library are broken out into the
python-tkinter and python-test packages, which may need to be installed
separately.

IDLE for Python is provided in the python-idle package and
development files are provided through python-devel package


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}
Requires: python%{version}-devel

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains 2to3 tool, an automatic source converter from Python 2.X.


%package idle
Summary: A basic graphical development environment for Python
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}
Requires: python%{version}-idle

Obsoletes: python3-tools < 3.9

%description idle
IDLE is Python's Integrated Development and Learning Environment.

IDLE has the following features: Python shell window (interactive
interpreter) with colorizing of code input, output, and error messages;
multi-window text editor with multiple undo, Python colorizing,
smart indent, call tips, auto completion, and other features;
search within any window, replace within editor windows, and
search through multiple files (grep); debugger with persistent
breakpoints, stepping, and viewing of global and local namespaces;
configuration, browsers, and other dialogs.


%package tkinter
Summary: A GUI toolkit for Python
Requires: %{name} = %{version}-%{release}
Requires: python%{version}-tkinter

%description tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package test
Summary: The self-test suite for the main python3 package
Requires: %{name} = %{version}-%{release}
Requires: python%{version}-test

%description test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{pkgname}, or a library such as
pytest.


%prep

%build

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_bindir}

cd $RPM_BUILD_ROOT%{_bindir}
for bin in pydoc python
do
    ln -s ${bin}%{version} ${bin}3
done

# Install macros
mkdir -p ${RPM_BUILD_ROOT}%{macro_location}
cp %SOURCE1 ${RPM_BUILD_ROOT}%{macro_location}

%check
%if %{with dotests}
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/*
%{macro_location}/macros.python

%files devel
%defattr(-,root,system)

%files idle
%defattr(-,root,system,-)

%files tkinter
%defattr(-,root,system,-)

%files test
%defattr(-,root,system,-)

%changelog
* Mon Nov 22 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 3.9-1
- Creation of metapackage
