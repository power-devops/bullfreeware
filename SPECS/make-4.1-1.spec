Summary: A GNU tool which simplifies the build process for users
Name: make
Epoch: 1
Version: 4.1
Release: 1
License: GPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/make/
Source0: ftp://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}-aixrealpath.patch
Patch1: %{name}-%{version}-aixSyncAndDashl.patch
Patch2: %{name}-%{version}-aixfopen-fail.patch
Patch3: %{name}-%{version}-aixREADME.patch
Source1: ftp://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# make check on anything below AIX 5.3 produces tons of errors :-(
BuildRequires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm >= 5.3.0.0

BuildRequires: /sbin/install-info, info
BuildRequires: gettext
Requires: /sbin/install-info, info
Requires: gettext

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.


%prep
%setup -q
%patch0 -p1 -b .aixrealpath
%patch1 -p1 -b .aixSyncAndDashl
cd tests
%patch2 -p1 -b .aixfopen-fail
%patch3 -p1 -b .aixREADME
cd ..

%build
export CC="xlc_r"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

ln -sf make ${RPM_BUILD_ROOT}%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/gmake.1

chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/make.info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
ln -sf ../../..%{_bindir}/make usr/linux/bin

mkdir -p usr/bin
ln -sf ../..%{_bindir}/make usr/bin/gmake


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc NEWS README COPYING AUTHORS
%{_bindir}/*
%{_mandir}/man?/*
%{_infodir}/*.info*
%{_datadir}/locale/*/*/*
/usr/bin/*
/usr/linux/bin/*


%changelog
* Mon Oct 06 2014 Michael Perzl <michael@perzl.org> - 4.1-1
- updated to version 4.1

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 4.0-1
- updated to version 4.0

* Wed Jul 28 2010 Michael Perzl <michael@perzl.org> - 3.82-1
- updated to version 3.82

* Wed Jul 28 2010 Michael Perzl <michael@perzl.org> - 3.81-1
- updated to version 3.81

* Thu Jul 01 2010 Michael Perzl <michael@perzl.org> - 3.80-3
- removed dependency on gettext

* Mon Sep 15 2008 Michael Perzl <michael@perzl.org> - 3.80-2
- first version for AIX V5.1 and higher
