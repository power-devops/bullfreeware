/*
 * This curlbuild.h is a wrapper include file for the original curlbuild.h,
 * which has been renamed to curlbuild-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef curlbuild_wrapper_h
#error "curlbuild_wrapper_h should not be defined!"
#endif
#define curlbuild_wrapper_h

#if defined(__64BIT__)
#include "curl/curlbuild-ppc64.h"
#else
#include "curl/curlbuild-ppc32.h"
#endif

#undef curlbuild_wrapper_h

