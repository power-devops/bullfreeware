# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


Summary: ODBC driver manager and drivers for PostgreSQL, MySQL, etc.
Name: unixODBC
Version: 2.3.7
Release: 2

# Added for managing the versioning of API. To be updated when changed.
# So that the lib*.a contain both .so and .so.%{APIrelease}
# See %install phase
%global APIrelease 2

License: LGPLv2+ and GPLv2+
Group: Applications/Databases
URL: http://www.unixodbc.org/

Source0: %{name}-%{version}.tar.gz
Source1: unixodbc_conf.h
Source2: odbcinst.ini
Source1000:	%{name}-%{version}-%{release}.build.log

# Old shared objects
Source4: unixODBC-libodbc-2.3.6.so-aix32
Source5: unixODBC-libodbc-2.3.6.so-aix64
Source6: unixODBC-libodbcinst-2.3.6.so-aix32
Source7: unixODBC-libodbcinst-2.3.6.so-aix64

BuildRequires: readline-devel >= 5.2
BuildRequires: automake >= 1.14
Requires: readline >= 5.2
Requires: libgcc >= 6.3.0
Requires: libtool-ltdl >= 2.4.6-4
Requires: libiconv >= 1.14-1


%define _libdir64 %{_prefix}/lib64

%description
unixODBC aims to provide a complete ODBC solution for the Unix platform.
All programs are GPL.
All libs are LGPL.


%package devel
Summary: Includes and static libraries for ODBC development
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.
All libs are LGPL.
This package contains the include files and static libraries
for development.

Starting from version 2.3.7-2, the names of the shared objects have been corrected.
The previous shared objects are kept to compatibility for the following packages:
- mariadb-connector-odbc <= 3.1.15-1 (requires "libodbcinst.a(libodbcinst.so.2.0.0)")
- openldap <= 2.4.48-1 (requires "libodbc.a(libodbc.so)")

Standalone shared object (".so" files) are also kept because of the following packages:
- apr-util-odbc <= 1.5.4-3 (requires "libodbc.so")
- freetds <= 0.92.79-1 (requires "libodbc.so" and "libobdcinst.so")
- php-odbc <= 7.2.9-1.ppc (requires "libodbc.so")

We recommand to update them as soon as a realease is available:



%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export RM="/usr/bin/rm -f"


export CFLAGS="-O2"
export CXXFLAGS="-O2"

build_unixODBC() {
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--infodir=%{_infodir} \
		--mandir=%{_mandir} \
		--disable-gui

	gmake %{?_smp_mflags} -j16
}


# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64

#export CC="/usr/vac/bin/xlc_r -q64"
#export CXX="/usr/vacpp/bin/xlC_r -q64"
export CC="gcc -maix64"
export CXX="g++ -maix64"

# export LDFLAGS="-Wl,-brtl -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"


build_unixODBC %{_libdir64}

# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32

#export CC="/usr/vac/bin/xlc_r -q32"
#export CXX="/usr/vacpp/bin/xlC_r -q32"
export CC="gcc -maix32"
export CXX="g++ -maix32"

# export LDFLAGS="-Wl,-brtl -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_unixODBC %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install-strip
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done
mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc64.h

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install-strip

#setting 64 bit as default
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
		mv $fic "$fic"_32
		ln -sf "$fic"_64 $fic
    done
)

mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc32.h

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}


(
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	for f in libodbc libodbccr libodbcinst; do
		# Extract .so from 64bit .a libraries and add them to the 32bit .a libraries.
		${AR} -x -X64 ${f}.a
		${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${f}.a ${f}.so.%{APIrelease}


		# Create links from /lib64 to /lib
		rm -f ${f}.a
		ln -sf ../lib/${f}.a ${f}.a

	done
)

# Remove .la files
(
	${RM} ${RPM_BUILD_ROOT}%{_libdir}/*.la
	${RM} ${RPM_BUILD_ROOT}%{_libdir64}/*.la

)


# # Add wrongly named shared objects for compatibility
# # TODO remove !
# cp %{SOURCE4}                                                libodbc.so
# /usr/bin/strip -X32 -e                                       libodbc.so
# ${AR}          -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libodbc.a libodbc.so
# cp %{SOURCE5}                                                libodbc.so
# /usr/bin/strip -X64 -e                                       libodbc.so
# ${AR}          -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libodbc.a libodbc.so
# cp %{SOURCE6}                                                     libodbcinst.so.2.0.0
# /usr/bin/strip -X32 -e                                            libodbcinst.so.2.0.0
# ${AR}          -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libodbcinst.a  libodbcinst.so.2.0.0
# cp %{SOURCE7}                                                     libodbcinst.so.2.0.0
# /usr/bin/strip -X64 -e                                            libodbcinst.so.2.0.0
# ${AR}          -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libodbcinst.a  libodbcinst.so.2.0.0
# 
# # Keep standalone shared objects for compatibility
# # TODO remove !
# (
# 	cd ${RPM_BUILD_ROOT}%{_libdir}
# 	${AR} -X32 -x libodbc.a libodbc.so.2
# 	ln -s libodbc.so.2 libodbc.so
# 	${AR} -X32 -x libodbcinst.a libodbcinst.so.2
# 	ln -s libodbcinst.so.2 libodbcinst.so
# 	cd ${RPM_BUILD_ROOT}%{_libdir64}
# 	${AR} -X64 -x libodbc.a libodbc.so.2
# 	ln -s libodbc.so.2 libodbc.so
# 	${AR} -X64 -x libodbcinst.a libodbcinst.so.2
# 	ln -s libodbcinst.so.2 libodbcinst.so
# )



%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# # No tests!
# cd 64bit
# (gmake -k check || true)
# 
# cd ../32bit
# (gmake -k check || true)


%pre
if [ -f %{sysconfdir}/odbc.ini ]; then
    mv -f %{sysconfdir}/odbc.ini %{sysconfdir}/odbc.ini.rpmpresave
fi
if [ -f %{sysconfdir}/odbcinst.ini ]; then
    mv -f %{sysconfdir}/odbcinst.ini %{sysconfdir}/odbcinst.ini.rpmpresave
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog 32bit/NEWS 32bit/README 32bit/README.AIX 32bit/doc
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/odbcinst*
%{_bindir}/isql*
%{_bindir}/dltest*
%{_bindir}/iusql*
%{_bindir}/odbc_config*
%{_bindir}/slencheck*

# Keep shared object for libodbc
%{_libdir}/libodbc.a
# %{_libdir}/libodbc.so*
%{_libdir64}/libodbc.a
# %{_libdir64}/libodbc.so*

# Keep shared object for libodbcinst
%{_libdir}/libodbcinst.a
# %{_libdir}/libodbcinst.so*
%{_libdir64}/libodbcinst.a
# %{_libdir64}/libodbcinst.so*

%{_libdir}/libodbccr.a
%{_libdir64}/libodbccr.a
%{_mandir}/man*/*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc


%changelog
* Wed Dec 11 2019 Clément Chigot <clement.chigot@atos.net> 2.3.7-2
- Remove -Wl,-brtl flags
- Remove BuildRoot
- Remove /usr links
- Add tests in %check
- Add pkgconfig directories in devel RPM
- Fix .so names
- Remove .so and .la files

* Fri Aug 02 2019 Tony Reix <tony.reix@atos.net> 2.3.6-3
- Fix .so in .a issue

* Wed Apr 25 2018 Tony Reix <tony.reix@atos.net> 2.3.6-2
- Add sed patch

* Wed Apr 25 2018 Tony Reix <tony.reix@atos.net> 2.3.6-1
- update to 2.3.6, initial port on AIX 6.1

* Mon Jun 11 2012 Patricia Cugny <patricia.cugny@bull.net> 2.3.1
- update to 2.3.1, initial port on AIX 6.1

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.3.0
- Initial port on Aix5.3
