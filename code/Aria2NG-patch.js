<div class="input-group"><input  type="text" class="form-control" placeholder="0 minutes" id="mintodown" aria-label="0 minus" value="0"/><button class="btn btn-default" onClick="mintodown()"><span translate>Shutdown Aria2 after Delay</span></button><script>function mintodown(){ setTimeout("document.getElementById(\'bt-clk\').click()",parseInt(document.getElementById("mintodown").value)*1000) }</script></div>

//todo
delimate confirmation button