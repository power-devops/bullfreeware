#!/bin/sh
#
# Splits NSS into nss-util and nss-softokn
# Takes as command line input the version of nss
# and assumes that a file nss-${nss_version}-stripped.tar.bz2
# exits in the current directory

set -e

if test -z $1
then
  echo "usage: $0 nss-version"
  exit
fi

export name=nss
export version=$1

echo "Extracting ${name}-${version}-stripped.tar.bz2"

tar -xjf ${name}-${version}-stripped.tar.bz2

# the directory will be named ${name}-${version}

nss_source_dir=${name}-${version}
softokn_dir=${name}-softokn-${version}

# make_nss_softokn
#-------------------------------------------------
# create the nss-softokn subset consisting of
#   mozilla/dbm                      --- full directory
#   mozilla/security                 --- top empty
#   mozilla/security/coreconf        --- full directory
#   mozilla/security/nss             --- top files only
#   mozilla/security/nss/lib         --- top files only
#   mozilla/security/nss/lib/freebl  --- full directory
#   mozilla/security/nss/lib/softoken --- full directory
#   mozilla/security/nss/lib/softoken/dbm --- full directory
#-------------------------------------------------------

SOFTOKN_WORK=${softokn_dir}-work
rm -rf ${SOFTOKN_WORK}
mkdir ${SOFTOKN_WORK}

# copy everything
cp -a ${nss_source_dir} ${SOFTOKN_WORK}/${softokn_dir}

# remove subdirectories that we don't want
rm -rf ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd
rm -rf ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/tests
rm -rf ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib
rm -rf ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/pkg
# rstart with an empty lib directory and copy only what we need
mkdir ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib
# copy entire freebl and softoken directories recursively
cp -a ${nss_source_dir}/mozilla/security/nss/lib/freebl ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib/freebl
cp -a ${nss_source_dir}/mozilla/security/nss/lib/softoken ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib/softoken
cp -a ${nss_source_dir}/mozilla/security/nss/lib/softoken ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib/softoken/dbm

# and some Makefiles and related files
cp ${nss_source_dir}/mozilla/security/nss/Makefile ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss
cp ${nss_source_dir}/mozilla/security/nss/manifest.mn ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss
cp ${nss_source_dir}/mozilla/security/nss/trademarks.txt ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss
cp ${nss_source_dir}/mozilla/security/nss/lib/Makefile ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib
cp ${nss_source_dir}/mozilla/security/nss/lib/manifest.mn ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/lib

# we do need shlibsign from cmd
mkdir ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd
# copy some files at the top and the slhlib subdirectory
cp -p ${nss_source_dir}/mozilla/security/nss/cmd/Makefile ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd
cp -p ${nss_source_dir}/mozilla/security/nss/cmd/manifest.mn ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd
cp -p ${nss_source_dir}/mozilla/security/nss/cmd/platlibs.mk ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd
cp -p ${nss_source_dir}/mozilla/security/nss/cmd/platrules.mk ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd

cp -a ${nss_source_dir}/mozilla/security/nss/cmd/shlibsign ${SOFTOKN_WORK}/${softokn_dir}/mozilla/security/nss/cmd/shlibsign

pushd ${SOFTOKN_WORK}
# the compressed tar ball for nss-softokn
tar -cjf ../${name}-softokn-${version}-stripped.tar.bz2 ${softokn_dir}
popd

# cleanup after ourselves
rm -fr ${nss_source_dir}
rm -rf ${SOFTOKN_WORK}



