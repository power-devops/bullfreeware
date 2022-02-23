Name:		libffi
Version:	3.0.9
Release:	3
Summary:	A portable foreign function interface library
Group:		System Environment/Libraries
License:	BSD
URL:		http://sourceware.org/libffi
Source0:	http://sourceware.org/libffi/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-aix_ffi.patch
Patch1:		%{name}-%{version}-as_aix.patch
Patch2:		%{name}-%{version}-32bit_aix.patch
BuildRoot:	/var/tmp/%{name}-%{version}-%{release}-root

#BuildRequires:	gcc >= 4.2.3-2
#Requires:	libgcc >= 4.2.3-2

%define _libdir64 %{_prefix}/lib64

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.
A calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.
The `libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.  


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkg-config
Requires:	/sbin/install-info, info

%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .aix_ffi
%patch1 -p1 -b .as_aix
%patch2 -p1 -b .32bit_aix
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export RM="/usr/bin/rm -f"
cd 64bit
# first build the 64-bit version
# on purpose we configure the "--build=powerpc-ibm-aix5.1.0.0" option
# differently from what config.guess provides
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc_r -q64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

# force the suppress of option -g from the Makefiles
perl -pi -e "s|CFLAGS = -g|CFLAGS =|g;" -e "s|CCASFLAGS = -g|CCASFLAGS =|g;" \
  ./include/Makefile ./man/Makefile ./testsuite/Makefile ./Makefile
make 

cd ../32bit
# now build the 32-bit version
# on purpose we configure the "--build=powerpc-ibm-aix5.1.0.0" option
# differently from what config.guess provides
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

# force the suppress of option -g from the Makefiles
perl -pi -e "s|CFLAGS = -g|CFLAGS =|g;" -e "s|CCASFLAGS = -g|CCASFLAGS =|g;" \
  ./include/Makefile ./man/Makefile ./testsuite/Makefile ./Makefile

make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%post devel
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 = 0 ] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{version}/include/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/%{name}.info.gz
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 3.0.9-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 3.0.9-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Mon Aug 01 2011 Gerard Visiedo <gerard.visiedo@bull.net>- 3.0.9-1
- Initial port on Aix5.3
