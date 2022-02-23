# There are two new File packages linked to python/python3 - Not yet built
%global with_python3 0
%global __python python2
%global __python3 python3

Summary: A utility for determining file types
Name: file
Version: 5.32
Release: 1
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/

Source10: %{name}-%{version}-%{release}.build.log

# Upstream says it's up to distributions to add a way to support local-magic.
# This can wait, not sure of interaction with AIX file LPP
# Patch0: file-localmagic.patch

# Fedora states these are not yet upstream (were not integrated on AIX for 5.29)
Patch3: file-4.17-rpm-name.patch
Patch4: file-5.04-volume_key.patch
Patch5: file-5.04-man-return-code.patch


BuildArch: ppc
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

%package -n python-magic
Summary: Python 2 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python-magic
This package contains the Python 2 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%if %{with_python3}
%package -n python3-magic
Summary: Python 3 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python3-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python3-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif

%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q

# %patch0 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Patches can generate *.orig files, which can't stay in the magic dir,
# otherwise there will be problems with compiling magic file!
rm -fv magic/Magdir/*.orig


%if %{with_python3}
# rm -rf %{py3dir}
# cp -a python %{py3dir}
# rm -rf ./py3dir
# cp -a python ./py3dir
%endif

%build
# setup environment for 32-bit and 64-bit
export AR="/usr/bin/ar -X32_64"        
export NM="/usr/bin/nm -X32_64" 

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# first build the 64-bit version 
export OBJECT_MODE=64
export CC='/usr/vac/bin/xlc_r -q64'
# export LDFLAGS="-s -L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib"

CFLAGS="-q64 -I/opt/freeware/include/ -D_ALL_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"  \
CPPFLAGS='-I/opt/freeware/include' \
./configure --prefix=%{_prefix} \
	   --mandir=%{_mandir} \
           --enable-fsect-man5 \
	   --disable-silent-rules
gmake "V=1"

cp src/.libs/libmagic.so.1 .

make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC='/usr/vac/bin/xlc_r -q32'
# export LDFLAGS="-s -Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib -L/usr/lib"

CFLAGS="-I/opt/freeware/include/ -D_ALL_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
CPPFLAGS='-I/opt/freeware/include' \
./configure --prefix=%{_prefix} \
	   --mandir=%{_mandir} \
           --enable-fsect-man5 \
	   --disable-silent-rules
gmake "V=1"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
# avoid "busy" error messages...
slibclean
${AR} -q  src/.libs/libmagic.a ./libmagic.so.1

cd python
# CFLAGS="%{optflags}" %{__python} setup.py build
%if %{with_python3}
# cd %{py3dir}
# cd ../py3dir
# CFLAGS="%{optflags}" %{__python3} setup.py build
%endif

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

# cd python
# %{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%if %{with_python3}
# cd %{py3dir}
# cd ../py3dir
# %{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif
# %{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}


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

# %files -n python-magic
# %{!?_licensedir:%global license %%doc}
# %license COPYING
# %doc python/README python/example.py
# %{python_sitelib}/magic.py
# %{python_sitelib}/magic.pyc
# %{python_sitelib}/magic.pyo
# %if 0%{?fedora} || 0%{?rhel} >= 6
# %{python_sitelib}/*egg-info
# %endif

# %if %{with_python3}
# %files -n python3-magic
# %{!?_licensedir:%global license %%doc}
# %license COPYING
# %doc python/README python/example.py
# %{python3_sitelib}/magic.py
# %{python3_sitelib}/*egg-info
# %{python3_sitelib}/__pycache__/*
# %endif


%changelog
* Fri Dec 08 2017 Michael Wilson <Michael.A.Wilson@atos.net> 5.32-1
-  update to version 5.32 on Aix 6.1

* Wed Dec 14 2016 Michael Wilson <Michael.A.Wilson@atos.net> 5.29-1
-  update to version 5.29 on Aix 6.1

* Thu Jul 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.12-2
-  update to version 5.12. on Aix5.3

* Tue Feb 12 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.12-1
- update to version 5.12. This version is mandatory for rpm manager 4.9.1.3

* Thu Mar 29 2012 Patricia Cugny <patricia.cugny@bull.net>  5.11-1
- update to version 5.11

* Fri Mar 13 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.00-1
- port to AIX

