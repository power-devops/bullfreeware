/*
 * This bson-config.h is a wrapper include file for the original bson-config.h,
 * which has been renamed to bson-config-<arch>.h. There are conflicts for the
 * original bson-config.h when compiling either in 32-bit or 64-bit mode.
 * Please do not use the arch-specific file directly.
 *
 * Tony Reix <tony.reix@atos.net>
 */

#ifdef libbson_wrapper_h
#error "libbson_wrapper_h should not be defined!"
#endif
#define libbson_wrapper_h

#if defined(__64BIT__)
#include "bson-config-ppc64.h"
#else
#include "bson-config-ppc32.h"
#endif

#undef libbson_wrapper_h
