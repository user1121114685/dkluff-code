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

HTML="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<style type="text/css">
    {_style}
</style>
<title>{_titlelocation} WEEKLY BLUECOAT REPORT [{_titletime}]</title>
</head>
<body>
<div id="sum">
<p>{_titlelocation} Weekly Usage:</p>
<pre>
[Total      Bytes]: {_totalBytes}(Intercepted)
  --VPN      Bytes: {_VPNBytes}{_VPNBytes_bar}
  --Internet Bytes: {_NonVPNBytes}{_NonVPNBytes_bar}

[Cached   Bytes]: {_totalBytes_cache}{_totalBytes_cache_bar}
[UnCached Bytes]: {_totalBytes_uncache}{_totalBytes_uncache_bar}

[Total Requests]: {_totalRequests}
  --PolicyDenied: {_totalDrequests}
</pre>
</div>
<!-- Daily Usage -->
<br><br><table id="custab1">
          <caption>Daily Usage</caption>
          <tr>
            <th>Date</th>
            <th>Requests</th>
            <th colspan="2">Bytes</th>
         </tr>
         {_daytab}
</table>



<!-- VPN Usage -->
<div id="navhead">
            <br><br><big id="vpn">Section of VPN:</big>
            <a href="#vpn">VPN</a>   <a href="#nonvpn">Internet</a>
</div>

<br><br><table id="custab1">
          <caption>VPN - Top 10 Hosts By BytesUnCached</caption>
          <tr>
            <th>Host</th>
            <th>Requests</th>
            <th>BytesCached</th>
            <th colspan="2">BytesUnCached</th>
            <!--[BytesUnCached] [BytesUnCached/TotalBytes]-->
         </tr>
         {_vpn_toptab}
</table>

<br><br><table id="custab1">
          <caption>VPN - Protocol Details</caption>
          <tr>
            <th>Protocol</th>
            <th>Requests</th>
            <th>BytesCached</th>
            <th>BytesUnCached</th>
            <th colspan="2">Total Protocol Bytes</th>
            <!--[BytesUnCached] [BytesUnCached/TotalBytes]-->
         </tr>
         {_vpn_protab}
</table>

<div id="navhead">
            <br><br><big id="nonvpn">Section of Internet:</big>
            <a href="#vpn">VPN</a>   <a href="#nonvpn">Internet</a>
</div>
<br><br><table id="custab1">
          <caption>Internet - Top 10 Hosts By BytesUnCached</caption>
          <tr>
            <th>Host</th>
            <th>Requests</th>
            <th>BytesCached</th>
            <th colspan="2">BytesUnCached</th>
            <!--[BytesUnCached] [BytesUnCached/TotalBytes]-->
         </tr>
         {_nonvpn_toptab}
</table>
<br><br><table id="custab1">
          <caption>Internet - Protocol Details</caption>
          <tr>
            <th>Protocol</th>
            <th>Requests</th>
            <th>BytesCached</th>
            <th>BytesUnCached</th>
            <th colspan="2">Total Protocol Bytes</th>
            <!--[BytesUnCached] [BytesUnCached/TotalBytes]-->
         </tr>
         {_nonvpn_protab}
</table>

<br><br><table id="custab1">
          <caption>Internet - Top 10 Hosts By Requests</caption>
          <tr>
            <th>Host</th>
            <th>BytesCached</th>
            <th>BytesUnCached</th>
            <th colspan="2">Requests</th>
            <!--[BytesUnCached] [BytesUnCached/TotalBytes]-->
         </tr>
         {_nonvpn_reqtab}
</table>

<br><br><table id="custab1">
          <caption>Internet - Top 10 Hosts By Denied Requests</caption>
          <tr>
            <th>Host</th>
            <th>Request</th>
            <th colspan="2">Involved Clients</th>
         </tr>
         {_nonvpn_dreqtab}
</table>
<br>
<br>
<br>
</body>
</html>
"""
