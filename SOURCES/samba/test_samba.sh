
# Verify WINDBIND and pam_winbind.so are present
if [ ! -f /opt/freeware/lib64/security/WINBIND/WINBIND.so ]; then
    echo "File 'WINBIND.so' must be present in '/opt/freeware/lib64/security/WINBIND'."
    exit 1
fi

if [ ! -f /opt/freeware/lib64/security/pam_winbind.so ]; then
    echo "File 'pam_winbind.so' must be present in '/opt/freeware/lib64/security/'."
    exit 1
fi

# Verify configuration is correctly fullfilled
if [ -z "`grep -e 'WINBIND:
 *program = /opt/freeware/lib64/security/WINBIND' /usr/lib/security/methods.cfg`" ];then
    echo "/usr/lib/security/methods.cfg must have"
    echo "WINBIND:"
    echo "      program = /opt/freeware/lib64/security/WINBIND"
    exit 1
fi

if [ -z "`grep -e 'WINBIND:
 *SYSTEM = "WINBIND or compat"
 *registry = WINBIND' /etc/security/user`" ];then
    echo "/etc/security/user must have"
    echo "WINBIND:"
    echo '       SYSTEM = "WINBIND or compat"'
    echo "       registry = WINBIND"
    exit 1
fi

echo "/opt/freeware/sbin/nmbd --version"
echo "`/opt/freeware/sbin/nmbd --version`"
echo "/opt/freeware/sbin/smbd --version"
echo "`/opt/freeware/sbin/smbd --version`"
echo "/opt/freeware/sbin/winbindd --version"
echo "`/opt/freeware/sbin/winbindd --version`"
echo "/opt/freeware/bin/smbclient --version"
echo "`/opt/freeware/bin/smbclient --version`"

echo "Check if a server is running."
if [ -z "`ps -ef | grep -E '/opt/freeware/sbin/smbd|/opt/freeware/sbin/nmbd|/opt/freeware/sbin/win' | grep -v grep`" ];then
    echo "No. Run it."
else
    echo "Yes. Exit check."
    echo "Checked with command \"ps -ef | grep -E '/opt/freeware/sbin/smbd|/opt/freeware/sbin/nmbd|/opt/freeware/sbin/win'\"."
    exit 1
fi

echo "/opt/freeware/bin/smbclient -U% -L localhost"
echo "`/opt/freeware/bin/smbclient -U% -L localhost`"
if [ "`/opt/freeware/bin/smbclient -U% -L localhost 2>&1`" != "do_connect: Connection to localhost failed (Error NT_STATUS_CONNECTION_REFUSED)" ];then
    echo "'smbclient -U% -L localhost' must return 'do_connect: Connection to localhost failed (Error NT_STATUS_CONNECTION_REFUSED)'"
    exit 1
fi

echo "Begin server"
echo "/opt/freeware/sbin/nmbd"
/opt/freeware/sbin/nmbd
if [ "$?" != "0" ];then
    echo "/opt/freeware/sbin/nmbd did not begin correctly."
    exit 1
fi

echo "/opt/freeware/sbin/smbd"
/opt/freeware/sbin/smbd
if [ "$?" != "0" ];then
    echo "/opt/freeware/sbin/smbd did not begin correctly."
    exit 1
fi

echo "/opt/freeware/sbin/winbindd"
/opt/freeware/sbin/winbindd
if [ "$?" != "0" ];then
    echo "/opt/freeware/sbin/winbindd did not begin correctly."
    exit 1
fi

sleep 5
echo "/opt/freeware/bin/wbinfo -p"
echo "`/opt/freeware/bin/wbinfo -p`"
if [ "`/opt/freeware/bin/wbinfo -p`" != "Ping to winbindd succeeded" ];then
    echo "'/opt/freeware/bin/wbinfo -p' must return 'Ping to winbindd succeeded'"
    exit 1
fi

echo "/opt/freeware/bin/wbinfo --own-domain"
echo "`/opt/freeware/bin/wbinfo --own-domain`"
if [ "`/opt/freeware/bin/wbinfo --own-domain`" != "MYGROUP" ];then
    echo "'/opt/freeware/bin/wbinfo --own-domain' must return 'MYGROUP'"
    exit 1
fi

echo "/opt/freeware/bin/smbclient -U% -L localhost"
echo "`/opt/freeware/bin/smbclient -U% -L localhost`"
if [ "`/opt/freeware/bin/smbclient -U% -L localhost 2>&1`" == "do_connect: Connection to localhost failed (Error NT_STATUS_CONNECTION_REFUSED)" ];then
    echo "'smbclient -U% -L localhost' shall NOT return 'do_connect: Connection to localhost failed (Error NT_STATUS_CONNECTION_REFUSED)'"
    exit 1
fi
