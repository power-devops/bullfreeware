Summary: The GNU core utilities - fileutils, sh-utils, and textutils
Name: coreutils
Version: 5.2.1
Release: 2
License: GPL
URL: http://www.gnu.org/software/coreutils
Group: Applications/File
Source0: ftp://ftp.gnu.org/gnu/coreutils/coreutils-%{version}.tar.bz2
Patch0: %{name}-%{version}-aix-uname.patch
Buildroot: %{_tmppath}/%{name}-root
Obsoletes: fileutils, sh-utils, textutils
Provides: fileutils, sh-utils, textutils
Prereq: /sbin/install-info
%define DEFCC xlc
## NOTE: Must run as root for 'su' to be included.

%description
These are the GNU core utilities.  This package is the union of the old GNU
fileutils, sh-utils, and textutils packages.

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
%patch0 -p0 -b .aix-uname

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else
       export CC=gcc
    fi
fi

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" ./configure
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
        install

# make sure we have the right permissions
chmod 4755 $RPM_BUILD_ROOT%{_prefix}/bin/su


( cd $RPM_BUILD_ROOT
  /usr/bin/strip .%{_prefix}/bin/* || :
  gzip -9nf .%{_prefix}/info/*info*

  mkdir -p usr/linux/bin
  mkdir -p usr/bin
  cd usr/linux/bin
  ln -sf ../../..%{_prefix}/bin/* .
  cd ../../bin
  for i in dir dircolors vdir tac md5sum pinky seq
  do
     rm ../linux/bin/$i
     ln -sf ../..%{_prefix}/bin/$i .
  done
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/info/coreutils.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_prefix}/info/coreutils.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%doc ABOUT-NLS AUTHORS COPYING NEWS README THANKS TODO
%{_prefix}/bin/*
%{_prefix}/man/man*/*
%{_prefix}/info/*info*
%{_prefix}/share/locale/*/*/coreutils.mo
/usr/linux/bin/*
/usr/bin/*

%changelog
* Thu Jan 26 2006 Reza Arbab <arbab@austin.ibm.com> 5.2.1-2
- Fix 'uname -p' on AIX.

* Thu Jul 08 2004 David Clissold <cliss@austin.ibm.com> 5.2.1-1
- Update to version 5.2.1.  (Patch from 5.0-2 now not needed).

* Wed Mar 03 2004 David Clissold <cliss@austin.ibm.com> 5.0-2
- Add patch for ls problem.

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 5.0-1
- Initial build of coreutils
- Adapt from prior fileutils, sh-utils, and textutils spec files.
