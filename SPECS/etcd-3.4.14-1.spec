# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: Distributed reliable key-value store for the most critical data of a distributed system
Name: etcd
Version: 3.4.14
Release: 1
License: ASL 2.0
URL: https://etcd.readthedocs.io/en/latest

# https://github.com/coreos/etcd/releases/download/v3.3.2/v3.3.2.tar.gz
Source0: etcd-%{version}.tar.gz

# Vendor directory seems to be complet but the modules.txt
# is missing. Thus, generates it with "go mod vendor" and
# add it as a Source. It would be possible to run the command
# for every built, but it might force extra dependency as
# ca-certificates. So, I'd rather have it as a Source.
Source1: etcd-%{version}-vendor-modules.txt

Source100: %{name}-%{version}-%{release}.build.log

Patch1: etcd-3.4.14-vendor-github.com-bgentry-speakeasy-support-for-AIX.patch
Patch2: etcd-3.4.14-vendor-gopkg.in-cheggaaa-partial-support-for-AIX.patch
Patch3: etcd-3.4.14-vendor-go.etcd.io-bbolt-partial-support-for-AIX.patch
Patch4: etcd-3.4.14-vendor-github.com-creack-pty-fix-compilation-for-AIX.patch
Patch5: etcd-3.4.14-pkg-fileutils-fix-flock-for-AIX.patch
Patch6: etcd-3.4.14-pkg-runtime-support-for-AIX.patch
Patch7: etcd-3.4.14-fix-tests-compilation-for-go1.15.patch


Group: Applications/System

BuildRequires: golang >= 1.13


%description
etcd is a distributed reliable key-value store for the most
critical data of a distributed system.
Support of Wal files might be a bit buggy, because
locking files doesn't work correctly on AIX.

%package -n etcdctl
Summary: Command-line client for etcd.

%description -n etcdctl
Command-line client for etcd.

%prep

%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# Copy modules.txt
cp %{SOURCE1} vendor/modules.txt


%build
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/sbin

mkdir -p ./_root
mkdir -p ./_build/src/github.com/coreos
ln -s $(pwd) ./_build/src/github.com/coreos/etcd

# ppc64 isn't officially supported
export GOPATH=$(pwd)/_build
unset GOROOT

export ETCD_UNSUPPORTED_ARCH=ppc64
make

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
strip -X64 -t bin/etcd
/opt/freeware/bin/install -m 0755 bin/etcd ${RPM_BUILD_ROOT}%{_bindir}
strip -X64 -t bin/etcdctl
/opt/freeware/bin/install -m 0755 bin/etcdctl ${RPM_BUILD_ROOT}%{_bindir}

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# ppc64 isn't officially supported
export ETCD_UNSUPPORTED_ARCH=ppc64
make test || true


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc LICENSE NOTICE
%{_bindir}/etcd

%files -n etcdctl
%defattr(-,root,system,-)
%doc LICENSE NOTICE
%{_bindir}/etcdctl

%changelog
* Fri Dec 04 2020 Clément Chigot <clement.chigot@atos.net> - 3.4.14-1
- Update to 3.4.14

* Mon Aug 27 2018 Damien Bergamini - 3.3.2-1
- Initial port of etcd 3.3.2 to AIX
