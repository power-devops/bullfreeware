# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

%define		_libdir64 %{_prefix}/lib64

Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 6.8
Release: 2
License: GPL
Group: Applications/Publishing
URL: http://www.gnu.org/software/texinfo
Source0: http://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
#Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz.sig

Source1000:	%{name}-%{version}-%{release}.build.log

# For texindex
BuildRequires: gawk
Requires: gawk

BuildRequires: gettext-devel >= 0.21
Requires: gettext >= 0.21

BuildRequires: perl(perl)
BuildRequires: perl(Encode)
BuildRequires: perl(Data::Dumper)

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation.
Group: System Environment/Base

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

You should install info, because GNUs texinfo documentation is a
valuable source of information about the software on your system.

%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS="-O2"

%if %{with gcc_compiler}
export __CC="gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export CC_="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"
%endif

build_texinfo () {
	./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--libdir=$1 \
		--disable-rpath \

	gmake %{?_smp_mflags}
}

# first build the 64-bit version
cd 64bit

# Building binaries in 64bit mode
export CC="$__CC $FLAG64"
export OBJECT_MODE=64
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
# Export Perl to force 64bit version. Absolute path is mandatory.
export PERL="/opt/freeware/bin/perl_64"

build_texinfo %{_libdir64}

#Now build the 32-bit version
cd ../32bit

# Building binaries in 32bit mode
export OBJECT_MODE=32
export CC="$__CC $FLAG32"
export CFLAGS="-D_LARGE_FILES"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
# Export Perl to force 32bit version. Absolute path is mandatory.
export PERL="/opt/freeware/bin/perl_32"

build_texinfo %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/sbin

# install 64-bit version
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 64bit binaries' name
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)

# install 32-bit version
cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 32bit binaries' name and make default link towards 64bit
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in $(ls | grep -v -e _32 -e _64)
	do
		mv ${f} ${f}_32
		ln -sf ${f}_64 ${f}
	done
)

# makeinfo is a link towards texi2any. Therefore, makeinfo_32 will still
# point to texi2any which points to texi2any_64.
# Therefore, force makeinfo_32 and makeinfo_64 towards texi2any_32 and texi2any_64.
(
	cd ${RPM_BUILD_ROOT}%{_bindir}
	ln -sf texi2any_32 makeinfo_32
	ln -sf texi2any_64 makeinfo_64
)

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*info*

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
	cd ${RPM_BUILD_ROOT}
	mkdir -p sbin
	ln -sf ..%{_bindir}/install-info ./sbin
)

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# tp/tests/test_scripts tests might all fail because of incompatibility
# between perl and our en_US.UTF-8 locale. A warning is reaised triggering
# unwanted diffs.
# TODO: Fix it, probably in Perl though

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)



%post
/sbin/install-info %{_infodir}/%{name}.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/%{name}.gz %{_infodir}/dir || :
fi

%pre -n info
[ -s /usr/opt/freeware/bin/install-info ] && mv /usr/opt/freeware/bin/install-info /usr/opt/freeware/bin/install-info.rpmsave || :

%post -n info
/sbin/install-info %{_infodir}/info-stnd.info.gz %{_infodir}/dir || :
echo "Please check that /etc/info-dir does exist."
echo "You might have to rename it from /etc/info-dir.rpmsave to /etc/info-dir."

%preun -n info
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/info-stnd.info.gz %{_infodir}/dir || :
fi

%postun -n info
if [ $1 = 0 ]; then
    if [ -s /usr/opt/freeware/bin/install-info.rpmsave ] ; then
		mv -f /usr/opt/freeware/bin/install-info.rpmsave /usr/opt/freeware/bin/install-info || :
		#cp -p /usr/opt/freeware/bin/install-info /opt/freeware/bin/install-info
		ln -sf /usr/opt/freeware/bin/install-info /sbin/install-info
    fi
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/INSTALL 32bit/NEWS 32bit/README 32bit/TODO
#%doc info/README
%{_bindir}/makeinfo*
%{_bindir}/pdftexi2dvi*
%{_bindir}/pod2texi*
%{_bindir}/texi2any*
%{_bindir}/texi2dvi*
%{_bindir}/texi2pdf*
%{_bindir}/texindex*

%{_mandir}/man1/makeinfo.1
%{_mandir}/man1/pdftexi2dvi.1
%{_mandir}/man1/texi2dvi.1
%{_mandir}/man1/texi2pdf.1
%{_mandir}/man1/texindex.1
%{_mandir}/man5/texinfo.5
%{_infodir}/texinfo*
%{_datadir}/%{name}

%files -n info
%defattr(-,root,system)
%doc 32bit/COPYING
%{_bindir}/info*
%{_bindir}/install-info*
%{_infodir}/info-stnd.info*
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
/sbin/install-info*

%changelog
* Fri Sep 10 2021 Clément Chigot <clement.chigot@atos.net> - 6.8-2
- Ensure libintl.a path is hardcoded to /opt/freeware/lib

* Wed Jul 21 2021 Clément Chigot <clement.chigot@atos.net> - 6.8-1
- Update to 6.8
- Add -D_LARGE_FILES in 32bit

* Wed Oct 28 2020 Clément Chigot <clement.chigot@atos.net> - 6.7-4
- Fix %pre when /usr/opt/freeware/bin/install-info doesn't exist

* Wed Oct 07 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 6.7-3
- Update to 6.7

* Thu Feb 20 2020 Clément Chigot <clement.chigot@atos.net> 6.7-2
- Fix makeinfo links

* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net> 6.7-1
- BullFreeware Compatibility Improvements
- Build with gcc
- Move tests to %check section
- Remove /usr links
- Fix configure for AIX shared libraries

* Mon Jul 29 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.0-2
- Fix issue with install-info inexplicitly deleted under /usr/opt/freeware/bin
- when deinstalling info package

* Mon Mar 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.0-1
- Update to version 5.0

* Tue Sep 20 2011 Patricia Cugny <patricia.cugny@bull.net> 4.13-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri May 6 2011 Patricia Cugny <patricia.cugny@bull.net> 4.13-2
- minor modif in spec file

* Wed Jun 2 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.13
- Update to version 4.13

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 4.6-1
- Update to version 4.6

* Tue Mar 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild with default compiler
- Rebuild without ncurses

* Fri Mar 02 2001 Marc Stephenson <marc@austin.ibm.com>
- Add desktop entry
- Fix INFODIR search path

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions

* Wed Jan 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move info-stnd.info* to the info package, /sbin/install-info it
  in %post (Bug #6632)

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- recompile to eliminate ncurses foul-up.
* Tue Nov  9 1999 Bernhard Rosenkr�nzer <bero@redhat.com>
- 4.0
- handle RPM_OPT_FLAGS

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- import version 3.12h into 6.1 tree from HJLu

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Erik Troan <ewt@redhat.com>
- hacked to use zlib to get rid of the requirement on gzip

* Wed Mar 17 1999 Matt Wilson <msw@redhat.com>
- install-info prerequires gzip

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- version 3.12f
- make /usr/info/dir to be a %config(noreplace)
* Wed Nov 25 1998 Jeff Johnson <jbj@redhat.com>
- rebuild to fix docdir perms.

* Thu Sep 24 1998 Cristian Gafton <gafton@redhat.com>
- fix allocation problems in install-info

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- /sbin/install-info should not depend on /usr/lib/libz.so.1 -- statically
  link with /usr/lib/libz.a.

* Fri Aug 07 1998 Erik Troan <ewt@redhat.com>
- added a prereq of bash to the info package -- see the comment for a
  description of why that was done

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add %attr to permit non-root build.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean
- manhattan build

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 3.12
- added buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- moved /usr/info/dir to /etc/info-dir and made /usr/info/dir a
  symlink to /etc/info-dir.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry for info

* Wed Oct 01 1997 Donnie Barnes <djb@redhat.com>
- stripped /sbin/install-info

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added info-dir to filelist

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added patch from sopwith to let install-info understand gzip'ed info files
- use skeletal dir file from texinfo tarball (w/ bash entry to reduce
  dependency chain) instead (and install-info command everywhere else)
- patches install-info to handle .gz names correctly

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- patched install-info.c for glibc.
- added /usr/bin/install-info to the filelist

* Tue Feb 18 1997 Michael Fulbright <msf@redhat.com>
- upgraded to version 3.9.

