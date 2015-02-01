// ==UserScript==
// @name           DK9yinjishi
// @namespace      http://userscripts.org/dkluffy002
// @include        http://jishi.woniu.com/*
// ==/UserScript==

function addGlobalStyle(css) {
  var head, style;
  head = document.getElementsByTagName('head')[0];
  if (!head) { return; }
  style = document.createElement('style');
  style.type = 'text/css';
  style.innerHTML = css;
  head.appendChild(style);
}

function getroleid(str){
  console.log(str)
  return str.split("=")[2];
}

function getuid(json){
  try
  {
    return JSON.parse(json)[0].pageData.sellerGameId;
  }
  catch(err)
  {
    console.log(err)
  }
}

function matchArr(tg,txt){
  var fd="";
  for(i=0;i<tg.length;i++){
    if (txt.match(tg[i]))
    {
      fd+=tg[i]+" ";
    }
  }
  console.log(fd)
  return fd

}
function requrl(url,chkfunc){
  xp=new XMLHttpRequest();
  xp.onreadystatechange = chkfunc;
  xp.open("GET",url,true);
  xp.send();
}
function procRole(id,item){
  //var tgskills = ["心佛","五郎八卦","古谱","九宫剑法","鸳鸯双刀","虬枝","金蛇剑法","玲珑骰" ]
  var skills="";
  var resp="";
  uidurl="http://jishi.woniu.com/9yin/getTradeItem.html?itemId="+id;
  skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=SkillContainer&roleUid=";
  requrl(uidurl,function (){
    if (this.readyState==4 && this.status==200){
	  uid=getuid(this.responseText);
	  requrl(skillurl+uid,function (){
	    if (this.readyState==4 && this.status==200){
		  skills=matchArr(tgskills,this.responseText);
		  addskilltext(item,skills);
		}
	   }
	  );
	}
  }
  );
}
function old_funcprocrole(id,item){
  //////var tgskills = ["心佛","五郎","古谱","九宫","鸳鸯","虬枝","金蛇","玲珑" ]
  var skills="";
  var resp="";
  uidurl="http://jishi.woniu.com/9yin/getTradeItem.html?itemId="+id;
  skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId=186100010&type=SkillContainer&roleUid=";
  requrl(uidurl,function (){
    if (xp.readyState==4 && xp.status==200){
          uid=getuid(xp.responseText);
          requrl(skillurl+uid,function (){
            if (xp.readyState==4 && xp.status==200){
                  skills=matchArr(tgskills,xp.responseText);
                  addskilltext(item,skills);
                }
           }
          );
        }
  }
  );
}

function addskilltext(item,str){
  var elBtdiv = document.createElement('p');
  elBtdiv.innerHTML=str
  item.appendChild(elBtdiv);
}

function matchrolelist(txt){
  if(localStorage.okrolelist.match(txt)){
    return "okrolename";
  }
  if(localStorage.ngrolelist.match(txt)){
    return "ngrolename";
  }
  return "unrolename";
}
function updatelist(elm,txt,rolelist,okng){
  if(rolelist.match(txt)){
    rolelist=rolelist.replace(eval("/"+txt+"/g"),"")
  }else{
    rolelist+=txt
  }
  
  if(okng){
    localStorage.okrolelist = rolelist;
  }else{
    localStorage.ngrolelist = rolelist;
  }
  elm.id=matchrolelist(txt)
  console.log(localStorage.ngrolelist+" NG");
  console.log(localStorage.okrolelist+" OK");
}


function markrole(){
  var titdivs = document.getElementsByClassName('tit')
  for(i=0;i<titdivs.length;i++){
    marktitdiv(titdivs[i],getrolename(titdivs[i]));
  }

}
function getrolename(elm){
  if(elm.getAttribute('rolename')){
    return elm.getAttribute('rolename')
  }
  return elm.innerHTML
}

function marktitdiv(elm,txt){
  var elmdiv = document.createElement('div')
  elm.setAttribute("rolename",txt)
  //elm.className=matchrolelist(txt)
  elm.id=matchrolelist(txt)
  
  elmdiv.innerHTML+=txt+"<a id='mark_ngp' class='mark_ng' href=\"javascript:void();\">[  NG  ]</a>" +
           "<a id='mark_ok' class='mark_ok' href=\"javascript:void();\">[  OK  ]</a>"
  
  elm.innerHTML=""
  elm.appendChild(elmdiv)
  elm.getElementsByClassName('mark_ng')[0].addEventListener('click',function(){updatelist(elm,txt,localStorage.ngrolelist,false);},false)
  elm.getElementsByClassName('mark_ok')[0].addEventListener('click',function(){updatelist(elm,txt,localStorage.okrolelist,true);},false)
   
}


function runview(){
  markrole();
  tb=document.getElementById("findSellingGoods")
  tblist=document.getElementById("findNoticeGoods")
  serverName=getCookie("serverName")
  tgskills=getSkills()

  
  if(tblist){
    tb=tblist
  }
  
  tbli=tb.getElementsByTagName("li")
  for(i=0;i<tbli.length;i++){
    try{
      a=tbli[i].getElementsByClassName("pic")[0]
      id=getroleid(a.href)
      procRole(id,a)
    }
    catch(err){
      console.log(err)
    }
  }
}

function getSkills(){
  //var skills=document.getElementById('wantedskills').value.split(",")
  var skills = localStorage.wantedskills.split(",")
  console.log("Wanted skills: "+skills)
  return skills
}

function updateskills(){
  localStorage.wantedskills = document.getElementById('wantedskills').value
  console.log("Update successsfully...:"+localStorage.wantedskills)
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}

var elmBtdiv = document.createElement('div');
elmBtdiv.className="controllbar";
elmBtdiv.innerHTML="<a id='btshow_all' href=\"javascript:void();\">[Show All]</a>"+
                   "<a id='btupdate' href=\"javascript:void();\">[Save/Update]</a>"+
                    "</br><textarea id='wantedskills' rows='1' cols='40'></textarea>"

document.body.appendChild(elmBtdiv);

if (localStorage.wantedskills){
  document.getElementById("wantedskills").value = localStorage.wantedskills
} else {
  localStorage.wantedskills = "神风诀,心佛,五郎八卦,古谱,九宫剑法,鸳鸯双刀,虬枝,金蛇剑法,玲珑骰,修罗刀"
  localStorage.ngrolelist = ""
  localStorage.okrolelist = ""
}
if(!localStorage.ngrolelist){
  localStorage.ngrolelist=""
}
if(!localStorage.okrolelist){
  localStorage.okrolelist=""
}

addGlobalStyle('.controllbar{position:absolute;right:10%;top:30%;}');
addGlobalStyle('#ngrolename{background:gray;}');
addGlobalStyle('#okrolename{background:green;}');

document.getElementById('btshow_all').addEventListener('click',function(){runview();},false);
document.getElementById('btupdate').addEventListener('click',function(){updateskills();},false);



