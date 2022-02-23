Summary: A GNU tool for automatically configuring source code.
Name: autoconf
Version: 2.65
Release: 1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/autoconf
Source: ftp://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.gz
Requires: m4
BuildRoot: /var/tmp/%{name}-root
BuildArchitectures: noarch

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.  Using
Autoconf, programmers can create portable and configurable packages, since the
person building the package is allowed to specify various configuration options.

You should install Autoconf if you are developing software and you'd like to
use it to create shell scripts which will configure your source code packages.
If you are installing Autoconf, you will also need to install the GNU m4
package.

Note that the Autoconf package is not required for the end user who may be
configuring software with an Autoconf-generated script; Autoconf is only
required for the generation of the scripts, not their use.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/info

make prefix=$RPM_BUILD_ROOT%{_prefix} install

gzip -9nf $RPM_BUILD_ROOT%{_prefix}/share/info/autoconf.info*

rm -f $RPM_BUILD_ROOT%{_prefix}/info/standards*
cp build-aux/install-sh $RPM_BUILD_ROOT%{_prefix}/share/autoconf

cd $RPM_BUILD_ROOT
mkdir -p usr/bin || true 
mkdir -p usr/share || true 
for file in autoconf autoheader autom4te autoreconf autoscan autoupdate ifnames
do
   ln -sf ../..%{_prefix}/bin/$file usr/bin/$file
done
ln -sf ../..%{_prefix}/share/autoconf usr/share/autoconf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/autoconf.info.gz %{_prefix}/info/dir

%preun
/sbin/install-info --del %{_prefix}/share/info/autoconf.info.gz %{_prefix}/info/dir

%files
%defattr(-,root,system)
%{_prefix}/share/info/autoconf.info*
%{_prefix}/bin/autoconf
%{_prefix}/bin/autoheader
%{_prefix}/bin/autoreconf
%{_prefix}/bin/autoscan
%{_prefix}/bin/autoupdate
%{_prefix}/bin/autom4te
%{_prefix}/bin/ifnames
/usr/bin/autoconf
/usr/bin/autoheader
/usr/bin/autoreconf
/usr/bin/autoscan
/usr/bin/autoupdate
/usr/bin/autom4te
/usr/bin/ifnames
%{_prefix}/share/autoconf
/usr/share/autoconf

%changelog
* Fri Apr 23 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.65
- update to version 2.65

* Mon Apr 02 2007 Christophe Belle <christophe.belle@bull.net> 2.61-1
- update to level 2.61

* Fri Apr 22 2005 David Clissold <cliss@austin.ibm.com> 2.59-1
- update to level 2.59

* Tue Feb 17 2004 David Clissold <cliss@austin.ibm.com> 2.58-1
- update to level 2.58

* Fri Jun 14 2002 David Clissold <cliss@austin.ibm.com>
- AIX Toolbox: update to level 2.53

* Tue Oct 02 2001 David Clissold <cliss@austin.ibm.com>
- AIX Toolbox: update to level 2.52

  with acin.* and acout.* files (can you say annoying?)
* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to help autoconf clean after itself and not leave /tmp clobbered
  with acin.* and acout.* files (can you say annoying?)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- use gawk, not mawk

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- moved /usr/lib/autoconf to /usr/share/autoconf (with automake)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.13.

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires perl

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- patch for fixing /tmp race conditions

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- made a noarch package
- uses autoconf
- uses install-info

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built with glibc
