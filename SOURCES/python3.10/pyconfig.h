/*
 * This pyconfig.h is a wrapper include file for the original pyconfig.h,
 * which has been renamed to pyconfig-<arch>.h. There are conflicts for the
 * original pyconfig.h when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef python_wrapper_h
#error "python_wrapper_h should not be defined!"
#endif
#define python_wrapper_h

#if defined(__64BIT__)
#include "pyconfig-ppc64.h"
#else
#include "pyconfig-ppc32.h"
#endif

#undef python_wrapper_h

