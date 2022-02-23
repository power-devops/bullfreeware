Summary: GNU a2ps is an Any to PostScript filter.
Name: a2ps
Version: 4.13
Release: 2
Copyright: GPL
Group: Applications/Archiving
Source: a2ps-%{version}b.tar.gz
Prefix: %{_prefix}
#Patch0: a2ps-%{version}-lt135a.patch
BuildRoot: /var/tmp/a2ps-root
Requires: info

%ifarch ia64
  %define stdlib lib/ia64l32
  %define liblink ../../..
  %define DEFCCIA cc
  %define DEFCC %{DEFCCIA}
%else
  %define stdlib lib
  %define liblink ../..
  %define DEFCC cc
%endif

%description
GNU a2ps is an Any to PostScript filter.  Of course it processes plain
text files, but also pretty prints quite a few popular languages.

Install the a2ps package if you need to convert files to PostScript.

%prep
%setup -q 
#%patch0 -p1 -b .lt135a

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else 
       export CC=gcc
    fi
fi
libtoolize --force
./configure --prefix=%{_prefix} #--enable-shared
make 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/man/man1

make prefix=$RPM_BUILD_ROOT%{_prefix} install

cd $RPM_BUILD_ROOT
gzip -9nf .%{_prefix}/info/*.info*

# Strip the executables
/usr/bin/strip $RPM_BUILD_ROOT%{_prefix}/bin/* || :

# Let's also check it -- i.e., run the tests
# make check


( cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir etc
 cd etc
 ln -sf ..%{_prefix}/etc/* .
 cd -

 mkdir -p usr/%{stdlib}
 cd usr/%{stdlib}
 ln -sf %{liblink}%{prefix}/lib/* .
)

%post
/sbin/install-info %{_prefix}/info/a2ps.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/ogonkify.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/regex.info.gz %{_prefix}/info/dir


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/a2ps.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/ogonkify.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/regex.info.gz %{_prefix}/info/dir
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ABOUT-NLS ANNOUNCE COPYING AUTHORS FAQ NEWS THANKS TODO
%{_prefix}/bin/*
%{_prefix}/etc/*
%{_prefix}/include/*
%{_prefix}/info/a2ps.info*
%{_prefix}/info/ogonkify.info*
%{_prefix}/info/regex.info*
%{_prefix}/lib/*
%{_prefix}/man/*
%{_prefix}/share/*
/usr/bin/*
/usr/%{stdlib}/*
/etc/*
/usr/include/*

%changelog
* Thu Feb 28 2002 David Clissold <cliss@austin.ibm.com>
- Fix bug in the %postun

* Thu Aug 23 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 4.13b

* Wed Mar 21 2001 David Clissold <cliss@austin.ibm.com>
- Correction to the IA64 lib links

* Wed Mar 07 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Update to libtool 1.3.5a

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Sun Feb 04 2001 David Clissold <aixtoolbox-l@austin.ibm.com>
- Initial version, for AIX
