# name threeparttable
# revision 17383
# category Package
# catalog-ctan /macros/latex/contrib/threeparttable
# catalog-date 2011-10-17 18:01:19 +0200
# catalog-license other-free
# catalog-version undef

%define  _texmfdistdir  %{_datadir}/texmf-dist

Name:		texlive-threeparttable
Version:	20140418
Release:	1
Summary:	Tables with captions and notes all the same width
Group:		Publishing
URL:		http://www.ctan.org/tex-archive/macros/latex/contrib/threeparttable
License:	OTHER-FREE
Source0:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/threeparttable.tar.xz
Source1:	http://mirrors.ctan.org/systems/texlive/tlnet/archive/threeparttable.doc.tar.xz
BuildArch:	noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires:	texlive-tlpkg
#Requires(pre):	texlive-tlpkg
#Requires(post):	texlive-kpathsea

%description
Provides a scheme for tables that have a structured note
section, after the caption. This scheme provides an answer to
the old problem of putting footnotes in tables -- by making
footnotes entirely unnecessary. Note that a threeparttable is
not a float of itself; but you can place it in a table or a
table* environment, if necessary.

#%post
#    %{_sbindir}/texlive.post

#%postun
#    if [ $1 -eq 0 ]; then
#	%{_sbindir}/texlive.post
#    fi

#-----------------------------------------------------------------------
%files
%defattr(-,root,system,755)
%{_texmfdistdir}/tex/latex/threeparttable/3parttable.sty
%{_texmfdistdir}/tex/latex/threeparttable/threeparttable.sty
%doc %{_texmfdistdir}/doc/latex/threeparttable/miscdoc.sty
%doc %{_texmfdistdir}/doc/latex/threeparttable/threeparttable.pdf
%doc %{_texmfdistdir}/doc/latex/threeparttable/threeparttable.tex

#-----------------------------------------------------------------------
%prep
%setup -c -a0 -a1

%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_texmfdistdir}
cp -fpar tex doc %{buildroot}%{_texmfdistdir}


%changelog
* Fri Nov 28 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 20140418-1
- First version for AIX V6.1 and higher
