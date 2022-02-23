#!/bin/sh
#
# Splits NSS into nss-util 
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
util_dir=${name}-util-${version}
softokn_dir=${name}-softokn-${version}

# make_nss_util
#-------------------------------------------------
# create the nss-util subset consisting of
#   mozilla/dbm                   --- full directory
#   mozilla/security              --- top empty
#   mozilla/security/coreconf     --- full directory
#   mozilla/security/nss          --- top files only
#   mozilla/security/nss/lib      --- top files only
#   mozilla/security/nss/lib/util --- full directory
#--------------------------------------------------

UTIL_WORK=${util_dir}-work
rm -rf ${UTIL_WORK}
mkdir ${UTIL_WORK}

# copy everything
cp -a ${nss_source_dir} ${UTIL_WORK}/${util_dir}

# remove subdirectories that we don't want
rm -rf ${UTIL_WORK}/${util_dir}/mozilla/security/nss/cmd
rm -rf ${UTIL_WORK}/${util_dir}/mozilla/security/nss/tests
rm -rf ${UTIL_WORK}/${util_dir}/mozilla/security/nss/lib

# start with an empty lib directory to be filled
mkdir ${UTIL_WORK}/${util_dir}/mozilla/security/nss/lib
# copy some files at the top and the util subdirectory recursively
cp ${nss_source_dir}/mozilla/security/nss/lib/Makefile ${UTIL_WORK}/${util_dir}/mozilla/security/nss/lib
cp ${nss_source_dir}/mozilla/security/nss/lib/manifest.mn ${UTIL_WORK}/${util_dir}/mozilla/security/nss/lib
cp -a ${nss_source_dir}/mozilla/security/nss/lib/util ${UTIL_WORK}/${util_dir}/mozilla/security/nss/lib/util
pushd ${UTIL_WORK}
# the compressed tar ball for nss-util
tar -cjf ../${name}-util-${version}.tar.bz2 ${util_dir}
popd

# cleanup after ourselves
rm -fr ${nss_source_dir}
rm -fr ${UTIL_WORK}



