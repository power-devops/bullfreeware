Summary:	Netscape Portable Runtime
Name:		nspr
Version:	4.7.3
Release: 	1
License:	MPL/GPL/LGPL
URL:		http://www.mozilla.org/projects/nspr/
Group:		System Environment/Libraries
BuildRoot:	/var/tmp/%{name}-root
Prefix:		%{_prefix}
Source:		ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v4.7.3/src/%{name}-%{version}.tar.gz


%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API for system 
level and libc like functions. The API is used in the Mozilla clients and 
many of Red Hat's, Sun's, and other software offerings.

%prep
%setup -q


%build
cd mozilla/nsprpub/
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-Wl,-brtl -L. -L/opt/freeware/lib" \
./configure --enable-optimize --disable-debug  --prefix=/opt/freeware/ \
		--includedir=/opt/freeware/lib --with-pthreads
make
cd pr/tests
make
cd ../..

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# As there aren t any install target to make we will do it manually
mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib
mkdir -p $RPM_BUILD_ROOT%{prefix}/include/private
mkdir -p $RPM_BUILD_ROOT%{prefix}/include/obsolete
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/aclocal

cd mozilla/nsprpub/

cp config/nspr-config $RPM_BUILD_ROOT%{prefix}/bin
cp config/nspr.m4 $RPM_BUILD_ROOT%{prefix}/share/aclocal
cp pr/include/*.h  $RPM_BUILD_ROOT%{prefix}/include
cp pr/include/private/*.h $RPM_BUILD_ROOT%{prefix}/include
cp lib/libc/include/*.h $RPM_BUILD_ROOT%{prefix}/include
cp lib/ds/p*.h $RPM_BUILD_ROOT%{prefix}/include
cp pr/include/md/_aix32.cfg $RPM_BUILD_ROOT%{prefix}/include/prcpucfg.h 
cp pr/include/obsolete/*.h $RPM_BUILD_ROOT%{prefix}/include/obsolete
cp pr/include/private/*.h $RPM_BUILD_ROOT%{prefix}/include/private
cp pr/src/libnspr4.a $RPM_BUILD_ROOT%{prefix}/lib
cp lib/libc/src/libplc4.a $RPM_BUILD_ROOT%{prefix}/lib
cp lib/ds/libplds4.a $RPM_BUILD_ROOT%{prefix}/lib

chmod 644 $RPM_BUILD_ROOT%{prefix}/share/aclocal/nspr.m4
chmod 644 $RPM_BUILD_ROOT%{prefix}/include/*.h
chmod 644 $RPM_BUILD_ROOT%{prefix}/include/private/*.h
chmod 644 $RPM_BUILD_ROOT%{prefix}/include/obsolete/*.h
chmod 755 $RPM_BUILD_ROOT%{prefix}/bin/nspr-config
chmod 755 $RPM_BUILD_ROOT%{prefix}/lib/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{prefix}/bin/nspr-config
%{prefix}/lib/libnspr4.a
%{prefix}/lib/libplc4.a
%{prefix}/lib/libplds4.a
%{prefix}/include/*.h
%{prefix}/include/obsolete/*.h
%{prefix}/include/private/*.h
%{prefix}/share/aclocal/nspr.m4

%changelog
* Wed Feb 18 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.7.3
- Initial port for AIX
