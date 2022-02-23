
# Shell script building copycsect binary.
# $1 is the target bit architecture (32 or 64)
# $2 is the source directory of binutils

default_arch=$1
BINUTILS_SRC_DIR=$2
COPYCSECT_SRC_DIR=${BINUTILS_SRC_DIR}/copycsect


if [[ "$default_arch" == "64" ]]; then
   CC="gcc -maix64"
   SYSLIBS="/opt/freeware/lib64/libintl.a -L/opt/freeware/lib64 -lz"
else
    CC="gcc -maix32"
    SYSLIBS="/opt/freeware/lib/libintl.a -L/opt/freeware/lib -lz"
fi

BFDLIBS="${BINUTILS_SRC_DIR}/libiberty/libiberty.a ${BINUTILS_SRC_DIR}/bfd/libbfd.a"

$CC					\
    -Wall				\
    $SYSLIBS				\
    $BFDLIBS				\
    -I${BINUTILS_SRC_DIR}/bfd/		\
    -I${BINUTILS_SRC_DIR}/include		\
    ${COPYCSECT_SRC_DIR}/copycsect.c		\
    -o ${COPYCSECT_SRC_DIR}/copycsect
