Summary:        The GNU Portable Threads library
Name:           pth
Version:        2.0.7
Release:        1
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.gnu.org/software/pth/

Source:         ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig

Patch0:         %{name}-%{version}-aix.patch
# host_os=aix
Patch1:         %{name}-%{version}-aix67v2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications.
All threads run in the same address space of the server application,
but each thread has it's own individual program-counter, run-time
stack, signal mask and errno variable.

%package devel
Summary:        Development headers and libraries for GNU Pth
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.


%prep
%setup -q
%patch0
%patch1


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export CC="/opt/IBM/xlc/13.1.3/bin/xlc -q64"
export CC="gcc -maix64"

export CFLAGS="-O"
./configure \
    --prefix=%{_prefix} \
    --enable-static --enable-shared \
    --with-fdsetsize=1024
# stupid configure gets this wrong :-(
cat pth_acdef.h | sed -e "s|#define HAVE_GETTIMEOFDAY_ARGS1 1|#undef HAVE_GETTIMEOFDAY_ARGS1|" > pth_acdef.tmp
mv -f  pth_acdef.tmp pth_acdef.h

gmake %{?_smp_mflags}

gmake check

cp .libs/libpth.so.20 .

make distclean
slibclean


# now build the 32-bit version
export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
export CC="gcc -maix32"

./configure \
    --prefix=%{_prefix} \
    --enable-static --enable-shared \
    --with-fdsetsize=1024

# stupid configure gets this wrong :-(
cat pth_acdef.h | sed -e "s|#define HAVE_GETTIMEOFDAY_ARGS1 1|#undef HAVE_GETTIMEOFDAY_ARGS1|" > pth_acdef.tmp
mv -f  pth_acdef.tmp pth_acdef.h
gmake %{?_smp_mflags}

gmake check
slibclean

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libpth.a ./libpth.so.20


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

(
  cd $RPM_BUILD_ROOT
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system,-)
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS PORTING README
%doc SUPPORT TESTS THANKS USERS
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc HACKING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_mandir}/*/*
%{_datadir}/aclocal/*
/usr/bin/*
/usr/include/*
/usr/lib/*.la


%changelog
* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 2.0.7-1
- Re-port on AIX. AIX v6 with gcc

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 2.0.7-3
- rebuilt with XLC/C++ and get compile errors fixed

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 2.0.7-2
- included both 32-bit and 64-bit shared objects

* Fri Oct 05 2007 Michael Perzl <michael@perzl.org> - 2.0.7-1
- first version for AIX V5.1 and higher
