/*
 * This tiffconf.h is a wrapper include file for the original tiffconf.h,
 * which has been renamed to tiffconf-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef tiffconf_wrapper_h
#error "tiffconf_wrapper_h should not be defined!"
#endif
#define tiffconf_wrapper_h

#if defined(__64BIT__)
#include "tiffconf-ppc64.h"
#else
#include "tiffconf-ppc32.h"
#endif

#undef tiffconf_wrapper_h

