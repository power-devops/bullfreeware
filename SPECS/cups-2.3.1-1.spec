%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: Common Unix Printing System
Name: cups
Version: 2.3.1
Release: 1
License: GPLv2
Group: System Environment/Daemons
URL: http://www.cups.org/

Source0: https://github.com/apple/%{name}/releases/download/v%{version}/%{name}-%{version}-source.tar.gz
Source99: cups-1.6.2-generic.png
Source2: %{name}-%{version}-%{release}.build.log

#Source3: %{name}-%{version}_script_test_user.ksh
#Source4: %{name}-%{version}_script_chmod.ksh

Patch0: %{name}-2.3.1-aix.patch
Patch1: %{name}-2.2.1-http_status_t.patch
Patch2: %{name}-2.2.3.test.patch
Patch3: %{name}-2.2.3-aix.patch

Patch4: %{name}-2.3.1-DSOFLAGS.patch
Patch5: %{name}-2.3.1-ipp-fnctl.patch
# Patch6: %{name}-2.3.1-strip.patch
Patch7: cups-2.3.1-socket.patch
# Patch4: %{name}-%{version}-aix-ippserver.patch

%define cups_serverbin %{_libdir}/%{name}
%define cups_serverbin64 %{_libdir64}/%{name}

BuildRequires: sed, gawk
BuildRequires: krb5-devel >= 1.18
# BuildRequires: libjpeg-devel >= 6b-7
# BuildRequires: libpaper-devel >= 1.1.23-1
# BuildRequires: libpng-devel >= 1.2.46-1
# BuildRequires: libtiff-devel >= 3.9.4-2
BuildRequires: zlib-devel >= 1.2.11
BuildRequires: compat-getifaddrs-devel
BuildRequires: gnutls-devel, libiconv


Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-ipptool = %{version}-%{release}


%description
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 


%package client
Summary: CUPS printing system - client programs
Group: System Environment/Daemons
License: GPLv2
Requires: %{name}-libs = %{version}-%{release}
#Requires: krb5-libs >= %{krb5_version}

%description client
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This package contains command-line client
programs.


%package libs
Summary: Common Unix Printing System - libraries
Group: System Environment/Libraries
License: LGPLv2

Requires: krb5-libs >= 1.18
# Requires: libjpeg >= 6b-7
# Requires: libpaper >= 1.1.23-1
# Requires: libpng >= 1.2.46-1
# Requires: libtiff >= 3.9.4-2
Requires: zlib >= 1.2.11
Requires: compat-getifaddrs
Requires: gnutls, libiconv

%description libs
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lp/lpr commands.


%package filesystem
Summary: CUPS printing system - directory layout
BuildArch: noarch

%description filesystem
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 
This package provides some directories which are
required by other packages that add CUPS drivers (i.e. filters, backends etc.).


%package devel
Summary: Common Unix Printing System - development environment
Group: Development/Libraries
License: LGPLv2
Requires: %{name}-libs = %{version}-%{release}
Requires: krb5-devel >= 1.18
# Requires: libjpeg-devel >= 6b-7
# Requires: libpaper-devel >= 1.1.23-1
# Requires: libpng-devel >= 1.2.46-1
# Requires: libtiff-devel >= 3.9.4-2
Requires: zlib-devel >= 1.2.11
Requires: compat-getifaddrs-devel

%description devel
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.


%package lpd
Summary: Common Unix Printing System - lpd emulation
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description lpd
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. This is the package that provices standard 
lpd emulation.


%package ipptool
Summary: Common Unix Printing System - tool for performing IPP requests
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the results.


%package printerapp
Summary: CUPS printing system - tools for printer application
Requires: %{name}-libs = %{version}-%{release}
# ippeveprinter needs avahi for registering and sharing printer
# Requires: avahi
# needed for mdns hostname translation
# Requires: nss-mdns

%description printerapp
Provides IPP everywhere printer application ippeveprinter and tools for printing
PostScript and HP PCL document formats - ippevepcl and ippeveps. The printer
application enables older printers for IPP everywhere standard - so if older printer
is installed with a printer application, its print queue acts as IPP everywhere printer
to CUPS daemon. This solution will substitute printer drivers and raw queues in the future.


%prep
export PATCH=/opt/freeware/bin/patch
%setup -q
cp %{SOURCE99} doc/images/generic.png
%patch0
%patch1
%patch2
%patch3 -p0

%patch4 -p1 -b .DSOFLAGS
%patch5 -p1 -b .ipp
# %patch6 -p1 -b .strip
%patch7 -p1 -b .socket

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

export CFLAGS=""
export CXXFLAGS=""

cp $0 %{name}-%{version}_script_build.ksh
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export MAKE="gmake --print-directory --trace"
export AR="/usr/bin/ar -X32_64"
export AWK=/opt/freeware/bin/gawk
export OPTFALGS="-O2"
export CPPFLAGS="$OPTFALGS"
export LIBS="-lcompat-getifaddrs -lpthreads -liconv -lgnutls -lz -lm -liconv"

build_cups () {
# need to change the KRB5 config file otherwise we'll end up with 32-bit libs
# which can't be linked to 64-bit objects

./configure \
    --prefix=%{_prefix} \
    --libdir=$1 \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --sysconfdir=/etc \
    --enable-shared \
    --disable-static \
    --localstatedir=/var \
    --enable-ssl \
    --enable-threads \
    --disable-cdsassl \
	--enable-gnutls \
    --enable-largefile \
    --with-perl=$2 \
    --without-php \
    --without-python \
    localedir=%{_datadir}/locale

# on AIX asl.h is the AIX Screen Library not cdsassl !
/opt/freeware/bin/sed -i 's|#define HAVE_ASL_H 1|/* undef HAVE_ASL_H */|g' config.h

cd cups
$MAKE %{?_smp_mflags} libcups.so.2
$AR -qc libcups.a libcups.so.2
cd ..

# fix 'Makedefs' so we link dynamically (from /opt/freeware/lib)
#/opt/freeware/bin/sed -i 's|../cups/libcups.a|-lcups|g' Makedefs
#/opt/freeware/bin/sed -i 's|../filter/libcupsimage.a|-lcupsimage|g' Makedefs
/opt/freeware/bin/sed -i 's|\(INSTALL_LIB[\t ]*=[\t ]*.*\)-s\(.*\)|\1\2|g' Makedefs

$MAKE %{?_smp_mflags}
}

# first build the 64-bit version
cd 64bit

export CC="/opt/freeware/bin/gcc -maix64 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix64 -D_DBUS_GNUC_EXTENSION=__extension__ "
export OBJECT_MODE=64
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 $LIBS -Wl,-blibpath:$LIBPATH"

build_cups %{_libdir64} /opt/freeware/bin/perl_64

# sed   -e 's|-L/opt/freeware/lib -lgnutls|-L/opt/freeware/lib -lgnutls|' -e 's|COMMONLIBS.*$|& -lgnutls|' -e 's|LIBZ.*=.*$|& -lgnutls -lpthread -liconv |' <Makedefs.tmp.sv >Makedefs

cd ../32bit
# now build the 32-bit version

export CC="/opt/freeware/bin/gcc -maix32 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix32 -D_DBUS_GNUC_EXTENSION=__extension__ "
export OBJECT_MODE=32
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib $LIBS -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:$LIBPATH"

build_cups %{_libdir} /opt/freeware/bin/perl_32

%install
cp $0 %{name}-%{version}_script_install.ksh
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export MAKE="gmake --print-directory --trace "
export INSTALL="/opt/freeware/bin/install "
export AR="/usr/bin/ar -X32_64"
export AWK=/opt/freeware/bin/gawk
export RM=/opt/freeware/bin/rm
export STRIP="/usr/bin/strip -X32_64"

cd 64bit

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix64 -D_DBUS_GNUC_EXTENSION=__extension__ "
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -Wl,-blibpath:$LIBPATH"

$MAKE install DSTROOT=${RPM_BUILD_ROOT}

(
    for dir in  backend cgi-bin command daemon filter monitor notifier ;
    do
	cd ${RPM_BUILD_ROOT}%{cups_serverbin}/$dir/
	mkdir -p ${RPM_BUILD_ROOT}%{cups_serverbin64}/$dir/
	for fic in *;
	do
	    mv $fic ${RPM_BUILD_ROOT}%{cups_serverbin64}/$dir/"$fic"
	done
    done
    mkdir ${RPM_BUILD_ROOT}%{cups_serverbin64}/driver
)


(
    for dir in bin sbin;
    do
	cd  ${RPM_BUILD_ROOT}/%{_prefix}/$dir
	for fic in $(ls -1| grep -v -e _32 -e _64)
	do
	    [ -L $fic ] && {
		cible=$(ls -l $fic|awk '{print $NF}');
		ln -s "$cible"_64 "$fic"_64;
		continue;
	    }
	    mv $fic "$fic"_64
	done
    done
)



cd ../32bit

export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix32 -D_DBUS_GNUC_EXTENSION=__extension__ "
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:$LIBPATH -Wl,-bmaxdata:0x80000000"

$MAKE install DSTROOT=${RPM_BUILD_ROOT}

cd ..

(
    for dir in bin sbin;
    do
	cd  ${RPM_BUILD_ROOT}/%{_prefix}/$dir
	for fic in $(ls -1| grep -v -e _32 -e _64)
	do
	    [ -L $fic ] && {
		cible=$(ls -l $fic|awk '{print $NF}');
		ln -s "$cible"_32 "$fic"_32;
		continue;
	    }
	    mv $fic "$fic"_32
	    ln -sf "$fic"_64 $fic
	done
    done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects

(
    cd  ${RPM_BUILD_ROOT}/%{_libdir}
    # Only 4 lib: libcups.so.2, libcupsimage.so.2, libcupsfilters.so.1 and libfontembed.so.1 provided by Fedora
    # The last two are provided in a separate package, and are not produced on AIX.
    # .so without version are installed bu cups but shall not be used to create archive.
    for fic in `ls *.so`; do
        current_lib_a=`basename $fic .so`.a
        $AR -qc ${current_lib_a} ${fic}.*
        $AR -qc ${current_lib_a} ../lib64/${fic}.*
        cd ../lib64
        ln -sf ../lib/${current_lib_a} ${current_lib_a}
        cd ../lib
    done
)

#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}/usr/bin/* || :
#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}/usr/sbin/* || :

/usr/bin/rm -rf ${RPM_BUILD_ROOT}/etc/rc.d/rc[05].d

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/locale
#/usr/bin/mv -f ${RPM_BUILD_ROOT}%{_libdir}/nls/msg/* ${RPM_BUILD_ROOT}%{_datadir}/locale/

find %{buildroot} -type f -o -type l | sed '
s:.*\('%{_datadir}'/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:
/^%lang(C)/d
/^\([^%].*\)/d
' > %{name}.lang


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
(gmake -k check --trace || true)

cd ../32bit
export OBJECT_MODE=32
(gmake -k check --trace || true)

# Some tests cannot be run automatically
# Partial code here for history
# ( mkdir /tmp/scheduler || true )
# export LIBPATH="$RPM_BUILD_ROOT/%{_libdir64}:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
# cp $RPM_BUILD_ROOT/%{_sbindir}/cupsd_64 /tmp/scheduler/cupsd
# chmod uga+rwx /tmp/scheduler/cupsd

# sed -i "s|User root|User guest|" /tmp/cups-root/cups-files.conf
# su guest -c "/tmp/cups-root/runcups /tmp/scheduler/cupsd -c /tmp/cups-root/cupsd.conf -f &"
%endif


%post
# Remove old-style certs directory; new-style is /var/run
# (see bug #194581 for why this is necessary).
/usr/bin/rm -rf /etc/%{name}/certs
/usr/bin/rm -f /var/cache/%{name}/*.ipp /var/cache/%{name}/*.cache
exit 0


%preun
if [ "$1" = "0" ]; then
    /etc/rc.d/init.d/cups stop > /dev/null 2>&1
fi
exit 0


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f cups.lang
%defattr(-,root,system)
%doc 32bit/LICENSE 32bit/README.md 32bit/CREDITS.md 32bit/CHANGES.md

/etc/rc.d/init.d/cups
/etc/rc.d/rc2.d/*cups
/etc/rc.d/rc3.d/*cups

%dir %attr(0755,root,lp) /etc/cups
%dir %attr(0755,root,lp) /var/run/cups
%dir %attr(0511,lp,system) /var/run/cups/certs

%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) /etc/cups/cupsd.conf
%attr(0640,root,lp) /etc/cups/cupsd.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) /etc/cups/cups-files.conf
%attr(0640,root,lp) /etc/cups/cups-files.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/cups/snmp.conf
%attr(0640,root,lp) /etc/cups/snmp.conf.default
%dir %attr(0755,root,lp) /etc/cups/ppd
%dir %attr(0700,root,lp) /etc/cups/ssl

# %dir %attr(0775,root,lp) /var/cache/cups
# %dir %attr(0775,root,lp) /var/cache/cups/rss


%{_bindir}/cupstestppd*
%{_bindir}/ppd*
%{cups_serverbin}/backend/*
%{cups_serverbin}/cgi-bin
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-deviced
%{cups_serverbin}/daemon/cups-driverd
%{cups_serverbin}/daemon/cups-exec
%{cups_serverbin}/notifier
%{cups_serverbin}/filter/*
%{cups_serverbin}/monitor

%dir %{cups_serverbin64}
%{cups_serverbin64}/backend/*
%{cups_serverbin64}/cgi-bin
%dir %{cups_serverbin64}/daemon
%{cups_serverbin64}/daemon/cups-deviced
%{cups_serverbin64}/daemon/cups-driverd
%{cups_serverbin64}/daemon/cups-exec
%{cups_serverbin64}/notifier
%{cups_serverbin64}/filter/*
%{cups_serverbin64}/monitor

%{_mandir}/man?/*

# client subpackage
%exclude %{_mandir}/man1/lp*.1*
%exclude %{_mandir}/man1/cancel.1*
%exclude %{_mandir}/man8/lpc.8*
# devel subpackage
%exclude %{_mandir}/man1/cups-config.1*
# ipptool subpackage
%exclude %{_mandir}/man1/ipptool.1*
%exclude %{_mandir}/man5/ipptoolfile.5*
# lpd subpackage
%exclude %{_mandir}/man8/cups-lpd.8*

%{_sbindir}/*
# client subpackage
%exclude %{_sbindir}/lpc*

%dir %{_datadir}/cups/templates
%dir %{_datadir}/cups/templates/de
%dir %{_datadir}/cups/templates/es
%dir %{_datadir}/cups/templates/ja
%dir %{_datadir}/cups/templates/ru
%dir %{_datadir}/cups/templates/pt_BR
%{_datadir}/cups/templates/*.tmpl
%{_datadir}/cups/templates/de/*.tmpl
%{_datadir}/cups/templates/fr/*.tmpl
%{_datadir}/cups/templates/es/*.tmpl
%{_datadir}/cups/templates/ja/*.tmpl
%{_datadir}/cups/templates/ru/*.tmpl
%{_datadir}/cups/templates/pt_BR/*.tmpl

%dir %attr(1770,root,lp) /var/spool/cups/tmp
%dir %attr(0710,root,lp) /var/spool/cups
%dir %attr(0755,lp,system) /var/log/cups

%{_datadir}/cups/drv
%{_datadir}/cups/examples
%{_datadir}/cups/mime/mime.types
%{_datadir}/cups/mime/mime.convs
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h

%files client
%defattr(-,root,system)
%{_sbindir}/lpc*
%{_bindir}/cancel*
%{_bindir}/lp*
%{_mandir}/man1/lp*.1*
%{_mandir}/man1/cancel.1*
%{_mandir}/man8/lpc.8*

%files libs
%defattr(-,root,system)
%{_libdir}/libcups.a
%{_libdir}/libcupsimage.a
%{_libdir64}/libcups.a
%{_libdir64}/libcupsimage.a

%files filesystem
%defattr(-,root,system)
%dir %{cups_serverbin}
%dir %{cups_serverbin}/backend
%dir %{cups_serverbin}/driver
%dir %{cups_serverbin}/filter
%dir %{cups_serverbin64}
%dir %{cups_serverbin64}/backend
%dir %{cups_serverbin64}/driver
%dir %{cups_serverbin64}/filter
%dir %{_datadir}/cups
#%%dir %%{_datadir}/cups/banners
#%%dir %%{_datadir}/cups/charsets
%dir %{_datadir}/cups/data
%dir %{_datadir}/cups/drv
%dir %{_datadir}/cups/mime
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
%dir %{_datadir}/cups/profiles

%files devel
%defattr(-,root,system)
%{_bindir}/cups-config*
%{_includedir}/cups
%{_mandir}/man1/cups-config.1*

%files lpd
%defattr(-,root,system)
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-lpd
%dir %{cups_serverbin64}/daemon
%{cups_serverbin64}/daemon/cups-lpd
%{_mandir}/man8/cups-lpd.8*


%files ipptool
%defattr(-,root,system)
# %{_bindir}/ippfind*
%{_bindir}/ipptool*
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*
%{_mandir}/man1/ipptool.1*
%{_mandir}/man5/ipptoolfile.5*

%files printerapp
%defattr(-,root,system)
%{_bindir}/ippeveprinter
%dir %{cups_serverbin}/command
%{cups_serverbin}/command/ippevepcl
%{cups_serverbin}/command/ippeveps
%dir %{cups_serverbin64}/command
%{cups_serverbin64}/command/ippevepcl
%{cups_serverbin64}/command/ippeveps
%{_mandir}/man1/ippeveprinter.1*
%{_mandir}/man7/ippevepcl.7*


%changelog
* Fri Mar 13 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> - 2.3.1-1
- Merge bullfreeware, toolbox and fedora specfile
- New version 2.3.1
- Bullfreeware OpenSSL removal

* Fri Aug 10 2018 Tony Reix <tony.reix@atos.net> - 2.2.1-4
- Remove Requires on AIX version

* Thu Mar 29 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> 2.2.3-2
- Rebuit commenting requires field to avoid Aix-rpm dependency.

* Wed Jan 04 2017 Jean Girardet <jean.girardet@atos.net> - 2.2.1-3
- Create new relead "-3" to compile with Xlc

* Thu Nov 24 2016 Jean Girardet <jean.girardet@atos.net> - 2.2.1-1
- updated to version 2.2.1 from 2.0.2

* Tue Oct 01 2013 Michael Perzl <michael@perzl.org> - 1.6.4-1
- updated to version 1.6.4

* Fri Jul 12 2013 Michael Perzl <michael@perzl.org> - 1.6.3-1
- updated to version 1.6.3

* Mon Mar 18 2013 Michael Perzl <michael@perzl.org> - 1.6.2-1
- updated to version 1.6.2

* Sat Jul 28 2012 Michael Perzl <michael@perzl.org> - 1.6.1-1
- updated to version 1.6.1

* Thu Jul 26 2012 Michael Perzl <michael@perzl.org> - 1.6.0-1
- updated to version 1.6.0

* Thu Jul 26 2012 Michael Perzl <michael@perzl.org> - 1.5.4-1
- updated to version 1.5.4

* Wed May 16 2012 Michael Perzl <michael@perzl.org> - 1.5.3-1
- updated to version 1.5.3

* Mon Feb 06 2012 Michael Perzl <michael@perzl.org> - 1.5.2-1
- updated to version 1.5.2

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.5.0-1
- updated to version 1.5.0

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.4.8-1
- updated to version 1.4.8

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.4.7-1
- updated to version 1.4.7

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.4.6-1
- updated to version 1.4.6

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.4.5-1
- updated to version 1.4.5

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.4.4-2
- added 64-bit libraries and RTL-style libraries

* Tue Aug 03 2010 Michael Perzl <michael@perzl.org> - 1.4.4-1
- first version for AIX V5.1 and higher
