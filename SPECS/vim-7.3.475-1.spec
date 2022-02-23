%define vimdir vim73
%define baseversion 7.3
%define patchlevel 475

Summary: The VIM editor
URL:     http://www.vim.org/
Name:    vim
Version: %{baseversion}.%{patchlevel}
Release: 2
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/%{name}-%{baseversion}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source12: vi_help.txt
Source14: %{name}-spec-template
Source15: http://www.cvjb.de/comp/vim/forth.vim

# patch to make python and perl work
Patch0: %{name}-%{baseversion}-aix-configure.patch

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
Patch2004: vim-7.0-crv.patch
# Patches 001 < 999 are patches from the base maintainer.
# If you're as lazy as me, generate the list using
# for i in `seq -w 1 475` ; do echo "Patch$i: vim-7.3.$i.patch" ; done
# the real names of the patches are like that:
#     ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.001
# however, I renamed them because I didn't want my SOURCES directory to be so
# cluttered
Patch001: vim-7.3.001.patch
Patch002: vim-7.3.002.patch
Patch003: vim-7.3.003.patch
Patch004: vim-7.3.004.patch
Patch005: vim-7.3.005.patch
Patch006: vim-7.3.006.patch
Patch007: vim-7.3.007.patch
Patch008: vim-7.3.008.patch
Patch009: vim-7.3.009.patch
Patch010: vim-7.3.010.patch
Patch011: vim-7.3.011.patch
Patch012: vim-7.3.012.patch
Patch013: vim-7.3.013.patch
Patch014: vim-7.3.014.patch
Patch015: vim-7.3.015.patch
Patch016: vim-7.3.016.patch
Patch017: vim-7.3.017.patch
Patch018: vim-7.3.018.patch
Patch019: vim-7.3.019.patch
Patch020: vim-7.3.020.patch
Patch021: vim-7.3.021.patch
Patch022: vim-7.3.022.patch
Patch023: vim-7.3.023.patch
Patch024: vim-7.3.024.patch
Patch025: vim-7.3.025.patch
Patch026: vim-7.3.026.patch
Patch027: vim-7.3.027.patch
Patch028: vim-7.3.028.patch
Patch029: vim-7.3.029.patch
Patch030: vim-7.3.030.patch
Patch031: vim-7.3.031.patch
Patch032: vim-7.3.032.patch
Patch033: vim-7.3.033.patch
Patch034: vim-7.3.034.patch
Patch035: vim-7.3.035.patch
Patch036: vim-7.3.036.patch
Patch037: vim-7.3.037.patch
Patch038: vim-7.3.038.patch
Patch039: vim-7.3.039.patch
Patch040: vim-7.3.040.patch
Patch041: vim-7.3.041.patch
Patch042: vim-7.3.042.patch
Patch043: vim-7.3.043.patch
Patch044: vim-7.3.044.patch
Patch045: vim-7.3.045.patch
Patch046: vim-7.3.046.patch
Patch047: vim-7.3.047.patch
Patch048: vim-7.3.048.patch
Patch049: vim-7.3.049.patch
Patch050: vim-7.3.050.patch
Patch051: vim-7.3.051.patch
Patch052: vim-7.3.052.patch
Patch053: vim-7.3.053.patch
Patch054: vim-7.3.054.patch
Patch055: vim-7.3.055.patch
Patch056: vim-7.3.056.patch
Patch057: vim-7.3.057.patch
Patch058: vim-7.3.058.patch
Patch059: vim-7.3.059.patch
Patch060: vim-7.3.060.patch
Patch061: vim-7.3.061.patch
Patch062: vim-7.3.062.patch
Patch063: vim-7.3.063.patch
Patch064: vim-7.3.064.patch
Patch065: vim-7.3.065.patch
Patch066: vim-7.3.066.patch
Patch067: vim-7.3.067.patch
Patch068: vim-7.3.068.patch
Patch069: vim-7.3.069.patch
Patch070: vim-7.3.070.patch
Patch071: vim-7.3.071.patch
Patch072: vim-7.3.072.patch
Patch073: vim-7.3.073.patch
Patch074: vim-7.3.074.patch
Patch075: vim-7.3.075.patch
Patch076: vim-7.3.076.patch
Patch077: vim-7.3.077.patch
Patch078: vim-7.3.078.patch
Patch079: vim-7.3.079.patch
Patch080: vim-7.3.080.patch
Patch081: vim-7.3.081.patch
Patch082: vim-7.3.082.patch
Patch083: vim-7.3.083.patch
Patch084: vim-7.3.084.patch
Patch085: vim-7.3.085.patch
Patch086: vim-7.3.086.patch
Patch087: vim-7.3.087.patch
Patch088: vim-7.3.088.patch
Patch089: vim-7.3.089.patch
Patch090: vim-7.3.090.patch
Patch091: vim-7.3.091.patch
Patch092: vim-7.3.092.patch
Patch093: vim-7.3.093.patch
Patch094: vim-7.3.094.patch
Patch095: vim-7.3.095.patch
Patch096: vim-7.3.096.patch
Patch097: vim-7.3.097.patch
Patch098: vim-7.3.098.patch
Patch099: vim-7.3.099.patch
Patch100: vim-7.3.100.patch
Patch101: vim-7.3.101.patch
Patch102: vim-7.3.102.patch
Patch103: vim-7.3.103.patch
Patch104: vim-7.3.104.patch
Patch105: vim-7.3.105.patch
Patch106: vim-7.3.106.patch
Patch107: vim-7.3.107.patch
Patch108: vim-7.3.108.patch
Patch109: vim-7.3.109.patch
Patch110: vim-7.3.110.patch
Patch111: vim-7.3.111.patch
Patch112: vim-7.3.112.patch
Patch113: vim-7.3.113.patch
Patch114: vim-7.3.114.patch
Patch115: vim-7.3.115.patch
Patch116: vim-7.3.116.patch
Patch117: vim-7.3.117.patch
Patch118: vim-7.3.118.patch
Patch119: vim-7.3.119.patch
Patch120: vim-7.3.120.patch
Patch121: vim-7.3.121.patch
Patch122: vim-7.3.122.patch
Patch123: vim-7.3.123.patch
Patch124: vim-7.3.124.patch
Patch125: vim-7.3.125.patch
Patch126: vim-7.3.126.patch
Patch127: vim-7.3.127.patch
Patch128: vim-7.3.128.patch
Patch129: vim-7.3.129.patch
Patch130: vim-7.3.130.patch
Patch131: vim-7.3.131.patch
Patch132: vim-7.3.132.patch
Patch133: vim-7.3.133.patch
Patch134: vim-7.3.134.patch
Patch135: vim-7.3.135.patch
Patch136: vim-7.3.136.patch
Patch137: vim-7.3.137.patch
Patch138: vim-7.3.138.patch
Patch139: vim-7.3.139.patch
Patch140: vim-7.3.140.patch
Patch141: vim-7.3.141.patch
Patch142: vim-7.3.142.patch
Patch143: vim-7.3.143.patch
Patch144: vim-7.3.144.patch
Patch145: vim-7.3.145.patch
Patch146: vim-7.3.146.patch
Patch147: vim-7.3.147.patch
Patch148: vim-7.3.148.patch
Patch149: vim-7.3.149.patch
Patch150: vim-7.3.150.patch
Patch151: vim-7.3.151.patch
Patch152: vim-7.3.152.patch
Patch153: vim-7.3.153.patch
Patch154: vim-7.3.154.patch
Patch155: vim-7.3.155.patch
Patch156: vim-7.3.156.patch
Patch157: vim-7.3.157.patch
Patch158: vim-7.3.158.patch
Patch159: vim-7.3.159.patch
Patch160: vim-7.3.160.patch
Patch161: vim-7.3.161.patch
Patch162: vim-7.3.162.patch
Patch163: vim-7.3.163.patch
Patch164: vim-7.3.164.patch
Patch165: vim-7.3.165.patch
Patch166: vim-7.3.166.patch
Patch167: vim-7.3.167.patch
Patch168: vim-7.3.168.patch
Patch169: vim-7.3.169.patch
Patch170: vim-7.3.170.patch
Patch171: vim-7.3.171.patch
Patch172: vim-7.3.172.patch
Patch173: vim-7.3.173.patch
Patch174: vim-7.3.174.patch
Patch175: vim-7.3.175.patch
Patch176: vim-7.3.176.patch
Patch177: vim-7.3.177.patch
Patch178: vim-7.3.178.patch
Patch179: vim-7.3.179.patch
Patch180: vim-7.3.180.patch
Patch181: vim-7.3.181.patch
Patch182: vim-7.3.182.patch
Patch183: vim-7.3.183.patch
Patch184: vim-7.3.184.patch
Patch185: vim-7.3.185.patch
Patch186: vim-7.3.186.patch
Patch187: vim-7.3.187.patch
Patch188: vim-7.3.188.patch
Patch189: vim-7.3.189.patch
Patch190: vim-7.3.190.patch
Patch191: vim-7.3.191.patch
Patch192: vim-7.3.192.patch
Patch193: vim-7.3.193.patch
Patch194: vim-7.3.194.patch
Patch195: vim-7.3.195.patch
Patch196: vim-7.3.196.patch
Patch197: vim-7.3.197.patch
Patch198: vim-7.3.198.patch
Patch199: vim-7.3.199.patch
Patch200: vim-7.3.200.patch
Patch201: vim-7.3.201.patch
Patch202: vim-7.3.202.patch
Patch203: vim-7.3.203.patch
Patch204: vim-7.3.204.patch
Patch205: vim-7.3.205.patch
Patch206: vim-7.3.206.patch
Patch207: vim-7.3.207.patch
Patch208: vim-7.3.208.patch
Patch209: vim-7.3.209.patch
Patch210: vim-7.3.210.patch
Patch211: vim-7.3.211.patch
Patch212: vim-7.3.212.patch
Patch213: vim-7.3.213.patch
Patch214: vim-7.3.214.patch
Patch215: vim-7.3.215.patch
Patch216: vim-7.3.216.patch
Patch217: vim-7.3.217.patch
Patch218: vim-7.3.218.patch
Patch219: vim-7.3.219.patch
Patch220: vim-7.3.220.patch
Patch221: vim-7.3.221.patch
Patch222: vim-7.3.222.patch
Patch223: vim-7.3.223.patch
Patch224: vim-7.3.224.patch
Patch225: vim-7.3.225.patch
Patch226: vim-7.3.226.patch
Patch227: vim-7.3.227.patch
Patch228: vim-7.3.228.patch
Patch229: vim-7.3.229.patch
Patch230: vim-7.3.230.patch
Patch231: vim-7.3.231.patch
Patch232: vim-7.3.232.patch
Patch233: vim-7.3.233.patch
Patch234: vim-7.3.234.patch
Patch235: vim-7.3.235.patch
Patch236: vim-7.3.236.patch
Patch237: vim-7.3.237.patch
Patch238: vim-7.3.238.patch
Patch239: vim-7.3.239.patch
Patch240: vim-7.3.240.patch
Patch241: vim-7.3.241.patch
Patch242: vim-7.3.242.patch
Patch243: vim-7.3.243.patch
Patch244: vim-7.3.244.patch
Patch245: vim-7.3.245.patch
Patch246: vim-7.3.246.patch
Patch247: vim-7.3.247.patch
Patch248: vim-7.3.248.patch
Patch249: vim-7.3.249.patch
Patch250: vim-7.3.250.patch
Patch251: vim-7.3.251.patch
Patch252: vim-7.3.252.patch
Patch253: vim-7.3.253.patch
Patch254: vim-7.3.254.patch
Patch255: vim-7.3.255.patch
Patch256: vim-7.3.256.patch
Patch257: vim-7.3.257.patch
Patch258: vim-7.3.258.patch
Patch259: vim-7.3.259.patch
Patch260: vim-7.3.260.patch
Patch261: vim-7.3.261.patch
Patch262: vim-7.3.262.patch
Patch263: vim-7.3.263.patch
Patch264: vim-7.3.264.patch
Patch265: vim-7.3.265.patch
Patch266: vim-7.3.266.patch
Patch267: vim-7.3.267.patch
Patch268: vim-7.3.268.patch
Patch269: vim-7.3.269.patch
Patch270: vim-7.3.270.patch
Patch271: vim-7.3.271.patch
Patch272: vim-7.3.272.patch
Patch273: vim-7.3.273.patch
Patch274: vim-7.3.274.patch
Patch275: vim-7.3.275.patch
Patch276: vim-7.3.276.patch
Patch277: vim-7.3.277.patch
Patch278: vim-7.3.278.patch
Patch279: vim-7.3.279.patch
Patch280: vim-7.3.280.patch
Patch281: vim-7.3.281.patch
Patch282: vim-7.3.282.patch
Patch283: vim-7.3.283.patch
Patch284: vim-7.3.284.patch
Patch285: vim-7.3.285.patch
Patch286: vim-7.3.286.patch
Patch287: vim-7.3.287.patch
Patch288: vim-7.3.288.patch
Patch289: vim-7.3.289.patch
Patch290: vim-7.3.290.patch
Patch291: vim-7.3.291.patch
Patch292: vim-7.3.292.patch
Patch293: vim-7.3.293.patch
Patch294: vim-7.3.294.patch
Patch295: vim-7.3.295.patch
Patch296: vim-7.3.296.patch
Patch297: vim-7.3.297.patch
Patch298: vim-7.3.298.patch
Patch299: vim-7.3.299.patch
Patch300: vim-7.3.300.patch
Patch301: vim-7.3.301.patch
Patch302: vim-7.3.302.patch
Patch303: vim-7.3.303.patch
Patch304: vim-7.3.304.patch
Patch305: vim-7.3.305.patch
Patch306: vim-7.3.306.patch
Patch307: vim-7.3.307.patch
Patch308: vim-7.3.308.patch
Patch309: vim-7.3.309.patch
Patch310: vim-7.3.310.patch
Patch311: vim-7.3.311.patch
Patch312: vim-7.3.312.patch
Patch313: vim-7.3.313.patch
Patch314: vim-7.3.314.patch
Patch315: vim-7.3.315.patch
Patch316: vim-7.3.316.patch
Patch317: vim-7.3.317.patch
Patch318: vim-7.3.318.patch
Patch319: vim-7.3.319.patch
Patch320: vim-7.3.320.patch
Patch321: vim-7.3.321.patch
Patch322: vim-7.3.322.patch
Patch323: vim-7.3.323.patch
Patch324: vim-7.3.324.patch
Patch325: vim-7.3.325.patch
Patch326: vim-7.3.326.patch
Patch327: vim-7.3.327.patch
Patch328: vim-7.3.328.patch
Patch329: vim-7.3.329.patch
Patch330: vim-7.3.330.patch
Patch331: vim-7.3.331.patch
Patch332: vim-7.3.332.patch
Patch333: vim-7.3.333.patch
Patch334: vim-7.3.334.patch
Patch335: vim-7.3.335.patch
Patch336: vim-7.3.336.patch
Patch337: vim-7.3.337.patch
Patch338: vim-7.3.338.patch
Patch339: vim-7.3.339.patch
Patch340: vim-7.3.340.patch
Patch341: vim-7.3.341.patch
Patch342: vim-7.3.342.patch
Patch343: vim-7.3.343.patch
Patch344: vim-7.3.344.patch
Patch345: vim-7.3.345.patch
Patch346: vim-7.3.346.patch
Patch347: vim-7.3.347.patch
Patch348: vim-7.3.348.patch
Patch349: vim-7.3.349.patch
Patch350: vim-7.3.350.patch
Patch351: vim-7.3.351.patch
Patch352: vim-7.3.352.patch
Patch353: vim-7.3.353.patch
Patch354: vim-7.3.354.patch
Patch355: vim-7.3.355.patch
Patch356: vim-7.3.356.patch
Patch357: vim-7.3.357.patch
Patch358: vim-7.3.358.patch
Patch359: vim-7.3.359.patch
Patch360: vim-7.3.360.patch
Patch361: vim-7.3.361.patch
Patch362: vim-7.3.362.patch
Patch363: vim-7.3.363.patch
Patch364: vim-7.3.364.patch
Patch365: vim-7.3.365.patch
Patch366: vim-7.3.366.patch
Patch367: vim-7.3.367.patch
Patch368: vim-7.3.368.patch
Patch369: vim-7.3.369.patch
Patch370: vim-7.3.370.patch
Patch371: vim-7.3.371.patch
Patch372: vim-7.3.372.patch
Patch373: vim-7.3.373.patch
Patch374: vim-7.3.374.patch
Patch375: vim-7.3.375.patch
Patch376: vim-7.3.376.patch
Patch377: vim-7.3.377.patch
Patch378: vim-7.3.378.patch
Patch379: vim-7.3.379.patch
Patch380: vim-7.3.380.patch
Patch381: vim-7.3.381.patch
Patch382: vim-7.3.382.patch
Patch383: vim-7.3.383.patch
Patch384: vim-7.3.384.patch
Patch385: vim-7.3.385.patch
Patch386: vim-7.3.386.patch
Patch387: vim-7.3.387.patch
Patch388: vim-7.3.388.patch
Patch389: vim-7.3.389.patch
Patch390: vim-7.3.390.patch
Patch391: vim-7.3.391.patch
Patch392: vim-7.3.392.patch
Patch393: vim-7.3.393.patch
Patch394: vim-7.3.394.patch
Patch395: vim-7.3.395.patch
Patch396: vim-7.3.396.patch
Patch397: vim-7.3.397.patch
Patch398: vim-7.3.398.patch
Patch399: vim-7.3.399.patch
Patch400: vim-7.3.400.patch
Patch401: vim-7.3.401.patch
Patch402: vim-7.3.402.patch
Patch403: vim-7.3.403.patch
Patch404: vim-7.3.404.patch
Patch405: vim-7.3.405.patch
Patch406: vim-7.3.406.patch
Patch407: vim-7.3.407.patch
Patch408: vim-7.3.408.patch
Patch409: vim-7.3.409.patch
Patch410: vim-7.3.410.patch
Patch411: vim-7.3.411.patch
Patch412: vim-7.3.412.patch
Patch413: vim-7.3.413.patch
Patch414: vim-7.3.414.patch
Patch415: vim-7.3.415.patch
Patch416: vim-7.3.416.patch
Patch417: vim-7.3.417.patch
Patch418: vim-7.3.418.patch
Patch419: vim-7.3.419.patch
Patch420: vim-7.3.420.patch
Patch421: vim-7.3.421.patch
Patch422: vim-7.3.422.patch
Patch423: vim-7.3.423.patch
Patch424: vim-7.3.424.patch
Patch425: vim-7.3.425.patch
Patch426: vim-7.3.426.patch
Patch427: vim-7.3.427.patch
Patch428: vim-7.3.428.patch
Patch429: vim-7.3.429.patch
Patch430: vim-7.3.430.patch
Patch431: vim-7.3.431.patch
Patch432: vim-7.3.432.patch
Patch433: vim-7.3.433.patch
Patch434: vim-7.3.434.patch
Patch435: vim-7.3.435.patch
Patch436: vim-7.3.436.patch
Patch437: vim-7.3.437.patch
Patch438: vim-7.3.438.patch
Patch439: vim-7.3.439.patch
Patch440: vim-7.3.440.patch
Patch441: vim-7.3.441.patch
Patch442: vim-7.3.442.patch
Patch443: vim-7.3.443.patch
Patch444: vim-7.3.444.patch
Patch445: vim-7.3.445.patch
Patch446: vim-7.3.446.patch
Patch447: vim-7.3.447.patch
Patch448: vim-7.3.448.patch
Patch449: vim-7.3.449.patch
Patch450: vim-7.3.450.patch
Patch451: vim-7.3.451.patch
Patch452: vim-7.3.452.patch
Patch453: vim-7.3.453.patch
Patch454: vim-7.3.454.patch
Patch455: vim-7.3.455.patch
Patch456: vim-7.3.456.patch
Patch457: vim-7.3.457.patch
Patch458: vim-7.3.458.patch
Patch459: vim-7.3.459.patch
Patch460: vim-7.3.460.patch
Patch461: vim-7.3.461.patch
Patch462: vim-7.3.462.patch
Patch463: vim-7.3.463.patch
Patch464: vim-7.3.464.patch
Patch465: vim-7.3.465.patch
Patch466: vim-7.3.466.patch
Patch467: vim-7.3.467.patch
Patch468: vim-7.3.468.patch
Patch469: vim-7.3.469.patch
Patch470: vim-7.3.470.patch
Patch471: vim-7.3.471.patch
Patch472: vim-7.3.472.patch
Patch473: vim-7.3.473.patch
Patch474: vim-7.3.474.patch
Patch475: vim-7.3.475.patch

Patch3000: vim-7.3-syntax.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3003: vim-6.1-rh3.patch
Patch3006: vim-6.4-checkhl.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch

Patch5000: vim-7.3-utf8.patch

Buildroot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: python-devel >= 2.6.2, gettext, perl >= 5.8.8
BuildRequires: patch, make

BuildRequires: gtk2-devel >= 2.8.3, glib2-devel >= 2.8.1, pango-devel >= 1.10.0
Requires: gettext

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%define osplat aix5
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.


%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.


%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Requires: gettext

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.


%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: %{name}-common = %{version}-%{release}
Provides: %{name} = %{version}-%{release}
Requires: gettext
#Requires: perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Requires: perl >= 5.8.8
Requires: python >= 2.6.2

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.


%package X11
Summary: The VIM version of the vi editor for the X Window System
Group: Applications/Editors
Requires: %{name}-common = %{version}-%{release}, gtk2 >= 2.8.3
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel >= 2.8.3, glib2-devel >= 2.8.1
BuildRequires: pango-devel >= 1.10.0
Requires: gtk2 >= 2.8.3, glib2 >= 2.8.1
Requires: pango >= 1.10.0
Requires: gettext
#Requires: perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Requires: perl >= 5.8.8
Requires: python >= 2.6.2

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.


%prep
%setup -q -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk

export PATH=/opt/freeware/bin:$PATH

%patch2002 -p1
%patch2003 -p1
%patch2004 -p1
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# Base patches...
# for i in `seq -w 1 475` ; do  echo "%patch$i -p0" ; done
%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0
%patch049 -p0
%patch050 -p0
%patch051 -p0
%patch052 -p0
%patch053 -p0
%patch054 -p0
%patch055 -p0
%patch056 -p0
%patch057 -p0
%patch058 -p0
%patch059 -p0
%patch060 -p0
%patch061 -p0
%patch062 -p0
%patch063 -p0
%patch064 -p0
%patch065 -p0
%patch066 -p0
%patch067 -p0
%patch068 -p0
%patch069 -p0
%patch070 -p0
%patch071 -p0
%patch072 -p0
%patch073 -p0
%patch074 -p0
%patch075 -p0
%patch076 -p0
%patch077 -p0
%patch078 -p0
%patch079 -p0
%patch080 -p0
%patch081 -p0
%patch082 -p0
%patch083 -p0
%patch084 -p0
%patch085 -p0
%patch086 -p0
%patch087 -p0
%patch088 -p0
%patch089 -p0
%patch090 -p0
%patch091 -p0
%patch092 -p0
%patch093 -p0
%patch094 -p0
%patch095 -p0
%patch096 -p0
%patch097 -p0
%patch098 -p0
%patch099 -p0
%patch100 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0
%patch111 -p0
%patch112 -p0
%patch113 -p0
%patch114 -p0
%patch115 -p0
%patch116 -p0
%patch117 -p0
%patch118 -p0
%patch119 -p0
%patch120 -p0
%patch121 -p0
%patch122 -p0
%patch123 -p0
%patch124 -p0
%patch125 -p0
%patch126 -p0
%patch127 -p0
%patch128 -p0
%patch129 -p0
%patch130 -p0
%patch131 -p0
%patch132 -p0
%patch133 -p0
%patch134 -p0
%patch135 -p0
%patch136 -p0
%patch137 -p0
%patch138 -p0
%patch139 -p0
%patch140 -p0
%patch141 -p0
%patch142 -p0
%patch143 -p0
%patch144 -p0
%patch145 -p0
%patch146 -p0
%patch147 -p0
%patch148 -p0
%patch149 -p0
%patch150 -p0
%patch151 -p0
%patch152 -p0
%patch153 -p0
%patch154 -p0
%patch155 -p0
%patch156 -p0
%patch157 -p0
%patch158 -p0
%patch159 -p0
%patch160 -p0
%patch161 -p0
%patch162 -p0
%patch163 -p0
%patch164 -p0
%patch165 -p0
%patch166 -p0
%patch167 -p0
%patch168 -p0
%patch169 -p0
%patch170 -p0
%patch171 -p0
%patch172 -p0
%patch173 -p0
%patch174 -p0
%patch175 -p0
%patch176 -p0
%patch177 -p0
%patch178 -p0
%patch179 -p0
%patch180 -p0
%patch181 -p0
%patch182 -p0
%patch183 -p0
%patch184 -p0
%patch185 -p0
%patch186 -p0
%patch187 -p0
%patch188 -p0
%patch189 -p0
%patch190 -p0
%patch191 -p0
%patch192 -p0
%patch193 -p0
%patch194 -p0
%patch195 -p0
%patch196 -p0
%patch197 -p0
%patch198 -p0
%patch199 -p0
%patch200 -p0
%patch201 -p0
%patch202 -p0
%patch203 -p0
%patch204 -p0
%patch205 -p0
%patch206 -p0
%patch207 -p0
%patch208 -p0
%patch209 -p0
%patch210 -p0
%patch211 -p0
%patch212 -p0
%patch213 -p0
%patch214 -p0
%patch215 -p0
%patch216 -p0
%patch217 -p0
%patch218 -p0
%patch219 -p0
%patch220 -p0
%patch221 -p0
%patch222 -p0
%patch223 -p0
%patch224 -p0
%patch225 -p0
%patch226 -p0
%patch227 -p0
%patch228 -p0
%patch229 -p0
%patch230 -p0
%patch231 -p0
%patch232 -p0
%patch233 -p0
%patch234 -p0
%patch235 -p0
%patch236 -p0
%patch237 -p0
%patch238 -p0
%patch239 -p0
%patch240 -p0
%patch241 -p0
%patch242 -p0
%patch243 -p0
%patch244 -p0
%patch245 -p0
%patch246 -p0
%patch247 -p0
%patch248 -p0
%patch249 -p0
%patch250 -p0
%patch251 -p0
%patch252 -p0
%patch253 -p0
%patch254 -p0
%patch255 -p0
%patch256 -p0
%patch257 -p0
%patch258 -p0
%patch259 -p0
%patch260 -p0
%patch261 -p0
%patch262 -p0
%patch263 -p0
%patch264 -p0
%patch265 -p0
%patch266 -p0
%patch267 -p0
%patch268 -p0
%patch269 -p0
%patch270 -p0
%patch271 -p0
%patch272 -p0
%patch273 -p0
%patch274 -p0
%patch275 -p0
%patch276 -p0
%patch277 -p0
%patch278 -p0
%patch279 -p0
%patch280 -p0
%patch281 -p0
%patch282 -p0
%patch283 -p0
%patch284 -p0
%patch285 -p0
%patch286 -p0
%patch287 -p0
%patch288 -p0
%patch289 -p0
%patch290 -p0
%patch291 -p0
%patch292 -p0
%patch293 -p0
%patch294 -p0
%patch295 -p0
%patch296 -p0
%patch297 -p0
%patch298 -p0
%patch299 -p0
%patch300 -p0
%patch301 -p0
%patch302 -p0
%patch303 -p0
%patch304 -p0
%patch305 -p0
%patch306 -p0
%patch307 -p0
%patch308 -p0
%patch309 -p0
%patch310 -p0
%patch311 -p0
%patch312 -p0
%patch313 -p0
%patch314 -p0
%patch315 -p0
%patch316 -p0
%patch317 -p0
%patch318 -p0
%patch319 -p0
%patch320 -p0
%patch321 -p0
%patch322 -p0
%patch323 -p0
%patch324 -p0
%patch325 -p0
%patch326 -p0
%patch327 -p0
%patch328 -p0
%patch329 -p0
%patch330 -p0
%patch331 -p0
%patch332 -p0
%patch333 -p0
%patch334 -p0
%patch335 -p0
%patch336 -p0
%patch338 -p0
%patch339 -p0
%patch340 -p0
%patch341 -p0
%patch342 -p0
%patch343 -p0
%patch344 -p0
%patch345 -p0
%patch346 -p0
%patch347 -p0
%patch348 -p0
%patch349 -p0
%patch350 -p0
%patch351 -p0
%patch352 -p0
%patch353 -p0
%patch354 -p0
%patch355 -p0
%patch356 -p0
%patch357 -p0
%patch358 -p0
%patch359 -p0
%patch360 -p0
%patch361 -p0
%patch362 -p0
%patch363 -p0
%patch364 -p0
%patch365 -p0
%patch366 -p0
%patch367 -p0
%patch368 -p0
%patch369 -p0
%patch370 -p0
%patch371 -p0
%patch372 -p0
%patch373 -p0
%patch374 -p0
%patch375 -p0
%patch376 -p0
%patch377 -p0
%patch378 -p0
%patch379 -p0
%patch380 -p0
%patch381 -p0
%patch382 -p0
%patch383 -p0
%patch384 -p0
%patch385 -p0
%patch386 -p0
%patch387 -p0
%patch388 -p0
%patch389 -p0
%patch390 -p0
%patch391 -p0
%patch392 -p0
%patch393 -p0
%patch394 -p0
%patch395 -p0
%patch396 -p0
%patch397 -p0
%patch398 -p0
%patch399 -p0
%patch400 -p0
%patch401 -p0
%patch402 -p0
%patch403 -p0
%patch404 -p0
%patch405 -p0
%patch406 -p0
%patch407 -p0
%patch408 -p0
%patch409 -p0
%patch410 -p0
%patch411 -p0
%patch412 -p0
%patch413 -p0
%patch414 -p0
%patch415 -p0
%patch416 -p0
%patch417 -p0
%patch418 -p0
%patch419 -p0
%patch420 -p0
%patch421 -p0
%patch422 -p0
%patch423 -p0
%patch424 -p0
%patch425 -p0
%patch426 -p0
%patch427 -p0
%patch428 -p0
%patch429 -p0
%patch430 -p0
%patch431 -p0
%patch432 -p0
%patch433 -p0
%patch434 -p0
%patch435 -p0
%patch436 -p0
%patch437 -p0
%patch438 -p0
%patch439 -p0
%patch440 -p0
%patch441 -p0
%patch442 -p0
%patch443 -p0
%patch444 -p0
%patch445 -p0
%patch446 -p0
%patch447 -p0
%patch448 -p0
%patch449 -p0
%patch450 -p0
%patch451 -p0
%patch452 -p0
%patch453 -p0
%patch454 -p0
%patch455 -p0
%patch456 -p0
%patch457 -p0
%patch458 -p0
%patch459 -p0
%patch460 -p0
%patch461 -p0
%patch462 -p0
%patch463 -p0
%patch464 -p0
%patch465 -p0
%patch466 -p0
%patch467 -p0
%patch468 -p0
%patch469 -p0
%patch470 -p0
%patch471 -p0
%patch472 -p0
%patch473 -p0
%patch474 -p0
%patch475 -p0

%patch3000 -p1
%patch3002 -p1
%patch3003 -p1
%patch3006 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1

%patch5000 -p1 -b .utf8

%patch0


%build
export PATH=$PATH:/opt/freeware/bin

# for gtk2 we need this compiler
export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

cd src

export PERL=/usr/bin/perl
export CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"
export LIBPATH="/opt/freeware/lib:/usr/lib:/usr/opt/perl5/lib/5.8.8/aix-thread-multi/CORE"


export vi_cv_path_python_plibs='-L/opt/freeware/lib/python2.7/config -lpython2.7 -ldl -lm -Wl,-bE:/opt/freeware/lib/python2.7/config/python.exp -lld'

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --exec-prefix=%{_prefix} \
    --with-features=huge \
    --enable-pythoninterp \
    --enable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-x=yes \
    --enable-xim \
    --enable-multibyte \
    --enable-gui=gtk2 \
    --enable-gtk2-check \
    --with-compiledby="<bullfreeware@project.bull.net>"

make
cp vim gvim

make clean

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --exec-prefix=%{_prefix} \
    --with-features=huge \
    --enable-pythoninterp \
    --disable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-x=no \
    --enable-gui=no \
    --enable-multibyte \
    --enable-fontset \
    --with-compiledby="<bullfreeware@project.bull.net>"

make
cp vim enhanced-vim

make clean

perl -pi -e "s/help.txt/vi_help.txt/" os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/" os_unix.h

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --exec-prefix=%{_prefix} \
    --with-features=tiny \
    --with-x=no \
    --disable-pythoninterp \
    --disable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-tlib=curses \
    --enable-multibyte \
    --enable-gui=no \
    --disable-gpm \
    --with-compiledby="<bullfreeware@project.bull.net>"

LIBS=" -L/opt/freeware/lib -L/usr/lib" make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export LIBPATH="/opt/freeware/lib:/usr/lib"
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles
cp %{SOURCE14} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles/template.spec
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles/template.spec

cp runtime/doc/uganda.txt LICENSE

# Those aren't GNU info files but some binary files for Amiga:
rm -f README*.info

cd src
make install DESTDIR=${RPM_BUILD_ROOT}

cp gvim enhanced-vim ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# install icons
for i in 16x16 32x32 48x48 64x64 ; do
    mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps
done

cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
cp %{SOURCE8} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
cp %{SOURCE9} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
cp %{SOURCE10} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/64x64/apps/gvim.png

chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/*/apps/gvim.png

(
  cd ${RPM_BUILD_ROOT}
  mv -f .%{_bindir}/vim .%{_bindir}/vi
  mv -f .%{_bindir}/enhanced-vim .%{_bindir}/vim
  ln -sf vi .%{_bindir}/ex
  ln -sf vi .%{_bindir}/rvi
  ln -sf vim .%{_bindir}/vimdiff
  ln -sf gvim .%{_bindir}/gview
  ln -sf gvim .%{_bindir}/gex
  ln -sf gvim .%{_bindir}/evim
  ln -sf gvim .%{_bindir}/gvimdiff
  ln -sf gvim .%{_bindir}/vimx
  ln -sf vimtutor .%{_bindir}/gvimtutor
  ln -sf vim.1 .%{_mandir}/man1/vi.1
  ln -sf vim.1 .%{_mandir}/man1/rvi.1
  mkdir -p ./etc/X11/applnk/Applications
  cp %{SOURCE3} ./etc/X11/applnk/Applications/gvim.desktop
)

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cat >${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x %{_bindir}/id ] || return
  [ \`%{_bindir}/id -u\` -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/vim.csh <<EOF
[ -x %{_bindir}/id ] || exit
[ \`%{_bindir}/id -u\` -gt 200 ] && alias vi vim
EOF
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/vimrc
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/virc
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/vi*rc
(
 mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}/doc
 cd ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}/doc
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
 )
rm -f ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/tools
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~

for i in rvim gvim.1 gvimdiff.1 ; do 
  echo ".so man1/vim.1" > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i
done

cd ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}
cp menu.vim plugin/

# make symlinks
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir -p usr/linux/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .
rm -f ex vi view
cd ../../usr/linux/bin
for f in ex vi view ; do
  ln -sf ../../..%{_bindir}/${f} .
done
%post X11
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi


%postun X11
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files common
%defattr(-,root,system)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{vimdir}
%dir %{_datadir}/%{name}/vimfiles
%{_datadir}/%{name}/vimfiles/template.spec
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
%{_bindir}/xxd
%{_mandir}/man1/vim.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*
%lang(fr) %{_mandir}/fr*/man1/*
%lang(it) %{_mandir}/it*/man1/*
%lang(pl) %{_mandir}/pl*/man1/*
%lang(ru) %{_mandir}/ru*/man1/*
/usr/bin/xxd


%files minimal
%defattr(-,root,system)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview
/usr/linux/bin/ex
/usr/linux/bin/vi
/usr/linux/bin/view
/usr/bin/rvi
/usr/bin/rview


%files enhanced
%defattr(-,root,system)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*
/usr/bin/vim
/usr/bin/rvim
/usr/bin/vimdiff
/usr/bin/vimtutor


%files X11
%defattr(-,root,system)
/etc/X11/applnk/*/gvim.desktop
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_mandir}/man1/gvim*
%{_datadir}/icons/hicolor/*/apps/*
/usr/bin/gvimtutor
/usr/bin/gvim
/usr/bin/gvimdiff
/usr/bin/gview
/usr/bin/gex
/usr/bin/vimx
/usr/bin/evim


%changelog
* Wed Apr 26 2012 Gerard Visiedo <gerard.visiedo@bull.net> 7.3.475-2
- Build on Aix6.1

* Tue Mar 20 2012 Michael Perzl <michael@perzl.org> - 7.3.475-1
- updated to version 7.3 patchlevel 7.3.475

* Sun Nov 20 2011 Michael Perzl <michael@perzl.org> - 7.3.353-1
- updated to version 7.3 patchlevel 7.3.353

* Sun Jun 26 2011 Michael Perzl <michael@perzl.org> - 7.3.237-1
- updated to version 7.3 patchlevel 7.3.237
- fixed perl and python inclusion, thus introduced a dependency on those

* Tue Mar 08 2011 Michael Perzl <michael@perzl.org> - 7.3.138-1
- updated to version 7.3 patchlevel 7.3.138

* Tue Jan 11 2011 Michael Perzl <michael@perzl.org> - 7.3.099-1
- updated to version 7.3 patchlevel 7.3.099

* Mon Dec 13 2010 Michael Perzl <michael@perzl.org> - 7.3.081-1
- updated to version 7.3 patchlevel 7.3.081

* Wed Nov 24 2010 Michael Perzl <michael@perzl.org> - 7.3.069-1
- updated to version 7.3 patchlevel 7.3.069

* Wed Sep 01 2010 Michael Perzl <michael@perzl.org> - 7.2.446-1
- updated to latest patchlevel 7.2.446

* Mon Jul 12 2010 Michael Perzl <michael@perzl.org> - 7.2.444-2
- removed dependency on gettext >= 0.17
- rebuilt with original AIX Linux Toolbox RPM files

* Tue Jun 29 2010 Michael Perzl <michael@perzl.org> - 7.2.444-1
- updated to latest patchlevel 7.2.444

* Thu May 20 2010 Michael Perzl <michael@perzl.org> - 7.2.436-1
- updated to latest patchlevel 7.2.436

* Thu Apr 01 2010 Michael Perzl <michael@perzl.org> - 7.2.411-1
- updated to latest patchlevel 7.2.411

* Mon Feb 22 2010 Michael Perzl <michael@perzl.org> - 7.2.368-1
- updated to latest patchlevel 7.2.368

* Thu Feb 11 2010 Michael Perzl <michael@perzl.org> - 7.2.356-1
- first version for AIX V5.1 and higher
