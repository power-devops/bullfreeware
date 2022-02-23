<!-- Copyright (C) Bull SAS - 2019 -->
<!DOCTYPE html>
<html lang="en">
<head>
	<title>Bull Freeware</title>
	<meta charset="utf-8"/>

	<!-- Meta tags -->
	<meta name="description" content="Here you can download all the packages that Bull-Atos has compiled for different versions of AIX"/>
	<meta name="keywords" content="Bull, bullfreeware, AIX, aixtoolbox, aix toolbox, bull freeware, atos, ibm, atos technologies, bull atos technologies, rpm, packages"/>

	<!-- Icon and viewport -->
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<LINK REL="SHORTCUT ICON" HREF="/images/monicone.ico"/>

	<!-- Fonts -->
	<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,700%7CRoboto+Slab:300,400,700&display=swap&subset=latin-ext" rel="stylesheet"/>
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.9.0/css/all.css" integrity="sha384-i1LQnF23gykqWXg6jxC2ZbCbUMxyw5gLZY6UiUS98LYV5unm8GWmfkIS6jqJfb4E" crossorigin="anonymous"/>

	<!-- CSS -->
	<link rel="stylesheet" type="text/css" href="/style/main.css" />
	<link rel="stylesheet" type="text/css" href="/style/forms.css" />
	<link rel="stylesheet" type="text/css" href="/style/pages.css" />

	<!-- Compatibility polifills -->
	<!--[if gte IE 10]><!-->
		<script src="https://cdnjs.cloudflare.com/ajax/libs/prefixfree/1.0.7/prefixfree.min.js" charset="utf-8" defer></script>
		<script src="https://cdn.polyfill.io/v2/polyfill.min.js" defer></script>
	<!--<![endif]-->

	
	<!-- JS -->
	<script type="text/javascript">var captcha_on = "1";</script>
	<script src="/scripts/js/search.js" defer></script>

	<!-- External JS scripts -->
	<script src="https://www.google.com/recaptcha/api.js?render=6LcEgakUAAAAAArCghOT0YRj-eLtt0cM9VP8TXo1&hl=en" defer></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>
<header>
	<a href="/">
		<img src="/images/Atos.svg" alt="Bull Atos Technologies">
		<h1>AIX Open Source Archives</h1>
	</a>
    <a href="/">
        <h2>This website will be closed on March 01, 2022 (check News tab) </h2>
    </a>

</header>
<div class="absoluteNav">
	<nav>
		<ul>
			<li >
				<a href="/">
					<i class="fas fa-home"></i><span>Home</span>
				</a>
			</li>
			<li >
				<a href="/newsPage">
					<i class="fas fa-newspaper"></i><span>News</span>
					<span class="fas fa-exclamation-circle"></i>
				</a>
			</li>
			<li >
				<a href="/last">
					<i class="fas fa-history"></i><span>Latests</span>
				</a>
			</li>
			<li >
				<a href="/howto">
					<i class="fas fa-question-circle"></i><span>How to use</span>
				</a>
			</li>
			<li >
				<a href="/contact">
					<i class="fas fa-envelope"></i><span>Contact</span>
				</a>
			</li>
			<!-- <li >
				<a href="/stats">
					<i class="fas fa-chart-bar"></i><span>Statistics</span>
				</a>
			</li> -->
			<!-- <li>
				<a href="/">
					<i class="fas fa-folder-open"></i><span>SRPM</span>
				</a>
			</li> -->
			<li >
				<a href="/tos">
					<i class="fas fa-scroll"></i><span>Policy</span>
				</a>
			</li>
		</ul>
	</nav>
</div>
<div class="absoluteSearch">
	<section class="search">
		<form id="search" action="" method="post">
			<div class="searchBar">
				<input type="search" name="package" id="searchPkg" placeholder="Search for a package" required>
				<button type="submit" name="validate" id="validate">
					<i class='fas fa-search'></i>
				</button>
			</div>
			<div class="options" style="display: none;">
				<div class="date">
					<span class="label">From</span>
					<input type="date" name="from" id="fromPkg">
					<span type="" name="fromPkgIcon" id="fromPkgIcon">
						<i class="fas fa-calendar-alt"></i>
					</span>
				</div>
				<div class="date">
					<span class="label">To</span>
					<input type="date" name="to" id="toPkg">
					<span type="" name="toPkgIcon" id="toPkgIcon">
						<i class="fas fa-calendar-alt"></i>
					</span>
				</div>
				<div class="checkbox">
					<label>
						<span class="label">Libraries</span>
						<input type="checkbox" id="libraries" name="libraries">
						<span class="checkboxInput"></span>
					</label>
				</div>
				<div class="checkbox">
					<label>
						<span class="label">Exact version</span>
						<input type="checkbox" name="exact" id="exact">
						<span class="checkboxInput"></span>
					</label>
				</div>
			</div>
			<div class="slider" style="display: none;">
				<span class="label">AIX Version</span>
				<div class="sliderBar">
					<input id="version" name="versionBar" type="range" min="0" max="5" value="5">
					<div class="versions">
						<div class='version'>5.1</div>
<div class='version'>5.2</div>
<div class='version'>5.3</div>
<div class='version'>6.1</div>
<div class='version'>7.1</div>
<div class='version'>7.2</div>
					</div>
				</div>
			</div>
		</form>
	</section>
</div>
<section class="pkgs"></section>
<!--[if IE]>
<section id="IEShield">
	<div class="content warning">
		<div class="header">
			<h3>Internet Explorer users</h3>
		</div>
		<div class="body">
			<p>
				<i class="fab fa-js-square"></i>&nbsp;&nbsp;&nbsp;&nbsp;Your browser does not support recent norms (ES5) of JavaScript !<br>
				<i class="fas fa-robot"></i>&nbsp;&nbsp;&nbsp;As this site is protected against bots, JavaScript is needed to send forms (search, mails, ...)<br>
				<i class="fas fa-folder-open"></i>&nbsp;&nbsp;&nbsp;You still can go <a href="/packages"><b>HERE</b></a> to download RPMS.<br>
				<i class="fab fa-firefox"></i>&nbsp;&nbsp;&nbsp;&nbsp;You may consider downloading Firefox <a href="https://www.mozilla.org/en-US/firefox/new/"><b>HERE</b></a>
			</p>
		</div>
	</div>
</section>
<![endif]-->
<noscript>
	<section>
		<div class="content warning">
			<div class="header">
				<h3>No JavaScript</h3>
			</div>
			<div class="body">
				<p>
					<i class="fab fa-js-square"></i>&nbsp;&nbsp;&nbsp;&nbsp;Your browser does not support JavaScript !<br>
					<i class="fas fa-robot"></i>&nbsp;&nbsp;&nbsp;As this site is protected against bots, JavaScript is needed to send forms (search, mails, ...)<br>
					<i class="fas fa-folder-open"></i>&nbsp;&nbsp;&nbsp;You still can go <a href="/packages"><b>HERE</b></a> to download RPMS.<br>
				</p>
			</div>
		</div>
	</section>
</noscript>

<script defer>
$(document).ready(function() {
	if (navigator.userAgent.match(/msie|trident/i) !== null) {
		$('#IEShield').remove();
		$('noscript').before(
'<section id="IEShield">' +
'	<div class="content warning">' +
'		<div class="header">' +
'			<h3>Internet Explorer users</h3>' +
'		</div>' +
'		<div class="body">' +
'			<p>' +
'				<i class="fab fa-js-square"></i>&nbsp;&nbsp;&nbsp;&nbsp;Your browser does not support recent norms (ES5) of JavaScript !<br>' +
'				<i class="fas fa-robot"></i>&nbsp;&nbsp;&nbsp;As this site is protected against bots, JavaScript is needed to send forms (search, mails, ...)<br>' +
'				<i class="fas fa-folder-open"></i>&nbsp;&nbsp;&nbsp;You still can go <a href="/packages"><b>HERE</b></a> to download RPMS.<br>' +
'				<i class="fab fa-firefox"></i>&nbsp;&nbsp;&nbsp;&nbsp;You may consider downloading Firefox <a href="https://www.mozilla.org/en-US/firefox/new/"><b>HERE</b></a>' +
'			</p>' +
'		</div>' +
'	</div>' +
'</section>');
		}
	});
</script>


<section id="notfound">
	<div class="content warning">
		<div class="header">
			<h3>404 Not Found</h3>
		</div>
		<div class="body">
			<p>
				Whoops, sorry, but the document you requested was not found on this server (/packages/SPECS//apr-util-1.3.9-3.spec)<br>
				If your problem persist, send us a mail <a href="/contact">here</a>.
			</p>
		</div>
	</div>
</section>
</body>
</html>
