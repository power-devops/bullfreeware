Summary: A utility for determining file types
Name: file
Version: 5.11
Release: 1
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
AutoReqProv:    no

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package libs
Summary: Libraries for applications using libmagic
Group:   Applications/File

%description libs

Libraries for applications using libmagic.

The library is available as 32-bit and 64-bit.

%package devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q

%build
# setup environment for 32-bit and 64-bit
export AR="/usr/bin/ar -X32_64"        
export NM="/usr/bin/nm -X32_64" 

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# first build the 64-bit version 
CFLAGS="-q64 -I/opt/freeware/include/ -D_ALL_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"  \
CPPFLAGS='-I/opt/freeware/include' \
./configure --prefix=%{_prefix} \
	   --mandir=%{_mandir} \
           --enable-fsect-man5
gmake

cp src/.libs/libmagic.so.1 .

make distclean

# now build the 32-bit version
CFLAGS="-I/opt/freeware/include/ -D_ALL_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"  \
CPPFLAGS='-I/opt/freeware/include' \
./configure --prefix=%{_prefix} \
	   --mandir=%{_mandir} \
           --enable-fsect-man5
gmake

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
# avoid "busy" error messages...
slibclean
${AR} -q  src/.libs/libmagic.a ./libmagic.so.1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/%{name}/magic

( 
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -sf ../../..%{_bindir}/* .
) 

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
/usr/linux/bin/*

%files libs
%defattr(-,root,system,-)
%{_libdir}/*.a
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/%{name}
%{_datadir}/misc/*
/usr/lib/*.a

%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_mandir}/man3/*
/usr/include/*

%changelog
* Thu Mar 29 2012 Patricia Cugny <patricia.cugny@bull.net>  5.11-1
- update to version 5.11

* Fri Mar 13 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.00-1
- port to AIX

