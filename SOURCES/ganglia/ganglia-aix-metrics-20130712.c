/*
 *  Rewrite of AIX metrics using libperfstat API
 *
 *  Libperfstat can deal with a 32-bit and a 64-bit Kernel and does not require root authority.
 *
 *  The code is tested with AIX 5.2 (32Bit- and 64Bit-Kernel), but 5.1 and 5.3 shoud be OK too
 *
 *  by Andreas Schoenfeld, TU Darmstadt, Germany (4/2005) 
 *  E-Mail: Schoenfeld@hrz.tu-darmstadt.de
 *
 *  Its based on the 
 *  First stab at support for metrics in AIX
 *  by Preston Smith <psmith@physics.purdue.edu>
 *  Wed Feb 27 14:55:33 EST 2002
 *
 *  AIX V5 support, bugfixes added by Davide Tacchella <tack@cscs.ch>
 *  May 10, 2002
 *
 *  you may still find some code (like "int bos_level(..)"  ) and the basic structure of this version. 
 *
 *  Some code fragments of the network statistics are "borowed" from  
 *  the Solaris Metrics   
 *
 *  Fix proc_total, proc_run, swap_free and swap_total. Implement mem_cached (MKN, 16-Jan-2006)
 *  Michael Perzl (michael@perzl.org), Mon, Jun 10 2013
 *  - Revisited the CPU statistics completely similar to the following example:
 *    http://pic.dhe.ibm.com/infocenter/aix/v6r1/index.jsp?topic=%2Fcom.ibm.aix.prftools%2Fdoc%2Fprftools%2Fidprftools_perfstat_glob_cpu.htm
 *  - Added a 'physc' and 'entc' field to the CPU statistics
 *  - If you define "-DDONATE_ENABLED" you need to compile on AIX 5.3 TL 06 or higher
 *
 *  Michael Perzl (michael@perzl.org), Thu, Oct 13 2011
 *  - Rewrote the CPU statistics completely similar to the following example:
 *    http://pic.dhe.ibm.com/infocenter/aix/v6r1/index.jsp?topic=%2Fcom.ibm.aix.prftools%2Fdoc%2Fprftools%2Fidprftools_perfstat_glob_cpu.htm
 *    If you define "-DDONATE_ENABLED" you need to compile on AIX 5.3 TL 06 or higher
 *  - Rewrote the "machine_type_func()" function
 */

#include <stdlib.h>
#include <utmp.h>
#include <stdio.h>
#include <procinfo.h>
#include <strings.h>
#include <signal.h>
#include <odmi.h>
#include <cf.h>
#include <sys/utsname.h>
#include <sys/proc.h>
#include <sys/types.h>
#include <time.h>

#include <libperfstat.h>
#include <sys/systemcfg.h>

#include "libmetrics.h"

/* order of includes must be changed or definition of 'malloc' as 'rpl_malloc' */
/* will interfere */
#include "interface.h"


struct Class *My_CLASS;

struct product
{
        char filler[12];
        char lpp_name[145];      /* offset: 0xc ( 12) */
        char comp_id[20];        /* offset: 0x9d ( 157) */
        short update;            /* offset: 0xb2 ( 178) */
        long cp_flag;            /* offset: 0xb4 ( 180) */
        char fesn[10];           /* offset: 0xb8 ( 184) */
        char *name;              /*[42] offset: 0xc4 ( 196) */
        short state;             /* offset: 0xc8 ( 200) */
        short ver;               /* offset: 0xca ( 202) */
        short rel;               /* offset: 0xcc ( 204) */
        short mod;               /* offset: 0xce ( 206) */
        short fix;               /* offset: 0xd0 ( 208) */
        char ptf[10];            /* offset: 0xd2 ( 210) */
        short media;             /* offset: 0xdc ( 220) */
        char sceded_by[10];      /* offset: 0xde ( 222) */
        char *fixinfo;           /* [1024] offset: 0xe8 ( 232) */
        char *prereq;            /* [1024] offset: 0xec ( 236) */
        char *description;       /* [1024] offset: 0xf0 ( 240) */
        char *supersedes;        /* [512] offset: 0xf4 ( 244) */
};

#if defined(_AIX43)
#ifndef SBITS
/*
 * For multiplication of fractions that are stored as integers, including
 * p_pctcpu.  Not allowed to do floating point arithmetic in the kernel.
 */
#define SBITS   16
#endif
#endif

#define MAX_CPUS  64

#define INFO_TIMEOUT   10
#define CPU_INFO_TIMEOUT INFO_TIMEOUT

#define MEM_KB_PER_PAGE (4096/1024)


/* values for the implementation field for POWER_PC architectures */

#ifndef POWER_4
#define POWER_4         0x0800          /* 4 class CPU */
#endif
#ifndef POWER_5
#define POWER_5         0x2000          /* 5 class CPU */
#endif
#ifndef POWER_6
#define POWER_6         0x4000          /* 6 class CPU */
#endif
#ifndef POWER_7
#define POWER_7         0x8000          /* 7 class CPU */
#endif


/* values for the version field for POWER_PC architectures */

#ifndef PV_4
#define PV_4            0x0C0000        /* Power PC 4 */
#endif
#ifndef PV_RS64IV
#define PV_RS64IV       PV_4            /* Power PC 4 */
#endif
#ifndef PV_4_2
#define PV_4_2          0x0E0000        /* Power PC 4 */
#endif
#ifndef PV_4_3
#define PV_4_3          0x0E0001        /* Power PC 4 */
#endif
#ifndef PV_5
#define PV_5            0x0F0000        /* Power PC 5 */
#endif
#ifndef PV_5_2
#define PV_5_2          0x0F0001        /* Power PC 5 */
#endif
#ifndef PV_5_3
#define PV_5_3          0x0F0002        /* Power PC 5 */
#endif
#ifndef PV_6
#define PV_6            0x100000        /* Power PC 6 */
#endif
#ifndef PV_6_1
#define PV_6_1          0x100001        /* Power PC 6 DD1.x */
#endif
#ifndef PV_7
#define PV_7            0x200000        /* Power PC 7 */
#endif
#ifndef PV_7_1
#define PV_7_1          0x200001        /* Power PC 7+ */
#endif


/*
 * The following Compat definitions indicate that the processor is running in
 * a mode that is compatible with the processor family as indicated by the
 * implementation field of the _system_configuration structure.  When running
 * in a compatible mode, BookIV processor features of that processor family
 * can not be assumed to be present or functional.
 */
#ifndef PV_5_Compat
#define PV_5_Compat     0x0F8000        /* Power PC 5 */
#endif
#ifndef PV_6_Compat
#define PV_6_Compat     0x108000        /* Power PC 6 */
#endif
#ifndef PV_7_Compat
#define PV_7_Compat     0x208000        /* Power PC 7 */
#endif


struct cpu_info_t
{
   double timestamp;  
   float  user;     /* percentage spent in user mode */
   float  sys;      /* percentage spent in system mode */
   float  idle;     /* percentage spent idle */
   float  wait;     /* percentage spent waiting for I/O */
   float  physc;    /* physical cores used */
   float  entc;     /* percent usage of entitled capacity */
};

struct net_stat
{
   double ipackets;
   double opackets;
   double ibytes;
   double obytes;
} cur_net_stat;



int ci_flag = 0;
int ni_flag = 0;

perfstat_netinterface_total_t ninfo[2], *last_ninfo, *cur_ninfo;


struct cpu_info_t cpu_info;


int aixver, aixrel, aixlev, aixfix;
static time_t boottime;

static int isVIOserver;

/* Prototypes
 */
void update_ifdata(void);
static void get_cpuinfo(void);
int bos_level(int *aix_version, int *aix_release, int *aix_level, int *aix_fix);


/*
 * This function is called only once by the gmond.  Use to 
 * initialize data structures, etc or just return SYNAPSE_SUCCESS;
 */
g_val_t
metric_init( void )
{
   g_val_t val;
   FILE *f;


/* find out if we are running on a VIO server */

   f = fopen( "/usr/ios/cli/ioscli", "r" );

   if (f)
   {
      isVIOserver = 1;
      fclose( f );
   }
   else
      isVIOserver = 0;


   update_ifdata();

   val = boottime_func();
   boottime = val.uint32; 
   cpu_info.timestamp = 0.0;
   get_cpuinfo();
   sleep( CPU_INFO_TIMEOUT + 1 );
   get_cpuinfo();

   update_ifdata();

   bos_level( &aixver, &aixrel, &aixlev, &aixfix );

   val.int32 = SYNAPSE_SUCCESS;

   return( val );
}


g_val_t
cpu_speed_func ( void )
{
   g_val_t val;
   perfstat_cpu_total_t c;

   if (perfstat_cpu_total( NULL, &c, sizeof( perfstat_cpu_total_t ), 1 ) == -1)
      val.uint32 = 0;
   else
      val.uint32 = c.processorHZ / 1000000;

   return val;
}


g_val_t
boottime_func( void )
{
   g_val_t val;
   struct utmp buf;
   FILE *utmp;


   if (!boottime)
   {
      utmp = fopen( UTMP_FILE, "r" );

      if (utmp == NULL)
      {
         /* Can't open utmp, use current time as boottime */
         boottime = time( NULL );
      }
      else
      {
         while (fread( (char *) &buf, sizeof( buf ), 1, utmp ) == 1)
         {
            if (buf.ut_type == BOOT_TIME)
            {
               boottime = buf.ut_time;
               break;
            }
         }
	 fclose( utmp );
      }
   }
   val.uint32 = boottime;

   return( val );
}


g_val_t
sys_clock_func( void )
{
   g_val_t val;


   val.uint32 = time( NULL );
   return val;
}


g_val_t
machine_type_func( void )
{
   g_val_t val;
   perfstat_cpu_total_t c;
   int len;


   if (perfstat_cpu_total (NULL, &c, sizeof( perfstat_cpu_total_t), 1) == -1)
      strcpy (val.str, "unknown");
   else
   {
      strncpy( val.str, c.description, MAX_G_STRING_SIZE );

      len = MAX_G_STRING_SIZE - strlen( val.str ) - 1;

      switch (_system_configuration.implementation)
      {
         case POWER_RS1: strncat( val.str, " (RS1 POWER1)", len );
                         break;
         case POWER_RSC: strncat( val.str, " (RSC)", len );
                         break;
         case POWER_RS2: strncat( val.str, " (RS2 POWER2)", len );
                         break;
         case POWER_601: strncat( val.str, " (601)", len );
                         break;
         case POWER_603: strncat( val.str, " (603)", len );
                         break;
         case POWER_604: strncat( val.str, " (604)", len );
                         break;
         case POWER_620: strncat( val.str, " (620)", len );
                         break;
         case POWER_630: strncat( val.str, " (630)", len );
                         break;
         case POWER_A35: strncat( val.str, " (A35)", len );
                         break;
         case POWER_RS64II: strncat( val.str, " (RS64-II)", len );
                            break;
         case POWER_RS64III: strncat( val.str, " (RS64-III)", len );
                             break;
         case POWER_4: switch (_system_configuration.version)
                       {
                          case PV_4:   strncat( val.str, " (POWER4/RS64-IV)", len ); 
                                       break;
                          case PV_4_2: strncat( val.str, " (POWER4.2)", len ); 
                                       break;
                          case PV_4_3: strncat( val.str, " (POWER4.3)", len );
                                       break;
                          default:     strncat( val.str, " (unknown)", len );
                                       break;
                       }    
                       break;
         case POWER_MPC7450: strncat( val.str, " (POWER MPC7450)", len );
                             break;
         case POWER_5: switch (_system_configuration.version)
                       {
                          case PV_5:   strncat( val.str, " (POWER5)", len ); 
                                       break;
                          case PV_5_2: strncat( val.str, " (POWER5.2)", len ); 
                                       break;
                          case PV_5_3: strncat( val.str, " (POWER5.3)", len );
                                       break;
                          default:     strncat( val.str, " (unknown)", len );
                                       break;
                       }    
                       break;
         case POWER_6: switch (_system_configuration.version)
                       {
                          case PV_6:        strncat( val.str, " (POWER6(+))", len );
                                            break;
                          case PV_6_1:      strncat( val.str, " (POWER6.1)", len );
                                            break;
                          case PV_5_Compat: strncat( val.str, " (POWER5)", len );
                                            break;
                          case PV_6_Compat: strncat( val.str, " (POWER6)", len );
                                            break;
                          default:          strncat( val.str, " (unknown)", len );
                                            break;
                       }
                       break;
         case POWER_7: switch (_system_configuration.version)
                       {
                          case PV_7:        strncat( val.str, " (POWER7)", len );
                                            break;
                          case PV_7_Compat: strncat( val.str, " (POWER7)", len );
                                            break;
                          default:          strncat( val.str, " (unknown)", len );
                                            break;
                       }
                       break;
      }
   }

   return( val );
}


g_val_t
os_name_func( void )
{
   g_val_t val;
   struct utsname uts;


   if (isVIOserver)
      strcpy( val.str, "Virtual I/O Server" );
   else
   {
      uname( &uts );
      strncpy( val.str, uts.sysname, MAX_G_STRING_SIZE );
   }

   return( val );
}        


g_val_t
os_release_func( void )
{
   g_val_t val;
   char oslevel[MAX_G_STRING_SIZE];


   sprintf( oslevel, "%d.%d.%d.%d", aixver, aixrel, aixlev, aixfix );
   strncpy( val.str, oslevel, MAX_G_STRING_SIZE );

   return( val );
}        


/* AIX defines
   CPU_IDLE, CPU_USER, CPU_SYS(CPU_KERNEL), CPU_WAIT
   so no metrics for cpu_nice, or cpu_aidle
*/

g_val_t
cpu_user_func( void )
{
   g_val_t val;
   
   
   get_cpuinfo();
   val.f = cpu_info.user;

   return( val );
}


/*
 * AIX does not have this
 */

g_val_t
cpu_nice_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


g_val_t 
cpu_system_func( void )
{
   g_val_t val;


   get_cpuinfo();
   val.f = cpu_info.sys;

   return( val );
}


g_val_t 
cpu_wio_func( void )
{
   g_val_t val;

   
   get_cpuinfo();
   val.f = cpu_info.wait;

   return( val );
}


g_val_t 
cpu_idle_func( void )
{
   g_val_t val;


   get_cpuinfo();
   val.f = cpu_info.idle;

   return( val );
}


/*
 * AIX does not have this
 */

g_val_t 
cpu_aidle_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


/*
 * AIX does not have this
 */
g_val_t 
cpu_intr_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


/*
 * AIX does not have this
 */

g_val_t 
cpu_sintr_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


/*
 * AIX does not have this
 */

g_val_t
cpu_steal_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


g_val_t 
cpu_physc_func( void )
{
   g_val_t val;


   get_cpuinfo();
   val.f = cpu_info.physc;

   return( val );
}


g_val_t 
cpu_entc_func( void )
{
   g_val_t val;


   get_cpuinfo();
   val.f = cpu_info.entc;

   return( val );
}


g_val_t 
bytes_in_func( void )
{
   g_val_t val;


   update_ifdata();
   val.f = cur_net_stat.ibytes;

   return( val );
}


g_val_t 
bytes_out_func( void )
{
   g_val_t val;


   update_ifdata();
   val.f = cur_net_stat.obytes;
   
   return( val );
}


g_val_t 
pkts_in_func( void )
{
   g_val_t val;


   update_ifdata();
   val.f = cur_net_stat.ipackets;

   return( val );
}


g_val_t 
pkts_out_func( void )
{
   g_val_t val;


   update_ifdata();
   val.f = cur_net_stat.opackets;

   return( val );
}


g_val_t 
disk_free_func( void )
{
   g_val_t val;
   perfstat_disk_total_t d;


   if (perfstat_disk_total( NULL, &d, sizeof( perfstat_disk_total_t ), 1 ) == -1)
      val.d = 0.0;
   else
      val.d = (double) d.free / 1024.0;

   return( val );
}


g_val_t 
disk_total_func( void )
{
   g_val_t val;
   perfstat_disk_total_t d;


   if (perfstat_disk_total(NULL, &d, sizeof(perfstat_disk_total_t), 1) == -1)
      val.d = 0.0;
   else
      val.d = (double)d.size / 1024.0;

   return( val );
}


/* AIX does not use fdisk-type partitions but LVs (logical volumes) */
g_val_t 
part_max_used_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


g_val_t
load_one_func( void )
{
   g_val_t val;
   perfstat_cpu_total_t c;

   
   if (perfstat_cpu_total( NULL, &c, sizeof( perfstat_cpu_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = (float) c.loadavg[0] / (float) (1<<SBITS);

   return( val );
}


g_val_t
load_five_func( void )
{  
   g_val_t val;
   perfstat_cpu_total_t c;


   if (perfstat_cpu_total( NULL, &c, sizeof( perfstat_cpu_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = (float) c.loadavg[1] / (float) (1<<SBITS);

   return( val );
}


g_val_t
load_fifteen_func( void )
{
   g_val_t val;
   perfstat_cpu_total_t c;


   if (perfstat_cpu_total(NULL, &c, sizeof( perfstat_cpu_total_t ), 1) == -1)
      val.f = 0.0;
   else
      val.f = (float) c.loadavg[2] / (float) (1<<SBITS);

   return( val );
}


g_val_t
cpu_num_func ( void )
{
   g_val_t val;
   perfstat_cpu_total_t c;


   if (perfstat_cpu_total( NULL, &c, sizeof( perfstat_cpu_total_t ), 1) == -1)
      val.uint16 = 0;
   else
      val.uint16 = c.ncpus;

   return( val );
}

#define MAXPROCS 20

#if !(defined(_AIX61) || defined(_AIX71))
/*
 * These missing prototypes have caused me an afternoon of real grief !!!
 */
int getprocs64( struct procentry64 *ProcessBuffer, int ProcessSize, 
                struct fdsinfo64 *FileBuffer, int FileSize,
                pid_t *IndexPointer, int Count );
int getthrds64( pid_t ProcessIdentifier, struct thrdentry64 *ThreadBuffer,
                int ThreadSize, tid64_t *IndexPointer, int Count );
#endif

/*
 * count_threads( pid ) finds all runnable threads belonging to
 * process==pid. We do not count threads with the TFUNNELLED
 * flag set, as they do not seem to count against the load
 * averages (pure WOODOO, also known as "heuristics" :-)
*/
int count_threads( pid_t pid )
{
   struct thrdentry64 ThreadsBuffer[MAXPROCS];
   tid64_t IndexPointer = 0;
   int stat_val;
   int nth = 0; 
   int i;


   while ((stat_val = getthrds64(pid,
			      ThreadsBuffer,
			      sizeof(struct thrdentry64),
			      &IndexPointer,
			      MAXPROCS )) > 0 ) 
    
   {
      for (i = 0;  i < stat_val;  i++)
      {
         /*
          * Do not count FUNNELED threads, as they do not seem to
          * be counted in loadavg.
          */
         if (ThreadsBuffer[i].ti_flag & TFUNNELLED) continue;
	 if (ThreadsBuffer[i].ti_state == TSRUN)
         {
          /*fprintf(stderr,"i=%d pid=%d tid=%lld state=%x flags=%x\n",i,ThreadsBuffer[i].ti_pid,
			ThreadsBuffer[i].ti_tid,ThreadsBuffer[i].ti_state,
			ThreadsBuffer[i].ti_flag);*/
            nth++;
         }
      }
      if (stat_val < MAXPROCS) break;
   }

   return( nth );
}

/*
** count_procs() computes the number of processes as shown in "ps -A".
**    Pass 0 as flag if you want to get a list of all processes.
**    Pass 1 if you want to get a list of all processes with
**    runnable threads.
*/
int count_procs(int flag)
{
   struct procentry64 ProcessBuffer[MAXPROCS];
   pid_t IndexPointer = 0;
   int np = 0; 
   int stat_val;
   int i;


   while ((stat_val = getprocs64( &ProcessBuffer[0],
			          sizeof( struct procentry64 ),
			          NULL,
			          sizeof( struct fdsinfo64 ),
			          &IndexPointer,
			          MAXPROCS )) > 0 ) 
    
   {
      for (i = 0;  i < stat_val;  i++)
      {
         if (flag != 0)
         {
          /*fprintf(stderr,"i=%d pid=%d state=%x flags=%x flags2=%x thcount=%d\n",i,
				ProcessBuffer[i].pi_pid,ProcessBuffer[i].pi_state,
				ProcessBuffer[i].pi_flags,ProcessBuffer[i].pi_flags2,
				ProcessBuffer[i].pi_thcount);*/
	    np += count_threads( ProcessBuffer[i].pi_pid );
         }
         else
         {
            np++;
         }
      }
      if (stat_val < MAXPROCS) break;
    }

/*
 * Reduce by one to make proc_run more Linux "compliant".
 */
   if ((flag != 0) && (np > 0)) np--;

   return( np );
}


g_val_t
proc_total_func( void )
{
   g_val_t val;

 
   val.uint32 = count_procs( 0 );
 
   return( val );
}


g_val_t
proc_run_func( void )
{
   g_val_t val;


   val.uint32 = count_procs( 1 );
 
   return( val );
}


g_val_t
mem_total_func( void )
{
   g_val_t val;
   perfstat_memory_total_t m;


   if (perfstat_memory_total( NULL, &m, sizeof( perfstat_memory_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = m.real_total * MEM_KB_PER_PAGE;
   
   return( val );
}


g_val_t
mem_free_func( void )
{
   g_val_t val;
   perfstat_memory_total_t m;


   if (perfstat_memory_total( NULL, &m, sizeof( perfstat_memory_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = m.real_free * MEM_KB_PER_PAGE;

   return( val );
}


/* AIX does not have this */
g_val_t
mem_shared_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


/* AIX does not have this */
g_val_t
mem_buffers_func( void )
{
   g_val_t val;


   val.f = 0.0;

   return( val );
}


g_val_t
mem_cached_func( void )
{
   g_val_t val;
   perfstat_memory_total_t m;


   if (perfstat_memory_total( NULL, &m, sizeof( perfstat_memory_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = m.numperm * MEM_KB_PER_PAGE;

   return( val );
}


g_val_t
swap_total_func( void )
{
   g_val_t val;
   perfstat_memory_total_t m;


   if (perfstat_memory_total( NULL, &m, sizeof( perfstat_memory_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = m.pgsp_total * MEM_KB_PER_PAGE;

   return( val );
}


g_val_t
swap_free_func( void )
{
   g_val_t val;
   perfstat_memory_total_t m;


   if (perfstat_memory_total( NULL, &m, sizeof( perfstat_memory_total_t ), 1 ) == -1)
      val.f = 0.0;
   else
      val.f = m.pgsp_free * MEM_KB_PER_PAGE;

   return( val );
}


g_val_t
mtu_func( void )
{
/* We want to find the minimum MTU (Max packet size) over all UP interfaces. */
   unsigned int min = 0;
   g_val_t val;


   val.uint32 = get_min_mtu();

/* A val of 0 means there are no UP interfaces. Shouldn't happen. */
   return( val );
}


static void get_cpuinfo() 
{
   struct timeval timeValue;
   struct timezone timeZone;
   double now;
   perfstat_cpu_total_t cpustats;
   longlong_t delta_lcpu_user,
              delta_lcpu_sys,
              delta_lcpu_idle,
              delta_lcpu_wait;
   longlong_t lcputime;
   static u_longlong_t last_lcpu_user = 0LL,
                       last_lcpu_sys  = 0LL,
                       last_lcpu_idle = 0LL,
                       last_lcpu_wait = 0LL;
#ifdef _AIX53
   perfstat_partition_total_t lparstats;
   longlong_t delta_pcpu_user,
              delta_pcpu_sys,
              delta_pcpu_idle,
              delta_pcpu_wait;
   longlong_t delta_purr,
              pcputime,
              entitled_purr,
              unused_purr;
   static u_longlong_t last_pcpu_user = 0LL,
                       last_pcpu_sys  = 0LL,
                       last_pcpu_idle = 0LL,
                       last_pcpu_wait = 0LL;
   static u_longlong_t last_time_base = 0LL;
   double entitlement;
   u_longlong_t delta_time_base;
#ifdef DONATE_ENABLED
   longlong_t delta_idle_donated,
              delta_busy_donated,
              delta_busy_stolen,
              delta_idle_stolen;
   static u_longlong_t last_idle_donated = 0LL,
                       last_busy_donated = 0LL,
                       last_busy_stolen  = 0LL,
                       last_idle_stolen  = 0LL;
#endif  /* DONATE_ENABLE */
#endif  /* _AIX53 */


   gettimeofday( &timeValue, &timeZone );
   now = (double) (timeValue.tv_sec - boottime) + (timeValue.tv_usec / 1000000.0);

   if (now - CPU_INFO_TIMEOUT > cpu_info.timestamp)
   {
/* remember last time stamp */
      cpu_info.timestamp = now;

/* collect CPU metrics */
      perfstat_cpu_total( NULL, &cpustats, sizeof( perfstat_cpu_total_t ), 1 );

/* calculate clock tics during the last interval in user, system, idle and wait mode */
      delta_lcpu_user  = cpustats.user - last_lcpu_user;
      delta_lcpu_sys   = cpustats.sys  - last_lcpu_sys;
      delta_lcpu_idle  = cpustats.idle - last_lcpu_idle;
      delta_lcpu_wait  = cpustats.wait - last_lcpu_wait;
/* prevent against nonsense values when suddenly performance data collection */
/* is enabled or disabled for this LPAR */
      if (delta_lcpu_user < 0LL) delta_lcpu_user = 1LL;
      if (delta_lcpu_sys  < 0LL) delta_lcpu_sys  = 1LL;
      if (delta_lcpu_idle < 0LL) delta_lcpu_idle = 1LL;
      if (delta_lcpu_wait < 0LL) delta_lcpu_wait = 1LL;

/* calculate total clock tics during the last interval */
      lcputime = delta_lcpu_user + delta_lcpu_sys + delta_lcpu_idle + delta_lcpu_wait;

/* save old values for next iteration */
      last_lcpu_user = cpustats.user;
      last_lcpu_sys  = cpustats.sys;
      last_lcpu_idle = cpustats.idle;
      last_lcpu_wait = cpustats.wait;

#ifdef _AIX53
      perfstat_partition_total( NULL, &lparstats, sizeof(perfstat_partition_total_t), 1 );

/* calculate physical processor tics during the last interval in user, system, idle and wait mode  */
      delta_pcpu_user = lparstats.puser - last_pcpu_user;
      delta_pcpu_sys  = lparstats.psys  - last_pcpu_sys;
      delta_pcpu_idle = lparstats.pidle - last_pcpu_idle;
      delta_pcpu_wait = lparstats.pwait - last_pcpu_wait;

/* prevent against nonsense values when suddenly performance data collection */
/* is enabled or disabled for this LPAR */
      if (delta_pcpu_user < 0LL) delta_pcpu_user = 1LL;
      if (delta_pcpu_sys  < 0LL) delta_pcpu_sys  = 1LL;
      if (delta_pcpu_idle < 0LL) delta_pcpu_idle = 1LL;
      if (delta_pcpu_wait < 0LL) delta_pcpu_wait = 1LL;

/* calculate total physical processor tics during the last interval */
      delta_purr = pcputime = delta_pcpu_user + delta_pcpu_sys + delta_pcpu_idle + delta_pcpu_wait;

/* calculate entitlement for this partition - entitled physical processors for this partition */
      entitlement = (double) lparstats.entitled_proc_capacity / 100.0 ;

/* calculate delta time in terms of physical processor tics */
      delta_time_base = lparstats.timebase_last - last_time_base;

/* save old values for next iteration */
      last_time_base = lparstats.timebase_last;
      last_pcpu_user = lparstats.puser;
      last_pcpu_sys  = lparstats.psys;
      last_pcpu_idle = lparstats.pidle;
      last_pcpu_wait = lparstats.pwait;

      if (lparstats.type.b.shared_enabled)   /* partition is a SPLPAR */
      {
/* calculate entitled physical processor tics for this partitions */
         entitled_purr = delta_time_base * entitlement;

         if (entitled_purr < delta_purr)   /* for uncapped SPLPAR */
         {         /* we have used more CPU cycles than our entitlement */
/* in case of uncapped SPLPAR, consider entitled physical processor tics or */
/* consumed physical processor tics, which ever is greater */
            entitled_purr = delta_purr;
         }

/* calculate unused physical processor tics out of the entitled physical processor tics */
         unused_purr = entitled_purr - delta_purr;

/* distribute unused physical processor tics amoung wait and idle proportionally to wait and idle in clock tics */
         delta_pcpu_wait += unused_purr * ((double) delta_lcpu_wait / (double) (delta_lcpu_wait + delta_lcpu_idle));
         delta_pcpu_idle += unused_purr * ((double) delta_lcpu_idle / (double) (delta_lcpu_wait + delta_lcpu_idle));

/* for SPLPAR, consider the entitled physical processor tics as the actual delta physical processor tics */
         pcputime = entitled_purr;
      }
#ifdef DONATE_ENABLED
      else if (lparstats.type.b.donate_enabled)  /* if donation is enabled for this DLPAR */
      {
/* calculate busy stolen and idle stolen physical processor tics during the last interval */
/* these physical processor tics are stolen from this partition by the hypervsior */
/* which will be used by wanting partitions */
         delta_busy_stolen = lparstats.busy_stolen_purr - last_busy_stolen;
         delta_idle_stolen = lparstats.idle_stolen_purr - last_idle_stolen;

/* prevent against nonsense values when suddenly performance data collection */
/* is enabled or disabled for this LPAR */
         if (delta_busy_stolen < 0LL) delta_busy_stolen = 0LL;
         if (delta_idle_stolen < 0LL) delta_idle_stolen = 0LL;

/* calculate busy donated and idle donated physical processor tics during the last interval */
/* these physical processor tics are voluntarily donated by this partition to the hypervsior */
/* which will be used by wanting partitions */
         delta_busy_donated = lparstats.busy_donated_purr - last_busy_donated;
         delta_idle_donated = lparstats.idle_donated_purr - last_idle_donated;

/* prevent against nonsense values when suddenly performance data collection */
/* is enabled or disabled for this LPAR */
         if (delta_busy_donated < 0LL) delta_busy_donated = 0LL;
         if (delta_idle_donated < 0LL) delta_idle_donated = 0LL;

/* add busy donated and busy stolen to the kernel bucket, as cpu */
/* cycles were donated / stolen when this partition is busy */
         delta_pcpu_sys += delta_busy_donated;
         delta_pcpu_sys += delta_busy_stolen;

/* distribute idle stolen to wait and idle proportionally to the logical wait and idle in clock tics, as */
/* cpu cycles were stolen when this partition is idle or in wait */
         delta_pcpu_wait += delta_idle_stolen *
                               ((double) delta_lcpu_wait / (double) (delta_lcpu_wait + delta_lcpu_idle));
         delta_pcpu_idle += delta_idle_stolen *
                               ((double) delta_lcpu_idle / (double) (delta_lcpu_wait + delta_lcpu_idle));

/* distribute idle donated to wait and idle proportionally to the logical wait and idle in clock tics, as */
/* cpu cycles were donated when this partition is idle or in wait */
         delta_pcpu_wait += delta_idle_donated *
                              ((double) delta_lcpu_wait / (double) (delta_lcpu_wait + delta_lcpu_idle));
         delta_pcpu_idle += delta_idle_donated *
                              ((double) delta_lcpu_idle / (double) (delta_lcpu_wait + delta_lcpu_idle));

/* add donated to the total physical processor tics for CPU usage calculation, as they were */
/* distributed to respective buckets accordingly */
         pcputime += (delta_idle_donated + delta_busy_donated);

/* add stolen to the total physical processor tics for CPU usage calculation, as they were */
/* distributed to respective buckets accordingly */
         pcputime += (delta_idle_stolen + delta_busy_stolen);

/* save old values */
         last_busy_donated = lparstats.busy_donated_purr;
         last_idle_donated = lparstats.idle_donated_purr;

         last_busy_stolen = lparstats.busy_stolen_purr;
         last_idle_stolen = lparstats.idle_stolen_purr;
      }
#endif

      if (pcputime == 0LL) pcputime = 1LL;

      cpu_info.user = 100.0 * (double) delta_pcpu_user / (double) pcputime;
      cpu_info.sys  = 100.0 * (double) delta_pcpu_sys  / (double) pcputime;
      cpu_info.idle = 100.0 * (double) delta_pcpu_idle / (double) pcputime;
      cpu_info.wait = 100.0 * (double) delta_pcpu_wait / (double) pcputime;

/* calculate physical cores used */
      cpu_info.physc = (double) delta_purr / (double) delta_time_base;

/* calculate ratio of physical cores used vs. entitlement */
      cpu_info.entc = 100.0 * cpu_info.physc / entitlement;
#else  /* _AIX53 */
      cpu_info.user = 100.0 * (double) delta_lcpu_user / (double) lcputime;
      cpu_info.sys  = 100.0 * (double) delta_lcpu_sys  / (double) lcputime;
      cpu_info.idle = 100.0 * (double) delta_lcpu_idle / (double) lcputime;
      cpu_info.wait = 100.0 * (double) delta_lcpu_wait / (double) lcputime;

/* calculate physical cores used */
      cpu_info.physc = (double) cpustats.ncpus_cfg * (cpu_info.user + cpu_info.sys) / 100.0;

/* calculate ratio of physical cores used vs. entitlement */
      cpu_info.entc = 100.0 * cpu_info.physc / (double) cpustats.ncpus_cfg;
      
#endif /* _AIX53 */
   }
}
  


/* int bos_level(int *aix_version, int *aix_release, int *aix_level, int *aix_fix)
 *  is copied form 
 *
 *  First stab at support for metrics in AIX
 *  by Preston Smith <psmith@physics.purdue.edu>
 *  Wed Feb 27 14:55:33 EST 2002
 *
 *  AIX V5 support, bugfixes added by Davide Tacchella <tack@cscs.ch>
 *  May 10, 2002
 *
 */

int bos_level( int *aix_version, int *aix_release, int *aix_level, int *aix_fix )
{
   struct Class *my_cl;   /* customized devices class ptr */
   struct product  productobj;     /* customized device object storage */
   int rc, getit, found = 0;
   char *path;

   /*
    * start up odm
    */
   if (odm_initialize() == -1)
      return( E_ODMINIT ); 

   /*
    * Make sure we take the right database
    */
   if ((path = odm_set_path( "/usr/lib/objrepos" )) == (char *) -1)
      return( odmerrno );
 
   /*
    * Mount the lpp class
    */
   if ((My_CLASS = odm_mount_class( "product" )) == (CLASS_SYMBOL) -1)
      return( odmerrno );

   /*
    * open customized devices object class
    */
   if ((int) (my_cl = odm_open_class( My_CLASS )) == -1)
      return( E_ODMOPEN );

   /*
    * Loop trough all entries for the lpp name, ASSUMING the last
    * one denotes the up to date number!!!
    */
   /*
    * AIX > 4.2 uses bos.mp or bos.up
    * AIX >= 6.1 uses bos.mp64
    */
   getit = ODM_FIRST;
   while ((rc = (int) odm_get_obj( my_cl, "name like bos.?p*",
                                   &productobj, getit )) != 0)
   {
      getit = ODM_NEXT;
      if (rc == -1)
      {
         /* ODM failure */
         break;
      }
      else
      {
         *aix_version = productobj.ver;
         *aix_release = productobj.rel;
         *aix_level   = productobj.mod;
         *aix_fix     = productobj.fix;
         found++;
      }
   }
   /*
    * AIX < 4.2 uses bos.rte.mp or bos.rte.up
    */
   if (!found)
   {
      getit = ODM_FIRST;
      while ((rc = (int) odm_get_obj( my_cl, "name like bos.rte.?p",
                                      &productobj, getit )) != 0)
      {
         getit = ODM_NEXT;
         if (rc == -1)
         {
            /* ODM failure */
            break;
         }
         else
         {
            *aix_version = productobj.ver;
            *aix_release = productobj.rel;
            *aix_level   = productobj.mod;
            *aix_fix     = productobj.fix;
            found++;
         }
      }
   }

   /*
    * close lpp object class
    */
   odm_close_class( my_cl );

   odm_terminate();

   free(path);

   return( found ? 0 : -1 );
} /* bos_level */


#define CALC_NETSTAT(type) (double) ((cur_ninfo->type<last_ninfo->type)?-1:(cur_ninfo->type - last_ninfo->type)/timediff)
void
update_ifdata( void )
{
   static int init_done = 0;
   static struct timeval lasttime = {0,0};
   struct timeval thistime;
   double timediff;


   /*
    * Compute time between calls
    */
   gettimeofday( &thistime, NULL );
   if (lasttime.tv_sec)
      timediff = ((double) thistime.tv_sec * 1.0e6 +
                  (double) thistime.tv_usec -
                  (double) lasttime.tv_sec * 1.0e6 -
                  (double) lasttime.tv_usec) / 1.0e6;
   else
      timediff = 1.0;

   /*
    * Do nothing if we are called to soon after the last call
    */
   if (init_done && (timediff < INFO_TIMEOUT)) return;

   lasttime = thistime;

   last_ninfo = &ninfo[ni_flag];

   ni_flag ^= 1;

   cur_ninfo = &ninfo[ni_flag];

   perfstat_netinterface_total( NULL, cur_ninfo, sizeof( perfstat_netinterface_total_t ), 1 );

   if (init_done)
   {
      cur_net_stat.ipackets = (CALC_NETSTAT(ipackets)<0)?cur_net_stat.ipackets:CALC_NETSTAT(ipackets);
      cur_net_stat.opackets = (CALC_NETSTAT(opackets)<0)?cur_net_stat.opackets:CALC_NETSTAT(opackets);
      cur_net_stat.ibytes   = (CALC_NETSTAT(ibytes)<0)  ?cur_net_stat.ibytes  :CALC_NETSTAT(ibytes);
      cur_net_stat.obytes   = (CALC_NETSTAT(obytes)<0)  ?cur_net_stat.obytes  :CALC_NETSTAT(obytes);
   }
   else
   {
      init_done = 1;

      cur_net_stat.ipackets = 0.0;
      cur_net_stat.opackets = 0.0;
      cur_net_stat.ibytes   = 0.0;
      cur_net_stat.obytes   = 0.0;
   }

}  /* update_ifdata */

