/*
 * This ap.h is a wrapper include file for the original apr.h,
 * which has been renamed to apr-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef apr_wrapper_h
#error "apr_wrapper_h should not be defined!"
#endif
#define apr_wrapper_h

#if defined(__64BIT__)
#include "apr-ppc64.h"
#else
#include "apr-ppc32.h"
#endif

#undef apr_wrapper_h

