#revision 34145
# category TLCore
# catalog-ctan undef
#catalogue-date 2012-03-14 12:38:42 +0100
# catalog-license lgpl
# catalog-version undef

%define _texmfdir                       %{_datadir}/texmf
%define _texmfdistdir                   %{_datadir}/texmf-dist
%define _texmflocaldir                  %{_datadir}/texmf-local
%define _texmfvardir                    %{_localstatedir}/lib/texmf
%define _texmfconfdir                   %{_sysconfdir}/texmf

Name:		texlive-kpathsea
Version:	20140512
Release:	1
Summary:	Path searching library for TeX-related files
Group:		Publishing
URL:		http://tug.org/texlive
License:	LGPL
Source0:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/kpathsea.tar.xz
Source1:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/kpathsea.doc.tar.xz
BuildArch:	noarch
BuildRequires:	texlive-tlpkg
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Requires(pre):	texlive-tlpkg
#Requires(post):	texlive-kpathsea.bin
#Requires(postun):texlive-kpathsea.bin
#%rename kpathsea

%description
Kpathsea is a library and utility programs which provide path
searching facilities for TeX file types, including the self-
locating feature required for movable installations, layered on
top of a general search mechanism. It is not distributed
separately, but rather is released and maintained as part of
the TeX live sources.

#%post
#    %{_sbindir}/texlive.post

#%postun
#    if [ $1 -eq 0 ]; then
#	%{_sbindir}/texlive.post
#    fi

#-----------------------------------------------------------------------
%files
%defattr(-,root,system,755)
%{_texmfdistdir}/web2c/amiga-pl.tcx
%{_texmfdistdir}/web2c/cp1250cs.tcx
%{_texmfdistdir}/web2c/cp1250pl.tcx
%{_texmfdistdir}/web2c/cp1250t1.tcx
%{_texmfdistdir}/web2c/cp227.tcx
%{_texmfdistdir}/web2c/cp852-cs.tcx
%{_texmfdistdir}/web2c/cp852-pl.tcx
%{_texmfdistdir}/web2c/cp8bit.tcx
%{_texmfdistdir}/web2c/empty.tcx
%config(noreplace) %{_texmfdistdir}/web2c/fmtutil.cnf
%{_texmfdistdir}/web2c/il1-t1.tcx
%{_texmfdistdir}/web2c/il2-cs.tcx
%{_texmfdistdir}/web2c/il2-pl.tcx
%{_texmfdistdir}/web2c/il2-t1.tcx
%{_texmfdistdir}/web2c/kam-cs.tcx
%{_texmfdistdir}/web2c/kam-t1.tcx
%{_texmfdistdir}/web2c/macce-pl.tcx
%{_texmfdistdir}/web2c/macce-t1.tcx
%{_texmfdistdir}/web2c/maz-pl.tcx
%{_texmfdistdir}/web2c/mktex.cnf
%{_texmfdistdir}/web2c/mktex.opt
%{_texmfdistdir}/web2c/mktexdir
%{_texmfdistdir}/web2c/mktexdir.opt
%{_texmfdistdir}/web2c/mktexnam
%{_texmfdistdir}/web2c/mktexnam.opt
%{_texmfdistdir}/web2c/mktexupd
%{_texmfdistdir}/web2c/natural.tcx
%{_texmfdistdir}/web2c/tcvn-t5.tcx
%{_texmfdistdir}/web2c/texmf.cnf
%{_texmfdistdir}/web2c/viscii-t5.tcx
%doc %{_texmfdistdir}/doc/info/dir
%doc %{_infodir}/kpathsea.info*
%doc %{_infodir}/tds.info*
%doc %{_infodir}/web2c.info*
%doc %{_texmfdistdir}/doc/kpathsea/kpathsea.html
%doc %{_texmfdistdir}/doc/kpathsea/kpathsea.pdf
%doc %{_mandir}/man1/kpseaccess.1*
%doc %{_texmfdistdir}/doc/man/man1/kpseaccess.man1.pdf
#%doc %{_mandir}/man1/kpsepath.1*
#%doc %{_texmfdistdir}/doc/man/man1/kpsepath.man1.pdf
%doc %{_mandir}/man1/kpsereadlink.1*
%doc %{_texmfdistdir}/doc/man/man1/kpsereadlink.man1.pdf
%doc %{_mandir}/man1/kpsestat.1*
%doc %{_texmfdistdir}/doc/man/man1/kpsestat.man1.pdf
#%doc %{_mandir}/man1/kpsetool.1*
#%doc %{_texmfdistdir}/doc/man/man1/kpsetool.man1.pdf
#%doc %{_mandir}/man1/kpsewhere.1*
#%doc %{_texmfdistdir}/doc/man/man1/kpsewhere.man1.pdf
%doc %{_mandir}/man1/kpsewhich.1*
%doc %{_texmfdistdir}/doc/man/man1/kpsewhich.man1.pdf
#%doc %{_mandir}/man1/kpsexpand.1*
#%doc %{_texmfdistdir}/doc/man/man1/kpsexpand.man1.pdf
%doc %{_mandir}/man1/mkocp.1*
%doc %{_texmfdistdir}/doc/man/man1/mkocp.man1.pdf
%doc %{_mandir}/man1/mkofm.1*
%doc %{_texmfdistdir}/doc/man/man1/mkofm.man1.pdf
%doc %{_mandir}/man1/mktexfmt.1*
%doc %{_texmfdistdir}/doc/man/man1/mktexfmt.man1.pdf
%doc %{_mandir}/man1/mktexlsr.1*
%doc %{_texmfdistdir}/doc/man/man1/mktexlsr.man1.pdf
%doc %{_mandir}/man1/mktexmf.1*
%doc %{_texmfdistdir}/doc/man/man1/mktexmf.man1.pdf
%doc %{_mandir}/man1/mktexpk.1*
%doc %{_texmfdistdir}/doc/man/man1/mktexpk.man1.pdf
%doc %{_mandir}/man1/mktextfm.1*
%doc %{_texmfdistdir}/doc/man/man1/mktextfm.man1.pdf
%doc %{_mandir}/man1/texhash.1*
%doc %{_texmfdistdir}/doc/man/man1/texhash.man1.pdf
%doc %{_texmfdistdir}/doc/web2c/web2c.html
%doc %{_texmfdistdir}/doc/web2c/web2c.pdf

#-----------------------------------------------------------------------
%prep
%setup -c -a0 -a1

perl -pi -e 's%^(TEXMFMAIN\s+= ).*%$1%{_texmfdir}%;'			  \
	 -e 's%^(TEXMFDIST\s+= ).*%$1%{_texmfdistdir}%;'		  \
	 -e 's%^(TEXMFLOCAL\s+= ).*%$1%{_texmflocaldir}%;'		  \
	 -e 's%^(TEXMFSYSVAR\s+= ).*%$1%{_texmfvardir}%;'		  \
	 -e 's%^(TEXMFSYSCONFIG\s+= ).*%$1%{_texmfconfdir}%;'		  \
	 -e 's%^(TEXMFHOME\s+= ).*%$1\$HOME/texmf%;'			  \
	 -e 's%^(TEXMFVAR\s+= ).*%$1\$HOME/.texlive2011/texmf-var%;'	  \
	 -e 's%^(TEXMFCONFIG\s+= ).*%$1\$HOME/.texlive2011/texmf-config%;'\
	 -e 's%^(OSFONTDIR\s+= ).*%$1%{_datadir}/fonts%;'		  \
	texmf-dist/web2c/texmf.cnf

%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}
cp -fpar texmf-dist %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_texmfdistdir}/doc/man/man1/*.1 %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_infodir}
mv %{buildroot}%{_texmfdistdir}/doc/info/*.info %{buildroot}%{_infodir}


%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20140512-1
- First version for AIX V6.1 and higher
