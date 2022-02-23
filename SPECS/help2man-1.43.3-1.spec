# Supported build option:
#

Name:           help2man
Summary:        Create simple man pages from --help output
Version:        1.43.3
Release:        1
Group:          Development/Tools
License:        GPLv3+
URL:            http://www.gnu.org/software/help2man
Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.gz

BuildRoot: /var/opt/freeware/%{name}-%{version}-root
BuildArch: noarch


%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.


%prep
%setup -q -n help2man-%{version}

%build
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`

./configure --prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--libdir=%{_libdir}/help2man

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
#%find_lang %name --with-man

(
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .
)

%post
/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/help2man.info \
    %{_infodir}/dir 2>/dev/null || :
fi

#%files -f %name.lang
%files
%doc README NEWS THANKS COPYING
/usr/bin/help2man
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*


%changelog
* Tue Nov 18 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.43.3-1
- Initial port on Aix6.1
