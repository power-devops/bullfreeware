/*
  Compile on hardy1 with:

Needs binutils installed:
  # gcc -Wall copycsect.c -L/opt/freeware/lib/ -lz -lintl -L/opt/freeware/src/packages/BUILD/binutils-2.25.1/libiberty/ -liberty -lbfd -I/opt/freeware/src/packages/BUILD/binutils-2.25.1/bfd/ -I/opt/freeware/src/packages/BUILD/binutils-2.25.1/include -o copycsect

All .h and .a files that are required are not in binutils package...
One must compile copycsect WITH the binutils sources
  # gcc -Wall copycsect.c -L/opt/freeware/lib/ -lz -lintl -L/opt/freeware/src/packages/BUILD/binutils-2.25.1/libiberty/ -liberty /opt/freeware/src/packages/BUILD/binutils-2.25.1/bfd/libbfd.a -I/opt/freeware/src/packages/BUILD/binutils-2.25.1/bfd/ -I/opt/freeware/src/packages/BUILD/binutils-2.25.1/include -o copycsect

  Run with:

Old:
  # copycsect input.o .go_export output.gox
New:
  # $(OBJCOPY) -j .go_export $$f $@.tmp
*/

#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bfd.h"
#include "coff/internal.h"
#include "libcoff.h"

int
main (int argc, char *argv[])
{
  bfd *ibfd, *obfd;
  asymbol **isymtab, *osymtab[2];
  asection *isect, *osect;
  asymbol *isym;
  void *csect;
  union internal_auxent auxent;
  long size, nsyms, i;
  long offset, scnlen;

  if (argc != 5)
    {
      fprintf (stderr, "copycsect -j csect_name input output\n");
      return 1;
    }

  bfd_init ();

  ibfd = bfd_openr (argv[3], NULL);
  if (ibfd == NULL)
    {
      fprintf (stderr, "bfd_openr %s\n", argv[3]);
      return 1;
    }

  /* NB: this needs to be called before anything else. */
  if (!bfd_check_format (ibfd, bfd_object))
    {
      fprintf (stderr, "%s not an object file\n", argv[3]);
      return 1;
    }

  /* Retrieve symbol table. */
  size = bfd_get_symtab_upper_bound (ibfd);
  if (size <= 0)
    {
      fprintf (stderr, "bfd_get_symtab_upper_bound\n");
      return 1;
    }
  isymtab = (asymbol **)malloc (size);
  if (isymtab == NULL)
    {
      fprintf (stderr, "malloc symtab\n");
      return 1;
    }
  nsyms = bfd_canonicalize_symtab (ibfd, isymtab);
  if (nsyms < 0)
    {
      fprintf (stderr, "bfd_canonicalize_symtab\n");
      return 1;
    }
  /* Search for the specified CSECT. */
  for (i = 0; i < nsyms; i++)
    {
      if (strcmp (isymtab[i]->name, argv[2]) == 0)
        {
          isym = isymtab[i];
          break;
        }
    }
  if (isym == NULL)
    {
      fprintf (stderr, "no %s CSECT found\n", argv[2]);
      return 1;
    }
  isect = isym->section;
  offset = isym->value;

  /* Retrieve the associated AUX symbol entry. */
  if (!bfd_coff_get_auxent (ibfd, isym, 0, &auxent))
    {
      fprintf (stderr, "bfd_coff_get_auxent\n");
      return 1;
    }
  scnlen = auxent.x_csect.x_scnlen.l;

  /* Retrieve CSECT contents. */
  if (scnlen)
    {
      csect = malloc (scnlen);
      if (csect == NULL)
        {
          fprintf (stderr, "malloc csect\n");
          return 1;
        }
      if (!bfd_get_section_contents (ibfd, isect, csect, offset, scnlen))
        {
          fprintf (stderr, "bfd_get_section_contents\n");
          return 1;
        }
    }

  /* Create output file with same format as input. */
  obfd = bfd_openw (argv[4], bfd_get_target (ibfd));
  if (obfd == NULL)
    {
      fprintf (stderr, "bfd_openw %s\n", argv[4]);
      return 1;
    }
  if (!bfd_set_format (obfd, bfd_get_format (ibfd)))
    {
      fprintf (stderr, "bfd_set_format\n");
      return 1;
    }
  if (!bfd_set_arch_mach (obfd, bfd_get_arch (ibfd), bfd_get_mach (ibfd)))
    {
      fprintf (stderr, "bfd_set_arch_mach\n");
      return 1;
    }

  /* Create the section that contains the CSECT. */
  osect = bfd_make_section_with_flags (obfd, isect->name, isect->flags);
  if (osect == NULL)
    {
      fprintf (stderr, "bfd_make_section_with_flags\n");
      return 1;
    }
  if (!bfd_set_section_size (obfd, osect, scnlen))
    {
      fprintf (stderr, "bfd_set_section_size\n");
      return 1;
    }
  if (!bfd_set_section_contents (obfd, osect, csect, 0, scnlen))
    {
      fprintf (stderr, "bfd_set_section_contents\n");
      return 1;
    }

  /* Reuse the CSECT symbol entry, change its offset to 0.
     This is the only way to preserve the AUX entry. */
  isym->value = 0;
  osymtab[0] = isym;
  osymtab[1] = NULL;
  bfd_set_symtab (obfd, osymtab, 1);

  bfd_close (obfd);
  bfd_close (ibfd);
  free (isymtab);
  free (csect);

  return 0;
}

