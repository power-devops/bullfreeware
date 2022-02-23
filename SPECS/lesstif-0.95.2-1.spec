Summary: OSF/Motif(R) library clone
Name: lesstif
Version: 0.95.2
Release: 1
License: LGPL
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/project/lesstif/lesstif/%{version}/lesstif-%{version}.tar.gz
#Source: http://sourceforge.net/projects/lesstif/files/lesstif/%{version}/lesstif-/%{version}.tar.bz2/download 
##Source: http://belnet.dl.sourceforge.net/sourceforge/lesstif/lesstif-%{version}.tar.bz2
Source1: lesstif-xmbind.txt
# put mwm conf file in %{_sysconfdir}, and install Dt in %_libdir
# ???? Patch0: lesstif-Makefile.in.diff
# have motif-config honor libdir
## ???? Patch1: lesstif-motif-config-use_libdir.diff
## OK Patch2: lesstif-0.95.0-CAN-2005-0605.patch
## OK Patch3: lesstif-0.95.0-64bitcleanups.patch
## OK Patch4: lesstif-0.95.0-c++fix.patch

## ?? Patch5: http://ftp.debian.org/debian/pool/main/l/lesstif2/lesstif2_0.95.2-1.diff.gz

## OK Patch6: lesstif-0.95.0-scroll.patch

Url: http://www.lesstif.org/

# monolithic X
#BuildRequires: xorg-x11-devel
#BuildRequires: xorg-x11-deprecated-libs-devel

## VSD BuildRequires: libXp-devel libXt-devel libXext-devel 
## VSD BuildRequires: freetype-devel fontconfig-devel
# lynx is used to transform html in txt
# VSD BuildRequires: lynx
# for tests
# VSD BuildRequires: libGLw-devel
# VSD BuildRequires: bitmap-devel
# needed for aclocal, to find the aclocal dir for the autoconf macro
BuildRequires: automake

# VSD Requires: xorg-x11-xinit 

# obsolete older openmotif may hurt third party repos
# not obsoleting it will leave openmotif on upgrade. 
# Rex makes a MUST not to have this obsolete
#Obsoletes: openmotif <=  2.3.0-0.2.1
# openmotif21 provides the same soname than lesstif. Both seem to work 
# fine with some apps (ddd, xpdf) but show binary incompatibility with
# nedit and runtime incompatible with grace. Moreover openmotif21
# are in /usr/X11R6/lib, and therefore may not be found by the linker.
# A conflict would break upgrade paths.
Obsoletes: openmotif21 <= 2.1.30-17.1.1

BuildRoot: /var/tmp/%{name}-%{version}-root
Prefix: %{_prefix}


%description
LessTif is a free replacement for OSF/Motif(R), which provides a full
set of widgets for application development (menus, text entry areas,
scrolling windows, etc.). LessTif is source compatible with
OSF/Motif(R).

This package provides the lesstif runtime libraries.


%package clients
Summary: Command line utilities for LessTif
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description clients
Command line utilities for LessTif:

* xmbind configures the virtual key bindings of LessTif applications.
* uil is a user interface language compiler.

%package mwm
Summary: Lesstif Motif window manager clone based on fvwm
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description mwm
"mwm" window manager that adheres largely to the Motif mwm specification.
Based on fvwm.


%package devel
Summary: Header files for LessTif/Motif development
Group: Development/Libraries
#Requires: libXt-devel libXp-devel libXext-devel
#Requires: imake
# for %{_datadir}/aclocal/
Requires: automake
Requires: %{name} = %{version}-%{release}

# Obsoletes older fedora releases. May hurt third party repos
Obsoletes: openmotif-devel <=  2.3.0-0.2.1


%description devel
Lesstif-devel contains the lesstif static library and header files
required to develop Motif based applications using LessTif. If you
want to develop LessTif applications, you'll need to install
lesstif-devel along with lesstif.

%prep
%setup -q
chmod a-x COPYING* doc/www.lesstif.org/BUG-HUNTING.html
## VSD %patch0 -p1
## VSD %patch1 -p1 -b .multilib
## VSD %patch2 -p1
## VSD %patch3 -p1
## VSD %patch4 -p1
## VSD %patch5 -p1
## VSD %patch6 -p1

# those substitutions are not usefull, since the symbols are defined
# in the Makefile, but it is clearer like that
sed -i -e 's:"/usr/X11/include":"%{_includedir}":' \
  -e 's:"/usr/lib/X11/mwm":"%{_sysconfdir}/mwm":' clients/Motif-2.1/mwm/mwm.h

%build
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r"


# --enable-shared --disable-static is the default
# the x libs and includes are empty in the default case, but we need to 
# have a non empty include defined (for a substitution in mwm)

# --enable-production is needed in order to avoid 
# http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-4124
CFLAGS='-I/opt/freeware/include -I/usr/include' \
./configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir} \
  --enable-shared \
  --disable-static \
  --with-xdnd \
  --enable-production \
  --disable-debug \
  --x-includes=%{_includedir} \
  --x-libraries=%{_libdir}

make 

%install
export RM="/usr/bin/rm -f"
${RM} -r $RPM_BUILD_ROOT

#make  prefix=${RPM_BUILD_ROOT}%{_prefix} install \
make install DESTDIR=$RPM_BUILD_ROOT \
 appdir='%{_datadir}/X11/app-defaults' configdir='%{_datadir}/X11/config'

# Handle debuginfo dangling-relative-symlink
# rpm doesn't handle symlinks properly when generating debuginfo
${RM} clients/Motif-2.1/xmbind/xmbind.c
cp -a clients/Motif-1.2/xmbind/xmbind.c \
      clients/Motif-2.1/xmbind/xmbind.c

### VSD --pourquoi ???? rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

${RM} -r $RPM_BUILD_ROOT%{_prefix}/LessTif

# install a script that launches xmbind in xinit
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/xmbind.sh

# correct the paths in mxmkmf
sed -i -e 's:"\${xprefix}/lib/X11/config":%{_datadir}/X11/config":' \
 -e 's:"\${lprefix}/lib/LessTif/config":%{_datadir}/X11/config":' \
 $RPM_BUILD_ROOT%{_bindir}/mxmkmf

# this is referenced into mwm
mkdir -p $RPM_BUILD_ROOT%{_includedir}/X11/bitmaps/

# will be in in %%doc
${RM} $RPM_BUILD_ROOT%{_sysconfdir}/mwm/README $RPM_BUILD_ROOT%{_sysconfdir}/mwm/alt.map

# the corresponding file is not shipped
${RM} $RPM_BUILD_ROOT%{_mandir}/man*/ltversion*

# prepare docs
cp -a doc clean_docs
find clean_docs -name 'Makefile*' -exec ${RM} {} \;
${RM} clean_docs/lessdox/clients/*.1 clean_docs/lessdox/clients/*.5
${RM} clean_docs/lessdox/widgets/*.3
# remove the empty directory
[ -d  clean_docs/lessdox/functions ] && rmdir  clean_docs/lessdox/functions

# remove host.def, it lives in the imake package
${RM} $RPM_BUILD_ROOT%{_datadir}/X11/config/host.def

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib bin etc
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

### Cannot use on Aix envirnomnent  %post -p /sbin/ldconfig
### Cannot use on Aix envirnomnent %postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system,-)
%doc COPYING COPYING.LIB CREDITS AUTHORS BUG-REPORTING FAQ README
%doc NEWS ReleaseNotes.html ReleaseNotes.txt
%{_libdir}/lib*.a
%{_mandir}/man1/lesstif*
%{_mandir}/man5/VirtualBindings*
/usr/lib//lib*.a

%files mwm
%defattr(-,root,system,-)
%doc clients/Motif-2.1/mwm/README clients/Motif-2.1/mwm/alt.map
%dir %{_libdir}/X11/mwm/
%config(noreplace) %{_libdir}/X11/mwm/system.mwmrc
#%{_includedir}/X11/bitmaps/
%{_bindir}/mwm
%{_mandir}/man*/mwm*
%{_datadir}/X11/app-defaults/Mwm
/usr/bin/mwm

%files clients
%defattr(-,root,system,-)
%{_sysconfdir}/X11/xinit/xinitrc.d/*xmbind.sh
%{_bindir}/xmbind*
%{_bindir}/uil
%{_mandir}/man1/uil*
%{_mandir}/man1/xmbind*
/usr/bin/xmbind*
/usr/bin/uil
/usr/etc/X11/xinit/xinitrc.d/*xmbind.sh

%files devel
%defattr(-,root,system,-)
%doc clean_docs/*
%{_bindir}/motif-config
%{_bindir}/mxmkmf
%{_includedir}/Dt/
%{_includedir}/Mrm/
%{_includedir}/Xm/
%{_includedir}/uil/
%{_libdir}/lib*.la
/usr/include/Dt/
/usr/include/Mrm/
/usr/include/Xm/
/usr/include/uil/
/usr/bin/motif-config
/usr/bin/mxmkmf
/usr/lib/lib*.la
# not shipped
#%{_mandir}/man1/ltversion*
%{_mandir}/man3/*
%{_datadir}/aclocal/ac_find_motif.m4
%{_datadir}/X11/config/*

%changelog
* Fri Jan  5 2007 Patrice Dumas <pertusus@free.fr> 0.95.0-15
- Obsolete openmotif21 versions provided in older fedora core releases.
  openmotif21 provides the same soname than lesstif, with some 
  incompatibility, and a conflict would break upgrade paths (fix #215560)

