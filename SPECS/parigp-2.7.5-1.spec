Name:           pari
Version:        2.7.5
Release:        1
Summary:        Number Theory-oriented Computer Algebra System
Group:          System Environment/Libraries
# No version is specified
License:        GPL+
URL:            http://pari.math.u-bordeaux.fr/
Source0:        http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{version}.tar.gz
Source1:        gp.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Patch0:         pari-2.5.1-xdgopen.patch
Patch1:         pari-2.7.0-optflags.patch
Patch10:        pari-2.7.2-missing-field-init.patch
Patch11:        pari-2.7.0-declaration-not-prototype.patch
Patch12:        pari-2.7.1-clobbered.patch
Patch20:	pari-2.7.5-aixconf.patch

BuildRequires:  readline-devel
BuildRequires:  gmp-devel
#BuildRequires:  tex(tex)
#BuildRequires:  tex(dvips)
BuildRequires:  desktop-file-utils
BuildRequires:  libX11-devel
#BuildRequires:  xmkmf
# Test suite requirements
BuildRequires:  pari-elldata
BuildRequires:  pari-galdata
BuildRequires:  pari-galpol
BuildRequires:  pari-seadata

%define _libdir64 %{_prefix}/lib64

# Avoid doc-file dependencies and provides
%global __provides_exclude_from ^%{_datadir}/pari/PARI/
%global __requires_exclude_from ^%{_datadir}/pari/PARI/

%description
PARI is a widely used computer algebra system designed for fast computations in
number theory (factorizations, algebraic number theory, elliptic curves...),
but also contains a large number of other useful functions to compute with
mathematical entities such as matrices, polynomials, power series, algebraic
numbers, etc., and a lot of transcendental functions.

This package contains the shared libraries. The interactive
calculator PARI/GP is in package pari-gp.

%package devel
Summary:        Header files and libraries for PARI development
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header files and libraries for PARI development.

%package gp
Summary:        PARI calculator
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Requires:       bzip2
Requires:       gzip
Requires:       xdg-utils
Requires:       mimehandler(application/x-dvi)

%description gp
PARI/GP is an advanced programmable calculator, which computes
symbolically as long as possible, numerically where needed, and
contains a wealth of number-theoretic functions.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

# Use xdg-open rather than xdvi to display DVI files (#530565)
%patch0

# Use our optflags, not upstream's
%patch1
sed -i -e 's|@OPTFLAGS@|%{optflags} -Wall -Wextra -Wstrict-prototypes|' config/get_cc

# Fix compiler warnings
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1316
%patch10
%patch11
%patch12

# Fix AIX errors
%patch20 -p1 -b .aixconf

# Avoid unwanted rpaths
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export PATH=/opt/freeware/bin:$PATH

export CFLAGS="-O3"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib -Wl,-bmaxdata:0x80000000"
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --includedir=%{_includedir} \
    --with-gmp \
    --with-readline-include=/opt/freeware/include/readline  \
    --with-readline-lib=/opt/freeware/lib \
    --with-gmp-include=/opt/freeware/include \
    --with-gmp-lib=/opt/freeware/lib64/ 

gmake %{?_smp_mflags} gp

cd Oaix-ppc
gmake all

(gmake -k check || true)

echo ******************

cd ../../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc -maix32 "

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib -Wl,-bmaxdata:0x80000000"
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --includedir=%{_includedir} \
    --with-gmp \
    --with-readline-include=/opt/freeware/include/readline  \
    --with-readline-lib=/opt/freeware/lib \
    --with-gmp-include=/opt/freeware/include \
    --with-gmp-lib=/opt/freeware/lib/ 

gmake %{?_smp_mflags} gp

cd Oaix-ppc
gmake all

(gmake -k check || true)

cd ../..

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


export PATH=/opt/freeware/bin:$PATH

cd 64bit 
make install \
  DESTDIR=%{buildroot} \
  INSTALL="install -p" \
  STRIP=/bin/true

# We move pari.cfg to the docdir
rm -fr %{buildroot}%{_prefix}/lib/pari

# Site-wide gprc
mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 644 misc/gprc.dft %{buildroot}%{_sysconfdir}/gprc

# Desktop menu entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

# Don't bother installing the simple gp wrapper script, so avoiding the
# need to patch it to fix the path to the executable
find %{buildroot} -name xgp -exec rm '{}' ';'

# Placate rpmlint regarding binary and library permissions
%{_fixperms} %{buildroot}{%{_bindir},%{_libdir}}

#install libs
mkdir -p %{buildroot}%{_libdir64}
install -p -m 644 Oaix-ppc/libpari.so %{buildroot}%{_libdir64}
install -p -m 644 Oaix-ppc/libpari-gmp.so.4 %{buildroot}%{_libdir64}
install -p -m 644 Oaix-ppc/libpari-gmp.so.2.7.5 %{buildroot}%{_libdir64}

mv %{buildroot}%{_bindir}/gp-2.7 %{buildroot}%{_bindir}/gp-2.7_64 
cd %{buildroot}%{_bindir}
ln -s gp-2.7_64 gp_64 
cd -


cd ../32bit
make install \
  DESTDIR=%{buildroot} \
  INSTALL="install -p" \
  STRIP=/bin/true

# We move pari.cfg to the docdir
rm -fr %{buildroot}%{_prefix}/lib/pari

# Site-wide gprc
mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 644 misc/gprc.dft %{buildroot}%{_sysconfdir}/gprc

# Desktop menu entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

# Don't bother installing the simple gp wrapper script, so avoiding the
# need to patch it to fix the path to the executable
find %{buildroot} -name xgp -exec rm '{}' ';'

# Placate rpmlint regarding binary and library permissions
%{_fixperms} %{buildroot}{%{_bindir},%{_libdir}}

#install libs
install -p -m 644 Oaix-ppc/libpari.so %{buildroot}%{_libdir}
install -p -m 644 Oaix-ppc/libpari-gmp.so.4 %{buildroot}%{_libdir}
install -p -m 644 Oaix-ppc/libpari-gmp.so.2.7.5 %{buildroot}%{_libdir}

#/usr/bin/ar -cr libpari.a
#/usr/bin/ranlib libpari.a
#install -p -m 644 libpari.a %{buildroot}%{_libdir}
#/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpari.a  ../64bit/Oaix-ppc/libpari-gmp.so*
#/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpari.a  ../64bit/Oaix-ppc/libpari.so
#/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpari.a  Oaix-ppc/libpari-gmp.so*
#/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpari.a  Oaix-ppc/libpari.so


#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc 32bit/COPYING
%endif
%doc 32bit/AUTHORS 32bit/CHANGES* 32bit/COMPAT 32bit/NEW 32bit/README
%doc 32bit/Oaix-*/pari.cfg
%{_libdir64}/libpari.so
%{_libdir}/libpari.so
%{_libdir64}/libpari-gmp.so.%{version}
%{_libdir}/libpari-gmp.so.%{version}
%{_libdir64}/libpari-gmp.so.4
%{_libdir}/libpari-gmp.so.4

%files gp
%{_bindir}/gp
%{_bindir}/gp_64
%{_bindir}/gp-2.7
%{_bindir}/gp-2.7_64
%{_bindir}/gphelp
%{_bindir}/tex2mail
%config(noreplace) %{_sysconfdir}/gprc
%dir %{_datadir}/pari/
%doc %{_datadir}/pari/PARI/
%doc %{_datadir}/pari/doc/
%doc %{_datadir}/pari/examples/
%{_datadir}/pari/misc/
%{_datadir}/pari/pari.desc
%{_datadir}/applications/*gp.desktop
%{_mandir}/man1/gp-2.7.1*
%{_mandir}/man1/gp.1*
%{_mandir}/man1/gphelp.1*
%{_mandir}/man1/pari.1*
%{_mandir}/man1/tex2mail.1*

%files devel
%{_includedir}/pari/
%{_libdir}/libpari.so

%changelog
* Wed Mar 23 2016 Maximilien Faure <maximilien.faure@atos.net> - 2.7.5-2
- Rebuilt for AIX systems

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Paul Howarth <paul@city-fan.org> - 2.7.5-1
- Update to 2.7.5 (see CHANGES for details)

* Sat Jun 20 2015 Paul Howarth <paul@city-fan.org> - 2.7.4-1
- Update to 2.7.4 (see CHANGES for details)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 Paul Howarth <paul@city-fan.org> - 2.7.3-1
- Update to 2.7.3 (see CHANGES for details)

* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 2.7.2-1
- Update to 2.7.2 (see CHANGES for details)
- Update patches as needed
- Drop libpari-gmp.so.3 compat library
- Use %%license where possible

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-4
- Fix crash in ellmul with obsolete use of E=[a1,a2,a3,a4,a6]
  (#1104802, upstream bug #1589)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-2
- Temporarily include old version of library to avoid broken deps whilst
  migration to pari 2.7 happens in Rawhide

* Fri May 16 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-1
- Update to 2.7.1 (see CHANGES for details)

* Mon Mar 24 2014 Paul Howarth <paul@city-fan.org> - 2.7.0-1
- Update to 2.7.0 (see NEW for details)
- Update patches as needed
- BR: pari-galpol for additional test coverage

* Sat Sep 21 2013 Paul Howarth <paul@city-fan.org> - 2.5.5-1
- Update to 2.5.5 (see CHANGES for details)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.5.4-2
- Perl 5.18 rebuild

* Tue May 14 2013 Paul Howarth <paul@city-fan.org> - 2.5.4-1
- update to 2.5.4 (see CHANGES for details)
- update missing-field-init patch

* Wed May  1 2013 Jon Ciesla <limburgher@gmail.com> - 2.5.3-3
- drop desktop vendor tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct  4 2012 Paul Howarth <paul@city-fan.org> - 2.5.3-1
- update to 2.5.3 (see CHANGES for details)
- further compiler warning fixes after discussion with upstream
- drop upstreamed parts of declaration-not-prototype patch

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.5.2-1
- update to 2.5.2 (see CHANGES for details)
- drop upstreamed gcc 4.7, bug#1264 and FSF address patches

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Paul Howarth <paul@city-fan.org> - 2.5.1-1
- update to 2.5.1 (#821191; see NEW for details)
- use rpm 4.9.x requires/provides filtering
- update xdg-open patch
- drop emacs sub-package; the PARI Emacs shell is now a separate project
- drop %%defattr, redundant since rpm 4.4
- gp sub-package requires bzip2 for support of bzipped files
- make %%files list more explicit
- drop redundant buildroot definition and cleaning
- BR: xmkmf for X11 detection
- make sure we use our %%{optflags} and only those
- call pari_init_defaults() before gp_expand_path() (upstream #1264)
- fix scoping issue that manifests as a test suite failure with gcc 4.7.x and
  -ftree-dse (#821918, upstream #1314)
- fix desktop file categories
- install site-wide /etc/gprc
- update FSF address (upstream #1315)
- fix various compiler warnings (upstream #1316)
- run the full test suite in %%check
- add buildreqs for data packages needed by full test suite
- hardcode %%{_datadir} in gp.desktop so no need to fiddle with it in %%prep

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> - 2.3.5-4
- s/\$RPM_BUILD_ROOT/%%{buildroot}/g for tidyness
- update source URL as 2.3.5 is now an OLD version

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.3.5-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3.5-3.1
- rebuild with new gmp

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct  1 2010 Mark Chappell <tremble@fedoraproject.org> - 2.3.5-2
- switch the latex dependencies over to tex(...)

* Fri Jul  9 2010 Paul Howarth <paul@city-fan.org> - 2.3.5-1
- update to 2.3.5 (see CHANGES for details)
- filter out perl dependencies from %%{_datadir}/pari/PARI/

* Thu Jul  8 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-5
- various clean-ups to pacify rpmlint:
  - uses spaces instead of tabs consistently
  - mark %%{_datadir}/emacs/site-lisp/pari/pariemacs.txt as %%doc
  - mark %%{_datadir}/pari/{PARI,doc,examples} as %%doc
  - fix permissions of gp
- don't strip gp so we get debuginfo for it
- move here documents out to separate source files
- make gp subpackage require same version-release of main package

* Wed Jul  7 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-4
- apply patch from Patrice Dumas to use xdg-open rather than xdvi to display
  DVI content, and move the xdg-open requirement from the main package to the
  gp sub-package (#530565)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.4-1
- new release 2.3.4

* Wed Aug 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.3-2
- fix license tag

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.3-1
- new release 2.3.3

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-3
- corrected desktop file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.1-2
- Autorebuild for GCC 4.3

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-1
- new version 2.3.1

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-5
- added -fno-strict-aliasing to CFLAGS and enabled ppc build

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-4
- Rebuild for FE6

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-3
- Exclude ppc for now, since test fails

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-2
- added %%check section
- use gmp

* Thu May 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-1
- new version 2.3.0

* Fri May 19 2006 Orion Poplawski <orion@cora.nwra.com> - 2.1.7-4
- Fix shared library builds

* Fri Dec  2 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-3
- Use none for architecture to guarantee working 64bit builds

* Fri Oct 21 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-2
- some cleanup

* Fri Sep 30 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-1
- New Version 2.1.7

* Sun Mar  6 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.6-1
- New Version 2.1.6

* Mon Nov 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.2
- Fixed problem with readline

* Wed Nov 12 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.x
- First Fedora release
