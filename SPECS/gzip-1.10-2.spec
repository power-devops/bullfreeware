# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: The GNU data compression program.
Name: gzip
Version: 1.10
Release: 2
License: GPLv3+ and GFDL
Source0: http://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.xz
Source1000:	%{name}-%{version}-%{release}.build.log

BuildRequires: grep
Requires: grep

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%prep
%setup -q

%build
# /opt/freeware/bin must be first for finding the BullFreeware grep which has a different Usage
export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/local/bin:.
export AR="/usr/bin/ar -X32_64"
export AR="/usr/bin/ar -X32_64"
export CC="gcc -maix64"
export CFLAGS=$RPM_OPT_FLAGS

./configure \
    --prefix=%{_prefix}		\
    --infodir=%{_infodir}	\
    --mandir=%{_mandir}

make


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

make DESTDIR=${RPM_BUILD_ROOT} install

cd $RPM_BUILD_ROOT%{_prefix}

# Strip all of the executables
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/gzip.info*

# for i in zcmp zdiff zforce zgrep zmore znew ; do
#         sed -e "s|$RPM_BUILD_ROOT||g" < $RPM_BUILD_ROOT%{_prefix}/bin/$i > $RPM_BUILD_ROOT%{_prefix}/bin/.$i
#         rm -f $RPM_BUILD_ROOT%{_prefix}/bin/$i
#         mv $RPM_BUILD_ROOT%{_prefix}/bin/.$i $RPM_BUILD_ROOT%{_prefix}/bin/$i
#         chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/$i
# done

# cat > $RPM_BUILD_ROOT%{_prefix}/bin/zless <<EOF
# #!/bin/sh
# %{_prefix}/bin/zcat "\$@" | %{_prefix}/bin/less
# EOF
# chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/zless

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

(gmake -k check || true)

%post
/sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir || :

# Make sure to restore links between /usr/bin and /usr/opt/rpm as
# they were before being overwritten by our previous versions.
for f in gunzip gzexe gzip zcmp zdiff zegrep zfgrep zforce zless zmore znew; do
    if ! test -e /usr/bin/$f; then
	ln -s /usr/opt/freeware/bin/$f /usr/bin/$f
    fi
done

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
%{_bindir}/*
%{_mandir}/*
%{_infodir}/*

%changelog
* Mon May 31 2021 Clément Chigot <clement.chigot@atos.net> 1.10-2
- Make sure previous /bin links are restored as default

* Tue May 25 2021 Clément Chigot <clement.chigot@atos.net> 1.10-1
- Update to version 1.10
- BullFreeware Compatibility Improvements
- Rebuild in 64bit
- Rebuild with RPMv4

* Wed Aug 03 2016 Jean Girardet <Jean.Girardet@atos.net> 1.8-1
- Initial port on AIX 6.1

* Wed Apr 20 2016 Tony Reix <tony.reix@atos.net> 1.6
- Don't overwrite /usr/bin/uncompress from AIX !

* Thu Jan 8 2015 Tony Reix <tony.reix@atos.net> 1.6
- Initial port on AIX 61

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.4-2
- Initial port on Aix61

* Tue Jun 1 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.4
- update to version 1.4
