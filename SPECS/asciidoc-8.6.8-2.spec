%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
#%define python64_sitelib %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

Summary: Text based document generation
Name: asciidoc
Version: 8.6.8
Release: 2
# The python code does not specify a version.
# The javascript example code is GPLv2+.
License: GPL+ and GPLv2+
Group: Applications/System
URL: http://www.methods.co.nz/asciidoc/
Source0: http://www.methods.co.nz/asciidoc/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: python >= 2.6.2, make, getopt >= 1.1.4, coreutils
Requires: python >= 2.6.2
Requires: libxslt >= 1.1.24-1
Requires: docbook-style-xsl >= 1.76.1-1

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH
gmake install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}

# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets ; do
    mv ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/${d} \
        ${RPM_BUILD_ROOT}%{_datadir}/%{name}
    ln -s %{_datadir}/%{name}/$d ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/
done

# Python API
install -Dpm 644 asciidocapi.py ${RPM_BUILD_ROOT}%{python_sitelib}/asciidocapi.py
install -Dpm 644 asciidocapi.py ${RPM_BUILD_ROOT}%{python64_sitelib}/asciidocapi.py

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc README BUGS CHANGELOG COPYRIGHT
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}
%{python_sitelib}/*
#%{python64_sitelib}/*
/usr/bin/*


%changelog
* Mon Jul 15 2013 Gerard Visiedo <gerard.visiedo@bull.net> 8.6.8-2
- Initial port on Aix6.1

* Wed Jul 18 2012 Michael Perzl <michael@perzl.org> - 8.6.8-1
- updated to version 8.6.8

* Thu Apr 19 2012 Michael Perzl <michael@perzl.org> - 8.6.7-1
- updated to version 8.6.7

* Sat Nov 19 2011 Michael Perzl <michael@perzl.org> - 8.6.6-1
- updated to version 8.6.6

* Sat Nov 19 2011 Michael Perzl <michael@perzl.org> - 8.6.3-2
- fixed rpm prerequisites

* Mon Nov 22 2010 Michael Perzl <michael@perzl.org> - 8.6.3-1
- updated to version 8.6.3

* Thu Nov 05 2009 Michael Perzl <michael@perzl.org> - 8.5.1-1
- first version for AIX V5.1 and higher
