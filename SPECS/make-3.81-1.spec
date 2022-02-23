Summary: A GNU tool which simplifies the build process for users.
Name: make
Version: 3.81
Release: 1
Copyright: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/make
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root

%define DEFCC cc

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about
how the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
%setup -q

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else 
       export CC=gcc
    fi
fi
LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
make

%install
rm -f $RPM_BUILD_ROOT%{_prefix}/info/make.info*

make prefix=$RPM_BUILD_ROOT%{_prefix} install

(
  cd $RPM_BUILD_ROOT/%{_prefix}
  rm -f ./info/dir
  gzip -9nf ./info/make.info*
  /usr/bin/strip ./bin/make
  ln -sf make ./bin/gmake

  cd $RPM_BUILD_ROOT
  mkdir -p usr/linux/bin
  ln -sf ../../..%{_prefix}/bin/make usr/linux/bin

  mkdir -p usr/bin
  ln -sf ../..%{_prefix}/bin/make usr/bin/gmake
) 

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /%{_prefix}/info/make.info.gz /%{_prefix}/info/dir --entry="* GNU make: (make).           The GNU make utility."

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete /%{_prefix}/info/make.info.gz /%{_prefix}/info/dir --entry="* GNU make: (make).           The GNU make utility."
fi

%files
%defattr(-,root,root)
%doc NEWS README
%{_prefix}/bin/make
%{_prefix}/bin/gmake
%{_prefix}/man/man1/make.1*
%{_prefix}/info/make.info*
/usr/linux/bin/make
/usr/bin/gmake

%changelog
* Wed Mar 30 2007 christophe.belle@bull.net
- Update to version 3.81

* Wed Oct 09 2002 David Clissold <cliss@austin.ibm.com>
- Update to version 3.80

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
