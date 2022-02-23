# Use --define 'noxlc 1' on the command line to use gcc
%{!?noxlc:%define XLC 1}
%{?noxlc:%define XLC 0}

Name: arts
Summary: Analog Real-Time Synthesizer
Prefix: %{_prefix}/kde
Version: 1.0.0
Release: 1
Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}-kde-common.patch
Patch1: %{name}-%{version}-xlc.patch
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Copyright: GPL
Requires: qt >= 3.0
BuildRequires: qt-devel >= 3.0, automake = 1.5, autoconf >= 2.5 

%description
aRts (Analog Real-Time Synthesizer) is a sound system.  It
creates and processes sound using small modules.  aRts modules 
can create waveforms (oscillators), play samples, filter data, 
add signals, perform effects like delay/flanger/chorus, or 
output the data to the soundcard.

By connecting all those small modules together, you can perform
complex tasks like simulating a mixer, generating an instrument, or
playing a wave file with effects.


%prep
rm -rf $RPM_BUILD_ROOT
%setup -q
# Common patches.
%patch0 -p0 -b .aix
# Per-compiler patches.  These will break (or are untested) on the other.
%if %{XLC} == 1
%patch1 -p0 -b .xlc
%endif

%if %{XLC} == 0
  # Deoptimize.  Temporary until compiler is in better shape.
  for file in `find . ! -name "*.png" -print | xargs grep -l '\-O2'`; do
    cp $file $file.withO2
    sed -e 's/\-O2/-O0/g' < $file.withO2 > $file
  done
%endif


%build
%{!?noxlc: export CC=xlc CXX=xlC}
export QTDIR=%{_prefix}/qt
#FIXME: -O2 was causing problems, otherwise FLAGS+="%{!?noxlc: -O2}"
#FIXME: Try --enable-final with xlC
export CXXFLAGS="%{!?noxlc: -qrtti=all}" CFLAGS="%{!?noxlc: -Dinline=_Inline}"
./configure --prefix=%{prefix} --disable-debug %{?noxlc: --enable-final}
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

export DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%if %{XLC} == 0
# Stripping decreases size a lot!
/usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/* || :
%endif

mkdir -p $RPM_BUILD_ROOT/usr
ln -sf ..%{prefix} $RPM_BUILD_ROOT/usr

cd $RPM_BUILD_ROOT
find .%{prefix} -type d | sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' > \
	$RPM_BUILD_DIR/file.list.%{name}

find . -type f | sed -e 's,^\.,\%attr(-\,root\,root) ,' \
	-e '/\/config\//s|^|%config |' >> \
	$RPM_BUILD_DIR/file.list.%{name}

find . -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >> \
	$RPM_BUILD_DIR/file.list.%{name}

echo "%docdir %{prefix}/share/doc" >> $RPM_BUILD_DIR/file.list.%{name}


%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/file.list.%{name}

%files -f ../file.list.%{name}

%changelog
* Thu Mar 28 2001 Reza Arbab <arbab@austin.ibm.com>
- 1.0.0
