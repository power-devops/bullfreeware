# category Package
# revision 26789
# catalog-ctan /macros/latex/contrib/framed
# catalogue-date 2012-06-01 12:48:04 +0200
# catalog-license other-free
# catalog-version 20140210
%define  _texmfdistdir	%{_datadir}/texmf/tex/latex/framed
Name:		texlive-framed
Version:	20140210
Release:	1
Summary:	Framed or shaded regions that can break across pages
Group:		Publishing
URL:		http://www.ctan.org/tex-archive/macros/latex/contrib/framed
License:	OTHER-FREE
Source0:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/framed.tar.xz
Source1:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/framed.doc.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch:	noarch
BuildRequires:	texlive-tlpkg
#Requires(pre):	texlive-tlpkg
#Requires(post):	texlive-kpathsea

%description
The package creates three environments: - framed, which puts an
ordinary frame box around the region, - shaded, which shades
the region, and - leftbar, which places a line at the left
side. The environments allow a break at their start (the
\FrameCommand enables creation of a title that is "attached" to
the environment); breaks are also allowed in the course of the
framed/shaded matter. There is also a command \MakeFramed to
make your own framed-style environments.

#%post
#    %{_sbindir}/texlive.post

#%postun
#    if [ $1 -eq 0 ]; then
#	%{_sbindir}/texlive.post
#    fi

#-----------------------------------------------------------------------
%files
%defattr(-,root,system,755)
%{_texmfdistdir}/tex/latex/framed/framed.sty
%doc %{_texmfdistdir}/doc/latex/framed/framed.pdf
%doc %{_texmfdistdir}/doc/latex/framed/framed.tex

#-----------------------------------------------------------------------
%prep
%setup -c -a0 -a1

%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_texmfdistdir}
cp -fpar tex doc $RPM_BUILD_ROOT%{_texmfdistdir}



%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20140210-1
- First version for AIX V6.1 and higher


