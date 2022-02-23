# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without dotests

%global modname pycurl

%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

Name:           python-%{modname}
Version:        7.43.0
Release:        1
Summary:        A Python interface to libcurl
Group:          Applications/System

License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://dl.bintray.com/pycurl/pycurl/pycurl-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Source1000:	%{name}-%{version}-%{release}.build.log

BuildRequires:  curl-devel >= 7.52.1-1
BuildRequires:  libssh2-devel >= 1.8.0-1
BuildRequires:  openssl-devel >= 1.0.2k-1
BuildRequires:  python-devel >= 2.7.13-1
BuildRequires:  zlib-devel >= 1.2.3-7
Requires:       curl >= 7.52.0-1
Requires:       libssh2 >= 1.8.0-1
Requires:       openssl >= 1.0.2k-1
Requires:       python >= 2.7.13-1
Requires:       zlib >= 1.2.3-7

%ifos aix6.1 || %ifos aix7.1 || %ifos aix7.2
Requires: AIX-rpm >= 6.1.1.0
%endif

%define _libdir64 %{_prefix}/lib64

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.


%prep
%setup -q -n %{modname}-%{version}

# remove binaries packaged by upstream
rm -f tests/fake-curl/libcurl/*.so

# remove a test-case that relies on sftp://web.sourceforge.net being available
rm -f tests/ssh_key_cb_test.py

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L%{_libdir64} -L%{_libdir} -Wl,-blibpath:%{_libdir64}:%{_libdir}:/usr/lib:/lib"
python_64 setup.py build

cd ../32bit
export OBJECT_MODE=32
export LDFLAGS="-L%{_libdir} -Wl,-blibpath:%{_libdir}:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
python setup.py build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/pycurl

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{modname}
%defattr(-,root,system,-)
%doc 32bit/ChangeLog 32bit/README.rst 32bit/examples 32bit/doc 32bit/tests
%{python_sitelib}/*
%{python_sitelib64}/*


%changelog
* Tue Jan 02 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> - 7.43.0-1
- first 64bit version for AIX V5.1 and higher
