/*
 * This rubyconfig.h is a wrapper include file for the original config.h,
 * to deal with 32 / 64 bits.
 */

#ifndef ruby_wrapper_h
#define ruby_wrapper_h
#else

#if defined(__64BIT__)
#include "config-ppc64.h"
#else
#include "config-ppc32.h"
#endif

#endif //python_wrapper_h

