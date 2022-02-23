#!/bin/ksh

usr=$(id -u)
[ $usr == 0 ] || { echo "Doit etre lance sous root";exit 0; }

export u="girardet"
[ "$1" == "" ] || export u=$1

find . -type d | xargs chmod a+rwx

find . -type f  | xargs chmod a+rw

find . -name cups-config | xargs chown $u


