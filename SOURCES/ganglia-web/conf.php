<?php

# Gmetad-webfrontend modifications for AIX.
# from Michael Perzl

$conf['auth_system'] = 'disabled';
#
# Default metric
#
$conf['default_metric'] = "cpu_used";


#
# Default color for single metric graphs
#
$conf['default_metric_color'] = "0000ff";

#
# Graph sizes
#
$conf['graph_sizes'] = array(
   'small'=>array(
     'height'=>65,
     'width'=>200,
     'fudge_0'=>0,
     'fudge_1'=>0,
     'fudge_2'=>0
   ),
   'medium'=>array(
     'height'=>95,
     'width'=>300,
     'fudge_0'=>0,
     'fudge_1'=>14,
     'fudge_2'=>28
   ),

  'large'=>array(
     'height'=>400,
     'width'=>800,
     'fudge_0'=>0,
     'fudge_1'=>0,
     'fudge_2'=>0
   ),

   'xlarge'=>array(
     'height'=>600,
     'width'=>1200,
     'fudge_0'=>0,
     'fudge_1'=>0,
     'fudge_2'=>0
   ),

   'mobile'=>array(
     'height'=>95,
     'width'=>220,
     'fudge_0'=>0,
     'fudge_1'=>0,
     'fudge_2'=>0
   ),

   # this was the default value when no other size was provided.
   'default'=>array(
     'height'=>100,
     'width'=>400,
     'fudge_0'=>0,
     'fudge_1'=>0,
     'fudge_2'=>0
   )

);
$conf['default_graph_size'] = 'default';
$conf['graph_sizes_keys'] = array_keys( $conf['graph_sizes'] );

#
# Colors for the CPU_USED report graph
#
$max_unique_colors = 30;

$unique_color[0]  = "ff0000";
$unique_color[1]  = "00ff00";
$unique_color[2]  = "0000ff";
$unique_color[3]  = "ffff00";
$unique_color[4]  = "ff00ff";
$unique_color[5]  = "00ffff";
$unique_color[6]  = "bb0000";
$unique_color[7]  = "00bb00";
$unique_color[8]  = "0000bb";
$unique_color[9]  = "bbbb00";
$unique_color[10] = "bb00bb";
$unique_color[11] = "00bbbb";
$unique_color[12] = "b22222";
$unique_color[13] = "adff2f";
$unique_color[14] = "ff1493";
$unique_color[15] = "f0e68c";
$unique_color[16] = "dda0dd";
$unique_color[17] = "8a2be2";
$unique_color[18] = "880000";
$unique_color[19] = "008800";
$unique_color[20] = "000088";
$unique_color[21] = "888800";
$unique_color[22] = "880088";
$unique_color[23] = "008888";
$unique_color[24] = "ff4500";
$unique_color[25] = "90ee90";
$unique_color[26] = "7b68ee";
$unique_color[27] = "aaaaaa";
$unique_color[28] = "87ceeb";
$unique_color[29] = "daa520";
?>
