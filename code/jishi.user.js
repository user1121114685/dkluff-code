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
  var tgskills = ["心佛","五郎八卦","古谱","九宫剑法","鸳鸯双刀","虬枝","金蛇剑法","玲珑骰" ]
  var skills="";
  var resp="";
  uidurl="http://jishi.woniu.com/9yin/getTradeItem.html?itemId="+id;
  skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId=186100010&type=SkillContainer&roleUid=";
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
function old_procRole(id,item){
  var tgskills = ["心佛","五郎","古谱","九宫","鸳鸯","虬枝","金蛇","玲珑" ]
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

function runview(){
  tb=document.getElementById("findSellingGoods")
  tblist=document.getElementById("findNoticeGoods")
  
  if(tblist){
    tb=tblist
  }
  
  tbli=tb.getElementsByTagName("li")
  for(i=0;i<tbli.length;i++){
    try{
      a=tbli[i].getElementsByTagName("a")[0]
      id=getroleid(a.href)
      procRole(id,a)
    }
    catch(err){
      console.log(err)
    }
  }
}

var elmBtdiv = document.createElement('div');
elmBtdiv.className="controllbar";
elmBtdiv.innerHTML="<a id='btshow_all' href=\"javascript:void();\">[Show All]</a>"

document.body.appendChild(elmBtdiv);
addGlobalStyle('.controllbar{position:absolute;right:10%;top:50%;}');

document.getElementById('btshow_all').addEventListener('click',function(){runview();},false);



