#!/bin/sh
# Example of a shell script to switch Python primary from Python 2 to Python 3

# There are tests to verify that the switch has not already been performed
# and that the destination *.P2 files do not exist.
# If the Python 3 *.P3 files do not exit, the switch is not performed.
# If the Python 2 files have not been moved, the switch is not performed.

# For RPMs python/python3

if test ! -e /opt/freeware/bin/python.P2 && /opt/freeware/bin/python --version 2>&1 | grep  'Python 2'
then
        mv /opt/freeware/bin/pydoc /opt/freeware/bin/pydoc.P2
        mv /opt/freeware/bin/pydoc_64 /opt/freeware/bin/pydoc_64.P2
        mv /opt/freeware/bin/python /opt/freeware/bin/python.P2
        mv /opt/freeware/bin/python_64 /opt/freeware/bin/python_64.P2
        echo "Files of RPM python moved to .P2"
else
        echo "Files of RPM python not moved or not found"
fi

# The link python may have been modified to link to python_64
if test ! -e /opt/freeware/bin/python && test -e /opt/freeware/bin/python_64.P3
then
        mv /opt/freeware/bin/pydoc.P3 /opt/freeware/bin/pydoc
        mv /opt/freeware/bin/pydoc_64.P3 /opt/freeware/bin/pydoc_64
        mv /opt/freeware/bin/python.P3 /opt/freeware/bin/python
        mv /opt/freeware/bin/python_64.P3 /opt/freeware/bin/python_64
        echo "Files of RPM python3 now primary version"
else
        echo "Files of RPM python3 not found or python not moved"
fi

# For RPMs python-devel/python3-devel

# /opt/freeware/bin/python2.7-config/: Python script, ASCII text executable
# /opt/freeware/bin/python3.6-config/: POSIX shell script, ASCII text executable


if test ! -e /opt/freeware/bin/python-config.P2 && file /opt/freeware/bin/python-config/ | grep  'Python script'
then
        mv /opt/freeware/bin/python-config /opt/freeware/bin/python-config.P2
        echo "File of RPM python-devel moved to .P2"
else
        echo "File python-config of RPM python-devel not moved or not found"
fi

if test ! -e /opt/freeware/bin/python-config && test -e /opt/freeware/bin/python-config.P3 
then
        mv /opt/freeware/bin/python-config.P3 /opt/freeware/bin/python-config
        echo "File of RPM python3-config now primary version"
else
        echo "File of RPM python3-devel not found or python-devel not moved"
fi

# For RPMs python-tools/python3-tools

if test ! -e /opt/freeware/bin/idle.P2 && grep -s python2 /opt/freeware/bin/idle
then
        mv /opt/freeware/bin/2to3 /opt/freeware/bin/2to3.P2
        mv /opt/freeware/bin/2to3_64 /opt/freeware/bin/2to3_64.P2
        mv /opt/freeware/bin/idle /opt/freeware/bin/idle.P2
        mv /opt/freeware/bin/idle_64 /opt/freeware/bin/idle_64.P2
        echo "Files of RPM python-tools moved to .P2"
else
        echo "Files of RPM python-tools not moved or not found"
fi

if test ! -e /opt/freeware/bin/idle && test -e /opt/freeware/bin/idle.P3
then
        mv /opt/freeware/bin/2to3.P3 /opt/freeware/bin/2to3
        mv /opt/freeware/bin/2to3_64.P3 /opt/freeware/bin/2to3_64
        mv /opt/freeware/bin/idle.P3 /opt/freeware/bin/idle
        mv /opt/freeware/bin/idle_64.P3 /opt/freeware/bin/idle_64
        echo "Files of RPM python3-tools now primary version"
else
        echo "Files of RPM python3-tools not found or python-tools not moved"
fi



