# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           p7zip
Version:        16.02
Release:        1
Summary:        Very high compression ratio file archiver
URL:            http://p7zip.sourceforge.net/
License:        LGPLv2 and (LGPLv2+ or CPL)
Group:          Applications/Archiving
Source0:        https://sourceforge.net/projects/p7zip/files/p7zip/%{version}/%{name}_%{version}_src_all.tar.bz2
Source1000:     %{name}-%{version}-%{release}.build.log

Patch0:         CVE-2016-9296.patch
Patch1:         CVE-2017-17969.patch
Patch2:         p7zip-makefile64-v2-aix.patch
Patch3:         p7zip-removeflags-aix.patch
Patch4:         p7zip-timegm-aix.patch

Requires:       libgcc >= 8.3.0
Requires:       libstdc++ >= 8.3.0

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.

%prep
%setup -q -n %{name}_%{version}
/usr/bin/cp makefile.aix_gcc makefile.aix_gcc_64

# move license files
/usr/bin/mv DOC/License.txt DOC/copying.txt .

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
cp makefile.aix_gcc_64 makefile.machine
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
gmake all3


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib"
# ulimit -d unlimited is required for running some tests here
    ulimit -d unlimited
    ulimit -m unlimited
    (gmake -k test || true)


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export OBJECT_MODE=64
gmake install \
    DEST_DIR=${RPM_BUILD_ROOT} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}

# strip is already done as part of make install


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_datadir}/doc/p7zip
%license copying.txt License.txt
%{_bindir}/*
%{_libexecdir}/p7zip
%{_mandir}/man1/*


%changelog
* Tue Nov 10 2020 Tony Reix <tony.reix@atos.net> - 16.02-1
- First release for ATOS Bullfreeware
- Use -O2. Add Fedora GCC options. Increase Memory for %check tests

* Tue Feb 25 2020 Ayappan P <ayappap2@in.ibm.com> - 16.02-1
- First release for AIX Toolbox

