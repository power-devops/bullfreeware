# rpm -ba --define 'dotests 0' guile-*.spec
%{!?dotests: %define dotests 1}

%define _libdir64 %{_prefix}/lib64

%define GuileVersion    2.0
%define ReadLineVersion  18

Summary: A GNU implementation of Scheme for application extensibility
Name: guile
Version: 2.0.11
Release: 7
URL: http://www.gnu.org/software/guile/
Source0: ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz.sig

Source2: %{name}-1.8.8-libtool-64bits.patch
Source3: %{name}-2.0.11-gch.patch
Source4: %{name}-2.0.11-read.patch
Source5: %{name}-2.0.11-socket.patch

# File %{name}-%{version}-%{release}.build.log will record the output generated when building the RPMs
# It must be built by means of:
# /usr/bin/rpm -ba guile-2.0.11-1.spec 2>&1 | tee $SOURCES/guile-2.0.11-1.build.log
Source6: %{name}-%{version}-%{release}.build.log

# Compatibility with version 1.8
Source101: lib%{name}.so.17-aix32
Source102: lib%{name}.so.17-aix64
Source103: lib%{name}readline-v-17.so.17-aix32
Source104: lib%{name}readline-v-17.so.17-aix64
Source105: %{name}-1.8-compatibility.tar.gz

# Et :
#	/opt/freeware/lib/libguile-srfi-srfi-1-v-3.so.3
#	/opt/freeware/lib/libguile-srfi-srfi-13-14-v-3.so.3
#	/opt/freeware/lib/libguile-srfi-srfi-4-v-3.so.3
#	/opt/freeware/lib/libguile-srfi-srfi-60-v-2.so.2
# ??


License: GPLv2+ and LGPLv2+ and GFDL and OFSFDL
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: coreutils
BuildRequires: gettext
BuildRequires: gmp-devel >= 4.3.2-2
BuildRequires: readline-devel >= 5.2-3

Requires: info, /sbin/install-info
Requires: coreutils
Requires: gettext
Requires: gmp-devel >= 4.3.2-2
Requires: readline-devel >= 5.2-3
Requires: gc

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the guile package if you'd like to add extensibility to programs
that you are developing.

Guile is available as 32-bit and 64-bit.


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

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q

patch -p1 < %{SOURCE3}
patch -p1 < %{SOURCE4}
patch -p1 < %{SOURCE5}

rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export CC="xlc_r"

export CFLAGS__=" -g -O0"
export CFLAGS__=" -O2"


cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CFLAGS="-q64 $CFLAGS__"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-error-on-warning

# Put /opt/freeware/lib64 BEFORE /opt/freeware/lib
# That adds shit
#patch -p0 < %{SOURCE2}

gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

cd ..


cd 32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CFLAGS="-q32 $CFLAGS__"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-error-on-warning

gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in guile ; do
    mv -f  ${f} ${f}_64
  done
)
cd ..

# Save the 64bit version of .go files. But don't know how to use them then with guile_64
# /var/opt/freeware/tmp/guile-2.0.11-3-root//opt/freeware/share
mv ${RPM_BUILD_ROOT}/%{_datadir} ${RPM_BUILD_ROOT}/%{_datadir}_64


cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in guile ; do
    mv -f  ${f} ${f}_32
  done
)


# .go files must be newer than .scm files.
# Otherwise, once guile package is installed, guile command tries to rebuild them.
# There was an issue with 64bit .go files mainly.
date
  touch ${RPM_BUILD_ROOT}%{_datadir   }/%{name}/%{GuileVersion}/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir   }/%{name}/%{GuileVersion}/*/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir   }/%{name}/%{GuileVersion}/*/*/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir   }/%{name}/%{GuileVersion}/*/*/*/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir}_64/%{name}/%{GuileVersion}/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir}_64/%{name}/%{GuileVersion}/*/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir}_64/%{name}/%{GuileVersion}/*/*/*.scm
  touch ${RPM_BUILD_ROOT}%{_datadir}_64/%{name}/%{GuileVersion}/*/*/*/*.scm
# In order to not have .scÃm and .go files in the same second.
sleep 2
date
  touch ${RPM_BUILD_ROOT}%{_libdir  }/%{name}/%{GuileVersion}/ccache/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir  }/%{name}/%{GuileVersion}/ccache/*/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir  }/%{name}/%{GuileVersion}/ccache/*/*/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir  }/%{name}/%{GuileVersion}/ccache/*/*/*/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/%{GuileVersion}/ccache/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/%{GuileVersion}/ccache/*/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/%{GuileVersion}/ccache/*/*/*.go
  touch ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/%{GuileVersion}/ccache/*/*/*/*.go
date


# Make the 32bit version of guile be the default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in guile ; do
    ln -sf ${f}_32 ${f}
  done
)


# For: guile guile_32 guile_64 . Others are shell scripts
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done
  ls -l

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
  ls -l
)

rm   -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

# compress large documentation
bzip2 NEWS


# /opt/freeware/lib/guile/2.0/ccache/srfi
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-1.go
# ...
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-4
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-4.go
# ...
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-9
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-9.go
# /opt/freeware/lib/guile/2.0/ccache/srfi/srfi-98.go
# /opt/freeware/lib64/guile/2.0/ccache/srfi
# /opt/freeware/lib64/guile/2.0/ccache/srfi/srfi-1.go
# /opt/freeware/lib64/guile/2.0/ccache/srfi/srfi-10.go
# ...

# # find /var/opt/freeware/tmp/guile-2.0.11-1-root -name "*\.so*"
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib/libguile-2.0.so.22
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib/libguilereadline-v-18.so.18
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib64/libguile-2.0.so.22
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib64/libguilereadline-v-18.so.18
# # find /var/opt/freeware/tmp/guile-2.0.11-1-root -name "*\.a"
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib/libguile-2.0.a
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib/libguilereadline-v-18.a
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib64/libguile-2.0.a
# /var/opt/freeware/tmp/guile-2.0.11-1-root/opt/freeware/lib64/libguilereadline-v-18.a


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
# ???? for i in "" -srfi-srfi-1-v-3 -srfi-srfi-13-14-v-3 -srfi-srfi-4-v-3 -srfi-srfi-60-v-2 readline-v-17
#for i in "" -srfi-srfi-1-v-3 -srfi-srfi-13-14-v-3 -srfi-srfi-4-v-3 -srfi-srfi-60-v-2 readline-v-17
#  /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}${i}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}${i}.so*

for i in -%{GuileVersion} readline-v-%{ReadLineVersion}
do
  /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}${i}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}${i}.so*
done

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


# Add a symlinc for libguile.a 32bit & 64bit and for libguile-%{GuileVersion}.a 64bit
cd ${RPM_BUILD_ROOT}%{_libdir}
ln -sf %{_libdir}/lib%{name}-%{GuileVersion}.a lib%{name}.a

cd ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf %{_libdir}/lib%{name}-%{GuileVersion}.a lib%{name}-%{GuileVersion}.a
ln -sf %{_libdir}/lib%{name}.a                 lib%{name}.a


# Create symlinks for compatibility
cd ${RPM_BUILD_ROOT}%{_bindir}
ln -sf guile       guile2
ln -sf guile-tools guile2-tools


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


# /var/opt/freeware/tmp/guile-2.0.11-3-root//opt/freeware/share/guile/
# /var/opt/freeware/tmp/guile-2.0.11-3-root//opt/freeware/share/guile/2.0

( ls -l ${RPM_BUILD_ROOT}/%{_datadir}/%{name}                 || true )
( ls -l ${RPM_BUILD_ROOT}/%{_datadir}/%{name}/%{GuileVersion} || true )


# Compatibility with version 1.8
cd ${RPM_BUILD_ROOT}
/opt/freeware/bin/tar zxf %{SOURCE105}


( ls -l ${RPM_BUILD_ROOT}%{_datadir}/%{name}/1.8 || true )


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
%{_bindir}/guile
%{_bindir}/guile_64
%{_bindir}/guile_32
%{_bindir}/guile-tools
%{_libdir}/*.a
%{_libdir}/*.so*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{GuileVersion}
%{_datadir}/%{name}/%{GuileVersion}/ice-9
%{_datadir}/%{name}/%{GuileVersion}/language
%{_datadir}/%{name}/%{GuileVersion}/oop
%{_datadir}/%{name}/%{GuileVersion}/rnrs
%{_datadir}/%{name}/%{GuileVersion}/scripts
%{_datadir}/%{name}/%{GuileVersion}/srfi
%{_datadir}/%{name}/%{GuileVersion}/sxml
%{_datadir}/%{name}/%{GuileVersion}/system
%{_datadir}/%{name}/%{GuileVersion}/texinfo
%{_datadir}/%{name}/%{GuileVersion}/web
%{_datadir}/%{name}/%{GuileVersion}/guile-procedures.txt
%{_datadir}/%{name}/%{GuileVersion}/*.scm
%dir %{_datadir}_64/%{name}
%dir %{_datadir}_64/%{name}/%{GuileVersion}
%{_datadir}_64/%{name}/%{GuileVersion}/ice-9
%{_datadir}_64/%{name}/%{GuileVersion}/language
%{_datadir}_64/%{name}/%{GuileVersion}/oop
%{_datadir}_64/%{name}/%{GuileVersion}/rnrs
%{_datadir}_64/%{name}/%{GuileVersion}/scripts
%{_datadir}_64/%{name}/%{GuileVersion}/srfi
%{_datadir}_64/%{name}/%{GuileVersion}/sxml
%{_datadir}_64/%{name}/%{GuileVersion}/system
%{_datadir}_64/%{name}/%{GuileVersion}/texinfo
%{_datadir}_64/%{name}/%{GuileVersion}/web
%{_datadir}_64/%{name}/%{GuileVersion}/guile-procedures.txt
%{_datadir}_64/%{name}/%{GuileVersion}/*.scm
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{GuileVersion}
%dir %{_libdir}/%{name}/%{GuileVersion}/ccache
%{_libdir}/%{name}/%{GuileVersion}/ccache/ice-9
%{_libdir}/%{name}/%{GuileVersion}/ccache/language
%{_libdir}/%{name}/%{GuileVersion}/ccache/oop
%{_libdir}/%{name}/%{GuileVersion}/ccache/rnrs
%{_libdir}/%{name}/%{GuileVersion}/ccache/scripts
%{_libdir}/%{name}/%{GuileVersion}/ccache/srfi
%{_libdir}/%{name}/%{GuileVersion}/ccache/sxml
%{_libdir}/%{name}/%{GuileVersion}/ccache/system
%{_libdir}/%{name}/%{GuileVersion}/ccache/texinfo
%{_libdir}/%{name}/%{GuileVersion}/ccache/web
%{_libdir}/%{name}/%{GuileVersion}/ccache/*.go
%{_libdir64}/*.a
%{_libdir64}/*.so*
%dir %{_libdir64}/%{name}
%dir %{_libdir64}/%{name}/%{GuileVersion}
%dir %{_libdir64}/%{name}/%{GuileVersion}/ccache
%{_libdir64}/%{name}/%{GuileVersion}/ccache/ice-9
%{_libdir64}/%{name}/%{GuileVersion}/ccache/language
%{_libdir64}/%{name}/%{GuileVersion}/ccache/oop
%{_libdir64}/%{name}/%{GuileVersion}/ccache/rnrs
%{_libdir64}/%{name}/%{GuileVersion}/ccache/scripts
%{_libdir64}/%{name}/%{GuileVersion}/ccache/srfi
%{_libdir64}/%{name}/%{GuileVersion}/ccache/sxml
%{_libdir64}/%{name}/%{GuileVersion}/ccache/system
%{_libdir64}/%{name}/%{GuileVersion}/ccache/texinfo
%{_libdir64}/%{name}/%{GuileVersion}/ccache/web
%{_libdir64}/%{name}/%{GuileVersion}/ccache/*.go
%{_infodir}/*info*
%{_mandir}/man1/guile.1*
# New from FC24. Needs more actions
#%dir %{_datadir}/%{name}/site
#%dir %{_datadir}/%{name}/site/%{mver}
# AIX specific sym links
/usr/bin/guile2
/usr/bin/guile2-tools*
/usr/bin/guile
/usr/bin/guile_64
/usr/bin/guile_32
/usr/bin/guile-tools*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*a
/usr/lib64/*.so*
# Compatibility with version 1.8
%{_datadir}/%{name}/1.8


%files devel
%defattr(-,root,system,-)
%{_bindir}/guile-config*
%{_bindir}/guile-snarf*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_datadir}/aclocal/*
/usr/bin/guile-config*
/usr/bin/guile-snarf*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
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
