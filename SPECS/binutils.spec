Summary: The GNU binutils development utilities
Name: binutils
Version: 2.14
Release: 3
Copyright: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/binutils/
Source0: http://ftp.gnu.org/gnu/binutls/%{name}-%{version}.tar.bz2
Patch0: %{name}-ppccore.patch
Prefix: %{_prefix}
BuildRequires: bzip2
BuildRoot: %{_tmppath}/binutils-root
Prereq: /sbin/install-info
Requires: AIX-rpm >= 5.1.0.0
%define DEFCC cc

%description
GNU binutils package contains utilities useful for development during
compilation.  Utilities such as nm, ar, elfdump, size, and others are included.

%prep
/usr/bin/lslpp -l bos.adt.libm >/dev/null 2>&1
if [[ $? -ne 0 ]] ; then
  echo "Build will fail without bos.adt.libm installed!"
  exit 1
fi
/usr/bin/lslpp -l bos.adt.include >/dev/null 2>&1
if [[ $? -ne 0 ]] ; then
  echo "Build will fail without bos.adt.include installed!"
  exit 1
fi

%setup -q
%patch0 -b .ppccore

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
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS=$RPM_OPT_FLAGS

./configure --prefix=%{prefix}
make


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{prefix}
cd $RPM_BUILD_ROOT%{prefix}

# Strip all of the executables
/usr/bin/strip bin/* 2>/dev/null || :

# compress the info files
gzip -9nf info/*

# The "ld" command is renamed to "gld".  For proper linking, please
# use the native AIX ld command, /usr/bin/ld.
# The "strip" command is not functioning correctly in all cases, so
# it has been renamed to "gstrip".  We strongly recommend the use
# of the native AIX strip command, /usr/bin/strip.
# Ditto for ranlib.
mv bin/ld bin/gld
mv bin/strip bin/gstrip
mv bin/ranlib bin/granlib
chmod 444 bin/gld bin/gstrip bin/granlib

# Create links into /usr/bin and /usr/linux/bin.
(
    cd $RPM_BUILD_ROOT
    mkdir -p usr/bin
    cd usr/bin
    for fname in  addr2line objcopy objdump readelf
    do
      ln -sf ../..%{prefix}/bin/$fname .
    done

    cd -
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    for fname in as c++filt nm size strings
    do
      ln -sf ../../..%{prefix}/bin/$fname .
    done

    cd -
    mkdir -p usr/lib
    cd usr/lib
    ln -sf ../..%{prefix}/lib/* .
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{prefix}/info/as.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/bfd.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/binutils.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/configure.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/standards.info.gz %{_prefix}/info/dir

%postun
if [ $1 = 0 ] ; then
 /sbin/install-info --delete %{prefix}/info/as.info.gz %{_prefix}/info/dir
 /sbin/install-info --delete %{prefix}/info/bfd.info.gz %{_prefix}/info/dir
 /sbin/install-info --delete %{prefix}/info/binutils.info.gz %{_prefix}/info/dir
 /sbin/install-info --delete %{prefix}/info/configure.info.gz %{_prefix}/info/dir
 /sbin/install-info --delete %{prefix}/info/standards.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,bin,bin)
%doc COPYING COPYING.LIB binutils/README binutils/NEWS
%doc %{prefix}/man/man1/*
%{prefix}/bin/*
%{prefix}/lib/*
%{prefix}/share/locale/
%{prefix}/include/*
%{prefix}/info/*
/usr/bin/*
/usr/linux/bin/*

%changelog
* Tue Oct 26 2004 David Clissold <cliss@austin.ibm.com> 2.14-3
- Ranlib has problems; rename to granlib and make nonexecutable.
- Users should use native AIX ranlib, but granlib will be present if
- anyone really wants it for whatever reason.

* Tue Jun 22 2004 David Clissold <cliss@austin.ibm.com> 2.14-2
- Fix "prereq" of install-info to be /sbin/install-info.

* Wed Jan 21 2004 David Clissold <cliss@austin.ibm.com> 2.14-1
- Initial version, adapted from old GNUPro.spec.

