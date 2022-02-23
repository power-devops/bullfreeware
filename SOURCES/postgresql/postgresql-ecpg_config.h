/*
 * This ecpg_config.h is a wrapper include file for the original ecpg_config.h,
 * which has been renamed to ecpg_config-<arch>.h. There are conflicts for the
 * when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Michael Perzl <michael@perzl.org>
 */

#ifdef ecpg_config_wrapper_h
#error "ecpg_config_wrapper_h should not be defined!"
#endif
#define ecpg_config_wrapper_h

#if defined(__64BIT__)
#include "ecpg_config-ppc64.h"
#else
#include "ecpg_config-ppc32.h"
#endif

#undef ecpg_config_wrapper_h

