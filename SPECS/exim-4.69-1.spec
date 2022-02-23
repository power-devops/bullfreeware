Summary: The exim mail transfer agent
Name: exim
Version: 4.69
Release: 1
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

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exim

make install DESTDIR=$RPM_BUILD_ROOT

cd build-`scripts/os-type`-`scripts/arch-type`
cp exim $RPM_BUILD_ROOT%{_sbindir}
chmod 4755 $RPM_BUILD_ROOT%{_sbindir}/exim
ln -sf $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/exim
cp convert4r4 $RPM_BUILD_ROOT%{_prefix}/exim/bin
chmod 0755 $RPM_BUILD_ROOT%{_prefix}/exim/bin/convert4r4

for i in eximon eximon.bin exim_dumpdb exim_fixdb exim_tidydb \
 	exinext exiwhat exim_dbmbuild exicyclog exim_lock \
 	exigrep eximstats exipick exiqgrep exiqsumm \
 	exim_checkaccess convert4r4
do
	cp $i  $RPM_BUILD_ROOT%{_sbindir}/$i
	chmod 0755 $RPM_BUILD_ROOT%{_sbindir}/$i
	cd $RPM_BUILD_ROOT%{_sbindir}
	ln -sf $i ../bin/
	cd -
done
cd ..

cp src/configure.default $RPM_BUILD_ROOT%{_sysconfdir}/exim/exim.conf
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/exim/exim.conf
 
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
ln -sf ../..%{_sbindir}/exim sendmail.exim
cd -

cd $RPM_BUILD_ROOT%{_sbindir}/
ln -sf exim sendmail.exim
ln -sf exim ../bin/mailq.exim
ln -sf exim ../bin/runq.exim
ln -sf exim ../bin/rsmtp.exim
ln -sf exim ../bin/rmail.exim
ln -sf exim ../bin/newaliases.exim
cd -

mkdir -p -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim
mkdir -p -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/db
mkdir -p -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/input
mkdir -p -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/msglog
mkdir -p -m 0750 $RPM_BUILD_ROOT%{_var}/log/exim

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
%{_sbindir}/useradd -d %{_var}/spool/exim -G mail -u 93 exim 2>/dev/null
exit 0

%files
%defattr(-,root,root)
%attr(4755,root,root) %{_sbindir}/exim
%{_sbindir}/exim_dumpdb
%{_sbindir}/exim_fixdb
%{_sbindir}/exim_tidydb
%{_sbindir}/exinext
%{_sbindir}/exiwhat
%{_sbindir}/exim_dbmbuild
%{_sbindir}/exicyclog
%{_sbindir}/exigrep
%{_sbindir}/eximstats
%{_sbindir}/exipick
%{_sbindir}/exiqgrep
%{_sbindir}/exiqsumm
%{_sbindir}/exim_lock
%{_sbindir}/exim_checkaccess
%{_sbindir}/convert4r4
%{_sbindir}/sendmail.exim
%{_bindir}/mailq.exim
%{_bindir}/runq.exim
%{_bindir}/rsmtp.exim
%{_bindir}/rmail.exim
%{_bindir}/newaliases.exim
%{_bindir}/exim_dumpdb
%{_bindir}/exim_fixdb
%{_bindir}/exim_tidydb
%{_bindir}/exinext
%{_bindir}/exiwhat
%{_bindir}/exim_dbmbuild
%{_bindir}/exicyclog
%{_bindir}/exigrep
%{_bindir}/eximstats
%{_bindir}/exipick
%{_bindir}/exiqgrep
%{_bindir}/exiqsumm
%{_bindir}/exim_lock
%{_bindir}/exim_checkaccess
%{_bindir}/convert4r4
/usr/lib/sendmail.exim
%{_mandir}/*/*

%defattr(-,exim,exim)
%dir %{_var}/spool/exim
%dir %{_var}/spool/exim/db
%dir %{_var}/spool/exim/input
%dir %{_var}/spool/exim/msglog
%dir %{_var}/log/exim

%defattr(-,root,mail)
%dir %{_sysconfdir}/exim
%config(noreplace) %{_sysconfdir}/exim/exim.conf

%doc ACKNOWLEDGMENTS LICENCE NOTICE README.UPDATING README 
%doc doc util/unknownuser.sh

%changelog
* Thu Dec 11 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.69
- Port on AIX plateform
