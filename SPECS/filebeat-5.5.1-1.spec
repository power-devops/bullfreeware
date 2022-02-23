Summary: Open source file harvester
Name: filebeat
Version: 5.5.1
Release: 1
License: ASL 2.0
URL: https://www.elastic.co/products/beats/filebeat

#Source: https://github.com/elastic/beats/archive/v5.5.1.tar.gz
Source: %{name}-%{version}.tar.gz

Group: Applications/System

BuildRequires: make
BuildRequires: rsync
BuildRequires: gcc-go >= 8.1.0

Requires: libgo >= 8.1.0-2
Requires: libgcc >= 8.1.0-2

%description
Filebeat is an open source file harvester, mostly used to fetch
log files and feed them into logstash.

%prep

%setup -q -n beats-5.5.1

%build
export PATH=/usr/bin:/etc:/usr/sbin:/sbin:/opt/freeware/bin

mkdir -p ./_root
mkdir -p ./_build/src/github.com/elastic
ln -s $(pwd) ./_build/src/github.com/elastic/beats

export GOPATH=$(pwd)/_build
export GOARCH=ppc64
export CGO_ENABLED=1
export GOROOT=$(pwd)/_root

ulimit -d unlimited
ulimit -m unlimited
ulimit -s unlimited
ulimit -f unlimited

# filebeat
go build -p=3 -v -gccgoflags="all=-mcmodel=large" -o dist/filebeat github.com/elastic/beats/filebeat

cd filebeat
gmake modules
cd -

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
strip -X64 -t dist/filebeat
/usr/bin/install -M 0755 -f ${RPM_BUILD_ROOT}%{_bindir} dist/filebeat
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat
/usr/bin/install -M 0644 -f ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat filebeat/filebeat.template.json
/usr/bin/install -M 0644 -f ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat filebeat/filebeat.yml
/usr/bin/install -M 0644 -f ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat filebeat/filebeat.template-es2x.json
/usr/bin/install -M 0644 -f ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat filebeat/filebeat.full.yml
/usr/bin/install -M 0644 -f ${RPM_BUILD_ROOT}%{_sysconfdir}/filebeat filebeat/filebeat.template-es6x.json
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/filebeat
cp -r filebeat/_meta/module.generated ${RPM_BUILD_ROOT}%{_datadir}/filebeat/module

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%doc LICENSE NOTICE README.md
%{_bindir}/filebeat
%{_sysconfdir}/filebeat/filebeat.template.json
%{_sysconfdir}/filebeat/filebeat.yml
%{_sysconfdir}/filebeat/filebeat.template-es2x.json
%{_sysconfdir}/filebeat/filebeat.full.yml
%{_sysconfdir}/filebeat/filebeat.template-es6x.json
%{_datadir}/filebeat/module

%changelog
* Wed Oct 10 2018 Tony Reix <tony.reix@atos.net> - 5.5.1-1
- Rebuild for BullFreeware

* Thu Oct 04 2018 Ayappan P <ayappap2@in.ibm.com> - 5.5.1-1
- Add rsync in BuildRequires

* Mon Aug 27 2018 Damien Bergamini - 5.5.1-1
- Initial port of Filebeat 5.5.1 to AIX
