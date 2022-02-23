/*
 * This art_config.h is a wrapper include file for the original art_config.h,
 * which has been renamed to art_config-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef art_config_wrapper_h
#error "art_config_wrapper_h should not be defined!"
#endif
#define art_config_wrapper_h

#if defined(__64BIT__)
#include "art_config-ppc64.h"
#else
#include "art_config-ppc32.h"
#endif

#undef art_config_wrapper_h

