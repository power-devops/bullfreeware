Summary: The GTK+ Object Builder, a preprocessor for making GObjects with inline C code
Name: gob2
Version: 2.0.18
Release: 1
License: GPL
Group: Development/Tools
URL: http://www.5z.com/jirka/gob.html

Source: http://ftp.5z.com/pub/gob/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

### gob2 2.0.9 was the last one to generate glib 2.2 compatible code
BuildRequires: glib2-devel >= 2.4.0, flex, bison

%description
GOB is a simple preprocessor for making GTK+ objects.  It makes objects from a
single file which has inline C code so that you don't have to edit the
generated files.  Syntax is somewhat inspired by java and yacc.

%prep
%setup

%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

./configure --prefix=%{_prefix}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_prefix}/bin/* .
)


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, system, 0755)
%doc AUTHORS NEWS README TODO
%doc examples/*.gob
%doc %{_datadir}//man/man1/*
%{_bindir}/*
%{_datadir}/aclocal/*
/usr/bin/*

%changelog
* Wed Jul 18 2012 <gerard.visiedo@bull.net> - 2.0.18-1
- Initial port on Aix6.1

