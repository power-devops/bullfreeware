Summary: A utility for determining file types
Name: file
Version: 5.00
Release: 1
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/
Patch0: file-4.21-pybuild.patch
Patch1: file-5.00-devdrv.patch
Patch2: file-5.00-non-english-word.patch
Patch3: file-5.00-thumbs-db.patch
Patch4: file-5.0-aixconf.patch
Patch5: file-5.0-magic-null_issue.patch

#Requires: file-libs = %{version}-%{release}
BuildRoot: /var/tmp/%{name}-root
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

#aix specific patches
%patch4 -p1
%patch5 -p1


%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L. -L.libs/ -L/opt/freeware/lib" \
./configure --prefix=%{_prefix}

# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/src/.libs
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc

make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}%{_prefix}/lib/*.la

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/file/magic
ln -s file/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
#ln -s file/magic.mime ${RPM_BUILD_ROOT}%{_datadir}/magic.mime
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/misc/magic

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_bindir}/*
%{_datadir}/man/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_datadir}/magic*
%{_datadir}/man/man4/*
%{_datadir}/file/*
%{_datadir}/misc/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_prefix}/include/magic.h
%{_datadir}/man/man3/*

%changelog
* Fri Mar 13 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.00-1
- port to AIX
