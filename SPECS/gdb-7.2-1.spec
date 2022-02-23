Summary: A GNU source-level debugger for C, C++, Java and other languages.
Name: gdb
Version: 7.2
Release: 1
License: GPL
Group: Development/Debuggers
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}-simppc.patch
Patch1: %{name}-%{version}-multiosdir.patch
URL: http://gnu.org/software/gdb/
Buildroot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: make, gettext
BuildRequires: expat-devel >= 2.0.0, python-devel >= 2.6-2, zlib-devel
 
Requires: info, gettext, expat >= 2.0.0, python-devel >= 2.6-2, zlib

%define DEFCC cc

%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%prep
%setup -q
%patch0 -p1 -b .simppc
%patch1 -p1 -b .multiosdir


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

export CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --disable-werror \
    --target powerpc-ibm-aix5.3.0.0

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

# Strip all of the executables
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# compress the info files
gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*

# install the gcore script in /usr/bin
cp gdb/gdb_gcore.sh ${RPM_BUILD_ROOT}%{_bindir}/gcore
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/gcore

# do not take %{_includedir}, %{_libdir}, %{_datadir}, %{_infodir}/bfd*, %{_infodir}/configure*, }%{_infodir}/dir*, %{_infodir}/standard* provide by binutils package

# Create links into /usr/bin and /usr/linux/bin
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

%post
/sbin/install-info %{_infodir}/annotate.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gdb.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gdbint.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/stabs.info.gz %{_infodir}/dir || :


%preun
if [ $1 -eq 0 ]; then
    /sbin/install-info --delete %{_infodir}/annotate.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gdb.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gdbint.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/stabs.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc COPYING COPYING.LIB README gdb/NEWS
%{_bindir}/*
%{_infodir}/gdb*.gz
%{_infodir}/annotate*.gz
%{_infodir}/stabs*.gz
%{_mandir}/man1/*
/usr/bin/*



%changelog
* Fri May 27 2011 Patricia Cugny <patricia.cugny@bull.net> 7.2-1
- update to version 7.2 

* Thu Sep 23 2004 David Clissold <cliss@austin.ibm.com> 6.0-1
- Initial version, adopted from old GNUPro.spec (which included an older gdb).

