// ==UserScript==
// @name           heherobot
// @namespace      http://userscripts.org/dkluffy00robot1
// @include        http://jxjycw.dongao.com/*
//  ==/UserScript==

function dkrobot(){
  var a=$("#pointDiv[style$='block;']");
  if(a.length >0 ){
    a=$("#questionAnswer").attr("value")
    s=":radio[value='"+a+"']"
    $(s).click()
    savePointAnswer()
    console.log("window showed:"+s);

  }else{
    console.log("none found... from extention v1");
  }


}

var robotloop=setInterval(dkrobot,1000);
//robotloop=window.clearInterval(robotloop);


