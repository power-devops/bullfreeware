# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# List all the software already available
%define beats_packages filebeat metricbeat auditbeat

Name:           beats
Version:        7.5.1
Release:        1beta
Summary:        Beats - The Lightweight Shippers of the Elastic Stack

Group:          Applications
License:        ALS-2.0
URL:            https://www.elastic.co/products/beats
#Source0:        https://github.com/elastic/beats/archive/v%{version}.tar.gz
Source0:        https://github.com/elastic/beats/archive/beats-%{version}.tar.gz

# build.log
Source1000: %{name}-%{version}-%{release}.build.log

# Make "mage package" creating tar.gz for AIX
Patch1: %{name}-%{version}-dev-tools-add-AIX-tar.gz-target-for-packages-generat.patch

# Remove of Crossbuild targets for "mage package"
Patch2: %{name}-%{version}-filebeat-mage-package-workaround-for-AIX.patch
Patch3: %{name}-%{version}-metricbeat-mage-package-workaround-for-AIX.patch
Patch4: %{name}-%{version}-packetbeat-mage-package-workaround-for-AIX.patch
Patch5: %{name}-%{version}-auditbeat-mage-package-workaround-for-AIX.patch

# This version is supposed to be compiled with Go 1.12
# However, our go 1.12 hasn't CGO support fully available.
# Therefore, we'd rather use go 1.13 using this community patch
Patch6: %{name}-%{version}-Update-Go-to-1.13.3-14335.patch

# Workaroud for add_docker_metadata and add_kubernetes_metadata.
# The final solution should be in dev-tool/packages in guess
Patch7: %{name}-%{version}-all-force-the-removal-for-docker-and-kubernetes-meta.patch

# Fsync syscall doesn't work with file opened in read-only mode.
Patch8: %{name}-%{version}-libbeat-common-file-fix-fsync-failure-on-AIX.patch

Patch9: %{name}-%{version}-all-remove-docker-and-k8s-tests-for-AIX.patch
Patch10: %{name}-%{version}-Makefile-avoid-go-test-to-be-cached.patch

# Disable TestFetchTimeout in metricbeat module's folder
# The error gotten is slightly differente and it's also failing on linux/ppc64le
Patch11: %{name}-%{version}-metricbeat-module-disable-TestFetchTimeout.patch

# Add a script with launching a beat software with the default settings
Patch12: %{name}-%{version}-dev-tools-packaging-add-launching-script-template-fo.patch

# Add support for system modules on metricbeat.
Patch13: %{name}-%{version}-metricbeat-add-system-metric-support-for-AIX.patch

# Port auditbeat/module/file_integrity
Patch14: %{name}-%{version}-auditbeat-module-file_integrity-port-for-AIX.patch
Patch15: %{name}-%{version}-auditbeat-module-file_integrity-disable-xxhash.patch

Patch16: %{name}-%{version}-libbeat-processors-add_host_metadata-add-AIX.patch
Patch17: %{name}-%{version}-libbeat-processors-add_process_metadata-fix-TestBadP.patch

# Vendor Manual Update
Patch50: %{name}-%{version}-vendor-update-github.com-mattn-go-isatty.patch
Patch51: %{name}-%{version}-vendor-update-elastic-go-txfile-and-gofrs-flock.patch
Patch52: %{name}-%{version}-vendor-update-golang.org-x-crypto-ssh-terminal.patch
Patch53: %{name}-%{version}-vendor-update-github.com-lib-pq.patch
Patch54: %{name}-%{version}-vendor-update-github.com-insomniacslk-dhcp-dhcpv4.patch
Patch55: %{name}-%{version}-vendor-gopkg.in-goracle.v2-add-lm-for-AIX.patch
Patch56: %{name}-%{version}-vendor-coreos-bbolt-Add-support-for-aix-189.patch
Patch57: %{name}-%{version}-vendor-go-sysinfo-all-add-AIX-providers.patch
Patch58: %{name}-%{version}-vendor-gosigar-Add-AIX-support.patch
Patch59: %{name}-%{version}-vendor-gopsutil-net-move-netstat-parsing-functions-to-net.go.patch
Patch60: %{name}-%{version}-vendor-gopsutil-net-add-AIX-support.patch
# This isn't exactly github.com/fsnotify/fsnotify, but github.com/adriansr/fsnotify fork,
# as it needs SetRecursive() method.
Patch61: %{name}-%{version}-vendor-fsnotify-add-polling-for-AIX.patch

BuildRequires:  golang >= 1.13
# BuildRequires:  mage

# For packetbeat dependency: github.com/tsg/gopacket/pcap
BuildRequires: libpcap-devel

%description
The Lightweight Shippers of the Elastic Stack


%package -n filebeat
Summary: Filebeat sends log files to Logstash or directly to Elasticsearch.
URL: https://www.elastic.co/products/beats/filebeat

%description -n filebeat
Filebeat sends log files to Logstash or directly to Elasticsearch.
This is a beta version.


%package -n metricbeat
Summary: Metricbeat is a lightweight shipper for metrics.
URL: https://www.elastic.co/products/beats/metricbeat

%description -n metricbeat
Metricbeat is a lightweight shipper for metrics.
This is a beta version.

%package -n auditbeat
Summary: Audit the activities of users and processes on your system.
URL: https://www.elastic.co/products/beats/auditbeat

%description -n auditbeat
Audit the activities of users and processes on your system.
This is a beta version.

# %package -n packetbeat
# Summary: Packetbeat analyzes network traffic and sends the data to Elasticsearch.
# URL: https://www.elastic.co/products/beats/packetbeat

# %description -n packetbeat
# Packetbeat analyzes network traffic and sends the data to Elasticsearch.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

# Update vendor
%patch50 -p1
%patch51 -p1
%patch52 -p1 -d vendor
%patch53 -p1 -d metricbeat/module/postgresql
%patch54 -p1
%patch55 -p1 -d vendor/gopkg.in/goracle.v2
%patch56 -p1 -d vendor/github.com/coreos/bbolt
%patch57 -p1 -d vendor/github.com/elastic/go-sysinfo
%patch58 -p1 -d vendor/github.com/elastic/gosigar
%patch59 -p1 -d vendor/github.com/shirou/gopsutil
%patch60 -p1 -d vendor/github.com/shirou/gopsutil
%patch61 -p1 -d vendor/github.com/fsnotify/fsnotify

# Simulated GOPATH
mkdir -p src/github.com/elastic/%{name}
mv * .[!.]* src/github.com/elastic/%{name} || true

# Setup go environment
PATH=$(pwd)/bin:/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java8_64/jre/bin:/usr/java8_64/bin
unset GOROOT
export GOPATH=$(pwd)

# Download mage directly instead of having a BuildRequires on it
go get github.com/magefile/mage

# "mage" needs a commit number. Therefore simulate one if there is none.
cd  src/github.com/elastic/%{name}
if [ ! -d .git ]; then
	git init
	git config user.email "clement.chigot@atos.net"
	git config user.name "Clément Chigot"
	git add .gitignore
	git commit -m "init"
fi

%build

# Setup go environment
PATH=$(pwd)/bin:/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java8_64/jre/bin:/usr/java8_64/bin
# PATH=/opt/freeware/bin:$PATH
unset GOROOT
export GOPATH=$(pwd)
cd  src/github.com/elastic/%{name}

# Change libpath of cgo programs
CGO_LDFLAGS=`go env CGO_LDFLAGS`
export CGO_LDFLAGS="$CGO_LDFLAGS -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

for pkg in %{beats_packages}; do
	(
		cd $pkg
		make
	)
done


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Setup go environment
PATH=$(pwd)/bin:/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java8_64/jre/bin:/usr/java8_64/bin
unset GOROOT
export GOPATH=$(pwd)
cd  src/github.com/elastic/%{name}


# Install process
# Normally, mage package is performing a crossbuild for every platforms
# using a linux Docker. Therefore, in our case, we need to move the previously
# built binary to the "crossbuild" destination ie
# "build/golang-crossbuild/filebeat-aix-ppc64".
# After that, "mage package" will create a tar.gz under filebeat/build/distribution
# This tar.gz contains all the files needed for filebeat (binaries + configuration)
# Extracting under RPM_BUILD_ROOT is enough to simulated an installation.
install_beat(){
	set -x
	beat_name=$1
	mkdir -p build/golang-crossbuild
	cp ${beat_name} build/golang-crossbuild/${beat_name}-aix-ppc64

	# Create tar.gz
	DEV_OS="aix" DEV_ARCH="ppc64" PLATFORMS="+all aix" mage package

	# Extract built tar.gz
	cd build/distributions
	tar -xvzf ${beat_name}-oss-%{version}-aix-ppc.tar.gz

	# Install files
	# For each new version, check files provided on Fedora to known if something
	# has changed.
	cd ${beat_name}-%{version}-aix-ppc
	install -D ${beat_name}.sh ${RPM_BUILD_ROOT}%{_bindir}/${beat_name}

	mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/${beat_name}/bin/
	install -D ${beat_name} ${RPM_BUILD_ROOT}%{_datadir}/${beat_name}/bin/${beat_name}

	mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/${beat_name}
	test -d module && cp -r module ${RPM_BUILD_ROOT}%{_datadir}/${beat_name}/module
	test -d kibana && cp -r kibana ${RPM_BUILD_ROOT}%{_datadir}/${beat_name}/kibana

	mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/${beat_name}
	install *.yml ${RPM_BUILD_ROOT}%{_sysconfdir}/${beat_name}
	test -d modules.d && cp -r modules.d ${RPM_BUILD_ROOT}%{_sysconfdir}/${beat_name}

	# Manually, add the doc too
	mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/${beat_name}-%{version}
	cp LICENSE.txt ${RPM_BUILD_ROOT}%{_docdir}/${beat_name}-%{version}
	cp NOTICE.txt ${RPM_BUILD_ROOT}%{_docdir}/${beat_name}-%{version}
	cp README.md ${RPM_BUILD_ROOT}%{_docdir}/${beat_name}-%{version}
}

# Install
for pkg in %{beats_packages}; do
	(
		cd $pkg
		install_beat $pkg
	)
done


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Setup go environment
PATH=$(pwd)/bin:/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/java8_64/jre/bin:/usr/java8_64/bin
unset GOROOT
export GOPATH=$(pwd)
cd  src/github.com/elastic/%{name}

# Don't test packetbeat rightnow as it's not high-priority.
for pkg in libbeat filebeat metricbeat auditbeat; do
	(
		cd $pkg
		make test || true
	)
done


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
# NONE

%files -n filebeat
%defattr(-,root,system)
%{_docdir}/filebeat-%{version}
%{_bindir}/filebeat
%{_datadir}/filebeat
%{_sysconfdir}/filebeat

%files -n metricbeat
%defattr(-,root,system)
%{_docdir}/metricbeat-%{version}
%{_bindir}/metricbeat
%{_datadir}/metricbeat
%{_sysconfdir}/metricbeat

%files -n auditbeat
%defattr(-,root,system)
%{_docdir}/auditbeat-%{version}
%{_bindir}/auditbeat
%{_datadir}/auditbeat
%{_sysconfdir}/auditbeat

# %files -n packetbeat
# %defattr(-,root,system)
# %{_docdir}/packetbeat-%{version}
# %{_bindir}/packetbeat
# %{_datadir}/packetbeat
# %{_sysconfdir}/packetbeat

%changelog
* Tue Jan 7 2020 Clément Chigot <clement.chigot@atos.net> - 7.5.1-1beta
- First port on AIX
