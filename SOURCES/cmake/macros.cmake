#
# Macros for cmake
#
# Warning: do not remove the -DCMAKE_MODULE_LINKER_FLAGS command as it is required to build kde and qt apps
#

%__cmake %{_bindir}/cmake

%_cmake_lib_suffix64 -DLIB_SUFFIX=64
%_cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=ON
%_cmake_verbose -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON
%_cmake_debug %{?with_debug:debug}%{?!with_debug:RelWithDebInfo}
%_cmake_module_linker_flags %(echo %ldflags|sed -e 's#-Wl,--no-undefined##')
%_cmake_disable_intree_build 1

%cmake \
    %setup_compile_flags \
    %{?_cmake_disable_intree_build:
    mkdir -p build \
    cd build} \
    %__cmake %{?_cmake_disable_intree_build:..} \\\
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \\\
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \\\
        -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \\\
        -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \\\
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \\\
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \\\
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \\\
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \\\
        -DCMAKE_BUILD_TYPE=%{_cmake_debug} \\\
        -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG" \\\
        -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG" \\\
%if "%{?_lib}" == "lib64" \
        %{?_cmake_lib_suffix64} \\\
%endif \
	%{?_cmake_skip_rpath} \\\
        %{?_cmake_verbose} \\\
        %{?_cmake_module_linker_flags:-DCMAKE_MODULE_LINKER_FLAGS="%_cmake_module_linker_flags%{?_cmake_module_linker_flags_extra: %_cmake_module_linker_flags_extra}"} \\\
        -DBUILD_SHARED_LIBS:BOOL=ON \\\
        -DBUILD_STATIC_LIBS:BOOL=OFF
