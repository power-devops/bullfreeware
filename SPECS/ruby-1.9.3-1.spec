Name:		ruby
Version:	1.9.3
Release:	1
License:	Distributable
URL:		http://www.ruby-lang.org/
Prefix:		%{_prefix}
Source:		%{name}-%{version}-p362.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Provides:	%{name}-libs

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
%define DEFCC cc

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.

%prep
%setup -q -n %{name}-%{version}-p362

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


export LDFLAGS="-brtl -L/usr/linux/lib -L/opt/freeware/lib -L/usr/lib -lpthreads"

#export LIBPATH="/usr/linux/lib:/opt/freeware/lib:/usr/lib"
export LIBPATH="/usr/linux/lib:/opt/freeware/lib:/usr/lib:`pwd`"


aclocal
autoconf
./configure \
	 --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
	--prefix=%{_prefix}  \
	--enable-pthread \
	--enable-shared


# Do not run KNOWNBUGS tests
sed "s/^/#/" ./KNOWNBUGS.rb >./KNOWNBUGS.rb.tmp
mv ./KNOWNBUGS.rb.tmp ./KNOWNBUGS.rb

make V=1

# ulimit needed for test with threads
ulimit -d unlimited

make test


%install
echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install prefix=$RPM_BUILD_ROOT%{prefix}

strip $RPM_BUILD_ROOT%{_bindir}/%{name}

# Link ruby into /usr/bin and /usr/lib
( cd $RPM_BUILD_ROOT
  for dir in bin lib include
  do
     mkdir -p usr/${dir}
     cd usr/${dir}
     ln -sf ../..%{prefix}/${dir}/* .
     cd -
  done
)

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/bin/*
%{_prefix}/include/ruby*
%{_prefix}/lib/libruby*
%{_prefix}/lib/ruby
%{_prefix}/lib/pkgconfig
%{_prefix}/share/ri
/usr/bin/*
/usr/lib/libruby*
/usr/lib/ruby
/usr/include/*

%doc %{_prefix}/share/man/man1/*.1
%doc README COPYING LEGAL NEWS README.EXT


%changelog
* Wed Jan 30 2013 by Bernard CAHEN <bernard.cahen@bull.net> 1.9.3-1
- Version for AIX 61
* Tue Aug 14 2007 by Christophe BELLE <christophe.belle@bull.net> 1.8.6-1
- Version for AIX 52S
