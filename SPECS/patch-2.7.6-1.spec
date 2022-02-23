# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: The GNU patch command, for modifying/upgrading files
Name: patch
Version: 2.7.6
Release: 1
License: GPLv3+
URL: https://savannah.gnu.org/projects/patch/
Source0: https://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz
Source1000: %{name}-%{version}-%{release}.build.log
# Source2:	%{name}-%{version}-strnlen.c

Patch0: patch-2.7.6-avoid-set_file_attributes-sign-conversion-warnings.patch
Patch1: patch-2.7.6-test-suite-compatibility-fixes.patch
Patch2: patch-2.7.6-fix-korn-shell-incompatibility.patch
Patch3: patch-2.7.6-fix-segfault-with-mangled-rename-patch.patch
Patch4: patch-2.7.6-allow-input-files-to-be-missing-for-ed-style-patches.patch
Patch5: patch-2.7.6-CVE-2018-1000156.patch
Patch6: patch-2.7.6-CVE-2019-13638-invoked-ed-directly-instead-of-using-the-shell.patch
Patch7: patch-2.7.6-switch-from-fork-execlp-to-execute.patch
Patch8: patch-2.7.6-cleanups-in-do_ed_script.patch
Patch9: patch-2.7.6-avoid-warnings-gcc8.patch
Patch10: patch-2.7.6-check-of-return-value-of-fwrite.patch
Patch11: patch-2.7.6-fix-ed-style-test-failure.patch
Patch12: patch-2.7.6-dont-leak-temporary-file-on-failed-ed-style-patch.patch
Patch13: patch-2.7.6-dont-leak-temporary-file-on-failed-multi-file-ed-style-patch.patch
Patch14: patch-2.7.6-make-debug-output-more-useful.patch
Patch15: patch-2.7.6-CVE-2018-6952-fix-swapping-fake-lines-in-pch_swap.patch
Patch16: patch-2.7.6-improve_support_for_memory_leak_detection.patch
Patch17: patch-2.7.6-skip-ed-test-when-the-ed-utility-is-not-installed.patch
Patch18: patch-2.7.6-abort_when_cleaning_up_fails.patch
Patch19: patch-2.7.6-crash-RLIMIT_NOFILE.patch
Patch20: patch-2.7.6-CVE-2019-13636-symlinks.patch
Patch21: patch-2.7.6-avoid-invalid-memory-access-in-context-format-diffs.patch
Patch22: patch-2.7.6-CVE-2018-17942.patch
Patch23: patch-2.7.6-failed_assertion.patch

BuildRequires: automake = 1.15.1

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# CVE-2018-1000156, Malicious patch files cause ed to execute arbitrary commands
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
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
# CVE-2018-17942 gnulib: heap-based buffer overflow
%patch22 -p1
%patch23 -p1

# cp %{SOURCE2} gl/lib/strnlen.c

# # fake a <stdbool.h> as AIX5L V5.1 and XLC/C++ V7 doesn't have one
# cat > stdbool.h << EOF
# #ifndef stdbool_h_wrapper
# #define stdbool_h_wrapper

# typedef enum {false = 0, true = 1} bool;

# #endif
# EOF


%build

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export OBJECT_MODE=64
export CC="gcc -maix64"
export CFLAGS=$RPM_OPT_FLAGS

./configure \
    --prefix=%{_prefix}		\
    --mandir=%{_mandir}

make

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

make DESTDIR=${RPM_BUILD_ROOT} install

cd $RPM_BUILD_ROOT%{_prefix}

# Strip all of the executables
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

(make -k check || true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc NEWS README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Wed May 26 2021 Clement Chigot <clement.chigot@atos.net> 2.7.6-1
- Update to version 2.7.6
- BullFreeware Compatibility Improvements
- Rebuild in 64bit only
- Rebuild with RPMv4

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.1-2
- Port on platform Aix6.1

* Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.1-1
- Port on platform Aix5.3

