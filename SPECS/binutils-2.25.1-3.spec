Summary: The GNU binutils development utilities
Name: binutils
Version: 2.25.1
Release: 3
Copyright: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/binutils/
Source0: http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/binutils-%{version}-root
Prereq: /sbin/install-info
Requires: AIX-rpm >= 5.1.0.0

Source1: BinUtils-2.25.1.GccGo-1.8.copycsect.c
Source2: BinUtils-2.25.1.GccGo-1.8.copycsect.make


%description
GNU binutils package contains utilities useful for development during
compilation.  Utilities such as nm, ar, elfdump, size, and others are included.


%package gccgov1
Summary:    Contains copycsect for GCCGo
Group:      Development/Languages

%description gccgov1
Contains copycsect ($OBJCOPY) for GCC Go.


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

%build
export RM="/usr/bin/rm -f"
CC=gcc
CXX=g++
export CFLAGS=$RPM_OPT_FLAGS
#export CFLAGS="$CFLAGS -g"


./configure --prefix=%{_prefix} \
	    --mandir=%{_prefix}/man \
	    --infodir=%{_prefix}/info 
	   #--disable-largefile

gmake

# remove the "-print-multi-os-directory" flag
sed -e "s/MULTIOSDIR = \`\$(CC) \$(CFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
mv -f Makefile.tmp libiberty/Makefile


# Build copycsect for GCC Go
# Usage in GCC: OBJCOPY=copycsect ; $(OBJCOPY) -j .go_export $$f $@.tmp

HERE=`pwd`
mkdir go
(
  cd go
  cp %{SOURCE1} copycsect.c
  cp %{SOURCE2} copycsect.make
  sh -x copycsect.make $HERE
)


# Tests
( gmake -k check || true )


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake    prefix=${RPM_BUILD_ROOT}%{_prefix} \
         mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
        infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
	install 

cp go/copycsect $RPM_BUILD_ROOT%{_prefix}/bin/


cd $RPM_BUILD_ROOT%{_prefix}

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
# The "as" command is renamed to "gas". 
mv bin/as  bin/gas
chmod 444 bin/gas

# Create links into /usr/bin and /usr/linux/bin.
(
    cd $RPM_BUILD_ROOT
    mkdir -p usr/bin
    cd usr/bin
    for fname in  addr2line objcopy objdump readelf
    do
      ln -sf ../..%{_prefix}/bin/$fname .
    done

    cd -
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    for fname in gas c++filt nm size strings
    do
      ln -sf ../../..%{_prefix}/bin/$fname .
    done

    cd -
    mkdir -p usr/lib
    cd usr/lib
    ln -sf ../..%{_prefix}/lib/* .
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_prefix}/info/as.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/bfd.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/binutils.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/configure.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/standards.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/ld.info.gz %{_prefix}/info/dir

## %postun
%preun
if [ ${1} = 0 ] ; then
 [ -f %{_prefix}/info/as.info.gz ] && /sbin/install-info --delete %{_prefix}/info/as.info.gz %{_prefix}/info/dir
 [ -f %{_prefix}/info/bfd.info.gz ] && /sbin/install-info --delete %{_prefix}/info/bfd.info.gz %{_prefix}/info/dir
 [ -f %{_prefix}/info/binutils.info.gz ] && /sbin/install-info --delete %{_prefix}/info/binutils.info.gz %{_prefix}/info/dir
 [ -f %{_prefix}/info/configure.info.gz ] && /sbin/install-info --delete %{_prefix}/info/configure.info.gz %{_prefix}/info/dir
 [ -f %{_prefix}/info/standards.info.gz ] && /sbin/install-info --delete %{_prefix}/info/standards.info.gz %{_prefix}/info/dir
 [ -f %{_prefix}/info/ld.info.gz ] && /sbin/install-info --delete %{_prefix}/info/ld.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%doc COPYING COPYING.LIB COPYING3 COPYING3.LIB binutils/README binutils/NEWS
%doc %{_prefix}/man/man1/*
%{_prefix}/bin/*
%{_prefix}/lib/*
%{_prefix}/share/locale/*/*/*
%{_prefix}/include/*
%{_prefix}/info/*
/usr/bin/*
/usr/linux/bin/*

%files gccgov1
%{_prefix}/bin/copycsect


%changelog
* Mon Mar 06 2017 Tony Reix <tony.reix@atos.net > 2.25.1-3
- Add copycsect fo GCC Go.
- Add package binutils-gccv7go

* Tue Oct 11 2016 Tony Reix <tony.reix@atos.net > 2.25.1-2
- Add tests

* Thu Aug 06 2015 Hamza Sellami <hamza.sellami@atos.net > 2.25.1-1
- update to version 2.25.1 

* Fri Jun 29 2012 Patricia Cugny <patricia.cugny@bull.net> 2.22-1
- update to 2.22 and rename as to gas

* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 2.21-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri May 27 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.21-1
- Update to 2.21

* Tue Oct 26 2004 David Clissold <cliss@austin.ibm.com> 2.14-3
- Ranlib has problems; rename to granlib and make nonexecutable.
- Users should use native AIX ranlib, but granlib will be present if
- anyone really wants it for whatever reason.

* Tue Jun 22 2004 David Clissold <cliss@austin.ibm.com> 2.14-2
- Fix "prereq" of install-info to be /sbin/install-info.

* Wed Jan 21 2004 David Clissold <cliss@austin.ibm.com> 2.14-1
- Initial version, adapted from old GNUPro.spec.

