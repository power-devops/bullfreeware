%define _libdir64 %{_prefix}/lib64

Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.5.35
Release: 2
License: BSD
Group: Development/Tools
URL: http://flex.sourceforge.net/
Source0: %{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}-aix.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: gettext m4
Requires: /sbin/install-info, info, gettext

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.


%prep
%setup -q
%patch0

mkdir ../32bit
mv * .indent.pro ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 32bit/.indent.pro 64bit

%build

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"

cd 64bit

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir64}
make

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}
make


%install
export RM="/usr/bin/rm -f"

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} prefix=%{_prefix} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32

make DESTDIR=${RPM_BUILD_ROOT} prefix=%{_prefix} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/%{name}.info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_libdir}/libl.a
 
  for dir in usr/bin usr/lib usr/lib64 usr/include usr/linux/bin usr/linux/lib usr/linux/lib64
  do
    [ -d ${dir} ] || mkdir -p ${dir}
  done

  cd usr/linux/bin
  ln -sf ../../..%{_bindir}/flex lex
  ln -sf ../../..%{_bindir}/flex_64 flex_64
  cd ../lib
  ln -sf ../../..%{_libdir}/libfl.a libl.a
  cd ../lib64
  ln -sf ../../..%{_libdir64}/libfl.a libl.a
  cd ../../bin
  ln -sf ../..%{_bindir}/flex .
  ln -sf ../..%{_bindir}/flex_64 .
  ln -sf ../..%{_bindir}/flex++ .
  ln -sf ../..%{_bindir}/flex++_64 .
  cd ../include
  ln -sf ../..%{_includedir}/* .
  cd ../lib
  ln -sf ../..%{_libdir}/libfl.a .
  cd ../lib64
  ln -sf ../..%{_libdir64}/libfl.a .
)

%post
/sbin/install-info %{_infodir}/%{name}.info.gz --dir-file=%{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir ||:
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc 32bit/COPYING 32bit/NEWS 32bit/README
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/*
%{_libdir64}/*
%{_includedir}/*
%{_infodir}/*
%{_datadir}/locale/*/*/*
/usr/bin/*
/usr/lib/*
/usr/lib64/*
/usr/include/*
/usr/linux/bin/*
/usr/linux/lib/*
/usr/linux/lib64/*


%changelog
* Fri Mar 16 2012 Gerard Visiedo <gerard.visiedo@bull.net> -- 2.5.35-2
-  Add lib64 libraries

* Tue May 25 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net>
- Update to version 2.5.35

* Thu Jul 10 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM VAC compiler for better size and performance.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Mar 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler

* Wed Feb 28 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Fix minor error in install section of previous patch

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI
