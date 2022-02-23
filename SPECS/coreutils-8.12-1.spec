Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 8.12
Release: 1
License: GPL
Group:   System Environment/Base
URL:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
#Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gettext >= 0.17-5 , gmp-devel >= 4.2.4
BuildRequires: make

Requires: /sbin/install-info
Requires: info, gettext >= 0.17-5, gmp >= 4.2.4

Conflicts: mktemp, coreutils-64bit

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21
Prereq: /sbin/install-info
## NOTE: Must run as root for 'su' to be included.


%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

These tools are the GNU versions of common useful and popular file and text
utilities which are used for:
- file management
- shell scripts
- modifying text file (spliting, joining, comparing, modifying, ...)

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer arbitrary
limits.


%prep
%setup -q


%build

export CFLAGS="-qcpluscmt -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE "
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --enable-largefile \
    --enable-install-program=su \
    --enable-nls

make 

# To control binaries production
## make check


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
## VSD gmake DESTDIR=${RPM_BUILD_ROOT} install

make prefix=${RPM_BUILD_ROOT}%{_prefix} \
        localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
        mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
        infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
        install

make  prefix=${RPM_BUILD_ROOT}%{_prefix} \
        localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
        mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
        infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
	installcheck

bzip2 -9f ChangeLog

# install su and make sure we have the right permissions
cp src/su ${RPM_BUILD_ROOT}%{_prefix}/bin/su
# make sure we have the right permissions
chmod 4755 ${RPM_BUILD_ROOT}%{_prefix}/bin/su


( cd $RPM_BUILD_ROOT
  /usr/bin/strip .%{_prefix}/bin/* || :
  gzip -9nf .%{_prefix}/info/*info*

  mkdir -p usr/linux/bin
  mkdir -p usr/bin
  # There are some incompatibility between some aix commands and GNU commands.
  # To assume to have no bad issues we conserve into usr/linus/bin repository
  # only the GNU commands which are not delivered on AIX base
  cd usr/linux/bin
  for i in $(ls ../../..%{_prefix}/bin )
  do
     [ -x /usr/bin/$i ] || ln -sf ../../..%{_prefix}/bin/$i .
  done
  #
  cd ../../bin
  for i in dir dircolors vdir tac md5sum pinky seq
  do
     rm -f ../linux/bin/$i
     ln -sf ../..%{_prefix}/bin/$i .
  done
)

%pre
# We must deinstall these info files since they're merged in
# coreutils.info. else their postun'll be run too late
# and install-info will fail badly because of duplicates
for file in sh-utils textutils fileutils; do
    [ -f %{_prefix}/info/$file.info.gz ] && /sbin/install-info --delete %{_prefix}/info/$file.info.gz --dir=%{_prefix}/info/dir &> /dev/null || :
done


%preun
if [ $1 = 0 ]; then
    [ -f %{_prefix}/info/%{name}.info.gz ] && /sbin/install-info --delete %{_prefix}/info/%{name}.info.gz %{_prefix}/info/dir || :
fi


%post
/usr/bin/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_prefix}/info/dir > \
  %{_prefix}/info/dir.rpmmodify || exit 0
    /usr/bin/mv -f %{_prefix}/info/dir.rpmmodify %{_prefix}/info/dir
[ -f  %{_prefix}/info/%{name}.info.gz ] && /sbin/install-info %{_prefix}/info/%{name}.info.gz %{_prefix}/info/dir || :


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc COPYING ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
%{_prefix}/bin/*
%{_prefix}/man/man*
%{_prefix}/info/coreutils*
%{_prefix}/share/locale/*/*/coreutils.mo
# exclude %{_libdir}/charset.alias as it conflicts with glib2
# %{_prefix}/lib/*
/usr/bin/*
/usr/linux/bin/*


%changelog
* Tue May 24 2011 Gerard Visiedo <gerard.visiedo@bull.net > 8.12
- Update to version 8.12

* Thu May 27 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 8.5
- Update to version 8.5

* Thu Mar 12 2009 Gerard Visiedo <gerard.visiedo@bull.net> 7.1-1
- Update to version 7.1

* Fri Apr 20 2007 Christophe Belle <christophe.belle@bull.net> 6.9-1
- Update to version 6.9

* Thu Jan 26 2006 Reza Arbab <arbab@austin.ibm.com> 5.2.1-2
- Fix 'uname -p' on AIX.

* Thu Jul 08 2004 David Clissold <cliss@austin.ibm.com> 5.2.1-1
- Update to version 5.2.1.  (Patch from 5.0-2 now not needed).

* Wed Mar 03 2004 David Clissold <cliss@austin.ibm.com> 5.0-2
- Add patch for ls problem.

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 5.0-1
- Initial build of coreutils
- Adapt from prior fileutils, sh-utils, and textutils spec files.

