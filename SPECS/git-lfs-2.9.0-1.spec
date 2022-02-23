# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           git-lfs
Version:        2.9.0
Release:        1%{?dist}
Summary:        Git extension for versioning large files

Group:          Applications/Archiving
License:        MIT
URL:            https://git-lfs.github.com/
Source0:        https://github.com/git-lfs/git-lfs/archive/v%{version}/%{name}-%{version}.tar.gz

# build.log
Source1000: %{name}-%{version}-%{release}.build.log

# Update dependencies
Patch1:         git-lfs-2.9.0-update-go-mod.patch
Patch2:         git-lfs-2.9.0-olekukonko-ts-add-AIX-support.patch
Patch3:         git-lfs-2.9.0-fsnotify-fsnotify-add-AIX-support.patch

# Force -mod=vendor in order to take upated dependencies
Patch4:         git-lfs-2.9.0-force-mod-vendor.patch

# Add missing files
Patch5:         git-lfs-2.9.0-add-AIX-support.patch

BuildRequires:  perl(Digest::SHA)
BuildRequires:  golang, tar, git >= 1.8.2

Requires: git >= 1.8.2

%define debug_package %{nil}
#I think this is because go links with --build-id=none for linux

%description
Git Large File Storage (LFS) replaces large files such as audio samples,
videos, datasets, and graphics with text pointers inside Git, while
storing the file contents on a remote server like GitHub.com or GitHub
Enterprise.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
go mod vendor

%patch2 -p1 -d vendor/github.com/olekukonko/ts
%patch3 -p1 -d vendor/github.com/fsnotify/fsnotify
%patch4 -p1
%patch5 -p1


mkdir -p src/github.com/git-lfs
ln -s $(pwd) src/github.com/git-lfs/%{name}

%build

# Reset Go env and force to take /opt/freeware/bin/go
PATH=/opt/freeware/bin:$PATH
unset GOROOT
unset GOPATH

cd  src/github.com/git-lfs/%{name}
make
cd -
# make man

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -D bin/git-lfs ${RPM_BUILD_ROOT}%{_bindir}/git-lfs
# mkdir -p -m 755 ${RPM_BUILD_ROOT}/usr/share/man/man1
# mkdir -p -m 755 ${RPM_BUILD_ROOT}/usr/share/man/man5
# install -D man/*.1 ${RPM_BUILD_ROOT}/usr/share/man/man1
# install -D man/*.5 ${RPM_BUILD_ROOT}/usr/share/man/man5

%post
%{_bindir}/%{name} install --system --skip-repo

%preun
if [ $1 -eq 0 ]; then
    %{_bindir}/%{name} uninstall --system --skip-repo
fi
exit 0

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export GIT_LFS_TEST_DIR=$(mktemp -d)

# test/git-lfs-server-api/main.go does not compile because github.com/spf13/cobra
# cannot be found in vendor, for some reason. It's not needed for installs, so
# skip it.
export SKIPAPITESTCOMPILE=1


# go test -mod=vendor -count=1 ./...
(
	cd src/github.com/git-lfs/%{name}
	make test GO_TEST_EXTRA_ARGS='-mod=vendor'

	# Don't test this subpackages because it don't have updated dependencies
	# go get github.com/git-lfs/go-ntlm/ntlm
	# make -C t PROVE_EXTRA_ARGS=-j4 test
)

rm -rf ${GIT_LFS_TEST_DIR}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md
%{_bindir}/git-lfs
# /usr/share/man/man1/*.1.gz
# /usr/share/man/man5/*.5.gz

%changelog
* Thu Nov 7 2019 Clément Chigot <clement.chigot@atos.net> - 2.9.0-1
- First port on AIX

* Sun Dec 6 2015 Andrew Neff <andyneff@users.noreply.github.com> - 1.1.0-1
- Added Requires and version for git back in

* Sat Oct 31 2015 Andrew Neff <andyneff@users.noreply.github.com> - 1.0.3-1
- Added GIT_LFS_TEST_DIR to prevent future test race condition

* Sun Aug 2 2015 Andrew Neff <andyneff@users.noreply.github.com> - 0.5.4-1
- Added tests back in

* Sat Jul 18 2015 Andrew Neff <andyneff@users.noreply.github.com> - 0.5.2-1
- Changed Source0 filename

* Mon May 18 2015 Andrew Neff <andyneff@users.noreply.github.com> - 0.5.1-1
- Initial Spec
