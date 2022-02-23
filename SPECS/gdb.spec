Summary: The GNU gdb debugger
Name: gdb
Version: 6.0
Release: 1
Copyright: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/gdb/
Source0: http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.bz2
Patch0: %{name}-ppccore.patch
Prefix: %{_prefix}
BuildRequires: bzip2
BuildRoot: %{_tmppath}/%{name}-root
Prereq: /sbin/install-info
Requires: AIX-rpm >= 5.1.0.0
%define DEFCC cc

%description
GNU gdb is the standard GNU program debugger.

%prep
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

# Create links into /usr/bin and /usr/linux/bin.
(
    cd $RPM_BUILD_ROOT
    mkdir -p usr/bin
    cd usr/bin
    for fname in  gdb
    do
      ln -sf ../..%{prefix}/bin/$fname .
    done
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{prefix}/info/gdb.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/gdbint.info.gz %{_prefix}/info/dir
/sbin/install-info %{prefix}/info/stabs.info.gz %{_prefix}/info/dir

%postun
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{prefix}/info/gdb.info.gz %{_prefix}/info/dir
/sbin/install-info --delete %{prefix}/info/gdbint.info.gz %{_prefix}/info/dir
/sbin/install-info --delete %{prefix}/info/stabs.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,bin,bin)
%doc COPYING COPYING.LIB README
%doc %{prefix}/man/man1/*
%{prefix}/bin/*
%{prefix}/info/gdb*.gz
%{prefix}/info/stabs*.gz
%{prefix}/info/annotate*.gz
/usr/bin/*

%changelog
* Thu Sep 23 2004 David Clissold <cliss@austin.ibm.com> 6.0-1
- Initial version, adopted from old GNUPro.spec (which included an older gdb).

