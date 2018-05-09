// ==UserScript==
// @match http://www.wzjxjy.cn/*
// ==/UserScript==

function mrobot(){
    console.log("cheating...");
    var checkCode = document.getElementById("checkCode").innerHTML;
    if(checkCode != "" ) {
        document.getElementById("inputCode").value=checkCode;
        validateCode();
        document.getElementById("checkCode").innerHTML="";
        console.log(checkCode);
        checkCode="";
    }
}

var robotloop=setInterval(mrobot,1000);