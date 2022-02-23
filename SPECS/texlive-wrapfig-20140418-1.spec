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

#name wrapfig
#category Package
#revision 22048
#catalogue-ctan /macros/latex/contrib/wrapfig
#catalogue-date 2012-05-30 14:33:40 +0200
#catalogue-license lppl
#catalogue-version 3.6

%define __perl_requires		%{nil}
%define __os_install_post	/usr/lib/rpm/brp-compress \\\
  %(ls /usr/lib/rpm/brp-suse.d/* 2> /dev/null | grep -vE 'check-la|boot-scripts|rpath|symlink|desktop|strip-debug|gcc-output|debuginfo|libtool|kernel-log') %{nil}

Name: texlive-wrapfig
Version: 20140418
Release: 1
License: LPPL-1.0
Summary: Produces figures which text can flow around
Group: Productivity/Publishing/TeX/Base
Url: http://www.tug.org/texlive/
Provides: tex(wrapfig.sty)
# Download at ftp://ftp.ctan.org/pub/tex/systems/texlive/tlnet/archive/
Source0: wrapfig.tar.xz
Source1: wrapfig.doc.tar.xz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define _texmfdistdir	%{_datadir}/texmf
%define _texmfmaindir	%{_libexecdir}/texmf
%define _texmfdirs	\{%{_texmfdistdir},%{_texmfmaindir}\}

%define _texmfconfdir	%{_sysconfdir}/texmf
%define _texmfvardir	%{_varlib}/texmf
%define _texmfcache	%{_localstatedir}/cache/texmf
%define _fontcache	%{_texmfcache}/fonts


%description
Allows figures or tables to have text wrapped around them. Does
not work in combination with list environments, but can be used
in a parbox or minipage, and in twocolumn format. Supports the
float package.


%package doc
Summary: Documentation for texlive-wrapfig
Group: Productivity/Publishing/TeX/Base

%description doc
This package includes the documentation for texlive-wrapfig

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
    ln -sf %{_texmfmaindir}/texconfig/zypper.py \
	%{buildroot}/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper
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
%{_texmfdistdir}/doc/latex/wrapfig/multiple-span.txt
%{_texmfdistdir}/doc/latex/wrapfig/wrapfig-doc.pdf
%{_texmfdistdir}/doc/latex/wrapfig/wrapfig-doc.tex

%files
%defattr(-,root,system,755)
%{_texmfdistdir}/tex/latex/wrapfig/wrapfig.sty
/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper

%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20140418-1
- First version for AIX V6.1 and higher
