# rpm -ba --define 'dotests 0' guile-*.spec
%{!?dotests: %define dotests 1}

%define _libdir64 %{_prefix}/lib64

Summary:	Automated text file generator
Name:		autogen
Version:	5.18.7
Release:	1
# Some files are licensed under GPLv2+.
# We redistribute them under GPLv3+.
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/autogen/
Source0:	ftp://ftp.gnu.org/gnu/autogen/rel5.12/%{name}-%{version}.tar.xz

Source1:	%{name}-5.18.7-pkgconfig.patch
Source2:	%{name}-5.18.7-lintl.patch

Source100:	%{name}-%{version}-%{release}.build.log


BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	guile-devel >= 2
BuildRequires:	libtool
BuildRequires:	libxml2-devel

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

This package is available in 32bit and 64bit.


%package libopts
Summary:	Automated option processing library based on %{name}
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser consisting of a set of
AutoGen templates and a run time library that nearly eliminates the hassle of
parsing and documenting command line options.


%package libopts-devel
Summary:	Development files for libopts
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		Development/Libraries

Requires:	automake
Requires:	%{name}-libopts = %{version}-%{release}
Requires:	pkgconfig

%description libopts-devel
This package contains development files for libopts.


%prep
%setup -q -n %{name}-%{version}

patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf *
mv   /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
#export LDFLAGS="-lguile"


# Due to a bug, the build breaks with this message:   columns program is not findable
# A work-around is to add a symlink to columns installed with previous version of autogen
# I'm not sure the columns built by this version works fine...
# ln -s /opt/freeware/bin/columns /columns
#
# Tests need the 64bit/32bit version... so 2 symlink are executed when testing.
# So: 1) Build 2) Install 3) Build&Test
#
if test -L /columns; then
echo "/columns is there !"
else
echo "/columns is missing !"
echo "Do: ln -s /opt/freeware/bin/columns /columns"
exit
fi
#
# The issue deals with:
# autoopts/tpl/agtexi-cmd.tpl :
#    (shell "CLexe=${AGexe%/agen5/*}/columns/columns
# where AGexe is empty.
# Code thus looks for: /columns/columns and then /columns .


#export CFLAGS="-g -O0"
export CFLAGS="-O2"

export M4=/usr/linux/bin/m4
export RM="/usr/bin/rm -f"


#first build the 64-bit version
export STRIP="i/usr/bin/strip -X64"

export CC="/usr/vac/bin/xlc    -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
export CXX="/usr/vacpp/bin/xlC -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "

cd 64bit
export OBJECT_MODE=64
export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"

CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} 

gmake #%{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    rm -f                               /columns
    ln -sf /opt/freeware/bin/columns_64 /columns

    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

cd ..


# now build the 32-bit version
export STRIP="/usr/bin/strip -X32"

export CC="/usr/vac/bin/xlc    -q32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX="/usr/vacpp/bin/xlC -q32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

cd 32bit
export OBJECT_MODE=32
export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"

CONFIG_SHELL=/bin/bash ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} 

gmake #%{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    rm -f                               /columns
    ln -sf /opt/freeware/bin/columns_32 /columns

    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"
export INSTALL=/opt/freeware/bin/install
/usr/sbin/slibclean

cd 64bit
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc    -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
export CXX="/usr/vacpp/bin/xlC -q64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
gmake install INSTALL="%{_bindir}/install -p" DESTDIR=$RPM_BUILD_ROOT
/usr/sbin/slibclean
cd ..

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in autogen autoopts-config columns getdefs xml2ag
  do
    mv ${f} ${f}_64
  done
)


cd 32bit
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc    -q32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
export CXX="/usr/vacpp/bin/xlC -q32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
gmake install INSTALL="%{_bindir}/install -p" DESTDIR=$RPM_BUILD_ROOT
/usr/sbin/slibclean

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in autogen autoopts-config columns getdefs xml2ag
  do
    mv ${f} ${f}_32
  done
)


(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libopts.a ${RPM_BUILD_ROOT}%{_libdir64}/libopts.so*

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  rm -f *.a
  ln -sf %{_libdir}/libopts.a .
)


# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for b in columns getdefs %{name} xml2ag autoopts-config
  do
    ln -sf ${b}_64 ${b}
  done
)

ls -lR $RPM_BUILD_ROOT


%clean
/usr/bin/rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/%{name}.info %{_prefix}/share/info/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_prefix}/share/info/%{name}.info \
  %{_prefix}/share/info/dir >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc 32bit/AUTHORS
%doc 32bit/ChangeLog
%doc 32bit/COPYING
%doc 32bit/NEWS
%doc 32bit/README
%doc 32bit/THANKS
%doc 32bit/pkg/libopts/COPYING.gplv3

%{_bindir}/columns*
%{_bindir}/getdefs*
%{_bindir}/%{name}*
%{_bindir}/xml2ag*
%{_prefix}/share/info/autogen.info
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%files libopts
%defattr(-,root,root,-)
%doc 32bit/pkg/libopts/COPYING.mbsd
%doc 32bit/pkg/libopts/COPYING.lgplv3
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.la
%{_libdir64}/*.so*


%files libopts-devel
%defattr(-,root,root,-)
%{_bindir}/autoopts-config*
%{_datadir}/aclocal/autoopts.m4
#%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
%{_libdir}/pkgconfig/autoopts.pc
%{_libdir64}/pkgconfig/autoopts.pc

%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h


%changelog
* Tue Aug 23 2016 Tony Reix <tony.reix@atos.net> - 5.18.7-1
- Initial port on AIX 6.1
- Work-around /columns issue
- Work-around defs & library -lintl issue
- Fix all 32/64 issues

* Tue Sep 29 2015 Pascal OLIVA <pascal.oliva@atos.net> - 5.12-1
- Porting for AIX
