Summary: Common Unix Printing System
Name: cups
Version: 1.6.4
Release: 2
License: GPLv2
Group: System Environment/Daemons
Source0: http://ftp.easysw.com/pub/cups/%{version}/%{name}-%{version}-source.tar.bz2
Source99: cups-1.6.2-generic.png
Patch0: %{name}-%{version}-aix.patch
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

%define cups_serverbin %{_libdir}/%{name}

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
%setup -q
cp %{SOURCE99} doc/images/generic.png
%patch0

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)


%build
export CC="/usr/vac/bin/xlc_r -D_LARGE_FILES=1"

cd 64bit
# first build the 64-bit version
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export DSOFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib"
export OBJECT_MODE=64
# need to change the KRB5 config file otherwise we'll end up with 32-bit libs
# which can't be linked to 64-bit objects
/opt/freeware/bin/sed -i 's/set dummy krb5-config/set dummy krb5-config_64/g' configure
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --enable-shared --disable-static \
    --enable-libpaper \
    --disable-dbus \
    --enable-64bit \
    --enable-image \
    --enable-jpeg \
    --enable-png \
    --enable-tiff \
    --enable-gssapi \
    --disable-slp \
    --enable-ldap \
    --enable-threads \
    --disable-cdsassl \
    --disable-gnutls \
    --enable-openssl \
    --enable-largefile \
    --enable-bannertops \
    --enable-texttops \
    --with-ldap-includes=%{_includedir} \
    --with-openssl-includes=%{_includedir} \
    --with-perl=/opt/freeware/bin/perl \
    --without-php \
    --without-python
make %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export DSOFLAGS="-L/opt/freeware/lib"
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --enable-shared --disable-static \
    --enable-libpaper \
    --disable-dbus \
    --enable-32bit \
    --enable-image \
    --enable-jpeg \
    --enable-png \
    --enable-tiff \
    --enable-gssapi \
    --disable-slp \
    --enable-ldap \
    --enable-threads \
    --disable-cdsassl \
    --disable-gnutls \
    --enable-openssl \
    --enable-largefile \
    --enable-bannertops \
    --enable-texttops \
    --with-ldap-libs=%{_libdir} \
    --with-ldap-includes=%{_includedir} \
    --with-openssl-libs=%{_libdir} \
    --with-openssl-includes=%{_includedir} \
    --with-perl=/opt/freeware/bin/perl \
    --without-php \
    --without-python
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make install DSTROOT=${RPM_BUILD_ROOT}

mv ${RPM_BUILD_ROOT}%{_bindir}/cups-config ${RPM_BUILD_ROOT}%{_bindir}/cups-config_64

cd ../32bit
export OBJECT_MODE=32
make install DSTROOT=${RPM_BUILD_ROOT}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_sbindir}/* || :

/usr/bin/rm -rf ${RPM_BUILD_ROOT}/etc/rc.d/rc[05].d

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/locale
/usr/bin/mv -f ${RPM_BUILD_ROOT}%{_libdir}/nls/msg/* ${RPM_BUILD_ROOT}%{_datadir}/locale/

(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  chmod 0644 *.a
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
    fn=`basename ${f} .a`
    mv ${fn}.o ${fn}.so
    fn=`basename ${f} _s.a`
    ln -s ${fn}_s.a ${fn}.a
    ln -s ${fn}_s.so ${fn}.so
  done

  cd ${RPM_BUILD_ROOT}%{_libdir64}
  chmod 0644 *.a
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
export AR="ar -X32_64"
for f in _s cgi_s image_s mime_s ppdc_s ; do
  ${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libcups${f}.a ${RPM_BUILD_ROOT}%{_libdir64}/libcups${f}.o
done

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    fn=`basename ${f} .a`
    mv ${fn}.o ${fn}.so
    fn=`basename ${f} _s.a`
    ln -s ${fn}_s.so ${fn}.so
  done
)

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


%files
%defattr(-,root,system)
%doc 32bit/LICENSE.txt 32bit/README.txt 32bit/CREDITS.txt 32bit/CHANGES.txt

%{_bindir}/cancel
%{_bindir}/cupstestdsc
%{_bindir}/cupstestppd
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
/etc/%{name}/interfaces
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

%{_mandir}/man?/*

%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/doc/%{name}/ca
%dir %{_datadir}/doc/%{name}/es
%doc %{_datadir}/doc/%{name}/help
%{_datadir}/doc/%{name}/images
%dir %{_datadir}/doc/%{name}/ja
%{_datadir}/doc/%{name}/*.css
%doc %{_datadir}/doc/%{name}/index.html
%doc %{_datadir}/doc/%{name}/robots.txt
%doc %{_datadir}/doc/%{name}/ca/index.html
%doc %{_datadir}/doc/%{name}/es/index.html
%doc %{_datadir}/doc/%{name}/ja/index.html

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/banners
%config(noreplace) %{_datadir}/%{name}/banners/*
%{_datadir}/%{name}/data
%{_datadir}/%{name}/model

%dir %{_datadir}/%{name}/templates
%config(noreplace) %{_datadir}/%{name}/templates/*.tmpl
%dir %{_datadir}/%{name}/templates/ca
%config(noreplace) %{_datadir}/%{name}/templates/ca/*.tmpl
%dir %{_datadir}/%{name}/templates/es
%config(noreplace) %{_datadir}/%{name}/templates/es/*.tmpl
%dir %{_datadir}/%{name}/templates/ja
%config(noreplace) %{_datadir}/%{name}/templates/ja/*.tmpl

%{_datadir}/locale/*/*.po

%{_datadir}/%{name}/drv
%{_datadir}/%{name}/examples
%dir %{_datadir}/%{name}/mime
%config(noreplace) %{_datadir}/%{name}/mime/mime.types*
%config(noreplace) %{_datadir}/%{name}/mime/mime.convs*
%dir %{_datadir}/%{name}/ppdc
%{_datadir}/%{name}/ppdc/*.defs
%{_datadir}/%{name}/ppdc/*.h
%dir %{_datadir}/%{name}/profiles

/usr/linux/bin/cancel
/usr/linux/bin/cupstestdsc
/usr/linux/bin/cupstestppd
/usr/linux/bin/lp*
/usr/linux/bin/ppd*
/usr/linux/sbin/*


%files libs
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/linux/lib/*.a
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
%{_bindir}/ipptool
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
/usr/linux/bin/ipptool


%changelog
* Wed Mar 25 2015 Gerard Visiedo <gerard.visiedo@bull.net> - 1.6.4-2
- Initial port on Aix6.1

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
