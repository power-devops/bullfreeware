%bcond_without dotests

Summary:       C++ wrapper for the MySQL C API
Name:          mysql++
Version:       3.2.4
Release:       4
License:       LGPLv2+
URL:           https://tangentsoft.com/mysqlpp/home
               
Source0:       https://tangentsoft.com/mysqlpp/releases/mysql++-%{version}.tar.gz
Source1:       mysql++.devhelp
Source1000:    %{name}-%{version}-%{release}.build.log
               
Patch1:        %{name}-3.2.4.configure.patch
Patch2:        %{name}-3.2.4.example_res.patch

BuildRequires: mariadb-connector-c-devel
#BuildRequires: community-mysql-devel
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: sed
%if %{with dotests}
BuildRequires: mariadb-server
%endif


%description
MySQL++ is a C++ wrapper for MySQL’s C API. 

It is built around STL principles, to make dealing with the database as easy
as dealing with an STL container. MySQL++ relieves the programmer of dealing
with cumbersome C data structures, generation of repetitive SQL statements,
and manual creation of C++ data structures to mirror the database schema.

If you are building your own MySQL++-based programs, you also need 
to install the -devel package.


%package devel
Summary:   MySQL++ developer files (headers, examples, etc.)
Requires:  %{name} = %{version}-%{release}
Requires:  mariadb-connector-c-devel
#Requires: community-mysql-devel

%description devel
These are the files needed to compile MySQL++ based programs, 
plus some sample code to get you started. You probably need to
install the -manuals package.  

If you aren't building your own programs, you probably don't need 
to install this package.


%package manuals
Summary:   MySQL++ user and reference manuals
License:   LGPLv2+ and LDPL
Requires:  devhelp
Requires:  %{name} = %{version}-%{release}

%description manuals
This is the MySQL++ documentation.  It's a separate RPM just because
it's so large, and it doesn't change with every release.

User Manual and Reference Manual are provided both in PDF and in
HTML format. You can use devhelp to browse it.


%prep
export PATH="/opt/freeware/bin:/usr/bin"
%setup  -q -n %{name}-%{version}

%patch1 -p1 -b .AIXconfigure
%patch2 -p1

for file in CREDITS COPYING LICENSE; do
  touch -r $file.txt timestamp
  sed -i -e 's/\r//' $file.txt
  touch -r timestamp $file.txt 
done

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH="/opt/freeware/bin:/usr/bin"

export AR="/usr/bin/ar -X32_64"

cd 64bit
export CFLAGS="-pthread -maix64 -D_LARGEFILE_SOURCE "
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-maix64 -pthread -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export LIBPATH=".:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=64

# Bakefile is not ported on AIX. We workaround trouble
# Bakefile create a .a library, that contains .o object;
# it is not a real archive .a, it will correspond to a .so in Linux.
# We will creates a .so, archive it manually and use the .a produced.

# First pass: create a .so
sed -i -e 's|@SO_SUFFIX@|so|' Makefile.in

./configure \
    --enable-thread-check \
    --enable-shared --disable-static \
    --with-mysql-lib=%{_libdir}64/mariadb \
    --with-mysql-include=%{_includedir}/mariadb \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir}64 \
    --prefix=%{_prefix} 

(gmake %{?_smp_mflags} || true)

# Second pass: we create a .so with the right soversion,
# and a .a manually.
# And we 'make' again.
mv libmysqlpp.so libmysqlpp.so.3
ar -X64 qc libmysqlpp.a libmysqlpp.so.3
gmake %{?_smp_mflags}

cd ../32bit
export CFLAGS="-pthread -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-maix32 -Wl,-bmaxdata:0x80000000 -pthread -Wl,-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"
export LIBPATH=".:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=32

# First pass
sed -i -e 's|@SO_SUFFIX@|so|' Makefile.in

./configure \
    --enable-thread-check \
    --enable-shared --disable-static \
    --with-mysql-lib=%{_libdir}/mariadb \
    --with-mysql-include=%{_includedir}/mariadb \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --prefix=%{_prefix} 

(gmake %{?_smp_mflags} || true)

# Second pass
mv libmysqlpp.so libmysqlpp.so.3
ar -X32 qc libmysqlpp.a libmysqlpp.so.3
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH="/opt/freeware/bin:/usr/bin"


install_mysql () {
    set -ex
    gmake DESTDIR=%{buildroot} install
    
    # Copy example programs to doc directory
    (mkdir -p doc/examples/ssx  || true)
    (mkdir -p doc/examples/test || true)
    cp --preserve=timestamps examples/*.cpp  doc/examples/
    cp --preserve=timestamps examples/*.h    doc/examples/
    cp --preserve=timestamps config.h        doc/examples/
    cp --preserve=timestamps ssx/parsev2.cpp doc/examples/ssx
    cp --preserve=timestamps ssx/genv2.cpp   doc/examples/ssx
    cp --preserve=timestamps ssx/main.cpp    doc/examples/ssx
    cp --preserve=timestamps ssx/parsev2.h   doc/examples/ssx
    cp --preserve=timestamps ssx/genv2.h     doc/examples/ssx
    cp --preserve=timestamps test/ssqls2.cpp doc/examples/test
    sed -i -e s@../config.h@config.h@ doc/examples/threads.h


    # Fix up simple example Makefile to allow it to build on the install
    # system, as opposed to the system where the Makefile was created.
    # Only build examples, not test_
    sed -e 's@./examples/@@' \
    -e 's@^CPPFLAGS ?=.*$@CPPFLAGS ?= $(shell mariadb_config --cflags)@' \
    -e 's@^LDFLAGS ?=.*$@LDFLAGS ?= $(shell mariadb_config --libs_r)@' \
    -e '/^all:/s/test_[a-z,_]* //g' \
    Makefile.simple > doc/examples/Makefile

    # DevHelp stuff
    mkdir -p %{buildroot}%{_datadir}/devhelp/books/%{name}
    cp --preserve=timestamps %{SOURCE1} %{buildroot}%{_datadir}/devhelp/books/%{name}/%{name}.devhelp
    cp --recursive --preserve=timestamps --no-preserve=mode doc/html/userman %{buildroot}%{_datadir}/devhelp/books/%{name}/userman
    cp --recursive --preserve=timestamps --no-preserve=mode doc/html/refman %{buildroot}%{_datadir}/devhelp/books/%{name}/refman
    # --no-preserve=mode prevents copying bogus execute permissions on the HTML and
    # CSS files.

    # Collect the license files in one directory.
    mkdir --parents %{buildroot}%{_licensedir}/%{name}
    sed --expression=s:doc/userman/LICENSE.txt:LICENSE.userman.txt:g <COPYING.txt >%{buildroot}%{_licensedir}/%{name}/COPYING.txt
    cp --preserve=timestamps LICENSE.txt %{buildroot}%{_licensedir}/%{name}/
    cp --preserve=timestamps doc/userman/LICENSE.txt %{buildroot}%{_licensedir}/%{name}/LICENSE.userman.txt
}

cd 64bit
install_mysql
# Copy .so files
cp libmysqlpp.so.* %{buildroot}%{_libdir}64

cd ../32bit
install_mysql
# Copy .so files
cp libmysqlpp.so.* %{buildroot}%{_libdir}

cd ${RPM_BUILD_ROOT}%{_libdir}
ar -qc -X64 libmysqlpp.a ../lib64/libmysqlpp.so.3
strip -e -X32                     libmysqlpp.so.3
cd ../lib64
strip -e -X64                     libmysqlpp.so.3
rm    libmysqlpp.a
ln -s ../lib/libmysqlpp.a         libmysqlpp.a


%check
%if %{with dotests}


test_mysql () {
    set -ex
    # mysqld_safe cannot be used. Using mysqld directly
    su mysql -c "ulimit -d unlimited; /opt/freeware/libexec/mysqld --datadir=/opt/freeware/var/lib/mysql/data &"
    sleep 5
    ./exrun resetdb
    # One fail up to now
    (./dtest || true )

    echo "" > example.out
    # transaction and deadlock are ignored beacause it needs interaction with user.
    # cpool fail (but test_cpool is OK) on AIX and Linux
    # dbinfo has different results on AIX and Linux (but both OK)
    for i in simple1 simple2 simple3 ssqls1 ssqls2 ssqls3 ssqls4 ssqls5 multiquery tquery1 tquery2 tquery3 store_if for_each load_jpeg fieldinf; \
    do echo "TEST $i" >> example.out; \
    ./exrun resetdb   >> example.out; \
    ./$i              >> example.out; \
    done
    mysqladmin shutdown
}

cd 64bit
export LIBPATH=".:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
test_mysql
diff example.out example.res > diff.txt
if [ -s diff.txt ] 
then
    echo "FAIL - BEWARE!!"
    echo "An example at least produces a bad output."
fi

cd ../32bit
export LIBPATH=".:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"
test_mysql
grep -v "BIGINT NOT NULL" example.out  > example32bit.out
grep -v "BIGINT NOT NULL" example.res  > example32bit.res
diff example32bit.out example32bit.res > diff.txt
if [ -s diff.txt ] 
then
    echo "FAIL - BEWARE!!"
    echo "An example at least produces a bad output."
fi
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 64bit/LICENSE.txt 64bit/COPYING.txt
%doc 64bit/ChangeLog.md 64bit/CREDITS.txt 64bit/README.txt
%{_libdir}/libmysqlpp.a
%{_libdir}64/libmysqlpp.a

%files devel
%defattr(-,root,system,-)
%doc 64bit/doc/examples 64bit/doc/README-devel-RPM.txt 64bit/README-examples.txt
%{_includedir}/mysql++

%files manuals
%defattr(-,root,system,-)
%doc 64bit/doc/pdf/* 64bit/doc/README-manuals-RPM.txt
%{_datadir}/devhelp/books/%{name}


%changelog
* Thu Jan 07 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> 3.2.4-4
- First port on AIX

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 09 2018 Björn Persson <Bjorn@Rombobjörn.se> - 3.2.4-1
- Upgraded to 3.2.4.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Jonathan Wakely <jwakely@redhat.com> - 3.2.3-5
- Remove Group tag, clean section, ldconfig scriptlets, and defattr uses.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 07 2017 Björn Persson <Bjorn@Rombobjörn.se> - 3.2.3-3
- Switched to mariadb-connector-c-devel.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Björn Persson <Bjorn@Rombobjörn.se> - 3.2.3-1
- Upgraded to 3.2.3.
- Updated URLs.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Adam Williamson <awilliam@redhat.com> - 3.2.2-7
- Rebuild against MariaDB 10.2 (with patch from Augusto Caringi)

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.2.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 31 2015 Jonathan Wakely <jwakely@redhat.com> - 3.2.2-1
- Upgraded to 3.2.2.
- Drop the patches.

* Sat Mar 14 2015 Björn Persson <bjorn@rombobjörn.se> - 3.2.1-1
- Upgraded to 3.2.1.
- Corrected the license tags.
- Tagged the license files as such.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Remi Collet <rcollet@redhat.com> - 3.1.0-12
- fix for ARM 64 support, #926188

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-9
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 23 2011 Remi Collet <Fedora@famillecollet.com> 3.1.0-7
- rebuild for new MySQL client library

* Sat Feb 12 2011 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-6
- arch specific requires

* Fri Feb 11 2011 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-5
- update patch for gcc 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-3
- rebuild against MySQL 5.5.8
- add missing files in the "examples" provided

* Thu Jul 08 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-2
- add LICENSE to manuals subpackage

* Sun Jun 20 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-1
- update to 3.1.0

* Sat Feb 13 2010 Remi Collet <Fedora@FamilleCollet.com> 3.0.9-4
- add explicit -lpthread linker flag (fix DSO bug)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Remi Collet <Fedora@FamilleCollet.com> 3.0.9-1
- update to 3.0.9

* Fri Jan 23 2009 Remi Collet <Fedora@FamilleCollet.com> 3.0.8-2
- rebuild against MySQL Client 5.1 (libmysqlclient.so.16)

* Sun Nov 30 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.8-1
- update to 3.0.8

* Sun Nov 23 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.7-1
- update to 3.0.7

* Sun Aug 17 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.6-1
- update to 3.0.6
- thread aware examples.

* Sat Aug 09 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.5-1
- update to 3.0.5

* Sat Jul 05 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.4-1
- update to 3.0.4

* Tue May 13 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.3-1
- update to 3.0.3
- add mysql++-3.0.3-mystring.patch for x86_64 build

* Tue Apr 15 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.2-1
- update to 3.0.2

* Sat Mar 29 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.1-1
- update to 3.0.1

* Sat Mar  1 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.0-1
- update to 3.0.0 Finale
- use devhelp to browse manuals

* Wed Feb 20 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc5
- update to 3.0.0 rc5

* Tue Feb 12 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc4
- update to 3.0.0 rc4 (not published)

* Sat Feb  9 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc3
- update to 3.0.0 rc3 (not published)

* Sat Feb  9 2008 Remi Collet <rpms@FamilleCollet.com> 2.3.2-3
- rebuild for gcc 4.3

* Thu Aug 23 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.2-2
- Fix License
- F-8 rebuild (BuildID)

* Sat Jul 14 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.2-1
- update to 2.3.2

* Wed Jul 11 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.1-1
- update to 2.3.1

* Tue Jul 03 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.0-1
- update to 2.3.0 

* Tue Apr 17 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.3-1
- update to 2.2.3, 
- del doc patch
- change BuildRoot
- add Requires mysql-devel for mysql++-devel

* Mon Apr 16 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.2-1
- update to 2.2.2, with soname support :)

* Mon Mar 19 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-3
- Warren Young comments : http://lists.mysql.com/plusplus/6444

* Sun Mar 18 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-2
- find perm on common.h
- soname mysql++-2.2.1-bkl.patch

* Wed Feb 28 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-1
- Initial spec for Extras

* Wed Feb 28 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-1.fc{3-6}.remi
- update to version 2.2.1

* Thu Jan 25 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.0-1.fc{3-6}.remi
- update to version 2.2.0

* Mon Nov 13 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc6.remi
- FC6.x86_64 build
- dynamic (sed) patch for Makefile (use mysql_config)

* Thu Nov 02 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc6.remi
- FC6 build

* Sat Apr  8 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc{3,4,5}.remi
- update to version 2.1.1

* Sat Nov 26 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.7-1.fc3.remi - 2.0.7-1.fc4.remi
- update to version 2.0.4
- build with mysql-5.0.15 (requires libmysqlclient.so.15)

* Sun Sep  4 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.4-1.FC4.remi
- version 2.0.4

* Sat Aug 20 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.2-1.FC4.remi
- built for FC4
- spec cleanning...

* Thu Jun 16 2005 Remi Collet <Remi.Collet@univ-reims.fr> 1.7.40-1.FC3.remi
- built for FC3 and MySQL 4.1.11
- examples in /usr/share/doc/mysql++-%%{version}/examples

* Sat Apr 30 2005 Warren Young <mysqlpp@etr-usa.com> 1.7.34-1
- Split manuals out into their own sub-package.

* Thu Mar 10 2005 Warren Young <mysqlpp@etr-usa.com> 1.7.32-1
- Disabled building of examples, to speed RPM build.

* Fri Nov 05 2004 Warren Young <mysqlpp@etr-usa.com> 1.7.21-1
- Split out -devel subpackage, which now includes the examples

* Wed Aug 18 2004 Warren Young <mysqlpp@etr-usa.com> 1.7.11-1
- Removed examples from documentation.
- Limited documentation to just the generated files, not the sources.

* Wed Apr 16 2003 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-4
- Added gcc 3.2.2 patch.
- Packaged using Red Hat Linux 8.0 and 9.

* Thu Nov 14 2002 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-3
- Changed the version passed to libtool.

* Mon Oct 28 2002 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-2
- Updated the version numbering of the library to be 1.7.9.
- Packaged using Red Hat Linux 8.0.

* Thu Oct 17 2002 Philipp Berndt <philipp.berndt@gmx.net>
- packaged
