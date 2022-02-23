Summary: A GNU set of database routines which use extensible hashing.
Name: gdbm
Version: 1.10
Release: 1
Source0: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz.sig
Source2: libgdbm.so.3-aix32
Source3: libgdbm.so.3-aix64
License: GPL
URL: http://www.gnu.org/software/gdbm/
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}--Ã%{version}-root

%description
Gdbm is a GNU database indexing library, including routines which use
extensible hashing.  Gdbm works in a similar way to standard UNIX dbm
routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple
database routines, you should install gdbm.  You'll also need to
install gdbm-devel.


%package devel
Summary: Development libraries and header files for the gdbm library.
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: /sbin/install-info, info

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.


%prep
%setup -q

%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static
make 

cp src/.libs/libgdbm.so.4 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libgdbm.a ./libgdbm.so.4

# Add the older 1.8.3 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libgdbm.so.3
/usr/bin/strip -X32 -e libgdbm.so.3
/usr/bin/ar -X32 -q src/.libs/libgdbm.a libgdbm.so.3

cp %{SOURCE3} libgdbm.so.3
/usr/bin/strip -X64 -e libgdbm.so.3
/usr/bin/ar -X64 -q src/.libs/libgdbm.a libgdbm.so.3


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)



%post devel
/sbin/install-info %{_infodir}/gdbm.info.gz %{_infodir}/dir --entry="* gdbm: (gdbm).                   The GNU Database." || :


%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gdbm.info.gz %{_infodir}/dir --entry="* gdbm: (gdbm).                   The GNU Database." || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc COPYING NEWS README
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/*.la
%{_infodir}/*.info*
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-1
- Initial port on Aix6.1

