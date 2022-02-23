%global go_name golang

%global ignore_tests 0
%global gopath %{_datadir}/gocode

# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# also, debuginfo extraction currently fails with
# "Failed to write file: invalid section alignment"
%global debug_package %{nil}

# we are shipping the full contents of src in the data subpackage, which
# contains binary-like things (ELF/DWARF data for tests, etc)
%global _binaries_in_noarch_packages_terminate_build 0

# Do not check any files in doc or src for requires
# %global __requires_exclude_from ^(%{_datadir}|/usr/lib)/%{name}/(doc|src)/.*$
# Remove find-requires calls because __requires_exclude doesn't work and dependencies
# are found in src folder.
%define __find_requires %{nil}

# Don't alter timestamps of especially the .a files (or else go will rebuild later)
# Actually, don't strip at all since we are not even building debug packages and this corrupts the dwarf testdata
%global __strip /bin/true


%global golibdir %{_libdir}/%{go_name}

# Golang build options.

# Build golang with cgo enabled/disabled(later equals more or less to internal linking).
%global cgo_enabled 1

# Use golang/gcc-go as bootstrap compiler
%global golang_bootstrap 1

# Controls what ever we fail on failed tests
%if %{ignore_tests} == 0
%global fail_on_tests 1
%else
%global fail_on_tests 0
%endif

# Build golang shared objects for stdlib
# Not yet implemented on AIX
%global shared 0

# Pre build std lib with -race enabled
# Not yet implemented on AIX
%global race 0


# AIX GOROOT
# Reuse a previous RPM-installed version of golang
%global gorootboot	/opt/freeware/lib/golang/

# Final official installation of golang on AIX
%global goroot		/opt/freeware/lib/%{go_name}

Name:           %{go_name}
Version: 1.17.3
Release: 2
Group:		Development/Languages
Summary:        The Go Programming Language
License:        BSD and Public Domain
URL:            http://golang.org/
BuildArch:      ppc

Source0:        https://go.dev/dl/go%{version}.src.tar.gz

# make possible to override default traceback level at build time by setting build tag rpm_crashtraceback
Source1:        aix.go

# build.log
Source1000: %{name}-%{version}-%{release}.build.log

# Fix linker errors with really huge binaries
Patch1: go-1.16-force-longcall-for-crosscall2.patch

# Fix startfiles for newest GCC versions
Patch2: go-1.16-cmd-link-fix-GCC-startfiles-names-on-AIX.patch

# The compiler is written in Go. Needs go(1.4+) compiler for build.
%if !%{golang_bootstrap}
BuildRequires:  gcc-go >= 5
%else
BuildRequires:  %{name} > 1.4
%endif

# For cp -a used in %install
BuildRequires:  coreutils >= 8.25
# For find used in %install
BuildRequires:  findutils >= 4.4.2
# For file used in %install
BuildRequires:  file >= 5.32
BuildRequires:  file-libs >= 5.32
# For tests
BuildRequires:  pcre-devel
BuildRequires:  perl(perl)

Provides:       go = %{version}-%{release}

# Bundled/Vendored provides generated by bundled-deps.sh based on the in tree module data
# - in version filed substituted with . per versioning guidelines
Provides: bundled(golang(github.com/google/pprof)) = 0.0.0.20201203190320.1bf35d6f28c2
Provides: bundled(golang(github.com/ianlancetaylor/demangle)) = 0.0.0.20200824232613.28f6c0f3b639
Provides: bundled(golang(golang.org/x/arch)) = 0.0.0.20201008161808.52c3e6f60cff
Provides: bundled(golang(golang.org/x/crypto)) = 0.0.0.20201016220609.9e8e0b390897
Provides: bundled(golang(golang.org/x/mod)) = 0.4.1
Provides: bundled(golang(golang.org/x/net)) = 0.0.0.20201209123823.ac852fbbde11
Provides: bundled(golang(golang.org/x/sys)) = 0.0.0.20201204225414.ed752295db88
Provides: bundled(golang(golang.org/x/text)) = 0.3.4
Provides: bundled(golang(golang.org/x/tools)) = 0.0.0.20210107193943.4ed967dd8eff
Provides: bundled(golang(golang.org/x/xerrors)) = 0.0.0.20200804184101.5ec99f83aff1

Requires:       %{name}-bin = %{version}-%{release}
Requires:       %{name}-src = %{version}-%{release}

Source100:      golang-gdbinit

%description
The Go Programming Language source tree v%{version} for AIX 7.2 / Power >= 8.
Some features are not yet available: race detector, shared buildmode.

%package       docs
Summary:       Golang compiler docs
Group:		   Development/Languages
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   docs
%{summary}.


%package       misc
Summary:       Golang compiler miscellaneous sources
Group:		Development/Languages
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   misc
%{summary}.


%package       tests
Summary:       Golang compiler tests for stdlib
Group:		Development/Languages
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   tests
%{summary}.


%package        src
Summary:        Golang compiler source tree
Group:		Development/Languages
BuildArch:      noarch

%description    src
%{summary}


%package        bin
Summary:        Golang core compiler tools
Group:		Development/Languages
#BuildArch:      ppc
Requires:       %{name} = %{version}-%{release}

# For cgo
Requires:       gcc

Recommends:     git, subversion, mercurial
Requires:     diffutils

%description    bin
%{summary}


# Not yet on AIX.
%if %{shared}
%package        shared
Summary:        Golang shared object libraries
Group:		Development/Languages

%description    shared
%{summary}.
%endif


# Not yet on AIX.
%if %{race}
%package        race
Summary:        Golang std library with -race enabled
Group:		Development/Languages

Requires:       %{name} = %{version}-%{release}

%description    race
%{summary}
%endif

%prep
%setup -q -n go

%patch1 -p1
%patch2 -p1

# Äfoo.go and Ämain.go are wrongly renamed by tar during setup.
# This seems to depend where the tarball have been generated. It
# seems to be linked to the format and something else.
# TODO: Find a true fix (OSS tar vs AIX tar ?)
mv test/fixedbugs/issue27836.dir/*foo.go test/fixedbugs/issue27836.dir/Äfoo.go || :
mv test/fixedbugs/issue27836.dir/*main.go test/fixedbugs/issue27836.dir/Ämain.go || :

cp %{SOURCE1} ./src/runtime/

%build

# Required for tests diff (blanks)
export PATH=/opt/freeware/bin:$PATH


# bootstrap compiler GOROOT
%if %{golang_bootstrap} == 0
export GOROOT_BOOTSTRAP=/
%else
export GOROOT_BOOTSTRAP=%{goroot}
%endif

# set up final install location
export GOROOT_FINAL=%{goroot}
export GOHOSTOS=aix
export GOHOSTARCH=ppc64
export GOOS=aix
export GOARCH=ppc64


cd src
# use our gcc options for this build, but store gcc as default for compiler
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
export CC="gcc"
export CC_FOR_TARGET="gcc"

%if !%{cgo_enabled}
export CGO_ENABLED=0
%endif

# In order to prevent golang to fill / (= $HOME for root on AIX)
export GOCACHE=/tmp/.cache/go-build-rpm

type go

go env

# Bootstrap !!
./make.bash --no-clean -v
cd -

# build shared std lib
%if %{shared}
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared -v -x std
%endif

%if %{race}
GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -race -v -x std
%endif




%install
[ "${RPM_BUILD_ROOT}" == ""  ] && exit
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
# remove GC build cache
rm -rf pkg/obj/go-build/*

# For using /opt/freeware/bin/cp  (-a option)
export PATH=/opt/freeware/bin:$PATH

# create the top level directories
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{goroot}

# install everything into libdir (until symlink problems are fixed)
# https://code.google.com/p/go/issues/detail?id=5830
cp -apv api bin doc lib pkg src misc test VERSION	$RPM_BUILD_ROOT%{goroot}

# bz1099206
find $RPM_BUILD_ROOT%{goroot}/src -exec touch -r $RPM_BUILD_ROOT%{goroot}/VERSION "{}" \;
# and level out all the built archives
touch $RPM_BUILD_ROOT%{goroot}/pkg
find $RPM_BUILD_ROOT%{goroot}/pkg -exec touch -r $RPM_BUILD_ROOT%{goroot}/pkg "{}" \;

# Build lists of files
# generate the spec file ownership of this source tree and packages
cwd=$(pwd)
base_list=$cwd/go-base.list
src_list=$cwd/go-src.list
pkg_list=$cwd/go-pkg.list
shared_list=$cwd/go-shared.list
race_list=$cwd/go-race.list
misc_list=$cwd/go-misc.list
docs_list=$cwd/go-docs.list
tests_list=$cwd/go-tests.list
rm -f $src_list $pkg_list $docs_list $misc_list $tests_list $shared_list $race_list
touch $src_list $pkg_list $docs_list $misc_list $tests_list $shared_list $race_list
(
	cd $RPM_BUILD_ROOT%{goroot}
	FWFIND=/opt/freeware/bin/find

    $FWFIND src/   -type d -a \( ! -name testdata -a ! -ipath '*/testdata/*' \)    -printf '%%%dir %{goroot}/%p\n' >> $src_list
    $FWFIND src/ ! -type d -a \( ! -ipath '*/testdata/*' -a ! -name '*_test.go' \) -printf        '%{goroot}/%p\n' >> $src_list

    # $FWFIND bin/ pkg/   -type d -a ! -path '*_dynlink/*' -a ! -path '*_race/*' -printf '%%%dir %{goroot}/%p\n' | grep -v golang/pkg/obj/go-build/ >> $bin_list
    # $FWFIND bin/ pkg/ ! -type d -a ! -path '*_dynlink/*' -a ! -path '*_race/*' -printf        '%{goroot}/%p\n' | grep -v golang/pkg/obj/go-build/ >> $bin_list

    $FWFIND bin/ pkg/ -type d -a ! -path '*_dynlink/*' -a ! -path '*_race/*' -printf '%%%dir %{goroot}/%p\n' >> $pkg_list
    $FWFIND bin/ pkg/ ! -type d -a ! -path '*_dynlink/*' -a ! -path '*_race/*' -printf '%{goroot}/%p\n' >> $pkg_list

    $FWFIND doc/   -type d -printf '%%%dir %{goroot}/%p\n' >> $docs_list
    $FWFIND doc/ ! -type d -printf        '%{goroot}/%p\n' >> $docs_list

    $FWFIND misc/   -type d -printf '%%%dir %{goroot}/%p\n' >> $misc_list
    $FWFIND misc/ ! -type d -printf        '%{goroot}/%p\n' >> $misc_list

%if %{shared}
    mkdir -p %{buildroot}/%{_libdir}/
    mkdir -p %{buildroot}/%{golibdir}/
    for file in $(find .  -iname "*.so" ); do
        chmod 755 $file
        mv  $file %{buildroot}/%{golibdir}
        cd $(dirname $file)
        ln -fs %{golibdir}/$(basename $file) $(basename $file)
        cd -
        echo "%%{goroot}/$file" >> $shared_list
        echo "%%{golibdir}/$(basename $file)" >> $shared_list
    done

    find pkg/*_dynlink/ -type d -printf '%%%dir %{goroot}/%p\n' >> $shared_list
    find pkg/*_dynlink/ ! -type d -printf '%{goroot}/%p\n' >> $shared_list
%endif

%if %{race}

    find pkg/*_race/ -type d -printf '%%%dir %{goroot}/%p\n' >> $race_list
    find pkg/*_race/ ! -type d -printf '%{goroot}/%p\n' >> $race_list

%endif

    $FWFIND test/ -type d -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    $FWFIND test/ ! -type d -printf '%{goroot}/%p\n' >> $tests_list
    $FWFIND src/ -type d -a \( -name testdata -o -ipath '*/testdata/*' \) -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    $FWFIND src/ ! -type d -a \( -ipath '*/testdata/*' -o -name '*_test.go' \) -printf '%{goroot}/%p\n' >> $tests_list
    # this is only the zoneinfo.zip
    $FWFIND lib/ -type d -printf '%%%dir %{goroot}/%p\n' >> $tests_list
    $FWFIND lib/ ! -type d -printf '%{goroot}/%p\n' >> $tests_list
)

# remove the doc Makefile
rm -rfv $RPM_BUILD_ROOT%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in {goroot}
mkdir -p $RPM_BUILD_ROOT%{goroot}/bin/aix_ppc64
ln -sf ../go $RPM_BUILD_ROOT%{goroot}/bin/aix_ppc64/go
ln -sf ../gofmt $RPM_BUILD_ROOT%{goroot}/bin/aix_ppc64/gofmt

# ensure these exist and are owned
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/github.com
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/bitbucket.org
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/code.google.com/p
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/golang.org/x

# Make sure binaries are available in /opt/freeware/bin
# and points to golang go binaries at /opt/freeware/lib/golang/bin
# Their name is changed to go.golang and gofmt.golang in order
# to have both golang and gccgo available on the same machine.
rm -f $RPM_BUILD_ROOT%{_bindir}/go
ln -sn ../lib/golang/bin/go $RPM_BUILD_ROOT%{_bindir}/go.golang
rm -f $RPM_BUILD_ROOT%{_bindir}/gofmt
ln -sn ../lib/golang/bin/gofmt $RPM_BUILD_ROOT%{_bindir}/gofmt.golang

# gdbinit
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
cp -av %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d/golang.gdb


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests


export GOROOT=$(pwd -P)
export PATH="$GOROOT"/bin:"$PATH"
cd src

export CC="gcc"
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"

%if !%{cgo_enabled}
export CGO_ENABLED=0
%endif

# make sure to not timeout
export GO_TEST_TIMEOUT_SCALE=2

%if %{fail_on_tests}
./run.bash --no-rebuild -v -v -v -k
%else
./run.bash --no-rebuild -v -v -v -k || :
%endif
cd ..


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post bin
if [[ -f %{_bindir}/go && ! -L %{_bindir}/go ]]; then
	# Save current go binaries if they are gccgo ones.
	# Provide compatibility with versions before 8.3.0
	if %{_bindir}/go version | grep -q gccgo; then
		mv %{_bindir}/go %{_bindir}/go.gcc
		if [[ -f %{_bindir}/gofmt && ! -L %{_bindir}/gofmt ]]; then
			# We can't check gofmt version, so move it if
			# go is gccgo's binary and gofmt not a link.
			mv %{_bindir}/gofmt %{_bindir}/gofmt.gcc
		fi
	fi
fi

(
	# Create links from default binaries to their .golang name
	cd %{_bindir}
	ln -sf go.golang go
	ln -sf gofmt.golang gofmt
)

%postun bin
if [ $1 = 0 ]; then
	# Remove links to binaries if they're pointing to this RPM binaries
	# And also check go.gcc presence and create links to it
	cd %{_bindir}
    if [[ -s go.gcc ]]; then
		ln -sf go.gcc go
    else
		rm go
    fi
    if [[ -s gofmt.gcc ]]; then
		ln -sf gofmt.gcc gofmt
    else
		rm gofmt
    fi
fi

%pre
# Processor Version: PV_8_Compat
# Processor Version: PV_7_Compat
# Processor Version: PV_6_Compat
ProcVersion=`prtconf | grep "Processor Version:" | awk -F_ '{ print $2}'`
#echo $ProcVersion
if [ $ProcVersion -lt 8 ]
then
        echo "This rpm won't work with Power $ProcVersion compatibiliy mode."
        echo "prtconf: "
        prtconf | grep "Processor Version:"
        exit 1
fi


%files
%defattr(-,root,system,-)

%doc AUTHORS CONTRIBUTORS LICENSE PATENTS
# VERSION has to be present in the GOROOT, for `go install std` to work
%doc %{goroot}/VERSION
%dir %{goroot}/doc

#go files
%dir %{goroot}
%{goroot}/api/
%{goroot}/lib/time/

# ensure directory ownership, so they are cleaned up if empty
%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com/
%dir %{gopath}/src/bitbucket.org/
%dir %{gopath}/src/code.google.com/
%dir %{gopath}/src/code.google.com/p/
%dir %{gopath}/src/golang.org
%dir %{gopath}/src/golang.org/x

# gdbinit (for gdb debugging)
%{_sysconfdir}/gdbinit.d


# /opt/freeware/lib/golang/src
%files -f go-src.list src
%defattr(-,root,system,-)

# /opt/freeware/lib/golang/doc/
%files -f go-docs.list docs
%defattr(-,root,system,-)


# /opt/freeware/lib/golang/misc
%files -f go-misc.list misc
%defattr(-,root,system,-)

# /opt/freeware/lib/golang/test
# /opt/freeware/lib/golang/src
# /opt/freeware/lib/golang/lib/time
%files -f go-tests.list tests
%defattr(-,root,system,-)


%files -f go-pkg.list bin
%defattr(-,root,system,-)
# Add /opt/freeware/bin/ links
%{_bindir}/go.golang
%{_bindir}/gofmt.golang


%if %{shared}
%files -f go-shared.list shared
%defattr(-,root,system,-)
%endif

%if %{race}
%files -f go-race.list race
%defattr(-,root,system,-)
%endif


%changelog
* Mon Nov 29 2021 Clement Chigot <clement.chigot@atos.net> - 1.17.3-2
- Adapt to new URL

* Sun Nov 07 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.17.3-1
- Update to 1.17.3

* Sun Oct 10 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.17.2-1
- Update to 1.17.2

* Sun Sep 12 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.17.1-1
- Update to 1.17.1

* Mon Aug 23 2021 Clement Chigot <clement.chigot@atos.net> - 1.17-1
- Update to version 1.17

* Mon Aug 09 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.7-1
- Update to 1.16.7

* Sun Jul 18 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.6-1
- Update to 1.16.6

* Sun Jun 06 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.5-1
- Update to 1.16.5

* Tue May 11 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.4-1
- Update to 1.16.4

* Fri Apr 02 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.3-1
- Update to 1.16.3

* Fri Mar 12 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.2-1
- Update to 1.16.2

* Wed Feb 17 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16-1
- Update to 1.16

* Thu Jan 28 2021 Clement Chigot <clement.chigot@atos.net> - 1.16rc1-1
- Update to version 1.16rc1

* Mon Jan 04 2021 Clement Chigot <clement.chigot@atos.net> - 1.16beta1-1
- Update to version 1.16beta1

* Fri Dec 04 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.15.6-1
- Update to 1.15.6

* Thu Nov 19 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.15.5-1
- Update to 1.15.5

* Fri Nov 06 2020 Clement Chigot <clement.chigot@atos.net> - 1.15.4-1
- Update specfile for automated build
- Update to version 1.15.4

* Thu Oct 15 2020 Clement Chigot <clement.chigot@atos.net> - 1.15.3-1
- Update to version 1.15.3

* Thu Sep 10 2020 Clement Chigot <clement.chigot@atos.net> - 1.15.2-1
- Update to version 1.15.2
- Fix for #41732

* Wed Sep 09 2020 Clement Chigot <clement.chigot@atos.net> - 1.15.1-1
- Update to version 1.15.1

* Wed Aug 12 2020 Clement Chigot <clement.chigot@atos.net> - 1.15-1
- Update to version 1.15
- Workaround for #40609

* Mon Jul 27 2020 Clement Chigot <clement.chigot@atos.net> - 1.15rc1-1
- Update to version 1.15rc1

* Tue Jun 09 2020 Clement Chigot <clement.chigot@atos.net> - 1.15beta1 - 1
- Update to version 1.15beta1

* Tue Jun 09 2020 Clement Chigot <clement.chigot@atos.net> - 1.14.4 - 1
- Update to version 1.14.4

* Fri Mar 20 2020 Clement Chigot <clement.chigot@atos.net> - 1.14.2 - 1
- Update to version 1.14.2

* Fri Mar 20 2020 Clement Chigot <clement.chigot@atos.net> - 1.14.1 - 1
- Update to version 1.14.1

* Wed Feb 26 2020 Clement Chigot <clement.chigot@atos.net> - 1.14 - 1
- Update to version 1.14

* Mon Feb 10 2020 Clement Chigot <clement.chigot@atos.net> - 1.14rc1 - 1
- Update to version 1.14rc1

* Thu Dec 19 2019 Clement Chigot <clement.chigot@atos.net> - 1.14beta1 - 1
- Update to version 1.14beta1

* Wed Nov 06 2019 Clement Chigot <clement.chigot@atos.net> - 1.13.5 - 1
- Update to version 1.13.5
- Add %defattr

* Wed Nov 06 2019 Clement Chigot <clement.chigot@atos.net> - 1.13.4 - 1
- Update to version 1.13.4
- Move to RPM v4
- Add fix for #35342
- Change git, svn, mercurial hard dependencies to weak ones

* Fri Oct 18 2019 Clement Chigot <clement.chigot@atos.net> - 1.13.3 - 1
- Update to version 1.13.3
- Add fix for #34604

* Thu Sep 26 2019 Clement Chigot <clement.chigot@atos.net> - 1.13.1 - 1
- Update to version 1.13.1

* Tue Sep 10 2019 Clement Chigot <clement.chigot@atos.net> - 1.13 - 1
- Update to version 1.13

* Fri Aug 30 2019 Clement Chigot <clement.chigot@atos.net> - 1.13.rc2 - 1
- Update to version 1.13rc2
- Add %clean

* Thu Jun 27 2019 Clement Chigot <clement.chigot@atos.net> - 1.13beta1 - 1
- Update to version 1.13beta1
- Enable pprof by default

* Thu Jun 13 2019 Clement Chigot <clement.chigot@atos.net> - 1.12.6 - 1
- Update to version 1.12.6

* Mon May 6 2019 Clement Chigot <clement.chigot@atos.net> - 1.12.5 - 1
- Update to version 1.12.5
- Improve runtime, syscall and net packages
- Fix GOROOT generation

* Mon Apr 08 2019 Clement Chigot <clement.chigot@atos.net> - 1.12.2 - 1
- Update to version 1.12.2
- Fix pprof and SIGPROF handling (issue/28555)
- Add c-archive buildmode

* Fri Mar 15 2019 Clement Chigot <clement.chigot@atos.net> - 1.12.1 - 1
- Update to version 1.12.1

* Tue Feb 26 2019 Clement Chigot <clement.chigot@atos.net> - 1.12 - 1
- Update to version 1.12
- Fix diffutils requirement
- Rename go binaries to have both golang and gccgo available

* Tue Feb 12 2019 Clement Chigot <clement.chigot@atos.net> - 1.12rc1 - 1
- Update to version 1.12rc1

* Fri Jan 11 2019 Clement Chigot <clement.chigot@atos.net> - 1.12beta2 - 1
- Update to version 1.12beta2

* Mon Jan 7 2019 Clement Chigot <clement.chigot@atos.net> - 1.12beta1 - 1
- Update to version 1.12beta1

* Mon Dec 17 2018 Clement Chigot <clement.chigot@atos.net> - 1.11.4-1
- Update to version 1.11.4

* Fri Dec 14 2018 Clement Chigot <clement.chigot@atos.net> - 1.11.3-1
- Update to version 1.11.3
- Remove unnecessary dependencies
- Update most of the patches with the official version

* Mon Nov 05 2018 Clement Chigot <clement.chigot@atos.net> - 1.11.2-1
- Updated to version 1.11.2

* Wed Oct 03 2018 Clement Chigot <clement.chigot@atos.net> - 1.11.1-1
- Updated to version 1.11.1

* Fri Aug 31 2018 Tony Reix <tony.reix@atos.net> - 1.11-2
- Prevent RPMs to be installed on Power < 8

* Mon Aug 27 2018 Tony Reix <tony.reix@atos.net> - 1.11-1
- Official version of v1.11 2018/08/25
- First port on AIX 7.2 TL0
- No cgo yet.

* Wed Jun 06 2018 Tony Reix <tony.reix@atos.net> - 1.10.2-1
- First port on AIX 7.2

* Wed May 02 2018 Jakub Čajka <jcajka@redhat.com> - 1.10.2-1
- Rebase to 1.10.2

* Wed Apr 04 2018 Jakub Čajka <jcajka@redhat.com> - 1.10.1-1
- Rebase to 1.10.1
- Resolves: BZ#1562270

* Sat Mar 03 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-2
- Fix CVE-2018-7187
- Resolves: BZ#1546386, BZ#1546388

* Wed Feb 21 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-1
- Rebase to 1.10

* Thu Feb 08 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-0.rc2.1
- Rebase to 1.10rc2
- Fix CVE-2018-6574
- Resolves: BZ#1543561, BZ#1543562

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-0.rc1.1
- Rebase to 1.10rc1

* Fri Jan 12 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-0.beta2.1
- Rebase to 1.10beta2

* Mon Jan 08 2018 Jakub Čajka <jcajka@redhat.com> - 1.10-0.beta1.1
- Rebase to 1.10beta1
- Drop verbose patch as most of it is now implemented by bootstrap tool and is easily toggled by passing -v flag to make.bash

* Thu Oct 26 2017 Jakub Čajka <jcajka@redhat.com> - 1.9.2-1
- Rebase to 1.9.2
- execute correctly pie tests
- allow to ignore tests via bcond
- reduce size of golang package

* Fri Oct 06 2017 Jakub Čajka <jcajka@redhat.com> - 1.9.1-1
- fix CVE-2017-15041 and CVE-2017-15042

* Fri Sep 15 2017 Jakub Čajka <jcajka@redhat.com> - 1.9-1
- bump to the relased version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-0.beta2.1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-0.beta2.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Jakub Čajka <jcajka@redhat.com> - 1.9-0.beta2.1
- bump to beta2

* Thu May 25 2017 Jakub Čajka <jcajka@redhat.com> - 1.8.3-1
- bump to 1.8.3
- fix for CVE-2017-8932
- make possible to use 31bit OID in ASN1
- Resolves: BZ#1454978, BZ#1455191

* Fri Apr 21 2017 Jakub Čajka <jcajka@redhat.com> - 1.8.1-2
- fix uint64 constant codegen on s390x
- Resolves: BZ#1441078

* Tue Apr 11 2017 Jakub Čajka <jcajka@redhat.com> - 1.8.1-1
- bump to Go 1.8.1
- Resolves: BZ#1440345

* Fri Feb 24 2017 Jakub Čajka <jcajka@redhat.com> - 1.8-2
- avoid possibly stale packages due to chacha test file not being test file

* Fri Feb 17 2017 Jakub Čajka <jcajka@redhat.com> - 1.8-1
- bump to released version
- Resolves: BZ#1423637
- Related: BZ#1411242

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-0.rc3.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jakub Čajka <jcajka@redhat.com> - 1.8-0.rc3.2
- make possible to override default traceback level at build time
- add sub-package race containing std lib built with -race enabled
- Related: BZ#1411242

* Fri Jan 27 2017 Jakub Čajka <jcajka@redhat.com> - 1.8-0.rc3.1
- rebase to go1.8rc3
- Resolves: BZ#1411242

* Fri Jan 20 2017 Jakub Čajka <jcajka@redhat.com> - 1.7.4-2
- Resolves: BZ#1404679
- expose IfInfomsg.X__ifi_pad on s390x

* Fri Dec 02 2016 Jakub Čajka <jcajka@redhat.com> - 1.7.4-1
- Bump to 1.7.4
- Resolves: BZ#1400732

* Thu Nov 17 2016 Tom Callaway <spot@fedoraproject.org> - 1.7.3-2
- re-enable the NIST P-224 curve

* Thu Oct 20 2016 Jakub Čajka <jcajka@redhat.com> - 1.7.3-1
- Resolves: BZ#1387067 - golang-1.7.3 is available
- added fix for tests failing with latest tzdata

* Fri Sep 23 2016 Jakub Čajka <jcajka@redhat.com> - 1.7.1-2
- fix link failure due to relocation overflows on PPC64X

* Thu Sep 08 2016 Jakub Čajka <jcajka@redhat.com> - 1.7.1-1
- rebase to 1.7.1
- Resolves: BZ#1374103

* Tue Aug 23 2016 Jakub Čajka <jcajka@redhat.com> - 1.7-1
- update to released version
- related: BZ#1342090, BZ#1357394

* Mon Aug 08 2016 Jakub Čajka <jcajka@redhat.com> - 1.7-0.3.rc5
- Obsolete golang-vet and golang-cover from golang-googlecode-tools package
  vet/cover binaries are provided by golang-bin rpm (thanks to jchaloup)
- clean up exclusive arch after s390x boostrap
- resolves: #1268206

* Wed Aug 03 2016 Jakub Čajka <jcajka@redhat.com> - 1.7-0.2.rc5
- rebase to go1.7rc5
- Resolves: BZ#1342090

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-0.1.rc2
- https://fedoraproject.org/wiki/Changes/golang1.7

* Tue Jul 19 2016 Jakub Čajka <jcajka@redhat.com> - 1.7-0.0.rc2
- rebase to 1.7rc2
- added s390x build
- improved shared lib packaging
- Resolves: bz1357602 - CVE-2016-5386
- Resolves: bz1342090, bz1342090

* Tue Apr 26 2016 Jakub Čajka <jcajka@redhat.com> - 1.6.2-1
- rebase to 1.6.2
- Resolves: bz1329206 - golang-1.6.2.src is available

* Wed Apr 13 2016 Jakub Čajka <jcajka@redhat.com> - 1.6.1-1
- rebase to 1.6.1
- Resolves: bz1324344 - CVE-2016-3959
- Resolves: bz1324951 - prelink is gone, /etc/prelink.conf.d/* is no longer used
- Resolves: bz1326366 - wrong epoll_event struct for ppc64le/ppc64

* Mon Feb 22 2016 Jakub Čajka <jcajka@redhat.com> - 1.6-1
- Resolves: bz1304701 - rebase to go1.6 release
- Resolves: bz1304591 - fix possible stack miss-alignment in callCgoMmap

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Jakub Čajka <jcajka@redhat.com> - 1.6-0.2.rc1
- disabled cgo and external linking on ppc64

* Thu Jan 28 2016 Jakub Čajka <jcajka@redhat.com> - 1.6-0.1.rc1
- Resolves bz1292640, rebase to pre-release 1.6
- bootstrap for PowerPC
- fix rpmlint errors/warning

* Thu Jan 14 2016 Jakub Čajka <jcajka@redhat.com> - 1.5.3-1
- rebase to 1.5.3
- resolves bz1293451, CVE-2015-8618
- apply timezone patch, avoid using bundled data
- print out rpm build system info

* Fri Dec 11 2015 Jakub Čajka <jcajka@redhat.com> - 1.5.2-2
- bz1290543 Accept x509 certs with negative serial

* Tue Dec 08 2015 Jakub Čajka <jcajka@redhat.com> - 1.5.2-1
- bz1288263 rebase to 1.5.2
- spec file clean up
- added build options
- scrubbed "Project Gutenberg License"

* Mon Oct 19 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5.1-1
- bz1271709 include patch from upstream fix

* Wed Sep 09 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5.1-0
- update to go1.5.1

* Fri Sep 04 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-8
- bz1258166 remove srpm macros, for go-srpm-macros

* Thu Sep 03 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-7
- bz1258166 remove srpm macros, for go-srpm-macros

* Thu Aug 27 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-6
- starting a shared object subpackage. This will be x86_64 only until upstream supports more arches shared objects.

* Thu Aug 27 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-5
- bz991759 gdb path fix

* Wed Aug 26 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-4
- disable shared object until linux/386 is ironned out
- including the test/ directory for tests

* Tue Aug 25 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-3
- bz1256910 only allow the golang zoneinfo.zip to be used in tests
- bz1166611 add golang.org/x directory
- bz1256525 include stdlib shared object. This will let other libraries and binaries
  build with `go build -buildmode=shared -linkshared ...` or similar.

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.5-2
- Enable aarch64
- Minor cleanups

* Thu Aug 20 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-1
- updating to go1.5

* Thu Aug 06 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.11.rc1
- fixing the sources reference

* Thu Aug 06 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.10.rc1
- updating to go1.5rc1
- checks are back in place

* Tue Aug 04 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.9.beta3
- pull in upstream archive/tar fix

* Thu Jul 30 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.8.beta3
- updating to go1.5beta3

* Thu Jul 30 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.7.beta2
- add the patch ..

* Thu Jul 30 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.5-0.6.beta2
- increase ELFRESERVE (bz1248071)

* Tue Jul 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.5-0.5.beta2
- correct package version and release tags as per naming guidelines

* Fri Jul 17 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.99-4.1.5beta2
- adding test output, for visibility

* Fri Jul 10 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.99-3.1.5beta2
- updating to go1.5beta2

* Fri Jul 10 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.99-2.1.5beta1
- add checksum to sources and fixed one patch

* Fri Jul 10 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.99-1.1.5beta1
- updating to go1.5beta1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.2-2
- obsoleting deprecated packages

* Wed Feb 18 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.2-1
- updating to go1.4.2

* Fri Jan 16 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4.1-1
- updating to go1.4.1

* Fri Jan 02 2015 Vincent Batts <vbatts@fedoraproject.org> - 1.4-2
- doc organizing

* Thu Dec 11 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.4-1
- update to go1.4 release

* Wed Dec 03 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.99-3.1.4rc2
- update to go1.4rc2

* Mon Nov 17 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.99-2.1.4rc1
- update to go1.4rc1

* Thu Oct 30 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.99-1.1.4beta1
- update to go1.4beta1

* Thu Oct 30 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.3-3
- macros will need to be in their own rpm

* Fri Oct 24 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.3-2
- split out rpm macros (bz1156129)
- progress on gccgo accomodation

* Wed Oct 01 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.3-1
- update to go1.3.3 (bz1146882)

* Mon Sep 29 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.2-1
- update to go1.3.2 (bz1147324)

* Thu Sep 11 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.1-3
- patching the tzinfo failure

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3.1-1
- update to go1.3.1

* Wed Aug 13 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-11
- merged a line wrong

* Wed Aug 13 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-10
- more work to get cgo.a timestamps to line up, due to build-env
- explicitly list all the files and directories for the source and packages trees
- touch all the built archives to be the same

* Mon Aug 11 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-9
- make golang-src 'noarch' again, since that was not a fix, and takes up more space

* Mon Aug 11 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-8
- update timestamps of source files during %%install bz1099206

* Fri Aug 08 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-7
- update timestamps of source during %%install bz1099206

* Wed Aug 06 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-6
- make the source subpackage arch'ed, instead of noarch

* Mon Jul 21 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-5
- fix the writing of pax headers

* Tue Jul 15 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-4
- fix the loading of gdb safe-path. bz981356

* Tue Jul 08 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-3
- `go install std` requires gcc, to build cgo. bz1105901, bz1101508

* Mon Jul 07 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-2
- archive/tar memory allocation improvements

* Thu Jun 19 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3-1
- update to go1.3

* Fri Jun 13 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.3rc2-1
- update to go1.3rc2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3rc1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Vincent Batts <vbatts@redhat.com> 1.3rc1-1
- update to go1.3rc1
- new arch file shuffling

* Wed May 21 2014 Vincent Batts <vbatts@redhat.com> 1.3beta2-1
- update to go1.3beta2
- no longer provides go-mode for xemacs (emacs only)

* Wed May 21 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-7
- bz1099206 ghost files are not what is needed

* Tue May 20 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-6
- bz1099206 more fixing. The packages %%post need golang-bin present first

* Tue May 20 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-5
- bz1099206 more fixing. Let go fix its own timestamps and freshness

* Tue May 20 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-4
- fix the existence and alternatives of `go` and `gofmt`

* Mon May 19 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-3
- bz1099206 fix timestamp issue caused by koji builders

* Fri May 09 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-2
- more arch file shuffling

* Fri May 09 2014 Vincent Batts <vbatts@redhat.com> 1.2.2-1
- update to go1.2.2

* Thu May 08 2014 Vincent Batts <vbatts@redhat.com> 1.2.1-8
- RHEL6 rpm macros can't %%exlude missing files

* Wed May 07 2014 Vincent Batts <vbatts@redhat.com> 1.2.1-7
- missed two arch-dependent src files

* Wed May 07 2014 Vincent Batts <vbatts@redhat.com> 1.2.1-6
- put generated arch-dependent src in their respective RPMs

* Fri Apr 11 2014 Vincent Batts <vbatts@redhat.com> 1.2.1-5
- skip test that is causing a SIGABRT on fc21 bz1086900

* Thu Apr 10 2014 Vincent Batts <vbatts@fedoraproject.org> 1.2.1-4
- fixing file and directory ownership bz1010713

* Wed Apr 09 2014 Vincent Batts <vbatts@fedoraproject.org> 1.2.1-3
- including more to macros (%%go_arches)
- set a standard goroot as /usr/lib/golang, regardless of arch
- include sub-packages for compiler toolchains, for all golang supported architectures

* Wed Mar 26 2014 Vincent Batts <vbatts@fedoraproject.org> 1.2.1-2
- provide a system rpm macros. Starting with gopath

* Tue Mar 04 2014 Adam Miller <maxamillion@fedoraproject.org> 1.2.1-1
- Update to latest upstream

* Thu Feb 20 2014 Adam Miller <maxamillion@fedoraproject.org> 1.2-7
- Remove  _BSD_SOURCE and _SVID_SOURCE, they are deprecated in recent
  versions of glibc and aren't needed

* Wed Feb 19 2014 Adam Miller <maxamillion@fedoraproject.org> 1.2-6
- pull in upstream archive/tar implementation that supports xattr for
  docker 0.8.1

* Tue Feb 18 2014 Vincent Batts <vbatts@redhat.com> 1.2-5
- provide 'go', so users can yum install 'go'

* Fri Jan 24 2014 Vincent Batts <vbatts@redhat.com> 1.2-4
- skip a flaky test that is sporadically failing on the build server

* Thu Jan 16 2014 Vincent Batts <vbatts@redhat.com> 1.2-3
- remove golang-godoc dependency. cyclic dependency on compiling godoc

* Wed Dec 18 2013 Vincent Batts <vbatts@redhat.com> - 1.2-2
- removing P224 ECC curve

* Mon Dec 2 2013 Vincent Batts <vbatts@fedoraproject.org> - 1.2-1
- Update to upstream 1.2 release
- remove the pax tar patches

* Tue Nov 26 2013 Vincent Batts <vbatts@redhat.com> - 1.1.2-8
- fix the rpmspec conditional for rhel and fedora

* Thu Nov 21 2013 Vincent Batts <vbatts@redhat.com> - 1.1.2-7
- patch tests for testing on rawhide
- let the same spec work for rhel and fedora

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 1.1.2-6
- don't symlink /usr/bin out to ../lib..., move the file
- seperate out godoc, to accomodate the go.tools godoc

* Fri Sep 20 2013 Adam Miller <maxamillion@fedoraproject.org> - 1.1.2-5
- Pull upstream patches for BZ#1010271
- Add glibc requirement that got dropped because of meta dep fix

* Fri Aug 30 2013 Adam Miller <maxamillion@fedoraproject.org> - 1.1.2-4
- fix the libc meta dependency (thanks to vbatts [at] redhat.com for the fix)

* Tue Aug 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 1.1.2-3
- Revert incorrect merged changelog

* Tue Aug 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 1.1.2-2
- This was reverted, just a placeholder changelog entry for bad merge

* Tue Aug 20 2013 Adam Miller <maxamillion@fedoraproject.org> - 1.1.2-1
- Update to latest upstream

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.1.1-6
- Perl 5.18 rebuild

* Wed Jul 10 2013 Adam Goode <adam@spicenitz.org> - 1.1.1-5
- Blacklist testdata files from prelink
- Again try to fix #973842

* Fri Jul  5 2013 Adam Goode <adam@spicenitz.org> - 1.1.1-4
- Move src to libdir for now (#973842) (upstream issue https://code.google.com/p/go/issues/detail?id=5830)
- Eliminate noarch data package to work around RPM bug (#975909)
- Try to add runtime-gdb.py to the gdb safe-path (#981356)

* Wed Jun 19 2013 Adam Goode <adam@spicenitz.org> - 1.1.1-3
- Use lua for pretrans (http://fedoraproject.org/wiki/Packaging:Guidelines#The_.25pretrans_scriptlet)

* Mon Jun 17 2013 Adam Goode <adam@spicenitz.org> - 1.1.1-2
- Hopefully really fix #973842
- Fix update from pre-1.1.1 (#974840)

* Thu Jun 13 2013 Adam Goode <adam@spicenitz.org> - 1.1.1-1
- Update to 1.1.1
- Fix basically useless package (#973842)

* Sat May 25 2013 Dan Horák <dan[at]danny.cz> - 1.1-3
- set ExclusiveArch

* Fri May 24 2013 Adam Goode <adam@spicenitz.org> - 1.1-2
- Fix noarch package discrepancies

* Fri May 24 2013 Adam Goode <adam@spicenitz.org> - 1.1-1
- Initial Fedora release.
- Update to 1.1

* Thu May  9 2013 Adam Goode <adam@spicenitz.org> - 1.1-0.3.rc3
- Update to rc3

* Thu Apr 11 2013 Adam Goode <adam@spicenitz.org> - 1.1-0.2.beta2
- Update to beta2

* Tue Apr  9 2013 Adam Goode <adam@spicenitz.org> - 1.1-0.1.beta1
- Initial packaging.
