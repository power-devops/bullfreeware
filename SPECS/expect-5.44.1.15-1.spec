Summary: A program-script interaction and testing utility
Name: expect
Version: 5.44.1.15
Release: 1
License: Public Domain
Group: Development/Languages
URL: http://expect.nist.gov/
Source0: http://expect.nist.gov/src/%{name}-%{version}.tar.bz2
# Patch0: fixes change log file permissions
Patch0: %{name}-5.43.0-log_file.patch
# Patch1: fixes install location, change pkgIndex
Patch1: %{name}-5.43.0-pkgpath.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

## BuildRequires: tcl-devel >= 8.5.8, tk-devel >= 8.5.8
Requires: tcl >= 8.5.8, tk >= 8.5.8

%description
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expect and some scripts that use it.


%package devel
Summary: A program-script interaction and testing utility
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel >= 8.5.8, tk-devel >= 8.5.8

%description devel
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains development files for the expect library.


%package -n expectk
Summary: A program-script interaction and testing utility
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl >= 8.5.8, tk >= 8.5.8

%description -n expectk
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expectk and some scripts that use it.


%prep
%setup -q
%patch0 -p1 -b .log_file
%patch1 -p1 -b .pkgpath


%build
export CFLAGS="$CFLAGS -I${RPM_BUILD_DIR}/tcl8.5.8/unix"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --with-tcl=%{_libdir} \
    --with-tk=%{_libdir} \
    --with-tclinclude=${RPM_BUILD_DIR}/tcl8.5.9 \
    --with-tkinclude=${RPM_BUILD_DIR}/tk8.5.9/generic \
    --with-x
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# we change libexpect inexpected location
mv  ${RPM_BUILD_ROOT}%{_libdir}/tcl8.5/*  ${RPM_BUILD_ROOT}%{_libdir}
rmdir ${RPM_BUILD_ROOT}%{_libdir}/tcl8.5

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# for linking with -lexpect
ln -s %{name}%{version}/libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libexpect.so

# remove cryptdir/decryptdir, as AIX has no crypt command
rm -f ${RPM_BUILD_ROOT}%{_bindir}/*cryptdir
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/*cryptdir.1

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done

# don't want to install over existing /usr/bin/mkpasswd
  rm usr/bin/mkpasswd
  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -sf ../../..%{_bindir}/mkpasswd .
  cd -
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc FAQ HISTORY NEWS README
%{_bindir}/autoexpect
%{_bindir}/autopasswd
%{_bindir}/dislocate
%{_bindir}/expect
%{_bindir}/ftp-rfc
%{_bindir}/kibitz
%{_bindir}/lpunlock
%{_bindir}/mkpasswd
%{_bindir}/passmass
%{_bindir}/rftp
%{_bindir}/rlogin-cwd
%{_bindir}/timed-read
%{_bindir}/timed-run
%{_bindir}/unbuffer
%{_bindir}/weather
%{_bindir}/xkibitz
%{_libdir}/lib*.so
%dir %{_libdir}/%{name}%{version}
%{_libdir}/%{name}%{version}/*
%{_mandir}/man1/autoexpect.1
%{_mandir}/man1/dislocate.1
%{_mandir}/man1/expect.1
%{_mandir}/man1/kibitz.1
%{_mandir}/man1/mkpasswd.1
%{_mandir}/man1/passmass.1
%{_mandir}/man1/tknewsbiff.1
%{_mandir}/man1/unbuffer.1
%{_mandir}/man1/xkibitz.1
/usr/bin/autoexpect
/usr/bin/autopasswd
/usr/bin/dislocate
/usr/bin/expect
/usr/bin/ftp-rfc
/usr/bin/kibitz
/usr/bin/lpunlock
/usr/bin/passmass
/usr/bin/rftp
/usr/bin/rlogin-cwd
/usr/bin/timed-read
/usr/bin/timed-run
/usr/bin/unbuffer
/usr/bin/weather
/usr/bin/xkibitz
/usr/linux/bin/mkpasswd
/usr/lib/lib*.so


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_mandir}/man3/libexpect.3*
/usr/include/*


%files -n expectk
%defattr(-,root,system,-)
%{_bindir}/expectk
%{_bindir}/multixterm
%{_bindir}/tknewsbiff
%{_bindir}/tkpasswd
%{_bindir}/xpstat
%{_mandir}/man1/expectk.1
%{_mandir}/man1/multixterm.1
%{_mandir}/man1/tknewsbiff.1
/usr/bin/expectk
/usr/bin/multixterm
/usr/bin/tknewsbiff
/usr/bin/tkpasswd
/usr/bin/xpstat


%changelog
* Thu Jun 09 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 5.44.1.15-1
- Port on Aix5.3 
