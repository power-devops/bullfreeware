Name:          randrproto
Version:       1.4.1
Release:       1
Summary:       X11 prototype headers for libXrandr
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.6/src/proto/%{name}-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X11 prototype headers for libXrandr.

%package devel
Summary:       X11 prototype headers for libXrandr
Group:         Development/Libraries

%description devel
X11 prototype headers for libXrandr

%prep
%setup -q

%build
CC="/usr/vac/bin/xlc"
./configure --prefix=%{_prefix}
make

%define LINKS_DEVEL include/X11/extensions/randr*.h

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
%{_includedir}/X11/extensions/randr*.h
%{_libdir}/pkgconfig/randrproto.pc
%dir %{_datadir}/doc/randrproto
%{_datadir}/doc/randrproto/*
/usr/include/X11/extensions/*.h


%changelog
* Tue Apr 26 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.4.1-1
- Inital port on Aix 6.1

