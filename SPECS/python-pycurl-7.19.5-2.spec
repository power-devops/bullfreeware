%define name python-pycurl
%define srcname pycurl
%define version 7.19.5
%define release 2

%define is_python %(test -e /usr/bin/python && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /usr/bin/python_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Summary: A Python interface to libcurl
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pycurl.sourceforge.net/download/%{srcname}-%{version}.tar.gz
Url:     http://pycurl.sourceforge.net
License: LGPLv2+ or MIT
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: curl-devel >= 7.19.0
BuildRequires: openssl-devel
BuildArch:     noarch


%define libdir64 /opt/freeware/lib64

# This is due in order to don't depend on libssl.so rather libssl.a(libssl.so.1.0.2) .
# When the build stops in the middle, files are not put back at their original place
# This is done at beg and end of %build
# Run:
# ln -s /opt/freeware/lib64/libssl.so.1.0.2 /opt/freeware/lib64/libssl.so ; ln -s /opt/freeware/lib64/libcrypto.so.1.0.2 /opt/freeware/lib64/libcrypto.so
# ln -s /opt/freeware/lib/libssl.so.1.0.2   /opt/freeware/lib/libssl.so ;   ln -s /opt/freeware/lib/libcrypto.so.1.0.2   /opt/freeware/lib/libcrypto.so


# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%define libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%define curlver_h /usr/include/curl/curlver.h
%define libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:       libcurl >= %{libcurl_ver}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup -q -n %{srcname}-%{version}

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build

###############################################
# for linking with openssl archive (not soname)
###############################################
if [ -f %{_libdir}/libcrypto.so ]; then
    mv %{_libdir}/libcrypto.so /tmp/libcrypto.so.32
fi
if [ -f %{_libdir}/libssl.so ]; then
    mv %{_libdir}/libssl.so /tmp/libssl.so.32
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{libdir64}/libcrypto.so /tmp/libcrypto.so.64
fi
if [ -f %{_libdir64}/libssl.so ]; then
    mv %{libdir64}/libssl.so /tmp/libssl.so.64
fi


cd 64bit
export OBJECT_MODE=64
python_64 setup.py build

cd ../32bit
export OBJECT_MODE=32
python setup.py build


##################################################################
# revert previous move - linking with openssl archive (not soname)
##################################################################

if [ -f /tmp/libcrypto.so.32 ]; then
    mv /tmp/libcrypto.so.32 %{_libdir}/libcrypto.so
fi
if [ -f /tmp/libssl.so.32 ]; then
    mv /tmp/libssl.so.32 %{_libdir}/libssl.so
fi
if [ -f /tmp/libcrypto.so.64 ]; then
    mv /tmp/libcrypto.so.64 %{libdir64}/libcrypto.so
fi
if [ -f /tmp/libssl.so.64 ]; then
    mv /tmp/libssl.so.64 %{libdir64}/libssl.so
fi


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/COPYING-LGPL 32bit/COPYING-MIT 32bit/README.rst 32bit/ChangeLog 32bit/PKG-INFO 32bit/examples 32bit/doc 32bit/AUTHORS
%{python_sitelib}/*
%{python_sitelib64}/*
%{_datadir}/doc/*

%changelog
* Thu Jun 22 2017 Tony Reix <tony.reix@bull.net> - 7.19.5-2
- Suppress dependency on libssl.so and libcrypto.so.
  Rather .a files

* Fri Nov 21 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 7.19.5-1
- First version for AIX V6.1 and higher
