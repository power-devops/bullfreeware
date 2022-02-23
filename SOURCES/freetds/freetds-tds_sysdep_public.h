/*
 * This tds_sysdep_public.h is a wrapper include file for the original
 * tds_sysdep_public.h, which has been renamed to tds_sysdep_public-<arch>.h.
 * There are conflicts for the when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef tds_sysdep_public_wrapper_h
#error "tds_sysdep_public_wrapper_h should not be defined!"
#endif
#define tds_sysdep_public_wrapper_h

#if defined(__64BIT__)
#include "tds_sysdep_public-ppc64.h"
#else
#include "tds_sysdep_public-ppc32.h"
#endif

#undef tds_sysdep_public_wrapper_h

