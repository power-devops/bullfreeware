# rpm -ba --define 'dotests 0' libXau-1.0.8-1.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Name:          libXau
Version:       1.0.8
Release:       1
Summary:       X.Org Xau library
Group:		System/Libraries
URL:		http://www.x.org
Source:		http://www.x.org/releases/X11R7.7/src/lib/%{name}-%{version}.tar.gz
License:	MIT
BuildRoot:	/var/tmp/%{name}-%{version}-root
Obsoletes:     libXorg


%define         _libdir64 %{_prefix}/lib64

%description
X.Org Xau library

If you are compiling a 32-bit program, no special compiler options are needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%package devel
Summary:       X.Org Xau library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xau library.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

#setup environment for 32-bit and 64-bit builds

export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

#export LDFLAGS="-Wl,-blibpath:`pwd`/.libs:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib"
export LDFLAGS=


# first build the 64-bit version
cd 64bit

export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc -q64"

./configure --prefix=%{_prefix} \
	    --libdir=%{_libdir64} \
	    --mandir=%{_mandir} \
	    --disable-selective-werror \
	    --disable-silent-rules

gmake

if [ "%{DO_TESTS}" == 1 ]
then
        (gmake -k check || true)
        /usr/sbin/slibclean
fi


# now build the 32-bit version
cd ../32bit

export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc"

./configure --prefix=%{_prefix} \
	    --libdir=%{_libdir} \
            --mandir=%{_mandir} \
	    --disable-selective-werror \
	    --disable-silent-rules

gmake

if [ "%{DO_TESTS}" == 1 ]
then
        (gmake -k check || true)
        /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


export OBJECT_MODE=64
cd 64bit
make DESTDIR=${RPM_BUILD_ROOT} install


export OBJECT_MODE=32
cd ../32bit
gmake DESTDIR=$RPM_BUILD_ROOT install


# No more !
#(
#  cd ${RPM_BUILD_ROOT}
#    mkdir -p usr/include/X11
#    cd usr/include/X11
#    ln -sf ../../..%{_prefix}/include/X11/* .
#    cd -
#)


cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir64}/lib*.a ; do
    /usr/bin/ar -X64 -x ${f}
    ls -l
done
cd -

# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libXau.a  ${RPM_BUILD_ROOT}%{_libdir64}/libXau.so.6



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/libXau.a
%doc 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog 32bit/README


%files devel
%defattr(-,root,system)
%{_includedir}/X11/*.h
%{_libdir}/libXau.la
%{_libdir}/pkgconfig/*.pc
#/usr/include/X11/*.h
%{_mandir}/man3/*

%changelog
* Tue May 03 2016 Tony Reix <tony.reix@bull.net> - 1.0.8-1
- Update to version 1.0.8-1

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-1
- Update to version 1.0.7-1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.6-1
- Inital port on Aix 5.3

