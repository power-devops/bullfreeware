Summary: A text file browser similar to more, but better
Name: less
Version: 429
Release: 1
License: GPL v3
Url: http://www.greenwoodsoftware.com/less/
Group: Applications/Text
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
Source: http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz 

%description 
Less is a pager. A pager is a program that displays text files. Other
pagers commonly in use are more and pg. Pagers are often used in
command-line environments like the Unix shell and the MS-DOS command
prompt to display files. Windowed environments like the Windows and
Macintosh desktops don't need pagers as much, since they have other
methods for viewing files.

Less is not an editor. You can't change the contents of the file you're
viewing. Less is not a windowing system. It doesn't have fancy scroll
bars or other GUI (graphical user interface) elements. It was designed
to work on simple text-only terminals. 

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/bin
cd $RPM_BUILD_ROOT/usr/bin
ln -sf ../..%{_prefix}/bin/* .
cd -

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/less
%{_bindir}/lesskey
%{_bindir}/lessecho
/usr/bin/*
%{_prefix}/share/man/man1/less.1
%{_prefix}/share/man/man1/lesskey.1
%{_prefix}/share/man/man1/lessecho.1

%changelog
* Wed Jun 24 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 429
- port of version 429 for AIX
