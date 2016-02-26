// ==UserScript==
// @name           DK9yinjishi_online
// @namespace      http://userscripts.org/dkluffy002
// @include        http://jishi.woniu.com/*
// @include        http://192.168.137.176/*
//  ==/UserScript==

js2 = "http://192.168.93.128:81/angular.min.js";
js3 = "http://192.168.93.128:81/wystock.user.js";

function requrl(url,chkfunc){
  xp=new XMLHttpRequest();
  xp.onreadystatechange = chkfunc;
  xp.open("GET",url,true);
  xp.send();
}

ag = "";
requrl(js2,function(){
	if (this.readyState==4 && this.status==200){
		ag = this.responseText;
		requrl(js3,function(){
			if (this.readyState==4 && this.status==200){
				eval(ag+this.responseText);
			}
		});
	}
});




