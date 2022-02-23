#ifndef __FTCONFIG_H__MULTILIB
#define __FTCONFIG_H__MULTILIB

/*
    Not on AIX  #include <bits/wordsize.h>
                #if __WORDSIZE == 32
 */

#ifndef __64BIT__
# include "ftconfig-32.h"
#else
# include "ftconfig-64.h"
#endif

#endif 
