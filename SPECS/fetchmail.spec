Name:		fetchmail
Version:	5.9.10
Release:	1
URL:		http://www.tuxedo.org/~esr/fetchmail
Source:         %{name}-%{version}.tar.gz
Group:		Applications/Mail
Group(pt_BR):   Aplicações/Correio Eletrônico
License:	GPL
Icon:		fetchmail.xpm
%ifos linux
Requires:	smtpdaemon
%endif
BuildRoot:	/var/tmp/%{name}-%{version}
Summary:	Full-featured POP/IMAP mail retrieval daemon
Summary(fr):    Collecteur (POP/IMAP) de courrier électronique
Summary(de):    Program zum Abholen von E-Mail via POP/IMAP
Summary(pt):    Busca mensagens de um servidor usando POP ou IMAP
Summary(es):    Recolector de correo via POP/IMAP
Summary(pl):    Zdalny demon pocztowy do protoko³ów POP2, POP3, APOP, IMAP
Summary(tr):    POP2, POP3, APOP, IMAP protokolleri ile uzaktan mektup alma yazýlýmý
Summary(da):    Alsidig POP/IMAP post-afhentnings dæmon

%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
%define DEFCC cc
%endif

%description
Fetchmail is a free, full-featured, robust, and well-documented remote
mail retrieval and forwarding utility intended to be used over
on-demand TCP/IP links (such as SLIP or PPP connections).  It
retrieves mail from remote mail servers and forwards it to your local
(client) machine's delivery system, so it can then be be read by
normal mail user agents such as mutt, elm, pine, (x)emacs/gnus, or mailx.
Comes with an interactive GUI configurator suitable for end-users.

%description -l fr
Fetchmail est un programme qui permet d'aller rechercher du courrier
électronique sur un serveur de mail distant. Fetchmail connait les
protocoles POP (Post Office Protocol), IMAP (Internet Mail Access
Protocol) et délivre le courrier électronique a travers le
serveur SMTP local (habituellement sendmail).

%description -l de
Fetchmail ist ein freies, vollständiges, robustes und
wohldokumentiertes Werkzeug zum Abholen und Weiterreichen von E-Mail,
gedacht zum Gebrauch über temporäre TCP/IP-Verbindungen (wie
z.B. SLIP- oder PPP-Verbindungen).  Es holt E-Mail von (weit)
entfernten Mail-Servern ab und reicht sie an das Auslieferungssystem
der lokalen Client-Maschine weiter, damit sie dann von normalen MUAs
("mail user agents") wie mutt, elm, pine, (x)emacs/gnus oder mailx
gelesen werden können.  Ein interaktiver GUI-Konfigurator auch gut
geeignet zum Gebrauch durch Endbenutzer wird mitgeliefert.

%description -l pt
Fetchmail é um programa que é usado para recuperar mensagens de um
servidor de mail remoto. Ele pode usar Post Office Protocol (POP)
ou IMAP (Internet Mail Access Protocol) para isso, e entrega o mail
através do servidor local SMTP (normalmente sendmail).
Vem com uma interface gráfica para sua configuração. 

%description -l es
Fetchmail es una utilidad gratis, completa, robusta y bien documentada
para la recepción y reenvío de correo pensada para ser usada en
conexiones TCP/IP temporales (como SLIP y PPP). Recibe el correo de
servidores remotos y lo reenvía al sistema de entrega local, siendo de
ese modo posible leerlo con programas como mutt, elm, pine, (x)emacs/gnus
o mailx. Contiene un configurador GUI interactivo pensado para usuarios.

%description -l pl
Fetchmail jest programem do ¶ci±gania poczty ze zdalnych serwerów
pocztowych. Do ¶ci±gania poczty mo¿e on uzywaæ protoko³ów POP (Post Office
Protocol) lub IMAP (Internet Mail Access Protocol). ¦ci±gniêt± pocztê
dostarcza do koñcowych odbiorców poprzez lokalny serwer SMTP.

%description -l tr
fetchmail yazýlýmý, POP veya IMAP desteði veren bir sunucuda yer alan
mektuplarýnýzý alýr.

%description -l da
Fetchmail er et gratis, robust, alsidigt og vel-dokumenteret værktøj 
til afhentning og videresending af elektronisk post via TCP/IP
baserede opkalds-forbindelser (såsom SLIP eller PPP forbindelser).   
Den henter post fra en ekstern post-server, og videresender den
til din lokale klient-maskines post-system, så den kan læses af
almindelige mail klienter såsom mutt, elm, pine, (x)emacs/gnus,
eller mailx. Der medfølger også et interaktivt GUI-baseret
konfigurations-program, som kan bruges af almindelige brugere.

%package -n fetchmailconf
Summary:        A GUI configurator for generating fetchmail configuration files
Summary(pl):    GUI konfigurator do fetchmaila
Summary(fr):	GUI configurateur pour fetchmail
Summary(es):	Configurador GUI interactivo para fetchmail
Summary(pt):	Um configurador gráfico para o fetchmail
Group:          Utilities/System
Group(pt):		Utilitários/Sistema
Requires:       %{name} = %{version}, python

%description -n fetchmailconf
A GUI configurator for generating fetchmail configuration file written in
python

%description -n fetchmailconf -l pt
Um configurador gráfico para a geração de arquivos de configuração do
fetchmail. Feito em python.

%description -n fetchmailconf -l es
Configurador gráfico para fetchmail escrito en python

%description -n fetchmailconf -l de
Ein interaktiver GUI-Konfigurator für fetchmail in python

%description -n fetchmailconf -l pl
GUI konfigurator do fetchmaila napisany w pythonie.

%prep
%setup -q

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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

LDFLAGS="-s"
./configure --prefix=%{_prefix} --with-datadir=%{_datadir} --enable-pop3        --without-kerberos --enable-imap --without-ssl        --enable-etrn --enable-ntlm --enable-nls --mandir=%{_mandir} 
                         # Remove --disable-nls, add --without-included-gettext
                         # for internationalization. Also look below.
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig
make install prefix=$RPM_BUILD_ROOT%{_prefix} mandir=$RPM_BUILD_ROOT%{_mandir}/man1
rm -rf contrib/RCS
chmod 644 contrib/*
cp rh-config/fetchmailconf.wmconfig $RPM_BUILD_ROOT/etc/X11/wmconfig/fetchmailconf
cd $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf fetchmail.1 fetchmailconf.1

mkdir -p %{buildroot}/usr/bin
cd %{buildroot}/usr/bin
/usr/bin/strip ../..%{_bindir}/* 2>/dev/null || :
ln -sf ../..%{_bindir}/* .
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (644, root, root, 755)
%doc README NEWS NOTES FAQ COPYING FEATURES contrib
%doc fetchmail-features.html fetchmail-FAQ.html design-notes.html
%attr(644, root, root) %{_mandir}/man1/*.1*
%attr(755, root, root) %{_prefix}/bin/fetchmail
/usr/bin/fetchmail
# Uncomment the following to support internationalization
%attr(644,root,root) %{_prefix}/share/locale/*/LC_MESSAGES/fetchmail.mo
# Uncomment the following to make split fetchmail and fetchmailconf packages
%files -n fetchmailconf
%attr(644,root,root) /etc/X11/wmconfig/fetchmailconf
%attr(755,root,root) %{_prefix}/bin/fetchmailconf
/usr/bin/fetchmailconf

%changelog
* Mon Mar 11 2002 David Clissold <cliss@austin.ibm.com>
- Update from version 5.9.6 --> 5.9.10

* Wed Jan 30 2002 David Clissold <cliss@austin.ibm.com>
- Update from version 5.9.4 --> 5.9.6

* Thu Oct 04 2001 David Clissold <cliss@austin.ibm.com>
- Eh?  No changelog?  Guess I'll start one.
- Update from version 5.9.0 --> 5.9.4

