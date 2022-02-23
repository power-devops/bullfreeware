Summary: Common Unix Printing System
Name: cups
Version: 2.2.1
Release: 3
License: GPLv2
Group: System Environment/Daemons
Source0: http://ftp.easysw.com/pub/cups/%{version}/%{name}-%{version}-source.tar.gz
Source99: cups-1.6.2-generic.png
Source2: %{name}-%{version}-%{release}.build.log
Source3: %{name}-%{version}_script_test_user.ksh
Source4: %{name}-%{version}_script_chmod.ksh

Patch2: %{name}-%{version}-aix-ippserver.patch

# Add patch from fedora :
patch3: cups-0755.patch
patch7: cups-banners.patch
patch8: cups-direct-usb.patch
patch9: cups-dnssd-deviceid.patch
patch10: cups-driverd-timeout.patch
patch11: cups-dymo-deviceid.patch
patch12: cups-eggcups.patch
patch13: cups-enum-all.patch
patch14: cups-filter-debug.patch
patch15: cups-freebind.patch
patch16: cups-hp-deviceid-oid.patch
patch17: cups-ipp-multifile.patch
patch18: cups-libusb-quirks.patch
patch19: cups-logrotate.patch
patch20: cups-lpr-help.patch
patch22: cups-multilib.patch
patch23: cups-no-export-ssllibs.patch
patch24: cups-no-gcry.patch
patch25: cups-no-gzip-man.patch
patch26: cups-peercred.patch
patch27: cups-pid.patch
patch28: cups-res_init.patch
patch29: cups-ricoh-deviceid-oid.patch
patch30: cups-serverbin-compat.patch
patch31: cups-str3382.patch
patch32: cups-strict-ppd-line-length.patch
patch33: cups-synconclose.patch
patch34: cups-system-auth.patch
patch35: cups-systemd-socket.patch
patch36: cups-uri-compat.patch
patch37: cups-usb-paperout.patch
patch38: cups-use-ipp1.1.patch
patch39: cups-web-devices-timeout.patch


URL: http://www.cups.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel >= 1.0.1
BuildRequires: sed
BuildRequires: krb5-devel >= 1.8.3-1
BuildRequires: libjpeg-devel >= 6b-7
BuildRequires: libpaper-devel >= 1.1.23-1
BuildRequires: libpng-devel >= 1.2.46-1
BuildRequires: libtiff-devel >= 3.9.4-2
BuildRequires: zlib-devel >= 1.2.3-3

Requires: %{name}-libs = %{version}-%{release}

%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%define _libdir64 %{_prefix}/lib64
%define _bindir %{_prefix}/bin

%define cups_serverbin %{_libdir}/%{name}
%define cups_serverbin64 %{_libdir64}/%{name}

%description
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 


%package devel
Summary: Common Unix Printing System - development environment
Group: Development/Libraries
License: LGPLv2
Requires: %{name}-libs = %{version}-%{release}
Requires: krb5-devel >= 1.8.3-1
Requires: libjpeg-devel >= 6b-7
Requires: libpaper-devel >= 1.1.23-1
Requires: libpng-devel >= 1.2.46-1
Requires: libtiff-devel >= 3.9.4-2
Requires: openssl-devel >= 1.0.1
Requires: zlib-devel >= 1.2.3-3


%description devel
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.


%package libs
Summary: Common Unix Printing System - libraries
Group: System Environment/Libraries
License: LGPLv2

Requires: krb5-libs >= 1.8.3-1
Requires: libjpeg >= 6b-7
Requires: libpaper >= 1.1.23-1
Requires: libpng >= 1.2.46-1
Requires: libtiff >= 3.9.4-2
Requires: openssl >= 1.0.1
Requires: zlib >= 1.2.3-3

%description libs
The Common UNIX Printing System provides a portable printing layer for 
UNIX operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lp/lpr commands.


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


%prep
export PATCH=/opt/freeware/bin/patch

%setup -q

cp %{SOURCE99} doc/images/generic.png

%patch2 -p1 
%patch3 -p1 


%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch22 -p1

$PATCH -p1 <$SOURCES/cups-no-export-ssllibs.patch

# %patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1

awk '{print $0; if (NR==1) print "set -x";}' <configure >configure.$$
cp  configure.$$  configure



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
export MAKE="gmake --print-directory "
export AR=/usr/bin/ar
export AWK=/opt/freeware/bin/gawk


# first build the 64-bit version

cd 64bit
[ -e /opt/freeware/lib64/crt0.o ] || {
    cd /opt/freeware/lib64/
    ls -s /usr/lib/crt0_64.o crt0.o
    cd -
}

# CFLAGS must include in CC vairiables 
#    export CFLAGS=" -maix64"
#    export CXXFLAGS="-maix64"
export CC="/opt/freeware/bin/gcc -maix64 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix64 -D_DBUS_GNUC_EXTENSION=__extension__ "
export OBJECT_MODE=64
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"
export LIBRARY_PATH=/opt/freeware/lib64:/opt/freeware/lib/gcc/powerpc-ibm-aix6.1.0.0/4.8.4/ppc64/:/opt/freeware/lib:/lib/:/usr/lib/

# need to change the KRB5 config file otherwise we'll end up with 32-bit libs
# which can't be linked to 64-bit objects

#  #/opt/freeware/bin/sed -i 's/set dummy krb5-config/set dummy krb5-config_64/g' configure

# autoconf


[ -e configure.save ] || {
    cp configure configure.save
    sed -e 's|-Wl,-soname,..basename .$....| |' -e '/define HAVE_ASL_H 1/d'  <configure.save  >configure
}


./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir64} \
    --sysconfdir=/etc \
    --enable-shared \
    --disable-static \
    --localstatedir=/var


[ -e Makedefs.tmp.sv ] || {
    cp -p Makedefs Makedefs.tmp.sv
}
# in 64 bits mode supress "-g"
# add gnutls library -lpthread -liconv

sed   -e 's|-L/opt/freeware/lib -lgnutls|-L/opt/freeware/lib -lgnutls|' -e 's|COMMONLIBS.*$|& -lgnutls|' -e 's|LIBZ.*=.*$|& -lgnutls -lpthread -liconv |' <Makedefs.tmp.sv >Makedefs



$MAKE %{?_smp_mflags}
$MAKE check %{?_smp_mflags} || true
cd ..


cd 32bit
# now build the 32-bit version

# export CFLAGS=" -maix32"
# export CXXFLAGS=" -maix32"
export CC="/opt/freeware/bin/gcc -maix32 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix32 -D_DBUS_GNUC_EXTENSION=__extension__ "
export OBJECT_MODE=32
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"
export LIBRARY_PATH=/opt/freeware/lib:/opt/freeware/lib/gcc/powerpc-ibm-aix6.1.0.0/4.8.4/:/lib/:/usr/lib/


# autoconf

[ -e configure.save ] || {
    cp configure configure.save
    sed -e 's|-Wl,-soname,..basename .$....| |' -e '/define HAVE_ASL_H 1/d'  <configure.save  >configure
    
}

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --enable-shared \
    --disable-static \
    --localstatedir=/var 



    [ -e Makedefs.tmp.sv ] || {
	cp -p Makedefs Makedefs.tmp.sv
    }
# add gnutls library -lpthread -liconv
    sed -e 's|COMMONLIBS.*$|& -lgnutls|' -e 's|LIBZ.*=.*$|& -lgnutls -lpthread -liconv -lgcc_s|' <Makedefs.tmp.sv >Makedefs


$MAKE %{?_smp_mflags}
$MAKE check %{?_smp_mflags} || true

cd ..


%install
cp $0 %{name}-%{version}_script_install.ksh
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


export CFLAGS=""
export CXXFLAGS=""

export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export MAKE="gmake --print-directory "
export INSTALL="/opt/freeware/bin/install "
export AR=/usr/bin/ar
export AWK=/opt/freeware/bin/gawk
export RM=/opt/freeware/bin/rm

cd 64bit


a='$(LIBCUPSCGI)';dir=cgi-bin;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPS)';dir=cups;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSIMAGE)';dir=filter;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSPPDC)';dir=ppdc;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSMIME)';dir=scheduler;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;


# first build the 64-bit version
export OBJECT_MODE=64
# export CFLAGS=" -maix64"
# export CXXFLAGS="-maix64"
export CC="/opt/freeware/bin/gcc -maix64 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix64 -D_DBUS_GNUC_EXTENSION=__extension__ "
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"
export LIBRARY_PATH=/opt/freeware/lib64:/opt/freeware/lib/gcc/powerpc-ibm-aix6.1.0.0/4.8.4/ppc64/:/opt/freeware/lib:/lib/:/usr/lib/
  
$MAKE install DSTROOT=${RPM_BUILD_ROOT}


(
    for dir in  backend cgi-bin daemon filter monitor notifier ;
    do
	cd ${RPM_BUILD_ROOT}%{cups_serverbin}/$dir/
	mkdir -p ${RPM_BUILD_ROOT}%{cups_serverbin64}/$dir/
	for fic in *;
	do
	    mv $fic ${RPM_BUILD_ROOT}%{cups_serverbin64}/$dir/"$fic"
	done
    done
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



cd ..

echo ************************** ${RPM_BUILD_ROOT} *************************


#mv ${RPM_BUILD_ROOT}%{_bindir}/cups-config ${RPM_BUILD_ROOT}%{_bindir}/cups-config_64

cd 32bit


a='$(LIBCUPSCGI)';dir=cgi-bin;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPS)';dir=cups;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSIMAGE)';dir=filter;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSPPDC)';dir=ppdc;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;
a='$(LIBCUPSMIME)';dir=scheduler;sed -e "s|if test $a|if test \"$a\"|" <$dir/Makefile >$dir/Makefile.tmp.$$;rm -f $dir/Makefile;mv $dir/Makefile.tmp.$$ $dir/Makefile;


export OBJECT_MODE=32
# export CFLAGS=" -maix32"
# export CXXFLAGS=" -maix32"
export CC="/opt/freeware/bin/gcc -maix32 -D_DBUS_GNUC_EXTENSION=__extension__" 
export CXX="/opt/freeware/bin/g++ -maix32 -D_DBUS_GNUC_EXTENSION=__extension__ "
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"
export LIBRARY_PATH=/opt/freeware/lib:/opt/freeware/lib/gcc/powerpc-ibm-aix6.1.0.0/4.8.4/:/usr/lib/

$MAKE install DSTROOT=${RPM_BUILD_ROOT}



# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects

echo "cups           .2"  > input.lib.$$.tmp
echo "cupscgi        .1" >> input.lib.$$.tmp
echo "cupsimage      .2" >> input.lib.$$.tmp
echo "cupsmime       .1" >> input.lib.$$.tmp
echo "cupsppdc       .1" >> input.lib.$$.tmp

cat input.lib.$$.tmp | while read lib number pad;
do

    # Build the  shared library from the 32-bit shared object
    # then add the 64-bit shared object to the shared library containing already the
    # 32-bit shared object

    $AR -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a ${RPM_BUILD_ROOT}/%{_libdir}/lib"$lib".so"$number"
    $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a ${RPM_BUILD_ROOT}/%{_libdir64}/lib"$lib".so"$number"

    (
	# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
	$RM -f ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
	cd  ${RPM_BUILD_ROOT}%{_libdir64}
	ln -s ../lib/lib"$lib".a lib"$lib".a
	strip -X64 -e  ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".so"$number"
	strip -X32 -e  ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".so"$number"
    )
done
rm -f input.lib.$$.tmp



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


#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}/usr/bin/* || :
#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}/usr/sbin/* || :

/usr/bin/rm -rf ${RPM_BUILD_ROOT}/etc/rc.d/rc[05].d

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/locale
#/usr/bin/mv -f ${RPM_BUILD_ROOT}%{_libdir}/nls/msg/* ${RPM_BUILD_ROOT}%{_datadir}/locale/



# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin include lib lib64
  do
    mkdir -p usr/linux/${dir}
    cd usr/linux/${dir}
    ln -sf ../../..%{_prefix}/${dir}/* .
    cd -
  done
)
cd ..




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
# [ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/LICENSE.txt 32bit/README.txt 32bit/CREDITS.txt 32bit/CHANGES.txt

%{_bindir}/cancel*
%{_bindir}/cupstestdsc*
%{_bindir}/cupstestppd*
%{_bindir}/lp*
%{_bindir}/ppd*

%{_sbindir}/*

/etc/rc.d/init.d/%{name}
/etc/rc.d/rc2.d/*%{name}
/etc/rc.d/rc3.d/*%{name}

%dir %attr(0755,root,lp) /etc/%{name}
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) /etc/%{name}/cupsd.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) /etc/%{name}/cupsd.conf.N
%attr(0640,root,lp) /etc/%{name}/cupsd.conf.default
# /etc/%{name}/interfaces
%dir %attr(0755,root,lp) /etc/%{name}/ppd
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/%{name}/snmp.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/%{name}/snmp.conf.N
%dir %attr(0700,root,lp) /etc/%{name}/ssl

%dir %attr(0755,root,lp) /var/run/%{name}
%dir %attr(0511,lp,system) /var/run/%{name}/certs

%dir %attr(0775,root,lp) /var/cache/%{name}
%dir %attr(0775,root,lp) /var/cache/%{name}/rss

%dir %attr(0710,root,lp) /var/spool/%{name}
%dir %attr(1770,root,lp) /var/spool/%{name}/tmp
%dir %attr(0755,lp,system) /var/log/%{name}

%dir %{cups_serverbin}
%{cups_serverbin}/backend
%{cups_serverbin}/cgi-bin
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-deviced
%{cups_serverbin}/daemon/cups-driverd
%{cups_serverbin}/daemon/cups-exec
%{cups_serverbin}/driver
%{cups_serverbin}/filter
%{cups_serverbin}/monitor
%{cups_serverbin}/notifier

%dir %{cups_serverbin64}
%{cups_serverbin64}/backend
%{cups_serverbin64}/cgi-bin
%dir %{cups_serverbin64}/daemon
%{cups_serverbin64}/daemon/cups-deviced
%{cups_serverbin64}/daemon/cups-driverd
%{cups_serverbin64}/daemon/cups-exec
# %{cups_serverbin64}/driver
%{cups_serverbin64}/filter
%{cups_serverbin64}/monitor
%{cups_serverbin64}/notifier

%{_mandir}/man?/*

%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/doc/%{name}/es
%doc %{_datadir}/doc/%{name}/help
%{_datadir}/doc/%{name}/images
%dir %{_datadir}/doc/%{name}/ja
%{_datadir}/doc/%{name}/*.css
%doc %{_datadir}/doc/%{name}/index.html
%doc %{_datadir}/doc/%{name}/robots.txt
%doc %{_datadir}/doc/%{name}/es/index.html
%doc %{_datadir}/doc/%{name}/ja/index.html

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/banners
# %config(noreplace) %{_datadir}/%{name}/banners/*
%{_datadir}/%{name}/data
%{_datadir}/%{name}/model

%dir %{_datadir}/%{name}/templates
%config(noreplace) %{_datadir}/%{name}/templates/*.tmpl
%dir %{_datadir}/%{name}/templates/es
%config(noreplace) %{_datadir}/%{name}/templates/es/*.tmpl
%dir %{_datadir}/%{name}/templates/ja
%config(noreplace) %{_datadir}/%{name}/templates/ja/*.tmpl

%{_datadir}/%{name}/drv
%{_datadir}/%{name}/examples
%dir %{_datadir}/%{name}/mime
%config(noreplace) %{_datadir}/%{name}/mime/mime.types*
%config(noreplace) %{_datadir}/%{name}/mime/mime.convs*
%dir %{_datadir}/%{name}/ppdc
%{_datadir}/%{name}/ppdc/*.defs
%{_datadir}/%{name}/ppdc/*.h
%dir %{_datadir}/%{name}/profiles

/usr/linux/bin/cancel*
/usr/linux/bin/cupstestdsc*
/usr/linux/bin/cupstestppd*
/usr/linux/bin/lp*
/usr/linux/bin/ppd*
/usr/linux/sbin/*


%files libs
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/linux/lib/*.a
/usr/linux/lib64/*.a
/usr/linux/lib/*.so*
/usr/linux/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_bindir}/cups-config*
%{_includedir}/%{name}
%{_mandir}/man1/cups-config.1*
/usr/linux/bin/cups-config*
/usr/linux/include/%{name}


%files lpd
%defattr(-,root,system)
%dir %{cups_serverbin}
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-lpd


%files ipptool
%defattr(-,root,system)
%{_bindir}/ipptool*
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/color.jpg
%{_datadir}/cups/ipptool/create-printer-subscription.test
%{_datadir}/cups/ipptool/document-*
%{_datadir}/cups/ipptool/get-completed-jobs.test
%{_datadir}/cups/ipptool/get-jobs.test
%{_datadir}/cups/ipptool/get-printer-attributes.test
%{_datadir}/cups/ipptool/gray.jpg
%{_datadir}/cups/ipptool/ipp-1.1.test
%{_datadir}/cups/ipptool/ipp-2.0.test
%{_datadir}/cups/ipptool/ipp-2.1.test
%{_datadir}/cups/ipptool/ipp-2.2.test
%{_datadir}/cups/ipptool/onepage-*
%{_datadir}/cups/ipptool/testfile.jpg
%{_datadir}/cups/ipptool/testfile.pcl
%{_datadir}/cups/ipptool/testfile.pdf
%{_datadir}/cups/ipptool/testfile.ps
%{_datadir}/cups/ipptool/testfile.txt
%{_mandir}/man1/ipptool.1*
/usr/linux/bin/ipptool*


%changelog
* Tue Jan 04 2017 Jean Girardet <jean.girardet@atos.net> - 2.2.1-3
- Create new relead "-3" to compile with Xlc

* Tue Nov 24 2016 Jean Girardet <jean.girardet@atos.net> - 2.2.1-1
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
