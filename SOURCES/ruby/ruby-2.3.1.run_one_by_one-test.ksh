#!/bin/ksh

export D=$(date +%y%d%m_%H%M)

run_test ()
{
    set -x
    echo LIGNE=$0 $@
    [ "$0" == "" ] && exit;
    CMD='./miniruby -I./lib -I. -I.ext/common ./tool/runruby.rb --extout=.ext --disable-gems "./test/runner.rb" --ruby="./miniruby -I./lib -I. -I.ext/common --extout=.ext -- --disable-gems" -n '
    CMD_ALL="$CMD \"$1\""
    echo "\n\n $CMD_ALL"    >> traces_run_tests.log
    echo "\n$CMD_ALL"       >> traces_liste_test_failed.$D.log
    eval ./$CMD_ALL  2>&1 | tee -a  traces_liste_test_failed.$D.log
}


SKIPTEST="TestTime#test_at
TestPTY#test_commandline
TestPTY#test_argv0"

TESTS="IMAPTest#test_idle_timeout
Rinda::TestRingFinger#test_make_socket_unicast
Rinda::TestRingServer#test_make_socket_ipv4_multicast
Rinda::TestRingServer#test_ring_server_ipv4_multicast
TestDBM_RDONLY#test_delete_rdonly
TestDir_M17N#test_glob_encoding
TestFileExhaustive#test_executable_p
TestFileExhaustive#test_executable_real_p
TestFind#test_unreadable_dir
TestFind#test_unsearchable_dir
TestFloatExt#test_nextafter_169_other_-0.0_0.0
TestFloatExt#test_nextafter_188_other_0.0_-0.0
TestGDBM#test_s_open_error
TestGDBM_RDONLY#test_delete_rdonly
TestGem#test_self_ensure_gem_directories_write_protected
TestGem#test_self_ensure_gem_directories_write_protected_parents
TestGemCommandsCleanupCommand#test_execute_all_user_no_sudo
TestGemCommandsInstallCommand#test_execute_no_user_install
TestGemExtCmakeBuilder#test_self_build
TestGemExtCmakeBuilder#test_self_build_has_makefile
TestGemExtConfigureBuilder#test_self_build
TestGemExtConfigureBuilder#test_self_build_has_makefile
TestGemExtExtConfBuilder#test_class_build
TestGemExtExtConfBuilder#test_class_build_rbconfig_make_prog
TestGemExtExtConfBuilder#test_class_build_unconventional
TestGemExtExtConfBuilder#test_class_make
TestGemInstallUpdateOptions#test_user_install_disabled_read_only
TestGemInstaller#test_generate_bin_script_no_perms
TestGemInstaller#test_generate_bin_symlink_no_perms
TestGemRDoc#test_remove_unwritable
TestGemRDoc#test_setup_unwritable
TestGemRemoteFetcher#test_download_local_read_only
TestGemRemoteFetcher#test_download_read_only
TestGemSpecification#test_build_extensions_extensions_dir_unwritable
TestParallel::TestParallelWorker#test_accept_run_command_multiple_times
TestParallel::TestParallelWorker#test_done
TestParallel::TestParallelWorker#test_run
TestParallel::TestParallelWorker#test_run_multiple_testcase_in_one_file
TestPathname#test_executable?
TestPathname#test_executable_real?
TestPathname#test_find
TestProcess#test_rlimit_value
TestRDocOptions#test_check_files
TestRDocRDoc#test_parse_file_forbidden
TestRDocRubygemsHook#test_remove_unwritable
TestRDocRubygemsHook#test_setup_unwritable
TestSDBM#test_readonly
TestSDBM#test_s_open_error
TestSocket#test_udp_recvmsg_truncation
TestSocketAddrinfo#test_ipv6_address_predicates
TestSocket_BasicSocket#test_getsockopt
TestZlib#test_adler32_combine
TestZlib#test_crc32_combine"

RPM_SOURCE_DIR="/opt/freeware/src/packages/SOURCES"
RPM_BUILD_DIR="/opt/freeware/src/packages/BUILD"
RPM_OPT_FLAGS="-O2 -fsigned-char"
RPM_ARCH="ppc"
RPM_OS="aix"
export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS

RPM_DOC_DIR="/opt/freeware/doc"
export RPM_DOC_DIR
RPM_PACKAGE_NAME="ruby"
RPM_PACKAGE_VERSION="2.3.1"
# RPM_PACKAGE_RELEASE="3"
# export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION 
# RPM_BUILD_ROOT="/var/opt/freeware/tmp/ruby-2.3.1-3-root"
# export RPM_BUILD_ROOT
umask 022




export MINIRUBYOPT="-v "

export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export GLOBAL_CC_OPTIONS=" "

export CONFIG_SHELL=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"



cd /opt/freeware/src/packages/BUILD || exit 1
cd ruby-2.3.1 || exit 1




cd 64bit
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64"
export CXX="/opt/freeware/bin/g++ -maix64"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

rm -f traces_liste_test_failed.$D.log resultat.traces.liste_test_failed.$D.log traces_run_tests.log
					
for str in $TESTS
do
    run_test $str
done
    
rm -f resultat.traces.liste_test_failed.$D.log
echo "Fini : "$(grep 'Finished tests'  traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Run  : "$(grep 'Running tests:'  traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "PASS : "$(grep '^\.[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Fail : "$(grep  '^F[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Erre : "$(grep  '^E[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "SKIP : "$(grep  '^S[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log


cd ../32bit
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32"
export CXX="/opt/freeware/bin/g++ -maix32"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"

rm -f traces_liste_test_failed.$D.log resultat.traces.liste_test_failed.$D.log traces_run_tests.log
					
for str in $TESTS
do
    run_test $str
done
    

rm -f resultat.traces.liste_test_failed.$D.log
echo "Fini : "$(grep 'Finished tests'  traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Run  : "$(grep 'Running tests:'  traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "PASS : "$(grep '^\.[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Fail : "$(grep  '^F[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "Erre : "$(grep  '^E[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log
echo "SKIP : "$(grep  '^S[ 	]*$' traces_liste_test_failed.$D.log |wc -l) >> resultat.traces.liste_test_failed.$D.log


