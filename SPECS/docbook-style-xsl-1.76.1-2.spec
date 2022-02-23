Name: docbook-style-xsl
Version: 1.76.1
Release: 2
Group: Applications/Text

Summary: Norman Walsh's XSL stylesheets for DocBook XML

License: Copyright only
URL: http://docbook.sourceforge.net/projects/xsl/

Provides: docbook-xsl = %{version}
Requires: docbook-dtd-xml
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires: libxml2 >= 2.6.32
# PassiveTeX before 1.21 can't handle the newer stylesheets.
Conflicts: passivetex < 1.21

BuildRequires: patch, tar, make

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Source0: http://downloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
Source1: %{name}.Makefile
Source2: http://downloads.sourceforge.net/docbook/docbook-xsl-doc-%{version}.tar.bz2
Patch10: %{name}-%{version}-aix.patch

# avoid proportional-column-width for passivetex (bug #176766).
Patch1: docbook-xsl-pagesetup.patch
# hard-code the margin-left work around to expect passivetex (bug #113456).
Patch2: docbook-xsl-marginleft.patch
# fix of #161619 - adjustColumnWidths now available
Patch3: docbook-xsl-newmethods.patch
# change a few non-constant expressions to constant - needed for passivetex(#366441)
Patch4: docbook-xsl-non-constant-expressions.patch
# added fixes for passivetex extension and list-item-body(#161371)
Patch5: docbook-xsl-list-item-body.patch


%description
These XSL stylesheets allow you to transform any DocBook XML document to
other formats, such as HTML, FO, and XHMTL.  They are highly customizable.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n docbook-xsl-%{version}
cd ..
tar jxf %{SOURCE2}
cd docbook-xsl-%{version}
%patch1 -p1 -b .pagesetup
%patch2 -p1 -b .marginleft
%patch3 -p1 -b .newmethods
%patch4 -p1 -b .nonconstant
%patch5 -p1 -b .listitembody

cp -p %{SOURCE1} Makefile

%patch10

for f in $(find -name "*'*") ; do
  mv -v "$f" $(echo "$f" | tr -d "'")
done


%build
# nothing to be done here


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export PATH=/opt/freeware/bin:$PATH

make install DESTDIR=${RPM_BUILD_ROOT}%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
ln -s xsl-stylesheets-%{version} \
	${RPM_BUILD_ROOT}%{_datadir}/sgml/docbook/xsl-stylesheets

# Don't ship the extensions (bug #177256).
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/sgml/docbook/xsl-stylesheets/extensions/*


%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG


%postun
# remove entries only on removal of package
if [ "$1" = 0 ] ; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" ${CATALOG}
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr (-,root,system,-)
%doc BUGS README TODO doc
%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-stylesheets


%changelog
* Mon Jul 15 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.76.1-2
- Initial port on Aix6.1

* Wed Aug 10 2011 Michael Perzl <michael@perzl.org> - 0.0.24-1
- first version for AIX V5.1 and higher
