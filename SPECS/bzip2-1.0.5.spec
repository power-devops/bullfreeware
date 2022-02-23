Summary: 	A file compression utility.
Name: 		bzip2
Version: 	1.0.5
Release:	1
License: 	IBM_ILA
Group: 		Archiving/Compression
Source: 	http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Source1: 	IBM_ILA
Patch0: 	bzip2-%{version}-shared.patch
URL: 		http://www.bzip.org/index.html
Prefix: 	%{_prefix}
BuildRoot: 	/var/tmp/%{name}-root
%define DEFCC cc

# Use --define 'no64 1' on the command line to disable 64bit build
%{!?no64:%define BUILD64 1}
%{?no64:%define BUILD64 0}
%define prefix64 %{prefix}/64

%description
Bzip2 is a freely available, patent-free, high quality data compressor.  Bzip2
compresses files to within 10 to 15 percent of the capabilities of the best
techniques available.  However, bzip2 has the added benefit of being
approximately two times faster at compression and six times faster at
decompression than those techniques.  Bzip2 is not the fastest compression
utility, but it does strike a balance between speed and compression capability.

Install bzip2 if you need a compression utility.

%prep
%setup -q
%patch0 -p1 -b .aixshared

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE.new
cat LICENSE >> LICENSE.new
mv LICENSE.new LICENSE

%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gunzip -c %{SOURCE0} |tar -xf -
cd %{name}-%{version}
%patch0 -p1 -b .aixshared
%endif


%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi

make CC="$CC" CFLAGS="$RPM_OPT_FLAGS" all
if [[ "$CC" = "gcc" ]]
then
   make -f Makefile-libbz2_so CFLAGS="$RPM_OPT_FLAGS" prefix=%{_prefix} all_ppc
else
   make -f Makefile-libbz2_so.nongcc CC="$CC" CFLAGS="$RPM_OPT_FLAGS" prefix=%{_prefix} all_ppc
fi

%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64

make CC="$CC" CFLAGS="$RPM_OPT_FLAGS" all
if [[ "$CC" = "gcc" ]]
then
   make -f Makefile-libbz2_so CFLAGS="$RPM_OPT_FLAGS" prefix=%{_prefix} all_ppc
else
   make -f Makefile-libbz2_so.nongcc CC="$CC" CFLAGS="$RPM_OPT_FLAGS" prefix=%{_prefix} all_ppc
fi

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../..
/usr/bin/ar -q libbz2.a \
   64bit/%{name}-%{version}/libbz2.so.1
%endif #BUILD64

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}
mv bzip2-shared bzip2
make install PREFIX="$RPM_BUILD_ROOT%{_prefix}"

( cd $RPM_BUILD_ROOT
#  /usr/bin/strip .%{_prefix}/bin/* || :
#  cat > .%{_prefix}/bin/bzless <<EOF
##!/bin/sh
#%{_prefix}/bin/bunzip2 -c "\$@" | /usr/bin/less
#EOF
#  chmod 755 .%{_prefix}/bin/bzless
 /usr/bin/strip .%{_prefix}/bin/* || :

# make clean links 
 rm .%{_prefix}/bin/bzfgrep .%{_prefix}/bin/bzegrep
 rm .%{_prefix}/bin/bzless .%{_prefix}/bin/bzcmp
 ln -sf %{_prefix}/bin/bzgrep .%{_prefix}/bin/bzegrep 
 ln -sf %{_prefix}/bin/bzgrep .%{_prefix}/bin/bzfgrep 
 ln -sf %{_prefix}/bin/bzdiff .%{_prefix}/bin/bzcmp
 ln -sf %{_prefix}/bin/bzmore .%{_prefix}/bin/bzless

 for dir in bin lib include
 do 
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done
 
 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)

( cd $RPM_BUILD_ROOT/%{prefix}/lib
  # Create a compatibility member to mitigate differences with Bull Freeware
  # offering
  COMPATMEMBER=libbz2.so
  for lib in *.a
  do
    /usr/bin/dump -Tv $lib |/usr/bin/awk 'match($4,"EXP|Exp") { print $NF }' > tmp.exp
    libbase=`print $lib | sed  -e 's/.a$//' -e 's/^lib//'`
    ld -L. -bI:tmp.exp -bE:tmp.exp -l$libbase -bM:SRE -bnoentry -o $COMPATMEMBER 
    /usr/bin/strip -e $COMPATMEMBER   # Make shr.o a load-only module
    /usr/bin/ar -r $lib $COMPATMEMBER
    rm -f $COMPATMEMBER tmp.exp
  done
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc  README *.html LICENSE
/usr/bin/*
/usr/lib/*
/usr/include/*
%{_prefix}/bin/*
%{_prefix}/man/man1/*
%{_prefix}/lib/libbz2.*
%{_prefix}/include/bzlib.h
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif

%changelog
* Fri Jun 4 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.0.5
- Update to 1.0.5

* Tue Mar 08 2005 David Clissold <cliss@austin.ibm.com> 1.0.2-3
- Clean up; build 64-bit libbz.a member

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri Apr 19 2002 David Clissold <cliss@austin.ibm.com>
- Update to version 1.0.2.

* Thu Mar 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Build both 32- and 64-bit libraries

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 31 1999 Bernhard Rosenkr�nzer <bero@redhat.com>
- 0.9.5d 
- Update download URL, add URL: tag in header

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 0.9.5c.

* Mon Aug  9 1999 Bill Nottingham <notting@redhat.com>
- install actual bzip2 binary, not libtool cruft.

* Sun Aug  8 1999 Jeff Johnson <jbj@redhat.com>
- run ldconfig to get shared library.

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- create shared libbz1.so.* library.

* Sun Apr  4 1999 Jeff Johnson <jbj@redhat.com>
- update to bzip2-0.9.0c.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- force compilation with egcs to avoid gcc optimization bug (thank God
  we haven't been beaten by it)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- version 0.9.0b

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.9.0

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- first build for Manhattan
