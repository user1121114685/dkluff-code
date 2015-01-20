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
  return JSON.parse(json)[0].pageData.sellerGameId;
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
function requrl(url){
  var resp=""
  try
  {
    xp=new XMLHttpRequest();
    xp.open("GET",url,true);
    console.log("Requesting URL...["+url+"]")
    xp.send();
    resp=xp.responseText
    console.log("Requesting URL...resp=["+resp+"]")
  }
  catch(err)
  {
    console.log(err)
    console.log("Requesting URL...Err")
  }
  return resp

}
function getroleskills(id){
  //get uid by id
  //get skill by uid
  //return found target skill texts
  tgskills = ["心佛","五郎","古谱","九宫","鸳鸯" ]
  uidurl="http://jishi.woniu.com/9yin/getTradeItem.html?itemId="+id
  skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId=186100010&type=SkillContainer&roleUid="

  uid=getuid(requrl(uidurl));
  skills=requrl(skillurl+uid);

  return matchArr(tgskills,skills)
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
      skillstr=getroleskills(id)
      addskilltext(a,skillstr)
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
addGlobalStyle('.controllbar{position:absolute;right:10%;top:5%;}');

document.getElementById('btshow_all').addEventListener('click',function(){runview();},false);


