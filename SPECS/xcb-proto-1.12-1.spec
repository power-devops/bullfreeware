%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python_sitelib64 %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%define _libdir64 %{_prefix}/lib64

%{!?dotests:%define DO_TESTS 0}
%{?dotests:%define DO_TESTS 1}

Name:           xcb-proto
Version:        1.12
Release:        1
Summary:        XCB protocol descriptions
Group:          Development/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	python-devel
Requires:	python
Requires:       pkg-config

%description
XCB is a project to enable efficient language bindings to the X11 protocol.
This package contains the protocol descriptions themselves.  Language
bindings use these protocol descriptions to generate code for marshalling
the protocol.


%prep
echo "DO_TESTS=%{DO_TESTS}"
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/usr/vac/bin/xlc"
export CC64="$CC32 -q64"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export PYTHON=python_64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64}
gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export PYTHON=python
./configure \
    --prefix=%{_prefix}
gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

mv ${RPM_BUILD_ROOT}%{_libdir}/python2.7 ${RPM_BUILD_ROOT}%{_libdir64}/

cd 32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/COPYING 32bit/NEWS 32bit/README 32bit/TODO 32bit/doc/xml-xcb.txt
%{_libdir}/pkgconfig/xcb-proto.pc
%{_libdir64}/pkgconfig/xcb-proto.pc
%dir %{_datadir}/xcb/
%{_datadir}/xcb/*.xsd
%{_datadir}/xcb/*.xml
%{python_sitelib}/xcbgen
%{_libdir64}/python2.7/site-packages/xcbgen


%changelog
* Fri May 20 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.12-1
- Updated to version 1.12

* Tue Apr 19 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.11-1
- Updated to version 1.11

* Mon Apr 08 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.8-1
- Initial port on Aix6.1

* Fri Jul 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.6
- Initial port on Aix 5.3
