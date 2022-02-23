Summary: A graphics library for drawing image files in various formats.
Name: gd
Version: 1.8.4
Release: 3
Source0: http://www.boutell.com/gd/http/gd-%{version}.tar.gz
Source1: IBM_ILA
Source2: %{name}.txt
Patch0: gd-%{version}-aix.patch
License: IBM_ILA
URL: http://www.boutell.com/gd/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: freetype-devel, libjpeg-devel, libpng-devel, zlib-devel
Requires: libpng >= 1.0.8-6, freetype >= 1.3.1, libjpeg >= 6b, zlib >= 1.1.3
Prefix: %{_prefix}
%define shlibver %(echo %{version} | cut -f-2 -d.)
%define DEFCC xlc

# Use --define 'no64 1' on the command line to disable 64bit build
%{!?no64:%define BUILD64 1}
%{?no64:%define BUILD64 0}
%define prefix64 %{prefix}/64

%description
Gd is a graphics library for drawing image files in various formats. Gd
allows your code to quickly draw images (lines, arcs, text, multiple colors,
cutting and pasting from other images, flood fills) and write out the result
as a jpeg, png or wbmp file. Gd is particularly useful in web applications,
where jpeg, png or wbmp files are commonly used as inline images.  Note,
however, that gd is not a paint program.

Install gd if you are developing applications which need to draw jpeg, png
or wbmp files. If you install gd, you'll also need to install the gd-devel
package.

%package progs
Requires: gd = %{version}, perl
Summary: Utility programs that use libgd.
Group: Applications/Multimedia

%description progs
These are utility programs supplied with gd, the .jpeg graphics library.
If you install these, you must install gd.

%package devel
Requires: gd = %{version}
Summary: The development libraries and header files for gd.
Group: Development/Libraries

%description devel
These are the development header files for gd, the jpeg,
png or wbmp graphics library.

%prep
%setup -q
%patch0 -p1 -b .aix

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat $RPM_SOURCE_DIR/%{name}.txt >> LICENSE

%if %{BUILD64} == 1
######################################################
# Prep 64-bit build in 64bit subdirectory
######################################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gzip -dc %{SOURCE0} |tar -xf -
cd %{name}-%{version}
%patch0 -p1 -b .aix
%endif

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export OBJECT_MODE=32  #just to be sure

make

%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64
make

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
/usr/bin/ar -x libgd.a shr.o
cd ../..
/usr/bin/ar -q libgd.a 64bit/%{name}-%{version}/shr.o

%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib
mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{prefix}/include
make install \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INCLUDE=$RPM_BUILD_ROOT%{_includedir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir}

strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

( cd $RPM_BUILD_ROOT
  mkdir -p usr/bin
  cd usr/bin
  ln -sf ../..%{prefix}/bin/* .
  cd -

  mkdir -p usr/lib
  cd usr/lib
  ln -sf ../..%{prefix}/lib/* .
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc readme.txt index.html LICENSE
%{_libdir}/*.a
/usr/lib/*
%if %{BUILD64} == 1
%dir %{prefix64}
%dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif


%files progs
%defattr(-,root,root)
%doc LICENSE
%{_bindir}/*
/usr/bin/*

%files devel
%defattr(-,root,root)
%doc LICENSE
%{_includedir}/*

%changelog
* Mon Feb 16 2004 David Clissold <cliss@austin.ibm.com> 1.8.4-3
- Add 64-bit library member.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri May 11 2001 David Clissold <cliss@austin.ibm.com>
- First build for AIX.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- Updates the descriptions to get rid of al references to gif

* Tue Dec 12 2000 Philipp Knirsch <Philipp.Knirsch@redhat.de>
- Fixed bug #22001 where during installation the .so.1 and the so.1.8 links
  didn't get installed and therefore updates had problems.

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- define HAVE_LIBTTF to actually enable ttf support (oops, #18299)
- remove explicit dependencies on libpng, libjpeg, et. al.
- add BuildPrereq: freetype-devel

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add %%postun run of ldconfig (#14915)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to 1.8.4

* Sat Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com> 
- rebuild in new environment

* Mon May 22 2000 Nalin Dahyabhai <nalin@redhat.com> 
- break out a -progs subpackage
- disable freetype support

* Fri May 19 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to latest version (1.8.2)
- disable xpm support

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- buiuld for glibc 2.1

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- built for 5.2
