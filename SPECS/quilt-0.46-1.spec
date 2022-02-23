#
# spec file for quilt - patch management scripts
#

Name:		quilt
Summary:	Scripts for working with series of patches
License:	GPL
Group:		Productivity/Text/Utilities
Version:	0.46
Release:	1
Requires:	coreutils diffutils patch gzip bzip2 perl gettext
Autoreqprov:	off
Source:		quilt-%{version}.tar.gz
Patch:		aix-spec.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%define DEFCC cc

%ifos aix6.1
Requires: AIX-rpm >= 5.3.0.0
Requires: findutils grep bash gawk
%define configureflags	--prefix=%{_prefix} --with-bash=/usr/bin/bash --mandir=%_mandir --with-cp=/usr/linux/bin/cp --with-grep=/usr/linux/bin/grep --without-column --without-getopt --with-find=/usr/linux/bin/find --with-awk=/usr/linux/bin/awk --with-date=/usr/linux/bin/date --with-sed=/usr/linux/bin/sed --with-diff=/usr/linux/bin/diff
%else
%define configureflags	--mandir=%_mandir --prefix=%{_prefix} --without-getopt --without-column
Requires:	coreutils
%endif

%description
The scripts allow to manage a series of patches by keeping
track of the changes each patch makes. Patches can be
applied, un-applied, refreshed, etc.

The scripts are heavily based on Andrew Morton's patch scripts
found at http://www.zip.com.au/~akpm/linux/patches/.

Authors:
--------
    Andrew Morton <akpm@digeo.com>
    Andreas Gruenbacher <agruen@suse.de>

%prep
%setup
%patch

%build

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else 
       export CC=gcc
    fi
fi
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi
%ifos aix6.1
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
%endif
CFLAGS="$RPM_OPT_FLAGS" ./configure %{configureflags}
make BUILD_ROOT=$RPM_BUILD_ROOT RELEASE=%release

%install
rm -rf $RPM_BUILD_ROOT
make install BUILD_ROOT=$RPM_BUILD_ROOT
%{find_lang} %{name}
mkdir -p $RPM_BUILD_ROOT/usr/bin/
for file in guards quilt; do
	ln -s %{_prefix}/bin/${file} $RPM_BUILD_ROOT/usr/bin/${file}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
/usr/bin/guards
/usr/bin/quilt
%{_prefix}/bin/guards
%{_prefix}/bin/quilt
%{_prefix}/share/quilt/
%{_prefix}/lib/quilt/
%{_prefix}/etc/bash_completion.d/quilt
%config(noreplace) %{_prefix}/etc/quilt.quiltrc
%doc %{_mandir}/man1/guards.1*
%doc %{_mandir}/man1/quilt.1*
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/README.MAIL
%doc %{_docdir}/%{name}-%{version}/quilt.pdf

%changelog
* Tue Feb 12 2008 - Laurent.Vivier@bull.net
- Modify quilt.spec.in to support AIX6.1
