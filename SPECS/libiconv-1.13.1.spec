Summary: Character Translation Library
Name: libiconv
Version: 1.13.1
Release: 1
License: GNU GPL
Url: http://www.gnu.org/software/libiconv/
Group: Converter
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
Source: http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.13.1.tar.gz

%description 
A character translation library providing the POSIX iconv(3) function.

%prep
%setup -q


%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure --prefix=%{prefix}

make 

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib
cd ${RPM_BUILD_ROOT}/usr/lib
ln -sf ../..%{prefix}/lib/*.a .
cd -
cd ${RPM_BUILD_ROOT}/usr/bin
ln -sf ../..%{prefix}/bin/iconv .
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/iconv
%{prefix}/include/iconv.h
%{prefix}/include/libcharset.h
%{prefix}/include/localcharset.h
%{prefix}/lib/libcharset.a
%{prefix}/lib/libiconv.a
%dir %{prefix}/share/doc
%dir %{prefix}/share/doc/libiconv
%{prefix}/share/doc/libiconv/*.html
%{prefix}/share/locale/*/LC_MESSAGES/*
%{prefix}/share/man/man1/iconv.1
%{prefix}/share/man/man3/*


%changelog
* Thu Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.13.1
- Initial port for AIX
