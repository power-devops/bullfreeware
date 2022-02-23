Summary: Powerful, light-weight programming language
Name: lua
Version: 5.1.4
Release: 1
License: MIT License
Url: http://www.lua.org/
Group: Development/Other
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
Source: http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0: lua-5.1.4-aixconf.patch

%description 
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

%package devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for lua.

%prep
%setup -q

%patch0 -p1 -b .aixconf

%build
make aix

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README 
%{prefix}/bin/lua*
%{prefix}/lib/liblua.a
%{prefix}/man/man1/lua*.1
%dir  %{prefix}/lib/lua
%dir  %{prefix}/lib/lua/5.1
%dir  %{prefix}/share/lua
%dir  %{prefix}/share/lua/5.1

%files devel
%defattr(-,root,root,-)
%{prefix}/include/l*.h
%{prefix}/include/l*.hpp

%changelog
* Wed Feb 11 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.1.4
- Initial port for AIX
