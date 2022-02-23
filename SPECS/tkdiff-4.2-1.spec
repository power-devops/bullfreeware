Name:           tkdiff
Summary:        2 and 3-way diff/merge tool
Version:        4.2
Release:        1
License:        GPL v2 or later
URL:            http://sourceforge.net/projects/tkdiff
Group:          Productivity/Text/Utilities
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       tk, diffutils

%description
TkDiff is a graphical 2 and 3-way diff/merge tool.


%prep
%setup -q -n %{name}-unix
# Force font size (fs) to size 10 due to abnormal font display issue
sed -e "s;^  set textfont \[list \$fm \$fs;  set textfont \[list \$fm \"10\";" tkdiff >tkdiff.tmp
[ -s tkdiff.tmp ] && mv tkdiff.tmp tkdiff

%build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp %{name} ${RPM_BUILD_ROOT}%{_bindir}/%{name}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/%{name}

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGELOG.txt LICENSE.txt README.txt
%{_bindir}/%{name}
/usr/bin/%{name}


%changelog
* Wed May 30 2012 Gerard Visiedo <gerard.visiedo@bull.net> -4.2-1
- Port on Aix6.1
