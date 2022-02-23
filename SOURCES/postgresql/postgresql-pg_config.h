/*
 * This pg_config.h is a wrapper include file for the original pg_config.h,
 * which has been renamed to pg_config-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef pg_config_wrapper_h
#error "pg_config_wrapper_h should not be defined!"
#endif
#define pg_config_wrapper_h

#if defined(__64BIT__)
#include "pg_config-ppc64.h"
#else
#include "pg_config-ppc32.h"
#endif

#undef pg_config_wrapper_h

