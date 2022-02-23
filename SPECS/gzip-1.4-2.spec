Summary: The GNU data compression program.
Name: gzip
Version: 1.4
Release: 2
Copyright: GPL
Group: Applications/File
Source: ftp://prep.ai.mit.edu/pub/gnu/gzip-%{version}.tar.gz
#Patch0: gzip-%version-dirinfo.patch
Prereq: /sbin/install-info
Buildroot: /var/tmp/gzip-root

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.

Gzip should be installed on your Red Hat Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
#%patch0 -p1 -b .infodir

%build
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
make CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/man
make prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
	infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
	install
/usr/bin/strip $RPM_BUILD_ROOT%{_prefix}/bin/gzip
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/linux/bin
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/info/gzip.info*

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

%post
/sbin/install-info %{_prefix}/info/gzip.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/gzip.info.gz %{_prefix}/info/dir
fi

%files
%doc NEWS README
/usr/bin/*
/usr/linux/bin/*
%{_prefix}/bin/*
%{_prefix}/man/*/*
%{_prefix}/info/gzip.info*

%changelog
* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.4-2
- Initial port on Aix61

* Tue Jun 1 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.4
- update to version 1.4
