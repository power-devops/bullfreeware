Name:          xproto
Version:       7.0.28
Release:       3
Summary:       The X.org xproto header
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.6/src/proto/%{name}-%{version}.tar.gz
License:       MIT
Provides:      xorg-proto
Obsoletes:     xorg-proto

BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
The X.org xproto header

%package devel
Summary:       The X.org xproto header
Group:         Development/Libraries

%description devel
The X.org xproto header

%prep
%setup -q

%build
export RM="/usr/bin/rm -f"
./configure --prefix=%{_prefix}
make

%define LINKS_DEVEL include/X11/DECkeysym.h include/X11/HPkeysym.h include/X11/Sunkeysym.h include/X11/X.h include/X11/XF86keysym.h include/X11/XWDFile.h include/X11/Xalloca.h include/X11/Xarch.h include/X11/Xatom.h include/X11/Xdefs.h include/X11/Xfuncproto.h include/X11/Xfuncs.h include/X11/Xmd.h include/X11/Xos.h include/X11/Xos_r.h include/X11/Xosdefs.h include/X11/Xpoll.h include/X11/Xproto.h include/X11/Xprotostr.h include/X11/Xthreads.h include/X11/Xw32defs.h include/X11/Xwindows.h include/X11/Xwinsock.h include/X11/ap_keysym.h include/X11/keysym.h include/X11/keysymdef.h

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install

# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/include/X11
LINKS=`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 %{LINKS_DEVEL}`
for LINK in $LINKS; do
    if [ ! -f /usr/$LINK -o "ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'" != "" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    fi
done

# %posttrans devel
# mkdir -p /usr/include/X11
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS_DEVEL}`
# # Add symbolic links in /usr if files not already exists
# for LINK in $LINKS; do
#     if [ ! -f /usr/$LINK ]; then
#         ln -s /opt/freeware/$LINK /usr/$LINK
#     fi
# done
#     
# %preun devel
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS_DEVEL}`
# # Remove the symbolic link from /usr
# for LINK in $LINKS; do
#     if [ -L /usr/$LINK ]; then
#         if [ "`ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'`" != "" ]; then
# 	    rm /usr/$LINK
#         fi
#     fi
# done
# rmdir --ignore-fail-on-non-empty /usr/include/X11

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%{_includedir}/X11/*.h
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/doc/
%{_datadir}/doc/*/*
/usr/include/X11/*.h


%changelog
* Tue Apr 19 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.0.28-1
- Update to version 7.0.28

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.23-1
- Update to version 7.0.23

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-3
- Initial port on Aix6.1

* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20
- Inital port on Aix 5.3

