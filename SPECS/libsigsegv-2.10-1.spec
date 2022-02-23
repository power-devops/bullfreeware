Summary:	Library for handling page faults in user mode
Name:		libsigsegv
Version:	2.10
Release:	1
License:	GPLv2+
URL:		http://libsigsegv.sourceforge.net/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Group:		System Environment/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
This is a library for handling page faults in user mode. A page fault
occurs when a program tries to access to a region of memory that is
currently not available. Catching and handling a page fault is a useful
technique for implementing:
  - pageable virtual memory
  - memory-mapped access to persistent databases
  - generational garbage collectors
  - stack overflow handlers
  - distributed shared memory

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Development libraries and header files for %{name} 
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs to handle
page faults in user mode.

%prep
%setup -q

%build
CONFIG_SHELL=/usr/bin/ksh
CONFIGURE_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make %{?_smp_mflags}

cp src/.libs/%{name}.so.2 ./%{name}.so.2
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.2


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

chmod 644 $RPM_BUILD_ROOT%{_includedir}/*.h

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%changelog
* Mon Oct 03 2011 Patricia Cugny <patricia.cugny@bull.net> - 2.10-1
- initial port of version 2.10 on AIX 5.3

