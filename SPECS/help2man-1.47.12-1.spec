%bcond_without dotests

Name:           help2man
Summary:        Create simple man pages from --help output
Version:        1.47.12
Release:        1
Group:          Development/Tools
License:        GPLv3+
URL:            http://www.gnu.org/software/help2man
Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz
Source1:        %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

BuildRequires:  sed
BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(strict)

Requires:       perl(perl) >= 5.30
Requires:       perl(Getopt::Long)
Requires:       perl(POSIX)
Requires:       perl(Text::ParseWords)
Requires:       perl(Text::Tabs)
Requires:       perl(strict)


%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.


%prep
%setup -q -n help2man-%{version}

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
# first build the 64-bit version
cd 64bit

export CC="gcc -maix64 -D_LARGE_FILES"
export OBJECT_MODE=64
./configure --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

gmake

#Now build the 32-bit version
cd ../32bit

export CC="gcc -maix32 -D_LARGE_FILES"
export OBJECT_MODE=32
./configure --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

gmake


%install

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
    mv $fic "$fic"_64
    done
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
    mv $fic "$fic"_32
    ln -sf "$fic"_64 $fic
    done
)

# Binaries are perl script. Only diff between 32 and 64 bits are perl called.
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    sed -i 's|#!/opt/freeware/bin/perl|#!/opt/freeware/bin/perl_64|'  help2man_64
    sed -i 's|#!/opt/freeware/bin/perl|#!/opt/freeware/bin/perl_32|'  help2man_32
)


%check
# No tests!
%if %{with dotests}
# cd 64bit
# export OBJECT_MODE=64
# (gmake -k check || true)
# cd ../32bit
# export OBJECT_MODE=32
# (gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/help2man.info \
    %{_infodir}/dir 2>/dev/null || :
fi


%files
%defattr(-,root,system,-)
%doc 32bit/README 32bit/NEWS 32bit/THANKS 32bit/COPYING
%{_bindir}/help2man*
%{_infodir}/*
%{_mandir}/man1/*


%changelog
* Fri Feb 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.47.12-1
- New version 1.47.9-1
- Add clean and check section
- Make the 32 and 64 bits version not identical
- No more AIX perl dependency

* Mon Sep 11 2017 Sushma M Bhat <susmbhat@in.ibm.com> - 1.47.4-1
- Updated to version 1.47.4-1 and built 64-bit version too

* Tue Nov 18 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.43.3-1
- Initial port on Aix6.1
