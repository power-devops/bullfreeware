<?php
 
/* Pass in by reference! */
function graph_cpu_used_report ( &$rrdtool_graph ) {

   global $conf,
          $context,
          $hostname,
          $range,
          $rrd_dir,
          $size,
          $max_unique_colors,
          $unique_color;

   if ($conf['strip_domainname']) {
      $hostname = strip_domainname($hostname);
   }

   $title = 'Physical Core Usage';

   if ($context != "host") {
      $rrdtool_graph['title'] = $title;
   } else {
      $rrdtool_graph['title'] = "$hostname $title last $range";
   }

   $rrdtool_graph['vertical-label'] = 'Physical Cores';
// Fudge to account for number of lines in the chart legend
   $rrdtool_graph['height']        += ($size == 'medium') ? 28 : 0 ;
   $rrdtool_graph['lower-limit']    = '0';
   $rrdtool_graph['extras']         = '--rigid';

   $series = '';

   if ((($size != 'large') && ($size != 'xlarge')) || 
       ((($size == 'large') || ($size == 'xlarge')) && ($context == "host"))) {
      $rrdtool_graph['extras'] .= ($conf['graphreport_stats'] == true) ? ' --font LEGEND:7' : '';
      //* we obtain the information from __SummaryInfo__
      if (file_exists( "${rrd_dir}/cpu_used.rrd" )) {
         $series =
         "DEF:'cpu_used'='${rrd_dir}/cpu_used.rrd':'sum':AVERAGE "
         ."AREA:'cpu_used'#$unique_color[0]:'Used CPU  ' ";

         if ($conf['graphreport_stats'] == true) {
            $series .= "CDEF:cused_pos=cpu_used,0,LT,0,cpu_used,IF "
                . "VDEF:cused_min=cused_pos,MINIMUM "
                . "VDEF:cused_avg=cused_pos,AVERAGE "
                . "VDEF:cused_max=cused_pos,MAXIMUM "
                . "GPRINT:'cused_min':'Min\:%7.2lf%s' "
                . "GPRINT:'cused_avg':'Avg\:%7.2lf%s' "
                . "GPRINT:'cused_max':'Max\:%7.2lf%s\\l' ";

            if ($context == "host") {
               $series .= "DEF:'entitlement'='${rrd_dir}/cpu_entitlement.rrd':'sum':AVERAGE "
                         ."LINE2:'entitlement'#000000:'CPU Entitlement' "
                         ."DEF:'cpu_in_lpar'='${rrd_dir}/cpu_in_lpar.rrd':'sum':AVERAGE "
                         ."LINE2:'cpu_in_lpar'#0000FF:'Number of virtual CPUs' ";
            }
         }
      }
   } else {
      // we have to obtain all metrics ourselves
      $pos = strpos( ${rrd_dir}, '__SummaryInfo__' );
      $cluster_dir = substr( ${rrd_dir}, 0, $pos-1 );

      $dh = opendir(${cluster_dir});

      $files = array();

      while (($file = readdir($dh)) !== false)
         if (($file != "__SummaryInfo__") && ($file != ".") && ($file != "..")) {
            array_push($files, $file);
         }

      closedir($dh);

      // sort the files
      sort($files);

      $i = 0;

      foreach ($files as $file) {
         if (file_exists( "${cluster_dir}/${file}/cpu_used.rrd" )) {
            $cmd =
            "DEF:'label$i'='${cluster_dir}/${file}/cpu_used.rrd':'sum':AVERAGE ";

            $color_index = $i % $max_unique_colors;

            if ($i == 0) {
               $cmd .= "AREA:'label$i'#$unique_color[$color_index]:'$file' ";
            } else {
               $cmd .= "STACK:'label$i'#$unique_color[$color_index]:'$file' ";
            }

            $series .= $cmd;

            $i += 1;
         }
      }
   }

   $rrdtool_graph['series'] = $series;

   return $rrdtool_graph;

}

?>
