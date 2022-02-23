/*
 * This orbit-config.h is a wrapper include file for the original orbit-config.h,
 * which has been renamed to orbitconfig-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef orbitconfig_wrapper_h
#error "orbitconfig_wrapper_h should not be defined!"
#endif
#define orbitconfig_wrapper_h

#if defined(__64BIT__)
#include "orbit-config-ppc64.h"
#else
#include "orbit-config-ppc32.h"
#endif

#undef orbitconfig_wrapper_h

