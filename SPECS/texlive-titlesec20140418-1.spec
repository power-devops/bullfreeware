#
# spec file for package 
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name: texlive-titlesec
Version: 20140418
Release: 1
License: LPPL-1.0
Summary: Select alternative section titles
Group: Productivity/Publishing/TeX/Base
Url: http://www.tug.org/texlive/
Provides: tex(titleps.sty)
Provides: tex(titlesec.sty)
Provides: tex(titletoc.sty)
Provides: tex(ttlkeys.def)
Provides: tex(ttlps.def)
# Download at ftp://ftp.ctan.org/pub/tex/systems/texlive/tlnet/archive/
Source0: titlesec.tar.xz
Source1: titlesec.doc.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch


%define _texmfdistdir	%{_datadir}/texmf
%define _texmfmaindir	%{_libexecdir}/texmf
%define _texmfdirs	\{%{_texmfdistdir},%{_texmfmaindir}\}

%define _texmfconfdir	%{_sysconfdir}/texmf
%define _texmfvardir	%{_varlib}/texmf
%define _texmfcache	%{_localstatedir}/cache/texmf
%define _fontcache	%{_texmfcache}/fonts


%description
A package providing an interface to sectioning commands for
selection from various title styles. E.g., marginal titles and
to change the font of all headings with a single command, also
providing simple one-step page styles. Also includes a package
to change the page styles when there are floats in a page. You
may assign headers/footers to individual floats, too.


%package doc
Summary: Documentation for texlive-titlesec
Group: Productivity/Publishing/TeX/Base

%description doc
This package includes the documentation for texlive-titlesec

%prep
%setup -q -c -T

%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
    mkdir -p %{buildroot}%{_texmfdistdir}
    mkdir -p %{buildroot}%{_texmfmaindir}
    mkdir -p %{buildroot}%{_datadir}/texlive
    mkdir -p %{buildroot}/var/adm/update-scripts
    ln -sf ../../share/texmf %{buildroot}%{_datadir}/texlive/texmf-dist
    ln -sf ../../lib/texmf   %{buildroot}%{_datadir}/texlive/texmf
#    ln -sf %{_texmfmaindir}/texconfig/zypper.py \
#	%{buildroot}/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper
    tar --use-compress-program=xz -xf %{S:0} -C %{buildroot}%{_datadir}/texlive/texmf-dist
    tar --use-compress-program=xz -xf %{S:1} -C %{buildroot}%{_datadir}/texlive/texmf-dist

    rm -v  %{buildroot}%{_datadir}/texlive/texmf
    rm -v  %{buildroot}%{_datadir}/texlive/texmf-dist
    rm -vr %{buildroot}%{_datadir}/texlive
    # Remove this
    rm -vrf %{buildroot}%{_texmfdistdir}/tlpkg/tlpobj
    rm -vrf %{buildroot}%{_texmfmaindir}/tlpkg/tlpobj

%clean
rm -rf %{buildroot}

#%post
#mkdir -p /var/run/texlive
#> /var/run/texlive/run-mktexlsr

#%postun
#if test $1 = 0; then
#    %{_bindir}/mktexlsr 2> /dev/null || :
#    exit 0
#fi
#mkdir -p /var/run/texlive
#> /var/run/texlive/run-mktexlsr

#%posttrans
#test -z "$ZYPP_IS_RUNNING" || exit 0
#VERBOSE=false %{_texmfmaindir}/texconfig/update || :

%files doc
%defattr(-,root,system,755)
%{_texmfdistdir}/doc/latex/titlesec/CHANGES
%{_texmfdistdir}/doc/latex/titlesec/README
%{_texmfdistdir}/doc/latex/titlesec/titleps.pdf
%{_texmfdistdir}/doc/latex/titlesec/titleps.tex
%{_texmfdistdir}/doc/latex/titlesec/titlesec.pdf
%{_texmfdistdir}/doc/latex/titlesec/titlesec.tex

%files
%defattr(-,root,system,755)
%{_texmfdistdir}/tex/latex/titlesec/block.tss
%{_texmfdistdir}/tex/latex/titlesec/drop.tss
%{_texmfdistdir}/tex/latex/titlesec/frame.tss
%{_texmfdistdir}/tex/latex/titlesec/leftmargin.tss
%{_texmfdistdir}/tex/latex/titlesec/margin.tss
%{_texmfdistdir}/tex/latex/titlesec/rightmargin.tss
%{_texmfdistdir}/tex/latex/titlesec/titleps.sty
%{_texmfdistdir}/tex/latex/titlesec/titlesec.sty
%{_texmfdistdir}/tex/latex/titlesec/titletoc.sty
%{_texmfdistdir}/tex/latex/titlesec/ttlkeys.def
%{_texmfdistdir}/tex/latex/titlesec/ttlps.def
%{_texmfdistdir}/tex/latex/titlesec/wrap.tss
#/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper

%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20140418-1
- First version for AIX V6.1 and higher
