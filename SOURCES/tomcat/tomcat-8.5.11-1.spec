# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global jspspec 2.3
%global major_version 8
%global minor_version 5
%global micro_version 11
%global packdname apache-tomcat-%{version}-src
%global servletspec 3.1
%global elspec 3.0
%global tcuid 91

%global _unitdir /opt/freeware/tomcat/unitdir
%global _javadocdir /opt/freeware/tomcat/javadocdir
%global _javadir /opt/freeware/tomcat/javadir
# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_var}/lib/%{name}
%global appdir %{basedir}/webapps
%global homedir %{_datadir}/%{name}
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global cachedir %{_var}/cache/%{name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _initrddir %{_sysconfdir}/init.d
%global _systemddir /lib/systemd/system

%global javaversion java8_64

Name:          tomcat
Epoch:         1
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       1
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

%global ant_home %{_datadir}/apache-ant-1.10.0
%global java_home %{_datadir}/java
%global ant      %{ant_home}/bin/ant
%global jar      /usr/%{javaversion}/bin/jar
%global javac      /usr/%{javaversion}/bin/javac

%global __install /opt/freeware/bin/install

Group:         System Environment/Daemons
License:       ASL 2.0
URL:           http://tomcat.apache.org/
Buildroot:%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Source0:       http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/src/%{packdname}.tar.gz
Source1:       %{name}-%{major_version}.0.conf
Source3:       %{name}-%{major_version}.0.sysconfig
Source4:       %{name}-%{major_version}.0.wrapper
Source5:       %{name}-%{major_version}.0.logrotate
Source6:       %{name}-%{major_version}.0-digest.script
Source7:       %{name}-%{major_version}.0-tool-wrapper.script
Source8:       servlet-api-OSGi-MANIFEST.MF
Source9:       jsp-api-OSGi-MANIFEST.MF
Source11:      %{name}-%{major_version}.0.service
Source12:      el-api-OSGi-MANIFEST.MF
Source13:      jasper-el-OSGi-MANIFEST.MF
Source14:      jasper-OSGi-MANIFEST.MF
Source15:      tomcat-api-OSGi-MANIFEST.MF
Source16:      tomcat-juli-OSGi-MANIFEST.MF
Source20:      %{name}-%{major_version}.0-jsvc.service
Source21:      tomcat-functions
Source30:      tomcat-preamble
Source31:      tomcat-server
Source32:      tomcat-named.service
Source40:      macros.fjava
Source40:      macros.jpackage

# patch from : //github.com/zawn/centos-rpm-tomcat/blob/CentOS_7/

Patch0:        %{name}-%{major_version}.0-bootstrap-MANIFEST.MF.patch
Patch1:        %{name}-%{major_version}.0-tomcat-users-webapp.patch
Patch2:        %{name}-8.0.36-CompilerOptionsV9.patch

BuildArch:     noarch

BuildRequires: ant
BuildRequires: ecj >= 1:4.4.0
BuildRequires: findutils
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-daemon
BuildRequires: apache-commons-dbcp
BuildRequires: apache-commons-pool
BuildRequires: tomcat-taglibs-standard
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils >= 0:1.7.0
BuildRequires: junit
BuildRequires: geronimo-jaxrpc
BuildRequires: wsdl4j
BuildRequires: systemd-units
Requires:      apache-commons-daemon
Requires:      apache-commons-logging
Requires:      apache-commons-collections
Requires:      apache-commons-dbcp
Requires:      apache-commons-pool
Requires:      java-headless >= 1:1.6.0
Requires:      jpackage-utils
Requires:      procps
Requires:      %{name}-lib = %{epoch}:%{version}-%{release}

# Requires(pre):    shadow-utils
# Requires(post):   chkconfig
# Requires(preun):  chkconfig
# Requires(post):   systemd-units
# Requires(preun):  systemd-units
# Requires(postun): systemd-units

# added after log4j sub-package was removed
Provides:         %{name}-log4j = %{epoch}:%{version}-%{release}

%description
WARNING : THIS VERSION IS AN EXPERIMENTAL AND INCOMPLETE VERSION : Do NOT USED
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%package admin-webapps
Group: Applications/System
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Group: Applications/Text
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package javadoc
Group: Documentation
Summary: Javadoc generated documentation for Apache Tomcat
Requires: jpackage-utils

%description javadoc
Javadoc generated documentation for Apache Tomcat.

%package jsvc
Group: System Environment/Daemons
Summary: Apache jsvc wrapper for Apache Tomcat as separate service
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: apache-commons-daemon-jsvc

%description jsvc
Systemd service to start tomcat with jsvc,
which allows tomcat to perform some privileged operations
(e.g. bind to a port < 1024) and then switch identity to a non-privileged user.

%package jsp-%{jspspec}-api
Group: Development/Libraries
Summary: Apache Tomcat JSP API implementation classes
Provides: jsp = %{jspspec}
Obsoletes: %{name}-jsp-2.2-api
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
# Requires(post): chkconfig
# Requires(postun): chkconfig

%description jsp-%{jspspec}-api
Apache Tomcat JSP API implementation classes.

%package lib
Group: Development/Libraries
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name}-jsp-%{jspspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Requires: ecj >= 1:4.2.1
Requires: apache-commons-collections
Requires: apache-commons-dbcp
Requires: apache-commons-pool
# Requires(preun): coreutils

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Group: Development/Libraries
Summary: Apache Tomcat Servlet API implementation classes
Provides: servlet = %{servletspec}
Provides: servlet6
Provides: servlet3
Obsoletes: %{name}-servlet-3.0-api
# Requires(post): chkconfig
# Requires(postun): chkconfig

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API implementation classes.

%package el-%{elspec}-api
Group: Development/Libraries
Summary: Expression Language v%{elspec} API
Provides: el_api = %{elspec}
Obsoletes: %{name}-el-2.2-api
# Requires(post): chkconfig
# Requires(postun): chkconfig

%description el-%{elspec}-api
Expression Language %{elspec}.

%package webapps
Group: Applications/Internet
Summary: The ROOT and examples web applications for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tomcat-taglibs-standard >= 0:1.1

%description webapps
The ROOT and examples web applications for Apache Tomcat.

%prep

# java configuration (java.conf)
export JAVACONFDIRS=/opt/freeware/share/apache-tomcat-8.5.11/webapps/examples/WEB-INF/lib

# export JAVAPACKAGES_DEBUG=1
# java Configuration fonctions: (/opt/freeware/share/java-utils/java-functions)

%setup -q -n %{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete


echo "ECHO libdir %{_javadir}/%{name}  "
echo "ECHO java_home %{_datadir}/java  "
echo "ECHO RPM_BUILD_ROOT = $RPM_BUILD_ROOT"

%patch0 -p0
%patch1 -p0
%patch2 -p0


%{__ln_s} $(build-classpath tomcat-taglibs-standard/taglibs-standard-impl) webapps/examples/WEB-INF/lib/jstl.jar
%{__ln_s} $(build-classpath tomcat-taglibs-standard/taglibs-standard-compat) webapps/examples/WEB-INF/lib/standard.jar




%build
rpm -qa
env

## expand %{SOURCE40}


export JAVACONFDIRS=/opt/freeware/share/apache-tomcat-8.5.11/webapps/examples/WEB-INF/lib


export ANT_OPTS="-Dhttp.proxyHost=ecfrec.frec.bull.fr -Dhttp.proxyPort=8080"

export JAVA_HOME=/usr/%{javaversion}/
export ANT_HOME=%{ant_home}

export CLASSPATH=/usr/java8_64/lib:$CLASSPATH
export CLASSPATH=""
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

export PATH=%{ant_home}/bin:/usr/%{javaversion}/jre/bin:/usr/%{javaversion}/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/opt/ifor/ls/os/aix/bin:/usr/opt/ifor/ls/os/aix/bin

export JAVAC=/usr/%{javaversion}/bin/javac
export OPT_JAR_LIST="xalan-j2-serializer"
   # we don't care about the tarballs and we're going to replace
   # tomcat-dbcp.jar with apache-commons-{collections,dbcp,pool}-tomcat5.jar
   # so just create a dummy file for later removal
   touch HACK
   %{__mkdir_p} HACKDIR
   touch HACKDIR/build.xml
   touch HACKDIR/LICENSE

   # who needs a build.properties file anyway

   #   %{ant}
   echo "ECHO JAVACMD $JAVACMD"

   [ -e build.xml.sauve ] || { cp build.xml build.xml.sauve; }
   rm -f build.xml
#   sed -e 's;e/7/;e/8/;' -e 's|1.7|1.8|' <build.xml.sauve  >build.xml
   sed -e 's|1.7|1.8|' -e 's|failonwarning="true"|failonwarning="false"|' <build.xml.sauve  >build.xml

   %{ant} -d -v --execdebug \
    -Dbase.path="." \
    -Dbuild.compiler="modern" \
    -Dcommons-collections.jar="$(build-classpath apache-commons-collections)" \
    -Dcommons-daemon.jar="$(build-classpath apache-commons-daemon)" \
    -Dcommons-daemon.native.src.tgz="HACK" \
    -Djasper-jdt.jar="$(build-classpath ecj)" \
    -Djdt.jar="$(build-classpath ecj)" \
    -Dtomcat-native.tar.gz="HACK" \
    -Dtomcat-native.home="." \
    -Dtomcat-native.win.path="HACKDIR" \
    -Dcommons-daemon.native.win.mgr.exe="HACK" \
    -Dnsis.exe="HACK" \
    -Dcommons-pool.home="HACKDIR" \
    -Dcommons-dbcp.home="HACKDIR" \
    -Dno.build.dbcp=true \
    -Dversion="%{version}" \
    -Dversion.build="%{micro_version}" \
    -Djava.8.home=%{java_home} \
    deploy dist-prepare dist-source \
    javadoc
   
    
##    -Djaxrpc-lib.jar="$(build-classpath jaxrpc)" \
##    -Dwsdl4j-lib.jar="$(build-classpath wsdl4j)" \
   
    # remove some jars that we'll replace with symlinks later
   %{__rm} output/build/bin/commons-daemon.jar \
           output/build/lib/ecj.jar

    # remove the cruft we created
   %{__rm} output/build/bin/tomcat-native.tar.gz




   HERE1=$PWD;
   cd output/dist/src/webapps/docs/appdev/sample/src
   # pushd output/dist/src/webapps/docs/appdev/sample/src
   %{__mkdir_p} ../web/WEB-INF/classes
   %{javac} -cp ../../../../../../../../output/build/lib/servlet-api.jar -d ../web/WEB-INF/classes mypackage/Hello.java
   
   
   HERE2=$PWD;
   cd ../web
   # pushd ../web
   %{jar} cf ../../../../../../../../output/build/webapps/docs/appdev/sample/sample.war *

   cd $HERE1
   # popd
   # popd

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE8} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/servlet-api.jar META-INF/MANIFEST.MF
cp -p %{SOURCE9} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/jsp-api.jar META-INF/MANIFEST.MF
cp -p %{SOURCE12} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/el-api.jar META-INF/MANIFEST.MF
cp -p %{SOURCE13} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/jasper-el.jar META-INF/MANIFEST.MF
cp -p %{SOURCE14} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/jasper.jar META-INF/MANIFEST.MF
cp -p %{SOURCE15} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/lib/tomcat-api.jar META-INF/MANIFEST.MF
cp -p %{SOURCE16} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u output/build/bin/tomcat-juli.jar META-INF/MANIFEST.MF








%install

## expand %{SOURCE40}

rm -fr /var/opt/freeware/tmp/tomcat-8.5.11-1-root
export JAVACONFDIRS=/opt/freeware/share/apache-tomcat-8.5.11/webapps/examples/WEB-INF/lib

# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_javadocdir}/%{name}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initrddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_systemddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{bindir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > ${RPM_BUILD_ROOT}%{confdir}/conf.d/README
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{logdir}
/bin/touch ${RPM_BUILD_ROOT}%{logdir}/catalina.out
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tomcats
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{tempdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{workdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

# move things into place
# First copy supporting libs to tomcat lib
HERE=$PWD
cd output/build
# pushd output/build

    %{__cp} -dpR bin/*.jar          ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} -dpR bin/*.xml          ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} -dpR conf/*.properties  ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -dpR conf/*.xml         ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -dpR conf/*.policy      ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -dpR lib/*.jar          ${RPM_BUILD_ROOT}%{libdir}
    %{__cp} -dpR webapps/*          ${RPM_BUILD_ROOT}%{appdir}
    # popd
    cd $HERE
    
# javadoc
%{__cp} -dpR output/dist/webapps/docs/api/* ${RPM_BUILD_ROOT}%{_javadocdir}/%{name}

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/%{name}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE3} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{name}
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service
%{__install} -m 0644 %{SOURCE20} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}-jsvc.service
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE7} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE21} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE30} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE31} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server
%{__install} -m 0644 %{SOURCE32} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service

# Substitute libnames in catalina-tasks.xml
sed -i \
   "s,el-api.jar,%{name}-el-%{elspec}-api.jar,;
    s,servlet-api.jar,%{name}-servlet-%{servletspec}-api.jar,;
    s,jsp-api.jar,%{name}-jsp-%{jspspec}-api.jar,;" \
    ${RPM_BUILD_ROOT}%{bindir}/catalina-tasks.xml

# create jsp and servlet API symlinks
HERE=$PWD
cd ${RPM_BUILD_ROOT}%{_javadir}
#   pushd ${RPM_BUILD_ROOT}%{_javadir}
   %{__mv} %{name}/jsp-api.jar %{name}-jsp-%{jspspec}-api.jar
   %{__ln_s} %{name}-jsp-%{jspspec}-api.jar %{name}-jsp-api.jar
   %{__mv} %{name}/servlet-api.jar %{name}-servlet-%{servletspec}-api.jar
   %{__ln_s} %{name}-servlet-%{servletspec}-api.jar %{name}-servlet-api.jar
   %{__mv} %{name}/el-api.jar %{name}-el-%{elspec}-api.jar
   %{__ln_s} %{name}-el-%{elspec}-api.jar %{name}-el-api.jar
   # popd
   cd $HERE
   

   HERE=$PWD
   cd output/build
# pushd output/build
    %{_bindir}/build-jar-repository lib apache-commons-collections \
                                        apache-commons-dbcp apache-commons-pool ecj 2>&1
    # need to use -p here with b-j-r otherwise the examples webapp fails to
    # load with a java.io.IOException
    %{_bindir}/build-jar-repository -p webapps/examples/WEB-INF/lib \
    tomcat-taglibs-standard/taglibs-standard-impl.jar tomcat-taglibs-standard/taglibs-standard-compat.jar 2>&1
    # popd
    cd $HERE
    

    HERE=$PWD
    cd ${RPM_BUILD_ROOT}%{libdir}
# pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/%{name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/%{name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/%{name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath apache-commons-collections) commons-collections.jar
    %{__ln_s} $(build-classpath apache-commons-dbcp) commons-dbcp.jar
    %{__ln_s} $(build-classpath apache-commons-pool) commons-pool.jar
    %{__ln_s} $(build-classpath ecj) jasper-jdt.jar

    # Temporary copy the juli jar here from /usr/share/java/tomcat (for maven depmap)
    %{__cp} -dpR ${RPM_BUILD_ROOT}%{bindir}/tomcat-juli.jar ./
    # popd
    cd $HERE
    

# symlink to the FHS locations where we've installed things
    HERE=$PWD
    cd ${RPM_BUILD_ROOT}%{homedir}
# pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
    # popd
    cd $HERE
    

# install sample webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/sample
HERE=$PWD
cd ${RPM_BUILD_ROOT}%{appdir}/sample
# pushd ${RPM_BUILD_ROOT}%{appdir}/sample
%{jar} xf ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war
# popd
cd $HERE

%{__rm} ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war

# Allow linking for example webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
HERE=$PWD
cd ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
# pushd ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
echo '<?xml version="1.0" encoding="UTF-8"?>' > context.xml
echo '<Context>' >> context.xml
echo '  <Resources allowLinking="true" />' >> context.xml
echo '</Context>' >> context.xml
# popd
cd $HERE


HERE=$PWD
cd ${RPM_BUILD_ROOT}%{appdir}/examples/WEB-INF/lib
# pushd ${RPM_BUILD_ROOT}%{appdir}/examples/WEB-INF/lib
%{__ln_s} -f $(build-classpath tomcat-taglibs-standard/taglibs-standard-impl) jstl.jar
%{__ln_s} -f $(build-classpath tomcat-taglibs-standard/taglibs-standard-compat) standard.jar
# popd
cd $HERE



# SKIP all maven install

#        # Install the maven metadata
#        %{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_mavenpomdir}
#        HERE=$PWD
#        cd output/dist/src/res/maven
#        # pushd output/dist/src/res/maven
#        for pom in *.pom; do
#            # fix-up version in all pom files
#            sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
#        done
#        
#        # we won't install dbcp, juli-adapters and juli-extras pom files
#        for libname in annotations-api catalina jasper-el jasper catalina-ha; do
#            %{__cp} -dpR %{name}-$libname.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-$libname.pom
#            %add_maven_depmap JPP.%{name}-$libname.pom %{name}/$libname.jar -f "tomcat-lib"
#        done
#        
#        # tomcat-util-scan
#        %{__cp} -dpR %{name}-util-scan.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-util-scan.pom
#        %add_maven_depmap JPP.%{name}-util-scan.pom %{name}/%{name}-util-scan.jar -f "tomcat-lib"
#        
#        # tomcat-jni
#        %{__cp} -dpR %{name}-jni.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-jni.pom
#        %add_maven_depmap JPP.%{name}-jni.pom %{name}/%{name}-jni.jar -f "tomcat-lib"
#        
#        # servlet-api jsp-api and el-api are not in tomcat subdir, since they are widely re-used elsewhere
#        %{__cp} -dpR tomcat-jsp-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-jsp-api.pom
#        %add_maven_depmap JPP-tomcat-jsp-api.pom tomcat-jsp-api.jar -f "tomcat-jsp-api" -a "org.eclipse.jetty.orbit:javax.servlet.jsp"
#        
#        %{__cp} -dpR tomcat-el-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-el-api.pom
#        %add_maven_depmap JPP-tomcat-el-api.pom tomcat-el-api.jar -f "tomcat-el-api" -a "org.eclipse.jetty.orbit:javax.el"
#        
#        %{__cp} -dpR tomcat-servlet-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-servlet-api.pom
#        # Generate a depmap fragment javax.servlet:servlet-api pointing to
#        # tomcat-servlet-3.0-api for backwards compatibility
#        # also provide jetty depmap (originally in jetty package, but it's cleaner to have it here
#        %add_maven_depmap JPP-tomcat-servlet-api.pom tomcat-servlet-api.jar -f "tomcat-servlet-api"
#        
#        # replace temporary copy with link
#        %{__ln_s} -f $(abs2rel %{bindir}/tomcat-juli.jar %{libdir}) ${RPM_BUILD_ROOT}%{libdir}/
#        
#        # two special pom where jar files have different names
#        %{__cp} -dpR tomcat-tribes.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-catalina-tribes.pom
#        %add_maven_depmap JPP.%{name}-catalina-tribes.pom %{name}/catalina-tribes.jar
#        
#        %{__cp} -dpR tomcat-coyote.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-coyote.pom
#        %add_maven_depmap JPP.%{name}-tomcat-coyote.pom %{name}/tomcat-coyote.jar
#        
#        %{__cp} -dpR tomcat-juli.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-juli.pom
#        %add_maven_depmap JPP.%{name}-tomcat-juli.pom %{name}/tomcat-juli.jar
#        
#        %{__cp} -dpR tomcat-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-api.pom
#        %add_maven_depmap JPP.%{name}-tomcat-api.pom %{name}/tomcat-api.jar
#        
#        %{__cp} -dpR tomcat-util.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-util.pom
#        %add_maven_depmap JPP.%{name}-tomcat-util.pom %{name}/tomcat-util.jar
#        
#        %{__cp} -dpR tomcat-jdbc.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-jdbc.pom
#        %add_maven_depmap JPP.%{name}-tomcat-jdbc.pom %{name}/tomcat-jdbc.jar
#        
#        # tomcat-websocket-api
#        %{__cp} -dpR tomcat-websocket-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-websocket-api.pom
#        %add_maven_depmap JPP.%{name}-websocket-api.pom %{name}/websocket-api.jar
#        
#        # tomcat-tomcat-websocket
#        %{__cp} -dpR tomcat-websocket.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-websocket.pom
#        %add_maven_depmap JPP.%{name}-tomcat-websocket.pom %{name}/tomcat-websocket.jar


%pre
# add the tomcat user and group
%{_sbindir}/groupadd -g %{tcuid} -r tomcat 2>/dev/null || :
%{_sbindir}/useradd -c "Apache Tomcat" -u %{tcuid} -g tomcat \
    -s /sbin/nologin -r -d %{homedir} tomcat 2>/dev/null || :

%post
# install but don't activate
%systemd_post %{name}.service

%post jsp-%{jspspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/jsp.jar jsp \
    %{_javadir}/%{name}-jsp-%{jspspec}-api.jar 20200

%post servlet-%{servletspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/servlet.jar servlet \
    %{_javadir}/%{name}-servlet-%{servletspec}-api.jar 30000

%post el-%{elspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/elspec.jar elspec \
   %{_javadir}/%{name}-el-%{elspec}-api.jar 20300

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service 

%postun jsp-%{jspspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jsp \
        %{_javadir}/%{name}-jsp-%{jspspec}-api.jar
fi

%postun servlet-%{servletspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove servlet \
        %{_javadir}/%{name}-servlet-%{servletspec}-api.jar
fi

%postun el-%{elspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove elspec \
        %{_javadir}/%{name}-el-%{elspec}-api.jar
fi

%triggerun -- tomcat < 0:7.0.22-2
/usr/bin/systemd-sysv-convert -- save tomcat > /dev/null 2>&1 || :
# Run these becasue the SysV package being removed won't do them
/sbin/chkconfig --del tomcat > /dev/null 2>&1 || :
/bin/systemctl try-restart tomcat.service > /dev/null 2>&1 || :

%files 
%defattr(0664,root,tomcat,0755)
# %doc {LICENSE,NOTICE,RELEASE*}
%attr(0755,root,root) %{_bindir}/%{name}-digest
%attr(0755,root,root) %{_bindir}/%{name}-tool-wrapper
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %{_unitdir}/%{name}@.service
%attr(0755,root,root) %dir %{_libexecdir}/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/%{name}/functions
%attr(0755,root,root) %{_libexecdir}/%{name}/preamble
%attr(0755,root,root) %{_libexecdir}/%{name}/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}

%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}

%defattr(0664,root,tomcat,0770)
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}

%defattr(0644,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/context.xml
%config(noreplace) %{confdir}/server.xml
%attr(0640,root,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{bindir}/bootstrap.jar
%{bindir}/catalina-tasks.xml
%{homedir}/lib
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%{homedir}/logs
%{homedir}/conf

%files admin-webapps
%defattr(0664,root,tomcat,0755)
%{appdir}/host-manager
%{appdir}/manager

%files docs-webapp
%defattr(-,root,root,-)
%{appdir}/docs

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

#     %files jsp-%{jspspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-jsp-api
#     %defattr(-,root,root,-)
#     %{_javadir}/%{name}-jsp-%{jspspec}*.jar

#     %files lib -f output/dist/src/res/maven/.mfiles-tomcat-lib
#     %defattr(-,root,root,-)
#     %{libdir}
#     %{bindir}/tomcat-juli.jar
#     %{_mavenpomdir}/JPP.%{name}-annotations-api.pom
#     %{_mavenpomdir}/JPP.%{name}-catalina-ha.pom
#     %{_mavenpomdir}/JPP.%{name}-catalina-tribes.pom
#     %{_mavenpomdir}/JPP.%{name}-catalina.pom
#     %{_mavenpomdir}/JPP.%{name}-jasper-el.pom
#     %{_mavenpomdir}/JPP.%{name}-jasper.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-api.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-juli.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-coyote.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-util.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-jdbc.pom
#     %{_mavenpomdir}/JPP.%{name}-websocket-api.pom
#     %{_mavenpomdir}/JPP.%{name}-tomcat-websocket.pom
#     %{_datadir}/maven-metadata/tomcat.xml
#     %exclude %{libdir}/%{name}-el-%{elspec}-api.jar

#     %files servlet-%{servletspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-servlet-api
#     %defattr(-,root,root,-)
#     %doc LICENSE
#     %{_javadir}/%{name}-servlet-%{servletspec}*.jar

#     %files el-%{elspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-el-api
#     %defattr(-,root,root,-)
#     %doc LICENSE
#     %{_javadir}/%{name}-el-%{elspec}-api.jar
#     %{libdir}/%{name}-el-%{elspec}-api.jar

%files webapps
%defattr(0644,tomcat,tomcat,0755)
%{appdir}/ROOT
%{appdir}/examples
%{appdir}/sample

%files jsvc
%defattr(755,root,root,0755)
%attr(0644,root,root) %{_unitdir}/%{name}-jsvc.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0660,tomcat,tomcat) %verify(not size md5 mtime) %{logdir}/catalina.out

%changelog
* Thu Jan 19 2017 Jean Girardet <jean.girardet@atos.net> - 8.5.11-1
- Update to 8.5.11

* Tue Nov 29 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.39-1
- Update to 8.0.39
- Resolves: rhbz#1397493 CVE-2016-6816 CVE-2016-6817 CVE-2016-8735 tomcat: various flaws

* Tue Oct 25 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.38-1
- Update to 8.0.38

* Sun Oct 23 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.37-3
- Resolves: rhbz#1383216 CVE-2016-6325 tomcat: tomcat writable config files allow privilege escalation
- Resolves: rhbz#1382310 CVE-2016-5425 tomcat: Local privilege escalation via systemd-tmpfiles service

* Tue Sep 13 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.37-1
- Rebase to 8.0.37
- Resolves: rhbz#1375581 CVE-2016-5388 CGI sets environmental variable based on user supplied Proxy request header
- Resolves: rhbz#1370262 catalina.out is no longer in use in the main package, but still gets rotated

* Thu Aug 11 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.36-2
- Related: rhbz#1349469 Correct typo in changelog entry

* Mon Aug 08 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.36-1
- Resolves: rhbz#1349469 CVE-2016-3092 tomcat: Usage of vulnerable FileUpload package can result in denial of service (updates to 8.0.36)
- Resolves: rhbz#1364056 The command tomcat-digest doesn't work
- Resolves: rhbz#1363884 The tomcat-tool-wrapper script is broken
- Resolves: rhbz#1347864 The systemd service unit does not allow tomcat to shut down gracefully
- Resolves: rhbz#1347835 The security manager doesn't work correctly (JSPs cannot be compiled)
- Resolves: rhbz#1341853 rpm -V tomcat fails on /var/log/tomcat/catalina.out
- Resolves: rhbz#1341850 tomcat-jsvc.service has TOMCAT_USER value hard-coded
- Resolves: rhbz#1359737 Missing maven depmap for the following artifacts: org.apache.tomcat:tomcat-websocket, org.apache.tomcat:tomcat-websocket-api
- Resolves: asfbz#59960  Building javadocs with java8 fails

* Wed Mar 2 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-4
- Revert sysconfig migration changes, resolves: rhbz#1311771, rhbz#1311905
- Add /etc/tomcat/conf.d/ with shell expansion support, resolves rhbz#1293636

* Sat Feb 27 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-3
- Load sysconfig from tomcat.conf, resolves: rhbz#1311771, rhbz#1311905
- Set default javax.sql.DataSource factory to apache commons one, resolves rhbz#1214381

* Sun Feb 21 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-2
- Fix symlinks from $CATALINA_HOME/lib perspective, resolves: rhbz#1308685

* Thu Feb 11 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-1
- Updated to 8.0.32
- Remove log4j support. It has never been working actually. See rhbz#1236297
- Move shipped config to /etc/sysconfig/tomcat. /etc/tomcat/tomcat.conf can now be used to override it with shell expansion, resolves rhbz#1293636
- Recommend tomcat-native, resolves: rhbz#1243132

* Wed Feb 10 2016 Coty Sutherland <csutherl@redhat.com> 1:8.0.26-4
- Resolves: rhbz#1286800 Failed to start component due to wrong allowLinking="true" in context.xml
- Program /bin/nologin does not exist (#1302718)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Robert Scheck <robert@fedoraproject.org> 1:8.0.26-2
- CATALINA_OPTS are only read when SECURITY_MANAGER is true (#1147105)

* Thu Aug 27 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.26-1
- Update to 8.0.26.

* Fri Jul 10 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.24-2
- Update to 8.0.24.

* Fri Jun 19 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.23-2
- Drop javax.el:el-api alias.

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.23-1
- Update to 8.0.23.

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.20-3
- Drop jetty alias for servlet.

* Tue Jun 09 2015 Michal Srb <msrb@redhat.com> - 1:8.0.20-2
- Fix metadata for org.apache.tomcat:{tomcat-jni,tomcat-util-scan}

* Thu Mar 5 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.18-5
- Rebuild against tomcat-taglibs-standard.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.18-4
- Fix epoch bumped el_1_0_api that would override all other glassfish/jboss/etc. due to wrong epoch.
- Drop old provides. 

* Tue Mar 03 2015 Stephen Gallagher <sgallagh@redhat.com> 1:8.0.18-3
- Bump epoch to maintain upgrade path from Fedora 22

* Mon Feb 16 2015 Michal Srb <msrb@redhat.com> - 0:8.0.18-2
- Install POM files for org.apache.tomcat:{tomcat-jni,tomcat-util-scan}

* Sun Feb 15 2015 Ivan Afonichev <ivan.afonichev@gmail.com> 0:8.0.18-1
- Updated to 8.0.18

* Sat Sep 20 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:8.0.12-1
- Updated to 8.0.12
- Substitute libnames in catalina-tasks.xml, resolves: rhbz#1126439
- Use CATALINA_OPTS only on start, resolves: rhbz#1051194

* Mon Jun 16 2014 Michal Srb <msrb@redhat.com> - 0:7.0.54-3
- jsp-api requires el-api

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.54-1
- Update to upstream 7.0.54 - fixes compile with Java 8.

* Wed May 21 2014 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.52-3
- Drop servlet/el api provides to reduce user machines ending with both.

* Sun Mar 30 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.52-2
- Don't provide maven javax.jsp:jsp-api and javax.servlet.jsp:javax.servlet.jsp-api resolves: rhbz#1076949
- Move log4j support into subpackage, resolves: rhbz#1027716

* Wed Mar 26 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.52-1
- Updated to 7.0.52
- Rewrite jsvc implementation, resolves: rhbz#1051743
- Switch to java-headless R, resolves: rhbz#1068566
- Create and own %{_localstatedir}/lib/tomcats, resolves: rhbz#1026741
- Add pom for tomcat-jdbc, resolves: rhbz#1011003 

* Tue Jan 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.47-3
- Fix installation of Maven metadata for tomcat-juli.jar
- Resolves: rhbz#1033664

* Wed Jan 15 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:7.0.47-2
- Rebuild for bug #1033664

* Sun Nov 03 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.47-1
- Updated to 7.0.47
- Fix java.security.policy

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.42-2
- Remove jpackage-utils R

* Thu Jul 11 2013 Dmitry Tikhonov <squall.sama@gmail.com> 0:7.0.42-1
- Updated to 7.0.42

* Tue Jun 11 2013 Paul Komkoff <i@stingr.net> 0:7.0.40-3
- Dropped systemv inits. Bye-bye.
- Updated the systemd wrappers to allow running multiple instances.
  Added wrapper scripts to do that, ported the original non-named
  service file to work with the same wrappers, updated
  /usr/sbin/tomcat to call systemctl.

* Sat May 11 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.40-1
- Updated to 7.0.40
- Resolves: rhbz 956569 added missing commons-pool link
- Remove ant-nodeps BR

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.37-2
- Add depmaps for org.eclipse.jetty.orbit
- Resolves: rhbz#917626

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.39-1
- Updated to 7.0.39

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.37-1
- Updated to 7.0.37

* Mon Feb 4 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.35-1
- Updated to 7.0.35
- systemd SuccessExitStatus=143 for proper stop exit code processing

* Mon Dec 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.34-1
- Updated to 7.0.34
- ecj >= 4.2.1 now required
- Resolves: rhbz 889395 concat classpath correctly; chdir to $CATALINA_HOME

* Fri Dec 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-2
- Resolves: rhbz 883806 refix logdir ownership 

* Sun Dec 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-1
- Updated to 7.0.33
- Resolves: rhbz 873620 need chkconfig for update-alternatives

* Wed Oct 17 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.32-1
- Updated to 7.0.32
- Resolves: rhbz 842620 symlinks to taglibs

* Fri Aug 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.29-1
- Updated to 7.0.29
- Add pidfile as tmpfile
- Use systemd for running as unprivileged user
- Resolves: rhbz 847751 upgrade path was broken
- Resolves: rhbz 850343 use new systemd-rpm macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.28-1
- Updated to 7.0.28
- Resolves: rhbz 820119 Remove bundled apache-commons-dbcp
- Resolves: rhbz 814900 Added tomcat-coyote POM
- Resolves: rhbz 810775 Remove systemv stuff from %post scriptlet
- Remove redhat-lsb R 

* Mon Apr 9 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-2
- Fixed native download hack

* Sat Apr 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-1
- Updated to 7.0.27
- Fixed jakarta-taglibs-standard BR and R

* Wed Mar 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:7.0.26-2
- Add more depmaps to J2EE apis to help jetty/glassfish updates

* Wed Mar 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:7.0.26-2
- Added the POM files for tomcat-api and tomcat-util (#803495)

* Wed Feb 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.26-1
- Updated to 7.0.26
- Bug 790334: Change ownership of logdir for logrotate

* Thu Feb 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-4
- Bug 790694: Priorities of jsp, servlet and el packages updated.

* Wed Feb 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-3
- Dropped indirect dependecy to tomcat 5

* Sun Jan 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-2
- Added hack for maven depmap of tomcat-juli absolute link [ -f ] pass correctly

* Sat Jan 21 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-1
- Updated to 7.0.25
- Removed EntityResolver patch (changes already in upstream sources)
- Place poms and depmaps in the same package as jars
- Added javax.servlet.descriptor to export-package of servlet-api
- Move several chkconfig actions and reqs to systemv subpackage
- New maven depmaps generation method
- Add patch to support java7. (patch sent upstream).
- Require java >= 1:1.6.0

* Fri Jan 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.23-5
- Exported javax.servlet.* packages in version 3.0 as 2.6 to make
  servlet-api compatible with Eclipse.

* Thu Jan 12 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-4
- Move jsvc support to subpackage

* Wed Jan 11 2012 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.23-2
- Add EntityResolver setter patch to jasper for jetty's need. (patch sent upstream).

* Mon Dec 12 2011 Joseph D. Wagner <joe@josephdwagner.info> 0:7.0.23-3
- Added support to /usr/sbin/tomcat-sysd and /usr/sbin/tomcat for
  starting tomcat with jsvc, which allows tomcat to perform some
  privileged operations (e.g. bind to a port < 1024) and then switch
  identity to a non-privileged user. Must add USE_JSVC="true" to
  /etc/tomcat/tomcat.conf or /etc/sysconfig/tomcat.

* Mon Nov 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-1
- Updated to 7.0.23

* Fri Nov 11 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-2
- Move tomcat-juli.jar to lib package
- Drop %%update_maven_depmap as in tomcat6
- Provide native systemd unit file ported from tomcat6

* Thu Oct 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-1
- Updated to 7.0.22

* Mon Oct 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 0:7.0.21-3.1
- rebuild (java), rel-eng#4932

* Mon Sep 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-3
- Fix basedir mode

* Tue Sep 20 2011 Roland Grunberg <rgrunber@redhat.com> 0:7.0.21-2
- Add manifests for el-api, jasper-el, jasper, tomcat, and tomcat-juli.

* Thu Sep 8 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-1
- Updated to 7.0.21

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-3
- Require java = 1:1.6.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-2
- Require java < 1.7.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-1
- Updated to 7.0.20

* Tue Jul 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.19-1
- Updated to 7.0.19

* Tue Jun 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.16-1
- Updated to 7.0.16

* Mon Jun 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-3
- Added initial systemd service
- Fix some paths

* Sat May 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-2
- Fixed http source link
- Securify some permissions
- Added licenses for el-api and servlet-api
- Added dependency on jpackage-utils for the javadoc subpackage

* Sat May 14 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-1
- Updated to 7.0.14

* Thu May 5 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-4
- Provided local paths for libs
- Fixed dependencies
- Fixed update temp/work cleanup

* Mon May 2 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-3
- Fixed package groups
- Fixed some permissions
- Fixed some links
- Removed old tomcat6 crap

* Thu Apr 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-2
- Package now named just tomcat instead of tomcat7
- Removed Provides:  %{name}-log4j
- Switched to apache-commons-* names instead of jakarta-commons-* .
- Remove the old changelog
- BR/R java >= 1:1.6.0 , same for java-devel
- Removed old tomcat6 crap

* Wed Apr 27 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-1
- Tomcat7
