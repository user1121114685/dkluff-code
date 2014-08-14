CSS = """
body
{
    margin:auto;
    padding:0;
    width:960px;
}
#custabx
{
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:100%;
    border-collapse:collapse;

}
td,tr,th
{
    font-size:1em;
    border:1px solid #98bf21;
    padding:3px 7px 2px 7px;
}
#custab1
{
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:100%;
    border-collapse:collapse;
    background-color:#EAF2D3;
}
#custab3
{
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:100%;
    border-collapse:collapse;
    background-color:#EAF2D3;
}

#navhead
{
     font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
     font-size:1em;
}
"""

HTML = """

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<style type="text/css">
{_style}
</style>
<title>Orion NPM Weekly REPORT [{_titletime}]</title>
</head>
<body>
{_tabs}
<br>
<br>
<br>
</body>
</html>
"""
lactabs="""
<div id="navhead">{_navhead}</div>
<pre id="{_lacid}">1.[{_titlelocation}]Network Latency({_titlelocation} <-->ASH):</pre>
<table id="custab3">
          <tr>
            <th>Location</th>
            <th>Average Response Time</th>
            <th>Peak Response Time</th>
            <th>Percent Packet Loss</th>
            <th>Total Device</th>
         </tr>
         {_lagtab}
</table>

<pre>2.[{_titlelocation}]Internet Transmission Performance</pre>
<table id="custab3">
          <tr>
            <th>Node Name</th>
            <th colspan="2">Average/Peak Receive bps</th>
            <th colspan="2">Average/Peak Transmit bps</th>
            <th>Average  Recv+Xmit bps</th>
            <th>Total Bytes Recv+Xmit</th>
         </tr>
         {_fwtab}
</table>

<pre>3.[{_titlelocation}]CPU and Memory Load</pre>
<table id="custab3">
<caption>Average CPU Load exceed 50%</caption>
          <tr>
            <th>Node Name</th>
            <th>Peak CPU Load</th>
            <th colspan="2">Average CPU Load</th>
         </tr>
         {_cputab}
</table>
<br>
<table id="custab3">
<caption>Average Memory Load exceed 50%</caption>
          <tr>
            <th>Node Name</th>
            <th>Peak Memory Load</th>
            <th colspan="2">Average Percent Memory Used</th>
         </tr>
         {_memtab}
</table>
<br>
<br>
<br>
"""
