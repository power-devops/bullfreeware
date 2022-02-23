%define  ver     0.2.5
%define  RELEASE 1
%define  rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define  prefix  %{_prefix}

Summary: A library to handle various audio file formats.
Name: audiofile
Version: %ver
Release: %rel
Copyright: LGPL
Group: System Environment/Libraries
Source: ftp://ftp.gnome.org/pub/GNOME/stable/sources/audiofile/audiofile-%{PACKAGE_VERSION}.tar.bz2
Patch0: audiofile-%{ver}-aix.patch
URL: http://www.68k.org/~michael/audiofile/
BuildRoot:/var/tmp/audiofile-%{PACKAGE_VERSION}-root
Docdir: %{prefix}/doc
Obsoletes: libaudiofile

%define DEFCC cc

%description
The Audio File Library provides an elegant API for accessing a variety
of audio file formats, such as AIFF/AIFF-C, WAVE, and NeXT/Sun
.snd/.au, in a manner independent of file and data formats.

%package devel
Summary: Library, headers, etc. to develop with the Audio File Library.
Group: Development/Libraries

%description devel
Library, header files, etc. for developing applications with the Audio
File Library.

%prep

%setup -q
%patch0 -p1 -b .aix

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
libtoolize --force

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --disable-static
make $MAKE_FLAGS

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

#
# makefile is broken, sets exec_prefix explicitly.
#
make exec_prefix=$RPM_BUILD_ROOT/%{prefix} prefix=$RPM_BUILD_ROOT/%{prefix} install 

( cd $RPM_BUILD_ROOT
 /usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/* || :
 for dir in bin include lib
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc COPYING TODO README ChangeLog docs
%{prefix}/bin/*
%{prefix}/lib/lib*.a
/usr/bin/*
/usr/lib/lib*.a

%files devel
%defattr(-, root, root)
%{prefix}/include/*
%{prefix}/share/aclocal/*
/usr/include/*
%{prefix}/lib/pkgconfig/*
%{prefix}/lib/libaudiofile.la

%changelog
* Thu Apr 15 2004 David Clissold <cliss@austin.ibm.com> 0.2.5-1
- Update to version 0.2.5

* Thu Oct 23 2003 David Clissold <cliss@austin.ibm.com> 0.2.4-1
- Update to version 0.2.4

* Thu Jul 10 2003 David Clissold <cliss@austin.ibm.com>
- libaudiofile.la and audiofile.pc missing from the devel package

* Mon Jun 30 2003 Dan McNichol
- Update to version 0.2.3

* Sat Feb 9 2002 David Clissold <cliss@austin.ibm.com>
- strip the binaries

* Wed Aug 1 2001 Dan McNichol <mcnichol@austin.ibm.com>
- Changes for AIX Toolbox

* Fri Nov 20 1998 Michael Fulbright <drmike@redhat.com>
- First try at a spec file

