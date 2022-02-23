Name:          xextproto
Version:       7.3.0
Release:       1
Summary:       X11 prototype headers for libXext
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.6/src/proto/%{name}-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X11 prototype headers for libXext.

%package devel
Summary:       X11 prototype headers for libXext
Group:         Development/Libraries

%description devel
X11 prototype headers for libXext

%prep
%setup -q

%build
CC="/usr/vac/bin/xlc"
./configure --prefix=%{_prefix}
make

%define LINKS_DEVEL include/X11/extensions/ag.h include/X11/extensions/agproto.h include/X11/extensions/cup.h include/X11/extensions/cupproto.h include/X11/extensions/dbe.h include/X11/extensions/dbeproto.h include/X11/extensions/dpmsconst.h include/X11/extensions/dpmsproto.h include/X11/extensions/EVI.h include/X11/extensions/EVIproto.h include/X11/extensions/ge.h include/X11/extensions/geproto.h include/X11/extensions/lbx.h include/X11/extensions/lbxproto.h include/X11/extensions/mitmiscconst.h include/X11/extensions/mitmiscproto.h include/X11/extensions/multibufconst.h include/X11/extensions/multibufproto.h include/X11/extensions/secur.h include/X11/extensions/securproto.h include/X11/extensions/shapeconst.h include/X11/extensions/shapeproto.h include/X11/extensions/shapestr.h include/X11/extensions/shm.h include/X11/extensions/shmproto.h include/X11/extensions/shmstr.h include/X11/extensions/syncconst.h include/X11/extensions/syncproto.h include/X11/extensions/syncstr.h include/X11/extensions/xtestconst.h include/X11/extensions/xtestext1const.h include/X11/extensions/xtestext1proto.h include/X11/extensions/xtestproto.h

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/include/X11/extensions
LINKS=`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 %{LINKS_DEVEL}`
for LINK in $LINKS; do
    if [ ! -f /usr/$LINK -o "ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'" != "" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    fi
done

# %posttrans devel
# mkdir -p /usr/include/X11/extensions
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
# rmdir --ignore-fail-on-non-empty /usr/include/X11/extensions

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%{_includedir}/X11/extensions/*.h
%{_libdir}/pkgconfig/xextproto.pc
%dir %{_datadir}/doc/xextproto
%{_datadir}/doc/xextproto/*
/usr/include/X11/extensions/*.h


%changelog
* Tue Apr 19 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.3.0-1
- Update to version 7.3.0

* Tue Feb 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.2.1-1
- Update to version 7.2.1

* Tue Feb 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.1.2-2
- Inital port on Aix 6.1

