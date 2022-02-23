%define __noautoreq			'perl\\(Text::Unidecode\\)|perl\\(Tie::Watch\\)|perl\\(SelfLoader\\)'

%define _tlpkgdir			%{_datadir}/tlpkg
%define _texmfdir			%{_datadir}/texmf
%define _texmfdistdir			%{_datadir}/texmf-dist
%define _texmflocaldir			%{_datadir}/texmf-local
%define _texmfextradir			%{_datadir}/texmf-extra
%define _texmffontsdir			%{_datadir}/texmf-fonts
%define _texmfprojectdir		%{_datadir}/texmf-project
%define _texmfvardir			%{_localstatedir}/lib/texmf
%define _texmfconfdir			%{_sysconfdir}/texmf
%define _texmf_fmtutil_d		%{_datadir}/tlpkg/fmtutil.cnf.d
%define _texmf_updmap_d			%{_datadir}/tlpkg/updmap.cfg.d
%define _texmf_language_dat_d		%{_datadir}/tlpkg/language.dat.d
%define _texmf_language_def_d		%{_datadir}/tlpkg/language.def.d
%define _texmf_language_lua_d		%{_datadir}/tlpkg/language.lua.d

%define _texmf_enable_asymptote		0
%define _texmf_enable_biber		0
%define _texmf_enable_xindy		0
%define _texmf_with_system_dialog	1
%define _texmf_with_system_lcdf		0
%define _texmf_with_system_poppler	1
%define _texmf_with_system_psutils	1
%define _texmf_with_system_t1lib	1
%define _texmf_with_system_tex4ht	0
%define _texmf_with_system_teckit	0

Name:		texlive-tlpkg
Version:	20141127
Release:	1
Summary:	The TeX formatting system
URL:		http://tug.org/texlive/
Group:		Publishing
License:	http://www.tug.org/texlive/LICENSE.TL
Source0:	http://mirrors.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
Source1:	http://mirrors.ctan.org/systems/texlive/tlnet/tlpkg/texlive.tlpdb.xz
Source2:	tlpobj2spec.pl
Source3:	fmtutil-hdr.cnf
Source4:	updmap-hdr.cfg
Source5:	texlive.post
Source6:	checkupdates.pl
Source7:	texlive.macros
Source8:	tlmgr
BuildRoot:	/var/tmp//%{name}-%{version}-%{release}-root
BuildArch:	noarch

Requires:	perl-Proc-Daemon
Requires:	perl-Proc-PID-File
Requires:	perl-XML-XPath

%post
    if [ ! -f %{_texmfconfdir}/web2c/updmap.cfg ]; then
	cp -f %{_texmfdir}/web2c/updmap-hdr.cfg %{_texmfconfdir}/web2c/updmap.cfg
    fi
    %{_sbindir}/texlive.post

%description
TeX Live is an easy way to get up and running with the TeX document
production system. It provides a comprehensive TeX system. It includes
all the major TeX-related programs, macro packages, and fonts that are
free software, including support for many languages around the world.

%files
%defattr(-,root,system,755)
%dir %{_tlpkgdir}
%{_tlpkgdir}/TeXLive/
%{_texmfdir}/web2c/fmtutil-hdr.cnf
%{_texmfdir}/web2c/updmap-hdr.cfg
%dir %{_texmf_fmtutil_d}
%dir %{_texmf_updmap_d}
%dir %{_texmf_language_dat_d}
%dir %{_texmf_language_def_d}
%dir %{_texmf_language_lua_d}
%ghost %{_texmfconfdir}/web2c/updmap.cfg
/usr/bin/*
/usr/sbin/*
%{_bindir}/tlmgr
%{_sbindir}/tlmgr
%{_sbindir}/texlive.post
%{_sysconfdir}/rpm/macros.d/texlive.macros
%{_sysconfdir}/pam.d/tlmgr
%{_sysconfdir}/console.apps/tlmgr

#-----------------------------------------------------------------------
%prep
%setup -q -n install-tl-%{version}

%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_tlpkgdir}
cp -fpr tlpkg/TeXLive %{buildroot}%{_tlpkgdir}

mkdir -p %{buildroot}%{_texmf_fmtutil_d}
mkdir -p %{buildroot}%{_texmf_updmap_d}
mkdir -p %{buildroot}%{_texmf_language_dat_d}
mkdir -p %{buildroot}%{_texmf_language_def_d}
mkdir -p %{buildroot}%{_texmf_language_lua_d}

install -D -m644 %{SOURCE3} %{buildroot}%{_texmfdir}/web2c/fmtutil-hdr.cnf
install -D -m644 %{SOURCE4} %{buildroot}%{_texmfdir}/web2c/updmap-hdr.cfg
install -D -m644 %{SOURCE4} %{buildroot}%{_texmfconfdir}/web2c/updmap.cfg
install -D -m755 %{SOURCE5} %{buildroot}%{_sbindir}/texlive.post
install -D -m644 %{SOURCE7} %{buildroot}%{_sysconfdir}/rpm/macros.d/texlive.macros

# install tlmgr like application
install -D -m755 %{SOURCE8} %{buildroot}%{_sbindir}/tlmgr
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/tlmgr
mkdir -p %{buildroot}%{_sysconfdir}/console.apps
cat > %{buildroot}%{_sysconfdir}/console.apps/tlmgr << EOF
USER=root
PROGRAM=%{_sbindir}/tlmgr
FALLBACK=false
SESSION=true
EOF
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/tlmgr

(
 cd ${RPM_BUILD_ROOT}
  for dir in bin sbin
  do
 	mkdir -p usr/$dir
 	cd usr/$dir
 	ln -sf ../..%{_prefix}/$dir/* .
	cd -
  done
)


%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20141127-1
- First version for AIX V6.1 and higher
