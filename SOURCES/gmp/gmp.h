/*
 * This gmp.h is a wrapper include file for the original gmp.h, which has been
 * renamed to gmp-<arch>.h. There are conflicts for the original gmp.h when
 * compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef gmp_wrapper_h
#error "gmp_wrapper_h should not be defined!"
#endif
#define gmp_wrapper_h

#if defined(__64BIT__)
#include "gmp-ppc64.h"
#else
#include "gmp-ppc32.h"
#endif

#undef gmp_wrapper_h

