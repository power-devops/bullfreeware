Summary: The GNU data compression program.
Name: gzip
Version: 1.6
Release: 2
Copyright: GPL
Group: Applications/File
Source: ftp://prep.ai.mit.edu/pub/gnu/gzip-%{version}.tar.gz
#Patch0: gzip-%version-dirinfo.patch
Prereq: /sbin/install-info
Buildroot: /var/tmp/gzip-root

BuildRequires: grep
Requires: grep

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.

Gzip should be installed on your Red Hat Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
#%patch0 -p1 -b .infodir

%build
# /opt/freeware/bin must be first for finding the BullFreeware grep which has a different Usage
export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/local/bin:.
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

./configure --prefix=%{_prefix}
gmake CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"

(gmake -k check || true)

%clean 
rm -rf $RPM_BUILD_ROOT


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/info

gmake DESTDIR=${RPM_BUILD_ROOT}	\
	prefix=%{_prefix} \
	mandir=%{_prefix}/share/man \
	infodir=%{_prefix}/share/info \
	install

/usr/bin/strip $RPM_BUILD_ROOT%{_prefix}/bin/gzip
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/linux/bin
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/share/info/gzip.info*

for i in zcmp zdiff zforce zgrep zmore znew ; do
        sed -e "s|$RPM_BUILD_ROOT||g" < $RPM_BUILD_ROOT%{_prefix}/bin/$i > $RPM_BUILD_ROOT%{_prefix}/bin/.$i
        rm -f $RPM_BUILD_ROOT%{_prefix}/bin/$i
        mv $RPM_BUILD_ROOT%{_prefix}/bin/.$i $RPM_BUILD_ROOT%{_prefix}/bin/$i
        chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/$i
done

cat > $RPM_BUILD_ROOT%{_prefix}/bin/zless <<EOF
#!/bin/sh
%{_prefix}/bin/zcat "\$@" | %{_prefix}/bin/less
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/zless

cd $RPM_BUILD_ROOT/usr/linux/bin
ln -sf ../../..%{_prefix}/bin/* .

cd $RPM_BUILD_ROOT/usr/bin
ln -sf ../..%{_prefix}/bin/* $RPM_BUILD_ROOT/usr/bin
rm $RPM_BUILD_ROOT/usr/bin/zcat
# Don't overwrite the AIX version of uncompress !!!
rm $RPM_BUILD_ROOT/usr/bin/uncompress

%post
/sbin/install-info %{_prefix}/share/info/gzip.info.gz %{_prefix}/share/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/share/info/gzip.info.gz %{_prefix}/share/info/dir
fi

%files
%doc NEWS README
/usr/bin/*
/usr/linux/bin/*
%{_prefix}/bin/*
%{_prefix}/share/man/*/*
%{_prefix}/share/info/gzip.info*

%changelog
* Fri Apr 20 2016 Tony Reix <tony.reix@atos.net> 1.6
- Don't overwrite /usr/bin/uncompress from AIX !

* Fri Jan 8 2015 Tony Reix <tony.reix@atos.net> 1.6
- Initial port on AIX 61

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.4-2
- Initial port on Aix61

* Tue Jun 1 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.4
- update to version 1.4
