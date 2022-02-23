# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL


%define modname pycurl

%define python_sitelib   %(python2_32 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python_sitelib64 %(python2_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%define base_release 2
%define release %{base_release}%{?without_ibm_SSL:opensourcessl}

Name:           python-%{modname}
Version:        7.43.0.4
Release:        %{release}
Summary:        A Python interface to libcurl
Group:          Applications/System

License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://dl.bintray.com/pycurl/pycurl/pycurl-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{base_release}.build.log

Patch1:         pycurl-test.7.43.0.4.patch

BuildRequires:  curl-devel >= 7.68.0-1
BuildRequires:  libssh2-devel >= 1.8.0-1
BuildRequires:  python-devel >= 2.7.13-1
BuildRequires:  zlib-devel >= 1.2.3-7
Requires:       curl >= 7.68.0-1
Requires:       libssh2 >= 1.8.0-1
Requires:       python >= 2.7.13-1
Requires:       zlib >= 1.2.3-7

%if %{with ibm_SSL}
# Workaround to use AIX libssl.a and libcrypto.a needs OpenSource sed
BuildRequires: sed
%else
BuildRequires: openssl-devel >= 1.0.2g
Requires: openssl >= 1.0.2g
%endif


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

%patch1 -p1 -b .test

# remove binaries packaged by upstream
rm -f tests/fake-curl/libcurl/*.so

# remove a test-case that relies on sftp://web.sourceforge.net being available
rm -f tests/ssh_key_cb_test.py

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
cd 64bit
export OBJECT_MODE=64
export CPPFLAGS="-maix64"
export LDFLAGS="-L%{_libdir64} -L%{_libdir} -Wl,-blibpath:%{_libdir64}:%{_libdir}:/usr/lib:/lib"
python2_64 setup.py build

cd ../32bit
export OBJECT_MODE=32
export CPPFLAGS="-maix32"
export LDFLAGS="-L%{_libdir} -Wl,-blibpath:%{_libdir}:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
python2_32 setup.py build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
python2_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python2_32 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/pycurl


%check
%if %{with dotests}
# # Tests can be run, but our proxy makes them long and causes lot of fails...

# cd 64bit
# rm -f ./examples/tests/test_gtk.py
# python2_64 -m virtualenv pycurl_env
# . ./pycurl_env/bin/activate
# pip install pytest bottle nose flaky
# ( PYTHONPATH=./build/lib.aix-6.1-2.7 python2_64 -m pytest -k "not curl_object_test and not global_init_test and not header_test and not multi_test and not setopt_string_test and not setopt_test and not setopt_unicode_test and not share_test" || true )
# deactivate
# 
# cd ../32bit
# rm -f ./examples/tests/test_gtk.py
# python2_32 -m virtualenv pycurl_env
# . ./pycurl_env/bin/activate
# pip install pytest bottle nose flaky
# (PYTHONPATH=./build/lib.aix-6.1-2.7 python2_32 -m pytest -k "not curl_object_test and not global_init_test and not header_test and not multi_test and not setopt_string_test and not setopt_test and not setopt_unicode_test and not share_test" || true )
# deactivate
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{modname}
%defattr(-,root,system,-)
%doc 32bit/ChangeLog 32bit/README.rst 32bit/examples 32bit/doc 32bit/tests
%{python_sitelib}/*
%{python_sitelib64}/*


%changelog
* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 7.43.0.4-2
- Bullfreeware OpenSSL removal

* Tue Jan 28 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 7.43.0.4-1
- New version 7.43.0.4
- add test
- Use AIX openssl conditionnaly

* Fri Dec 20 2019 Clément Chigot <clement.chigot@atos.net> - 7.43.0-2
- Rebuild for BullFreeware

* Tue Jan 02 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> - 7.43.0-1
- first 64bit version for AIX V5.1 and higher
