##########################
#  User-modifiable configs
##########################
#  Build tkinter?
#WARNING: Commenting out doesn't work.  Last line is what's used.
%define config_tkinter no
%define config_tkinter yes

%define osplat aix5

#################################
#  End of user-modifiable configs
#################################
%define name python
%define version 2.5.2
%define BASE_VERSION 2.5
%define release 2

#  kludge to get around rpm <percent>define weirdness
%define include_tkinter %(if [ "%{config_tkinter}" = yes ]; then echo 1; else echo 0; fi)

Summary: An interpreted, interactive, object-oriented programming language.
Name: %{name}
Version: %{version}
Release: %{release}
License: Modified CNRI Open Source License
Group: Development/Languages
Source0: ftp://ftp.python.org/pub/python/%{version}/Python-%{version}.tgz
Source1: ftp://ftp.python.org/pub/python/doc/%{version}/html-%{version}.tar.bz2
Patch0: Python-%{version}-aixsetup.patch
Patch1: Python-%{version}-termios.patch
Patch2: Python-%{version}-pypath.patch
Patch3: Python-%{version}-tools.patch

URL: http://www.python.org
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildPrereq: expat-devel >= 1.95.2
BuildPrereq: gdbm-devel
BuildRequires: readline >= 4.2a , tcl , tk
Prefix: %{_prefix}

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
Python is an interpreted, interactive, object-oriented programming language.
It incorporates modules, exceptions, dynamic typing, very high level dynamic
data types, and classes.  Python combines remarkable power with very clear
syntax.  It has interfaces to many system calls and libraries, as well as to
various window systems, and is extensible in C or C++.  It is also usable as an
extension language for applications that need a programmable interface.
Finally, Python is portable: it runs on many brands of UNIX, on PCs under
Windows, MS-DOS, and OS/2, and on the Mac.

%package  devel
Summary: The libraries and header files needed for Python extension development.
Requires: python = %{PACKAGE_VERSION}
Group: Development/Libraries

%description devel
The Python programming language's interpreter can be extended with dynamically
loaded extensions and can be embedded in other programs.  This package contains
the header files and libraries needed to do these types of tasks.

Install python-devel if you want to develop Python extensions.  The python
package will also need to be installed.  You'll probably also want to install
the python-docs package, which contains Python documentation.

%package docs
Summary: Documentation for the Python programming language.
Group: Documentation
Conflicts: python < %{PACKAGE_VERSION}

%description docs
The python-docs package contains documentation on the Python programming
language and interpreter.  The documentation is provided in ASCII text files
and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation for the
Python language.

%if %{include_tkinter}
%package -n tkinter
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
Requires: python = %{PACKAGE_VERSION}

%description -n tkinter
The Tkinter (Tk interface) program is an graphical user interface for the
Python scripting language.

You should install the tkinter package if you'd like to use a graphical user
interface for Python programming.
%endif

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: python = %{PACKAGE_VERSION}

%description tools
The Python package includes several development tools that are used to build
python programs.  This package contains a selection of those tools, including
the IDLE Python IDE.

Install python-tools if you want to use these tools to develop Python programs.
You will also need to install the python and tkinter packages.

%prep
%setup -q -n Python-%{version}
#cp Modules/Setup.dist Modules/Setup
%patch0 -p1 -b .aixsetup
%patch1 -p1 -b .decl
%patch2 -p1
%patch3 -p1 -b .tools

# A couple of one-liner patches, on the fly.
perl -pi -e "s|/usr/lpp/xlC/include/load.h|/usr/vacpp/include/load.h|;" \
  Python/dynload_aix.c configure.in configure
perl -pi -e "s|yperr_string|(const char*)yperr_string|g;" \
  Modules/nismodule.c

%setup -q -D -T -a 1 -n Python-%{version} -q

%build
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
CC='/usr/vacpp/bin/xlc_r'
CXX='/usr/vacpp/bin/xlC_r'

export CPPFLAGS="-I/usr/include"
export LDFLAGS="-L. -L/opt/freeware/lib"
export CFLAGS="-O2"
CPPFLAGS="-I/usr/include" LDFLAGS="-L. -L/opt/freeware/lib" \
CFLAGS="-O2" ./configure --prefix=%{prefix} --with-gcc="xlc_r" --with-cxx="xlC_r" \
--disable-ipv6 AR="ar" --without-pymalloc 

make BINLIBDEST=%{_builddir}/Python-%{version}/Modules
make libpython%{BASE_VERSION}.so
mv libpython%{BASE_VERSION}.a libpython%{BASE_VERSION}-static.a
/usr/bin/ar -qv libpython%{BASE_VERSION}.a libpython%{BASE_VERSION}.so
rm python
LIBPATH=`pwd`:/usr/lib/threads:/usr/lib make LDFLAGS="$LDFLAGS -blibpath:%{prefix}/lib:/usr/lib/threads:/usr/lib"

%install
#  set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{prefix}/bin" >>setup.cfg

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
#LIBPATH=`pwd`:/usr/lib/threads:/usr/lib make prefix=$RPM_BUILD_ROOT%{prefix} install
LIBPATH=`pwd`:/usr/lib/threads:/usr/lib make install DESTDIR=$RPM_BUILD_ROOT

strip $RPM_BUILD_ROOT%{prefix}/bin/python || :

########
#  Tools
echo '#!/bin/ksh' >${RPM_BUILD_ROOT}%{_bindir}/idle
echo 'exec %{_prefix}/bin/python /usr/lib/python%{BASE_VERSION}/Tools/idle/idle.py' >>${RPM_BUILD_ROOT}%{_bindir}/idle
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/idle
cp -a Tools ${RPM_BUILD_ROOT}%{prefix}/lib/python%{BASE_VERSION}


#  MAKE FILE LISTS
rm -f mainpkg.files
find "$RPM_BUILD_ROOT""%{prefix}"/lib/python%{BASE_VERSION}/lib-dynload -type f |
	sed "s|^${RPM_BUILD_ROOT}|/|" |
	grep -v -e '_tkinter.so$' >mainpkg.files

find "$RPM_BUILD_ROOT""%{prefix}"/bin -type f |
	sed "s|^${RPM_BUILD_ROOT}|/|" |
	grep -v -e '/bin/idle$' >>mainpkg.files

rm -f tools.files
find "$RPM_BUILD_ROOT""%{prefix}"/lib/python%{BASE_VERSION}/Tools -type f |
	sed "s|^${RPM_BUILD_ROOT}|/|" >tools.files
echo "%{prefix}"/bin/idle >>tools.files

(cd $RPM_BUILD_ROOT
 for dir in bin lib include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
 mkdir -p usr/local/
 mkdir -p usr/local/bin
 cd usr/local/bin
 ln -sf ../../..%{_prefix}/bin/* .
 cd -
 rm usr/bin/idle usr/local/bin/idle
)

%clean
rm -fr $RPM_BUILD_ROOT
rm -f mainpkg.files tools.files

%files -f mainpkg.files
%defattr(-,root,system)
%doc LICENSE
%{prefix}/share/man/man1/python.1*

%dir %{prefix}/include/python%{BASE_VERSION}
%dir %{prefix}/lib/python%{BASE_VERSION}/
%{prefix}/lib/libpython%{BASE_VERSION}.a
%{prefix}/lib/python%{BASE_VERSION}/*.py*
%{prefix}/lib/python%{BASE_VERSION}/pdb.doc
%{prefix}/lib/python%{BASE_VERSION}/compiler
%{prefix}/lib/python%{BASE_VERSION}/curses
%{prefix}/lib/python%{BASE_VERSION}/distutils
%{prefix}/lib/python%{BASE_VERSION}/email
%{prefix}/lib/python%{BASE_VERSION}/encodings
%{prefix}/lib/python%{BASE_VERSION}/hotshot
%{prefix}/lib/python%{BASE_VERSION}/idlelib
%{prefix}/lib/python%{BASE_VERSION}/plat-%{osplat}
%{prefix}/lib/python%{BASE_VERSION}/site-packages
%{prefix}/lib/python%{BASE_VERSION}/xml
/usr/include/python%{BASE_VERSION}
/usr/lib/libpython%{BASE_VERSION}.a
/usr/lib/python%{BASE_VERSION}
/usr/local/bin/*
/usr/bin/*

#%{prefix}/bin/pydoc
#%{prefix}/bin/python
#%{prefix}/bin/python-config
#%{prefix}/bin/python%{BASE_VERSION}
#%{prefix}/bin/python%{BASE_VERSION}-config
#%{prefix}/bin/smtpd.py
#/usr/bin/pydoc
#/usr/bin/python
#/usr/bin/python-config
#/usr/bin/python%{BASE_VERSION}
#/usr/bin/python%{BASE_VERSION}-config
#/usr/bin/smtpd.py

%files devel
%defattr(-,root,system)
%{prefix}/include/python%{BASE_VERSION}/*.h
%{prefix}/lib/python%{BASE_VERSION}/config
%{prefix}/lib/python%{BASE_VERSION}/test

%files docs
%defattr(-,root,system)
%doc Misc/README Misc/cheatsheet Misc/Porting
%doc Misc/ACKS Misc/HISTORY Misc/NEWS

%if %{include_tkinter}
%files -n tkinter
%defattr(-,root,system)
%{prefix}/lib/python%{BASE_VERSION}/lib-tk
%{prefix}/lib/python%{BASE_VERSION}/lib-dynload/_tkinter.so*
%endif

%files -f tools.files tools
%defattr(-,root,system)

%changelog
* Wed Nov 28 2008 <jean-noel.cordenner@bull.net> 2.5.2-2
- Rebuild to fix an issue with python-tools.

* Wed Nov 5 2008 <jean-noel.cordenner@bull.net> 2.5.2
- Update to version 2.5.2.

* Thu Jul 13 2006 Reza Arbab <arbab@austin.ibm.com> 2.3.4-3
- Rebuild so tkinter can link to our latest libtk8.4.so.

* Mon Aug 08 2005 Philip K. Warren <pkw@us.ibm.com> 2.3.4-2
- Include patch for PSF-2005-001.
- Build with large files support.

* Thu Aug 05 2004 David Clissold <cliss@austin.ibm.com> 2.3.4-1
- Update to version 2.3.4.

* Wed Jul 28 2004 David Clissold <cliss@austin.ibm.com> 2.3.2-1
- Update to version 2.3.2. (but 2.3.4 is latest).

* Mon Feb 17 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM C++ compiler; --with-threads and --enable-shared
-  (as per tzy@us.ibm.com).  Also added BuildRequires.

* Fri Feb 15 2002 David Clissold <cliss@austin.ibm.com>
- Remove the old libpython2.1.a image.

* Thu Feb 14 2002 Marc Stephenson <marc@austin.ibm.com>
- Include compiler, email, and hotshot
- Move test to devel

* Sun Feb 10 2002 David Clissold <cliss@austin.ibm.com>
- Updated to version 2.2

* Tue Oct 09 2001 David Clissold <cliss@austin.ibm.com>
- Updated to version 2.1.1

* Wed Jun 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Adapted for AIX Toolbox

* Thu Jun 7 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1-5]
- Added entry to disable building tkinter.  (Mentioned by Msquared)
- Added gdbm-devel build pre-req.  (Thanks to Pat Callahan)
- Added db1-devel build pre-req.  (Thanks to Pat Callahan)
- Changed expat build pre-req to expat-devel.  (Thanks to Pat Callahan)
- Ugh, can't have spaces in defattr.  (Thanks to Pat Callahan)

* Sat Apr 21 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1-4]
- Added more "defattr" entries for the files sections.
- Ugh, the .so files were lost in the last package.
- Fixed IDLE.

* Sat Apr 21 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1-3]
- pymalloc wasn't properly getting disabled.  Not sure how rpm is picking up
  commented-out %define directives, but that's what it was doing.  Ugh.
- Made a similar change for binsuffix.
- Adding a "tools" sub-package.

* Tue Apr 17 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1-2tummy]
- Removed --with-pymalloc in configure.  Apparently threaded programs like
   Zope have problems with this.  Thanks for pointing that out, Guido.

* Tue Apr 17 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1-1tummy]
- Updated to the 2.1 final release.

* Mon Apr 16 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1c1-2tummy]
- Fixed naming to "python2" instead of "python2.1".
- Fixing up path in pydoc if binsuffix is set.

* Sun Apr 15 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1c1-1tummy]
- Upgraded to 2.1c1
- Changed package name to "python2" if building /usr/bin/python2
- Changed binary suffix to "2" instead of "2.1", in preperation for final
  release.

* Fri Mar 23 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1b2-1tummy]
- Upgraded to 2.1b2
- Enabled --with-pymalloc

* Tue Mar  6 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1b1-1tummy]
- Upgraded to 2.1b1

* Thu Feb 15 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1a2-2tummy]
- Tony Seward sent a patch to fix the expat module's header path in setup.py.

* Sat Feb 3 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1a2-1tummy]
- Updated to 2.1a2.

* Wed Jan 25 2001 Sean Reifschneider <jafo-rpms@tummy.com>
[Release 2.1a1-1tummy]
- Release for 2.1a1
- Splitting out devel and tk packages.
