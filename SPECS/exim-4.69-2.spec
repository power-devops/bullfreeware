Summary: The exim mail transfer agent
Name: exim
Version: 4.69
Release: 2
License: GPLv2+
Url: http://www.exim.org/
Group: System Environment/Daemons
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
Source: ftp://ftp.exim.org/pub/exim/exim4/exim-%{version}.tar.bz2
Patch0: exim-4.69-aixconf.patch
Patch1: exim-4.69-exim_install.patch
BuildRequires: openssl-devel openldap-devel

%description 
Exim is a message transfer agent (MTA) developed at the University of
Cambridge for use on Unix systems connected to the Internet. It is
freely available under the terms of the GNU General Public Licence. In
style it is similar to Smail 3, but its facilities are more
general. There is a great deal of flexibility in the way mail can be
routed, and there are extensive facilities for checking incoming
mail. Exim can be installed in place of sendmail, although the
configuration of exim is quite different to that of sendmail.

%prep
%setup -q
cp src/EDITME Local/Makefile
cp exim_monitor/EDITME Local/eximon.conf

%patch0 -p1 -b .aixconf
%patch1 -p1 -b .aix

%build
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROO%{prefix}/exim/bin
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/exim

make install DESTDIR=$RPM_BUILD_ROOT

if [ -e $RPM_BUILD_ROOT%{prefix}/exim/bin/exim ]; then
  rm -f $RPM_BUILD_ROOT%{prefix}/exim/bin/exim
fi
cd build-`scripts/os-type`-`scripts/arch-type`
cp exim $RPM_BUILD_ROOT%{prefix}/exim/bin
chmod 4755 $RPM_BUILD_ROOT%{prefix}/exim/bin/exim
cd $RPM_BUILD_ROOT%{prefix}/bin/
ln -sf ../exim/bin/exim exim
cd -
cd $RPM_BUILD_ROOT/usr/sbin
ln -sf ../..%{prefix}/exim/bin/exim exim
cd -

for i in eximon eximon.bin exim_dumpdb exim_fixdb exim_tidydb \
 	exinext exiwhat exim_dbmbuild exicyclog exim_lock \
 	exigrep eximstats exipick exiqgrep exiqsumm \
 	exim_checkaccess convert4r4
do
	cp $i  $RPM_BUILD_ROOT%{prefix}/exim/bin/$i
	chmod 0755 $RPM_BUILD_ROOT%{prefix}/exim/bin/$i
	cd $RPM_BUILD_ROOT%{prefix}/bin/
	ln -sf ../exim/bin/$i $i
	cd -
	cd $RPM_BUILD_ROOT/usr/sbin/
	ln -sf ../..%{prefix}/exim/bin/$i $i
	cd -
done
cd ..

cp src/configure.default $RPM_BUILD_ROOT/etc/exim/exim.conf
chmod 0644 $RPM_BUILD_ROOT/etc/exim/exim.conf
 
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
ln -sf ../..%{prefix}/exim/bin/exim sendmail.exim
cd -

cd $RPM_BUILD_ROOT/usr/sbin/
ln -sf ../..%{prefix}/exim/bin/exim sendmail.exim
ln -sf ../..%{prefix}/exim/bin/exim mailq.exim
ln -sf ../..%{prefix}/exim/bin/exim runq.exim
ln -sf ../..%{prefix}/exim/bin/exim rsmtp.exim
ln -sf ../..%{prefix}/exim/bin/exim rmail.exim
ln -sf ../..%{prefix}/exim/bin/exim newaliases.exim
cd -

mkdir -p -m 0750 $RPM_BUILD_ROOT/var/spool/exim
mkdir -p -m 0750 $RPM_BUILD_ROOT/var/spool/exim/db
mkdir -p -m 0750 $RPM_BUILD_ROOT/var/spool/exim/input
mkdir -p -m 0750 $RPM_BUILD_ROOT/var/spool/exim/msglog
mkdir -p -m 0750 $RPM_BUILD_ROOT/var/log/exim

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
cp doc/exim.8 $RPM_BUILD_ROOT%{_mandir}/man8/exim.8
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man8/exim.8

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT/etc/pki/tls/private
touch $RPM_BUILD_ROOT/etc/pki/tls/private/exim.pem
chmod 600 $RPM_BUILD_ROOT/etc/pki/tls/private/exim.pem

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Creation of exim user and group
mkgroup -a id=93 exim
useradd -d /var/spool/exim -g exim -u 93 exim
exit 0

%postun
# deletion of exim user and group
userdel -r exim
rmgroup exim
exit 0

%files
%defattr(-,root,root)
%attr(4755,root,root) %{prefix}/exim/bin/exim
%{prefix}/exim/bin/exim_dumpdb
%{prefix}/exim/bin/exim_fixdb
%{prefix}/exim/bin/exim_tidydb
%{prefix}/exim/bin/exinext
%{prefix}/exim/bin/exiwhat
%{prefix}/exim/bin/exim_dbmbuild
%{prefix}/exim/bin/exicyclog
%{prefix}/exim/bin/exigrep
%{prefix}/exim/bin/eximstats
%{prefix}/exim/bin/exipick
%{prefix}/exim/bin/exiqgrep
%{prefix}/exim/bin/exiqsumm
%{prefix}/exim/bin/exim_lock
%{prefix}/exim/bin/exim_checkaccess
%{prefix}/exim/bin/convert4r4
%{prefix}/exim/configure
%{_bindir}/*
/usr/sbin/*
/usr/lib/sendmail.exim
%{_mandir}/*/*

%defattr(-,exim,exim)
%dir /var/spool/exim
%dir /var/spool/exim/db
%dir /var/spool/exim/input
%dir /var/spool/exim/msglog
%dir /var/log/exim

%defattr(-,root,mail)
%dir /etc/exim
%config(noreplace) /etc/exim/exim.conf

%doc ACKNOWLEDGMENTS LICENCE NOTICE README.UPDATING README 
%doc doc util/unknownuser.sh

%changelog
* Wed Jan 14 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.69-2
- Fix some issues with installation

* Thu Dec 11 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.69
- Port on AIX plateform
