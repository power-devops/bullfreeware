Name:           cvsps
Version:        2.2b1
Release:        1
Summary:        Patchset tool for CVS

Group:          Development/Tools
License:        GPL+
URL:            http://www.cobite.com/cvsps/
Source0:        http://www.cobite.com/cvsps/%{name}-%{version}.tar.gz
# #516083
Patch0:         %{name}-%{version}-dynamic-logbuf.patch
# AIX5L V5.1 doesn't have unsetenv()
Patch1:         %{name}-%{version}-aix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  zlib-devel

Requires: cvs
Requires: zlib

%description
CVSps is a program for generating 'patchset' information from a CVS
repository.  A patchset in this case is defined as a set of changes
made to a collection of files, and all committed at the same time
(using a single 'cvs commit' command).  This information is valuable
to seeing the big picture of the evolution of a cvs project.  While
cvs tracks revision information, it is often difficult to see what
changes were committed 'atomically' to the repository.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch0 -p1
%patch1
sed -i -e 's/diffs\\-opts/diff\\-opts/' cvsps.1


%build
#export CC="cc -qcpluscmt"
export CC="gcc"
gmake %{?_smp_mflags}


%install
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake install prefix=${RPM_BUILD_ROOT}%{_prefix}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mv ${RPM_BUILD_ROOT}%{_datadir}/man ${RPM_BUILD_ROOT}%{_prefix}

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc CHANGELOG COPYING README merge_utils.sh
%{_bindir}/cvsps
%{_mandir}/man1/cvsps.1*
/usr/bin/cvsps


%changelog
* Mon Mar 18 2019 Tony Reix <tony.reix@atos.net> - 2.2b1-1
- First version for AIX V6.1 and higher

* Thu Nov 19 2009 Michael Perzl <michael@perzl.org> - 2.2b1-1
- first version for AIX V5.1 and higher
