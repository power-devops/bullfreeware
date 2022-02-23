#include <stdio.h>
#include <string.h>
#include <ldfcn.h>
#include <libgen.h>
#include <sys/param.h>
#include <sys/stat.h>

static int debug_find_provides = 0;

#define START_MACRO do {
#define END_MACRO } while(0)

#define DEBUG(...) \
START_MACRO \
if (debug_find_provides) { \
    fprintf(stderr, "%s(%d): ", __FILE__, __LINE__); \
    fprintf(stderr, __VA_ARGS__); \
} \
END_MACRO

/**
 * List of known extensions that we can skip processing.
 */
static char* SKIP_EXTENSIONS[] = {
    ".auiml",
    ".awk",
    ".bm",
    ".bnd",
    ".c",
    ".cat",
    ".cdef",
    ".cfg",
    ".cgi",
    ".class",
    ".conf",
    ".csh",
    ".css",
    ".dt",
    ".exe",
    ".exp",
    ".gif",
    ".gz",
    ".h",
    ".hs",
    ".htm",
    ".html",
    ".idl",
    ".jar",
    ".jhm",
    ".jpg",
    ".js",
    ".jsp",
    ".m4",
    ".map",
    ".mdef",
    ".pdf",
    ".perl",
    ".pl",
    ".pm",
    ".png",
    ".pod",
    ".properties",
    ".ps",
    ".rpm",
    ".sed",
    ".sgs",
    ".sh",
    ".tar",
    ".tif",
    ".tpl",
    ".ttf",
    ".txt",
    ".xml",
    ".xpm",
    ".zip",
    ".Z",
};

#define SKIP_EXTENSIONS_LENGTH (sizeof(SKIP_EXTENSIONS)/sizeof(SKIP_EXTENSIONS[0]))

static int skip_file(const char *filename) {
    char *lastdir = strrchr(filename, '/');
    int skip = 0;

    if (lastdir != NULL) {
        char *extension = strrchr(lastdir, '.');
        int i;

        /**
         * Skip extensions of files that we don't need to process.
        */
        if (extension != NULL) {
            for (i = 0; i < SKIP_EXTENSIONS_LENGTH; i++) {
                if (!strcmp(SKIP_EXTENSIONS[i], extension)) {
                    skip = 1;
                    DEBUG("Skipping file: %s\n", filename);
                    break;
                }
            }
        }
    }
    return skip;
}

/**
 * This program replicates what is currently done in the find-provides script 
 * for RPM on the AIX Toolbox. It reads lines of input from stdin (filenames) 
 * and then outputs the shared libraries or shared libraries + members. All 
 * files which are not shared libraries or shared archive members are filtered 
 * out.
 */
int main(int argc, char **argv) {
    FILE *fp = stdin;
    char buf[MAXPATHLEN+1];
    char *bn;
    char *extension;
    size_t len;
    LDFILE *file;
    ARCHDR arhdr;
    FILE *sort;
    struct stat st;

    if (getenv("FIND_PROVIDES_DEBUG") != NULL) {
        debug_find_provides = 1;
        DEBUG("DEBUG ENABLED\n");
    }

    if ((sort = popen("/usr/bin/sort -u", "w")) == NULL) {
        perror("popen");
        return 1;
    }

    while (fgets(buf, MAXPATHLEN, fp)) {
        bn = NULL;

        /* Remove trailing newline */
        len = strlen(buf);
        if (len > 0 && buf[len-1] == '\n') {
            buf[len-1] = '\0';
        }

        /* Skip files with known extensions */
        if (skip_file(buf)) {
            continue;
        }

        if (stat(buf, &st) != 0) {
            continue;
        }

        /* Skip everything but files/links */
        if (!(S_ISREG(st.st_mode) || S_ISLNK(st.st_mode))) {
            continue;
        }

        DEBUG("Processing file: %s\n", buf);

        file = NULL;
        do {
            if ((file = ldopen(buf, file)) != NULL) {
                /* 32-bit or 64-bit XCOFF magic numbers */
                if (HEADER(file).f_magic != U802TOCMAGIC &&
                    HEADER(file).f_magic != U64_TOCMAGIC) {
                    DEBUG("Skipping file with missing XCOFF magic number: %s\n", buf);
                    continue;
                }

                if (bn == NULL) {
                    bn = basename(buf);
                }

                if (HEADER(file).f_flags & F_SHROBJ) {
                    if (TYPE(file) == ARTYPE && ldahread(file, &arhdr) == SUCCESS) {
                        fprintf(sort, "%s(%s)\n", bn, arhdr.ar_name);
                    }
                    else {
                        fprintf(sort, "%s\n", bn);
                    }
                }
            }
        } while(ldclose(file) == FAILURE);
    }
    pclose(sort);

    return 0;
}
