Summary: Graphical tool used to capture an analyse network traffic.
Name: ethereal
Version: 0.8.18
Release: 1
License: GPL
#AIXBuildRequires: bos.net.tcp.adt
# On AIX 4.3.3, you must create symlinks from /usr/opt/perl5/bin/* to
# /usr/bin or else add /usr/opt/perl5/bin to the PATH
Group: Applications/Networking
Source: ftp://ftp.ethereal.com/pub/ethereal/%{name}-%{version}.tar.gz
Patch0: ethereal-0.8.18-aix.patch
Buildroot: /var/tmp/ethreal-root
Prefix: %{_prefix}

# The following section establishes preferred compilers to use to build the
# executables. The eventual default compiler on IA is still to be determined. 

%ifarch ia64
  %define DEFCCIA cc
  %define DEFCC %{DEFCCIA}
%else
  %define DEFCC cc
%endif


%description
Ethereal is a free network protocol analyzer for Unix and Windows. It allows you to examine data from a live
network or from a capture file on disk. You can interactively browse the capture data, viewing summary and detail
information for each packet. Ethereal has several powerful features, including a rich display filter language and the
ability to view the reconstructed stream of a TCP session.



%prep
%setup -q
%patch0 -p1 -b .bak



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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       if test "X$CC" = "Xcc"
       then
          # Workaround compiler bug
          export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-O2::'`
       fi
       export CFLAGS="$RPM_OPT_FLAGS"
fi

%define optflags $RPM_OPT_FLAGS

export LDFLAGS="-Wl,-brtl"
%configure
make



%install
rm -rf $RPM_BUILD_ROOT
make install install-man DESTDIR=$RPM_BUILD_ROOT

(cd $RPM_BUILD_ROOT
for dir in bin lib
do
   mkdir -p usr/$dir
   cd usr/$dir
   ln -sf ../..%{_prefix}/$dir/* .
   cd -
done
)




%files

# The /usr/bin entry part reflects the links which we added.
# The %files section can be much more complicated, with %doc entries
# for documentation, %attr() and %defattr() entries to define permissions,
# and %dir directory entries.   At least one match must be found for every
# entry or else you will get "File not found" errors and no RPM package will be
# produced.

%{prefix}/bin/*
%{prefix}/etc/*
%{prefix}/lib/ethereal/*
/usr/bin/*
/usr/lib/ethereal
%{prefix}/man/man1/*



%clean
rm -rf $RPM_BUILD_ROOT



%changelog

* Tue Jun 26 2001 Olof Johansson
- First version


