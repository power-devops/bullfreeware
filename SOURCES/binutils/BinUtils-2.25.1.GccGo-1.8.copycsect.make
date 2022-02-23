BINUTILSPATH=$1
gcc 					\
        -Wall 				\
        -lz 				\
        -lintl 				\
        -L$BINUTILSPATH/libiberty/ 	\
        -liberty 			\
          $BINUTILSPATH/bfd/libbfd.a 	\
        -I$BINUTILSPATH/bfd/	 	\
        -I$BINUTILSPATH/include		\
        ./copycsect.c 			\
        -o copycsect
