#!/bin/sh
# Example of a shell script to switch Python primary from Python 3 to Python 2

BINDIR=/opt/freeware/bin

function check_link {
	if [[ ! -L $1 ]]; then
		echo "Error: $1 should be a link !"
		echo "Aborting..."
		exit 1
	fi
}


function usage {
	echo "Usage: ChangePythonPrimaryVersion.sh [V2|V3]"
	echo "  V2 means python2 will be default."
	echo "  V3 means python3 will be default."
}

TARGET_VERSION=

case "$1" in
	"V2") TARGET_VERSION=2;;
	"V3") TARGET_VERSION=3;;
	*) usage; exit ;;
esac

if [[ "$TARGET_VERSION" == "V2" ]]; then
	PYDEVEL_NAME=python-devel
	PYTOOLS_NAME=python-tools
else
	PYDEVEL_NAME=python3-devel
	PYTOOLS_NAME=python3-tools
fi

if rpm -qa | grep -q $PYDEVEL_NAME; then
	HAS_PYDEVEL=True
fi
if rpm -qa | grep -q $PYTOOLS_NAME; then
	HAS_PYTOOLS=True
fi

PY_VERSION_OUT=`${BINDIR}/python --version 2>&1`
if echo $PY_VERSION_OUT | grep -q "Python $TARGET_VERSION"; then
	echo "Python $TARGET_VERSION seems to be already set by default:"
	echo "  ${BINDIR}/python --version: $PY_VERSION_OUT"
	echo ""
	echo "No change performed"
	exit 0
fi

DEFAULT_BIT=32
if ls -l ${BINDIR}/python${TARGET_VERSION} | grep -q "_64"; then
	DEFAULT_BIT=64
fi

cd $BINDIR


# Check that current links are correct
check_link python
check_link python_32
check_link python_64
check_link pydoc
check_link pydoc_32
check_link pydoc_64

if [[ ! -z "$HAS_PYDEVEL" ]]; then
	check_link python-config
	check_link python-config_32
	check_link python-config_64
fi

if [[ ! -z "$HAS_PYTOOLS" ]]; then
	check_link idle
	check_link idle_32
	check_link idle_64
fi

# Make links
ln -sf python${TARGET_VERSION}    python
ln -sf python${TARGET_VERSION}_32 python_32
ln -sf python${TARGET_VERSION}_64 python_64
ln -sf pydoc${TARGET_VERSION}     pydoc
ln -sf pydoc${TARGET_VERSION}_32  pydoc_32
ln -sf pydoc${TARGET_VERSION}_64  pydoc_64

if [[ ! -z "$HAS_PYDEVEL" ]]; then
	ln -sf python${TARGET_VERSION}-config    python-config
	ln -sf python${TARGET_VERSION}-config_32 python-config_32
	ln -sf python${TARGET_VERSION}-config_64 python-config_64
fi

if [[ ! -z "$HAS_PYTOOLS" ]]; then
	ln -sf idle${TARGET_VERSION}    idle
	ln -sf idle${TARGET_VERSION}_32 idle_32
	ln -sf idle${TARGET_VERSION}_64 idle_64
fi

# Restore default architecture
if [[ "$DEFAULT_BIT" == "64" ]]; then
	echo "64 bit version set by default"
	ln -sf python${TARGET_VERSION}_64        python${TARGET_VERSION}
	ln -sf pydoc${TARGET_VERSION}_64         pydoc${TARGET_VERSION}
	[[ ! -z "$HAS_PYDEVEL" ]] && ln -sf python${TARGET_VERSION}-config_64 python${TARGET_VERSION}-config
	[[ ! -z "$HAS_PYTOOLS" ]] && ln -sf idle${TARGET_VERSION}_64          idle${TARGET_VERSION}
else
	echo "32 bit version set by default"
	ln -sf python${TARGET_VERSION}_32        python${TARGET_VERSION}
	ln -sf pydoc${TARGET_VERSION}_32         pydoc${TARGET_VERSION}
	[[ ! -z "$HAS_PYDEVEL" ]] && ln -sf python${TARGET_VERSION}-config_32 python${TARGET_VERSION}-config
	[[ ! -z "$HAS_PYTOOLS" ]] && ln -sf idle${TARGET_VERSION}_32          idle${TARGET_VERSION}
fi

echo "Python $TARGET_VERSION is now the default version."
