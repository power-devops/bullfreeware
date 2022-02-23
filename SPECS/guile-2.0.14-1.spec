# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests
%define _libdir64 %{_prefix}/lib64

%define GuileVersion    2.0
%define ReadLineVersion  18

Summary: A GNU implementation of Scheme for application extensibility
Name: guile
Version: 2.0.14
Release: 1
URL: http://www.gnu.org/software/guile/
Source0: ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz

# Patch1: %{name}-1.8.8-libtool-64bits.patch
Patch2: %{name}-2.0.11-gch.patch
Patch3: %{name}-2.0.11-read.patch
Patch4: %{name}-2.0.11-socket.patch
Patch5: %{name}-2.0.14-lib-intprops.h-fix-builtins-macros.patch

Source1000: %{name}-%{version}-%{release}.build.log

# Compatibility with version 1.8
Source101: lib%{name}.so.17-aix32
Source102: lib%{name}.so.17-aix64
Source103: lib%{name}readline-v-17.so.17-aix32
Source104: lib%{name}readline-v-17.so.17-aix64
Source105: %{name}-1.8-compatibility.tar.gz

License: GPLv2+ and LGPLv2+ and GFDL and OFSFDL
Group: Development/Languages

BuildRequires: gcc libtool libtool-ltdl-devel
BuildRequires: make
BuildRequires: libunistring-devel >= 0.9.10
BuildRequires: libffi-devel >= 3.2.1-3
BuildRequires: gc-devel >= 8.0.4
BuildRequires: gettext-devel >= 0.20.1
BuildRequires: gmp-devel >= 6.2.0
BuildRequires: readline-devel >= 7.0
# AIX awk is unable to generate some docs in user mode
BuildRequires: gawk

Requires: info, /sbin/install-info
Requires: coreutils

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the guile package if you'd like to add extensibility to programs
that you are developing.

%package devel
Summary: Libraries and header files for the GUILE extensibility library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel >= 4.3.2-2
Requires: pkg-config
Requires: readline-devel >= 5.2-3
Requires: gc-devel

%description devel
The guile-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the guile-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to
install the guile package.


%prep
%setup -q

# %patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

build_guile(){
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-shared --disable-static \
	--disable-error-on-warning

    gmake -j8

}

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export CFLAGS="-O2"

build_guile %{_libdir64}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc -maix32"
export CFLAGS="-O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_guile %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)
cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 32bit binaries' name and make default link towards 64bit
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _32 -e _64)
    do
	mv ${f} ${f}_32
	ln -sf ${f}_64 ${f}
    done
)

cd ..

# Ensure guile-tools_X points to the correct guild
(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    ln -sf guild_32 guile-tools_32
    ln -sf guild_64 guile-tools_64
)

mkdir -p $RPM_BUILD_ROOT%{_datadir}/guile/site/%{GuileVersion}

# Create symlinks for compatibility
ln -s guile $RPM_BUILD_ROOT%{_bindir}/guile2
ln -s %{_mandir}/man1/guile.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/guile2.1.gz
ln -s guile-tools $RPM_BUILD_ROOT%{_bindir}/guile2-tools

# Adjust mtimes so they are all identical on all architectures.
# When guile.x86_64 and guile.i686 are installed at the same time on an x86_64 system,
# the *.scm files' timestamps change, as they normally reside in /usr/share/guile/.
# Their corresponding compiled *.go file go to /usr/lib64/, or /usr/lib/, depending on the arch.
# The mismatch in timestamps between *.scm and *.go files makes guile to compile itself
# everytime it's run. The following code adjusts the files so that their timestamps are the same
# for every file, but unique between builds.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1208760.
find $RPM_BUILD_ROOT%{_datadir} -name '*.scm' -exec touch -r "%{_specdir}/guile-%{version}-%{release}.spec" '{}' \;
find $RPM_BUILD_ROOT%{_libdir} -name '*.go' -exec touch -r "%{_specdir}/guile-%{version}-%{release}.spec" '{}' \;

# For: guile guile_32 guile_64 . Others are shell scripts
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x libguile-%{GuileVersion}.a
    ${AR} -x libguilereadline-v-%{ReadLineVersion}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q libguile-%{GuileVersion}.a ${RPM_BUILD_ROOT}%{_libdir64}/libguile-%{GuileVersion}.so.22
    ${AR} -q libguilereadline-v-%{ReadLineVersion}.a ${RPM_BUILD_ROOT}%{_libdir64}/libguilereadline-v-%{ReadLineVersion}.so.%{ReadLineVersion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libguile-%{GuileVersion}.so.22
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libguilereadline-v-%{ReadLineVersion}.so.%{ReadLineVersion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm libguile-%{GuileVersion}.a
    ln -sf ../lib/libguile-%{GuileVersion}.a libguile-%{GuileVersion}.a
    rm libguilereadline-v-%{ReadLineVersion}.a
    ln -sf ../lib/libguilereadline-v-%{ReadLineVersion}.a libguilereadline-v-%{ReadLineVersion}.a
)

# Add a symlink for libguile.a 32bit & 64bit and for libguile-%{GuileVersion}.a 64bit
(
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -sf lib%{name}-%{GuileVersion}.a lib%{name}.a

    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf lib%{name}-%{GuileVersion}.a lib%{name}.a
)


# Add previous version to current version of: libguile-*.a
cp %{SOURCE101}                                                                           lib%{name}.so.17
strip       -X32 -e                                                                       lib%{name}.so.17
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-%{GuileVersion}.a              lib%{name}.so.17
cp %{SOURCE102}                                                                           lib%{name}.so.17
strip       -X64 -e                                                                       lib%{name}.so.17
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-%{GuileVersion}.a              lib%{name}.so.17

# Add previous version to current version of: libguilereadline-v-*.a
cp %{SOURCE103}                                                                           lib%{name}readline-v-17.so.17
strip       -X32 -e                                                                       lib%{name}readline-v-17.so.17
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}readline-v-%{ReadLineVersion}.a lib%{name}readline-v-17.so.17
cp %{SOURCE104}                                                                           lib%{name}readline-v-17.so.17
strip       -X64 -e                                                                       lib%{name}readline-v-17.so.17
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}readline-v-%{ReadLineVersion}.a lib%{name}readline-v-17.so.17


rm   -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

# compress large documentation
bzip2 32bit/NEWS

(
    # Compatibility with version 1.8
    cd ${RPM_BUILD_ROOT}
    /opt/freeware/bin/tar zxf %{SOURCE105}
)


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


%post
for i in guile r5rs goops guile-tut ; do
    /sbin/install-info %{_infodir}/${i}.info.gz %{_infodir}/dir &> /dev/null
done
:


%preun
if [ "$1" = 0 ]; then
    for i in guile r5rs goops guile-tut ; do
        /sbin/install-info --delete %{_infodir}/${i}.info.gz \
            %{_infodir}/dir &> /dev/null
    done
fi
:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING* 32bit/ChangeLog 32bit/HACKING 32bit/NEWS.bz2
%doc 32bit/README 32bit/THANKS
%{_bindir}/guile2
%{_bindir}/guile2-tools
%{_bindir}/guild
%{_bindir}/guild_32
%{_bindir}/guild_64
%{_bindir}/guile
%{_bindir}/guile_32
%{_bindir}/guile_64
%{_bindir}/guile-tools
%{_bindir}/guile-tools_32
%{_bindir}/guile-tools_64
%{_libdir}/*.a
%{_libdir}/guile
%{_libdir64}/*.a
%{_libdir64}/guile
%dir %{_datadir}/guile
%dir %{_datadir}/guile/%{GuileVersion}
%{_datadir}/guile/%{GuileVersion}/ice-9
%{_datadir}/guile/%{GuileVersion}/language
%{_datadir}/guile/%{GuileVersion}/oop
%{_datadir}/guile/%{GuileVersion}/rnrs
%{_datadir}/guile/%{GuileVersion}/scripts
%{_datadir}/guile/%{GuileVersion}/srfi
%{_datadir}/guile/%{GuileVersion}/sxml
%{_datadir}/guile/%{GuileVersion}/system
%{_datadir}/guile/%{GuileVersion}/texinfo
%{_datadir}/guile/%{GuileVersion}/web
%{_datadir}/guile/%{GuileVersion}/guile-procedures.txt
%{_datadir}/guile/%{GuileVersion}/*.scm
%dir %{_datadir}/guile/site
%dir %{_datadir}/guile/site/%{GuileVersion}
%{_infodir}/*

%files devel
%defattr(-,root,system,-)
%{_bindir}/guile-config*
%{_bindir}/guile-snarf*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_datadir}/aclocal/*


%changelog
* Thu May 27 2021 Tony Reix <tony.reix@bull.net> - 2.0.14-1

* Fri Sep 23 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-7
- Add Requires: gc-devel for guile-devel

* Thu Sep 15 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-6
- Add TOUCHing the .go files

* Thu Sep 15 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-5
- Fix guile start issue: add ccache in %files

* Wed Sep 14 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-4
- Fix missing dires (rnrs sxml ...)

* Wed Sep 07 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-3
- Add /opt/freeware/share/guile/1.8 directory for compatibility with previous version
- Use new dotests
- Manage guile binary as _32 & _64
- Fix missing symlink from lib64/libguile.a to lib/libguile.a

* Tue May 17 2016 Tony Reix <tony.reix@bull.net> - 2.0.11-1
- First version for AIX V6.1

* Tue May 17 2016 Tony Reix <tony.reix@bull.net> - 1.8.8-1
- First version for AIX V6.1

* Wed Sep 12 2012 Michael Perzl <michael@perzl.org> - 1.8.8-1
- first version for AIX V5.1 and higher
