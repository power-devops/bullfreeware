/*
 * This unixodbc_conf.h is a wrapper include file for the original
 * unixodbc_conf.h, which has been renamed to unixodbc_conf-<arch>.h.
 * There are conflicts for the original unixodbc_conf.h file when compiling
 * either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef unixodbc_conf_wrapper_h
#error "unixodbc_conf_wrapper_h should not be defined!"
#endif
#define unixodbc_conf_wrapper_h

#if defined(__64BIT__)
#include "unixodbc_conf-ppc64.h"
#else
#include "unixodbc_conf-ppc32.h"
#endif

#undef unixodbc_conf_wrapper_h

