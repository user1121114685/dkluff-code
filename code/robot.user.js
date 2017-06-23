// ==UserScript==
// @name           heherobot
// @namespace      http://userscripts.org/dkluffy00robot1
// @include        http://jxjycw.dongao.com/*
//  ==/UserScript==

function dkrobot(){
  var a=$("#pointDiv[style$='block;']");
  if(a.length >0 ){
    a=$("#questionAnswer").attr("value")
    if(a.length == 1){
      var s=":radio[value='"+a+"']";
      $(s).click();
    }else{
      for(var i in a){
        $(":checkbox[value='"+a[i]+"']")[0].checked=true;
      }
    }

    savePointAnswer();
    console.log("window showed:"+s);

  }else{
    console.log("none found... from extention v1");
  }


}

var robotloop=setInterval(dkrobot,1000);
//robotloop=window.clearInterval(robotloop);


