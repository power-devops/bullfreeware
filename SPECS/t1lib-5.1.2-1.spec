Name:       t1lib
Version:    5.1.2
Release:    1

Summary:   PostScript Type 1 font rasterizer

Group:     Applications/Publishing
License:   LGPL
URL:       ftp://sunsite.unc.edu/pub/Linux/libs/graphics
Source:    ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.tar.gz
# Patches taken from Debian and adapted for AIX
Patch0:    t1lib-5.1.1-manpages.patch
Patch1:    t1lib-5.1.1-xglyph-env.patch
Patch2:    t1lib-5.1.1-t1libconfig.patch
Patch3:    %{name}-%{version}-aixconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
T1lib is a rasterizer library for Adobe Type 1 Fonts. It supports
rotation and transformation, kerning underlining and antialiasing. It
does not depend on X11, but does provides some special functions for
X11.

AFM-files can be generated from Type 1 font files and font subsetting
is possible.

The library is available as 32-bit and 64-bit.


%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and static libraries for %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1 -b .aixconf


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared --enable-static
make without_doc

cp lib/.libs/libt1.so.5 .
cp lib/.libs/libt1x.so.5 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared --enable-static
make without_doc

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q lib/.libs/libt1.a ./libt1.so.5
${AR} -q lib/.libs/libt1x.a ./libt1x.so.5


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT prefix=$RPM_BUILD_ROOT/%{_prefix}
#make install prefix=$RPM_BUILD_ROOT/%{_prefix}
make install DESTDIR=$RPM_BUILD_ROOT

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q $RPM_BUILD_ROOT%{_libdir}/libt1x.a ./libt1x.so.5

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/
cp debian/type1afm.1 $RPM_BUILD_ROOT%{_mandir}/man1/
cp debian/xglyph.1 $RPM_BUILD_ROOT%{_mandir}/man1/
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man1/*
cp debian/FontDataBase.5 $RPM_BUILD_ROOT%{_mandir}/man5/
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man5/*
cp debian/t1libconfig.8 $RPM_BUILD_ROOT%{_mandir}/man8/
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man8/*

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
cp debian/t1libconfig $RPM_BUILD_ROOT%{_sbindir}/
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/t1libconfig

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/t1lib
cp examples/FontDataBase $RPM_BUILD_ROOT%{_sysconfdir}/t1lib/
cp lib/t1lib.config $RPM_BUILD_ROOT%{_sysconfdir}/t1lib/
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/t1lib/*


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system,-)
%doc Changes LGPL LICENSE README.t1lib-5.1.2
%dir %{_sysconfdir}/t1lib
%config %{_sysconfdir}/t1lib/t1lib.config
%config %{_sysconfdir}/t1lib/FontDataBase
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%{_libdir}/*.a

%files devel
%defattr(-,root,system,-)
%doc doc/t1lib_doc.pdf
%{_includedir}/*
%{_libdir}/*.la


%changelog
* Fri Feb 01 2008 Michael Perzl <michael@perzl.org> - 5.1.2-1
- updated to 5.1.2

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 5.1.1-2
- included both 32-bit and 64-bit shared objects

* Tue Aug 14 2007 Michael Perzl <michael@perzl.org> - 5.1.1-1
- updated to 5.1.1

* Wed Jan 04 2006 Michael Perzl <michael@perzl.org> - 5.1.0-1
- first version for AIX V5.1 and higher
