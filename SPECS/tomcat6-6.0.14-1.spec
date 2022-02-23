%define jspspec 2.1
%define servletspec 2.5
%define embeddedname apache-tomcat

Name: tomcat6
Version: 6.0.14
Release: 1
Summary: Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

Group: Networking/Daemons
License: Apache Software License 2.0
URL: http://tomcat.apache.org
Source0: http://www.apache.org/dist/tomcat/tomcat-6/v%{version}/src/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides: %{name}
BuildArch: noarch

#Requires: java5
BuildRequires: sed
BuildRequires: gzip
BuildRequires: tar

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

Instead of using this package, if you have java5 installed, you can
simply download apache-tomcat-6.0.14.tar.gz from http://tomcat.apache.org/

This will download and install the latest version from tomcat.apache.org

%prep
# Nothing to setup
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}
%setup -q -c -T -a 0

%build
# Nothing to build

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && %{__rm} -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
# put tarball at the good place
mv %{embeddedname}-%{version}.tar.gz $RPM_BUILD_ROOT%{_prefix}

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && %{__rm} -rf $RPM_BUILD_ROOT

%pre
# add the tomcat user and group
%{_bindir}/mkgroup tomcat 2>/dev/null || :
%{_bindir}/mkuser pgrp=tomcat tomcat 2>/dev/null || :

%post

# install but don't activate
echo "proceeding ..." 
cd $RPM_BUILD_ROOT%{_prefix} && gzip -dc %{embeddedname}-%{version}.tar.gz | tar -xf - && cd -

# Create tomcat:secret in tomcat-users.xml
FILE=$CATALINA_HOME/conf/tomcat-users.xml
echo "<?xml version='1.0' encoding='utf-8'?>" > $FILE
echo "<tomcat-users>" >> $FILE
echo "  <role rolename=\"manager\"/>" >> $FILE
echo "  <user username=\"tomcat\" password=\"secret\" roles=\"manager\"/>" >> $FILE
echo "</tomcat-users>" >> $FILE

echo "***************************************************************"
echo "* export CATALINA_HOME=/opt/freeware/%{embeddedname}-%{version}"
echo "* export JAVA_HOME=/usr/java5/bin"
echo "* export JRE_HOME=/usr/java5/jre"
echo "* then:"
echo "* to start: \$CATALINA_HOME/bin/startup.sh"
echo "* to check: Browser: http://localhost:8080/"
echo "* to see admin status: http://localhost:8080/manager/status"
echo "*   (username=tomcat password=secret)"
echo "*   (remember to change username=tomcat password=secret)"
echo "* to stop: \$CATALINA_HOME/bin/shutdown.sh"
echo "***************************************************************"

%postun
rm -fr $CATALINA_HOME

%files
%defattr(-, root, system)
%{_prefix}/%{embeddedname}-%{version}.tar.gz


%changelog
* Fri Oct  5 2007 Christophe Belle <christophe.belle@bull.net> - 6.0.14-1
- Update to version 6.0.14 for AIX 52S
