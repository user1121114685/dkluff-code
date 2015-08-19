// ==UserScript==
// @name           DK9yinjishi
// @namespace      http://userscripts.org/dkluffy002
// @include        http://jishi.woniu.com/9yin/index.html
// @include        http://192.168.137.176/*
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
  var equarr = ["阴柔属性","太极属性","阳刚属性"]

  var uidurl="http://jishi.woniu.com/9yin/getTradeItem.html?itemId="+id;
  var skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=SkillContainer&roleUid=";
  var jmurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=JingMaiContainer"+"&roleUid=";
  var equurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=EquipBox"+"&roleUid=";

  requrl(uidurl,function (){
    if (this.readyState==4 && this.status==200){
	  uid=getuid(this.responseText);
	  
	  //equipment
	  requrl(equurl+uid,function (){
	    if (this.readyState==4 && this.status==200){
		  var equ=matchArr(equarr,this.responseText);
		  addskilltext(item,equ);
		}
	   }
	  );
	  
	  //skills
	  requrl(skillurl+uid,function (){
	    if (this.readyState==4 && this.status==200){
		  var skills=matchArr(tgskills,this.responseText);
		  addskilltext(item,skills);
		}
	   }
	  );
	  
	  //jinmai
	  requrl(jmurl+uid,function (){
	    if (this.readyState==4 && this.status==200){
		  var jm=fixjmtext(this.responseText);
		  addjmtext(item,jm);
		}
	   }
	  );
	  
	  
	  
	}
  }
  );
}
function fixjmtext(str){
  var p=str.match(/[0-9]*周天/g).sort()
  var jmgood= [];
  for(i=0;i<p.length;i++){
	if(parseInt(p[i])>108){
	  jmgood.push(p[i])
	}
  }
  return "GOOD "+jmgood.length+" :"+jmgood.join()
	
}
function fixjmtextj(str){
  var p=str.match(/[0-9]*周天/g).sort()
  var jmgood= [];
  for(i=0;i<p.length;i++){
	if(parseInt(p[i])>144){
	  jmgood.push(p[i])
	}
  }
  return [jmgood.length,jmgood.join()]
	
}

function addskilltext(item,str){
  var elBtdiv = document.createElement('p');
  elBtdiv.innerHTML=str
  item.appendChild(elBtdiv);
}

function addjmtext(item,str){
  //item.getElementsByClassName('goods_tips_desc')[0].value="<div class='reolesDesc'>"+str+"</div>"
  s=item.getElementsByClassName('goods_tips_desc')[0].value
  item.getElementsByClassName('goods_tips_desc')[0].value=s.replace("</div>","")+str+"</div>"
}

function matchrolelist(txt){
  txt=escape(txt)
  if(escape(localStorage.ngrolelist).match(txt)){
    return "ngrolename";
  }
  if(escape(localStorage.exprolelist).match(txt)){
    return "exprolename";
  }
  if(escape(localStorage.okrolelist).match(txt)){
    return "okrolename";
  }
  
  return "unrolename";
}
function updatelist(elm,txt,rolelist,okng){
  etxt=escape(txt);
  rolelist=escape(rolelist);
  if(rolelist.match(etxt)){
    rolelist=rolelist.replace(eval("/"+etxt+"/g"),"")
  }else{
    rolelist+=etxt
  }
  
  if(okng == 2){
    localStorage.okrolelist = unescape(rolelist);
  }
  if(okng ==1){
    localStorage.exprolelist = unescape(rolelist);
  }
  if(okng ==0){
    localStorage.ngrolelist = unescape(rolelist);
  }
  elm.id=matchrolelist(txt)
  console.log(localStorage.ngrolelist+" NG");
  console.log(localStorage.okrolelist+" OK");
  console.log(localStorage.exprolelist+" EXPENSIVE");

}


function markrolej(){
  var titdivs = document.getElementsByClassName('titjj')
  for(i=0;i<titdivs.length;i++){
    marktitdiv(titdivs[i],getrolename(titdivs[i]));
  }

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
  //--elm.className=matchrolelist(txt)
  elm.id=matchrolelist(txt)
  
  elmdiv.innerHTML+=txt+"<a id='mark_ng' class='mark_ng' href=\"javascript:void();\">[NG]</a>" + "-"+
 		    "<a id='mark_ok' class='mark_ok' href=\"javascript:void();\">[OK]</a>"+ "-"+
		                "<a id='mark_exp' class='mark_exp' href=\"javascript:void();\">[EXPENSIVE]</a>"

  
  elm.innerHTML=""
  elm.appendChild(elmdiv)
  elm.getElementsByClassName('mark_ok')[0].addEventListener('click',function(){updatelist(elm,txt,localStorage.okrolelist,2);},false)
  elm.getElementsByClassName('mark_exp')[0].addEventListener('click',function(){updatelist(elm,txt,localStorage.exprolelist,1);},false)
  elm.getElementsByClassName('mark_ng')[0].addEventListener('click',function(){updatelist(elm,txt,localStorage.ngrolelist,0);},false)


   
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
  var skills = localStorage.wantedskills.split(" ")
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
  localStorage.wantedskills = "神风诀 心佛 五郎八 古谱 九宫剑 鸳鸯双 虬枝 金蛇剑 玲珑骰 修罗刀 辟邪 神行无 雪斋"
}
if(!localStorage.ngrolelist){
  localStorage.ngrolelist=""
}
if(!localStorage.okrolelist){
  localStorage.okrolelist=""
}
if(!localStorage.exprolelist){
  localStorage.exprolelist=""
}

addGlobalStyle('.controllbar{position:absolute;right:10%;top:30%;z-index:200;}');
addGlobalStyle('#ngrolename{background:gray;}');
addGlobalStyle('#okrolename{background:green;}');
addGlobalStyle('#exprolename{background:red;}');
addGlobalStyle('a.pic img {opacity:0.4;width: 90px;height: 70px;border: 1px solid #fff;float: left;background: url("img/tipsImg.png") no-repeat 0 0;}');

document.getElementById('btshow_all').addEventListener('click',function(){runview();},false);
document.getElementById('btupdate').addEventListener('click',function(){updateskills();},false);




var elmBtdiv3 = document.createElement('div');
elmBtdiv3.className="controllbar2";
elmBtdiv3.innerHTML="<a  href='#angtable1'>[GoTO Ang Table]</a>";
document.body.appendChild(elmBtdiv3);
addGlobalStyle('.controllbar2{position:absolute;right:10%;top:20%;}');

//start table
var elmBtdiv2 = document.createElement('div');
elmBtdiv2.id="angtable1";
elmBtdiv2.innerHTML="<div ng-app='apptb1' ng-controller='ctr1'>"+
                    "<a  href='#btshow_all'>[GoTO Top]</a>  "+
                    "<button id='angtable' ng-click='fetchdata()'>[Refresh]</button>"+
                    "- - - <button  ng-click='ptable()'>[PaintTable]</button>"+
                    "<h3><input type='checkbox' ng-model='iformodel' >OrModel </h3>"+
                    "<br>start loop<br><div>"+

                    "<label ng-repeat='w in wantedskills'>"+
                    "<input type='checkbox' ng-click='chkboxf(w)' >{{ w }}"+
                    "</label><br>--------------------------------------<br>"+

                    "<label ng-repeat='w in chktxt'>"+
                    "<input type='checkbox' ng-click='chkboxf(w)' >{{ w }}"+
                    "</label><br>--------------------------------------<br>"+

                    "Checkbox_txt:<input type='text' ng-model='q_txt'/> - "+
                    " -- Any:<input type='text' ng-model='q_comtxt.$'/> - "+

                    "Price:<input type='number' ng-model='q_price1'/> - "+
                    "<input type='number' ng-model='q_price2'/><br>"+

                    "JM: <input type='number' ng-model='q_jmlen'/><br>"+

                    "Table:<br><table id='maintable'>"+
          "<tr ng-repeat='xxx in ctslocal | filter:uifilter1 | filter:uifilter2 | filter:q_comtxt | orderBy:tborder ' >"+
                    "<td class='titjj' rolename='{{ xxx.itemName }}'>{{ xxx.itemName }}</td>"+
    "<td id='{{xxx.rolemark}}'>[{{$index+1}}]<a href='{{roleurl+xxx.id}}' target='_blank'>{{ xxx.itemName }}</a></td>"+
                    "<td>- {{ xxx.equtext }}</td>"+
                    "<td>{{ xxx.gender }}<br></td>"+
                    "<td>{{ xxx.gradeName }}</td>"+
                    "<td>{{ xxx.price }}</td>"+
                    "<td>{{ xxx.guild }}</td>"+
                    "<td id='{{ xxx.rolemark }}'>{{ xxx.skilltext }}</td>"+
                    "<td>{{ xxx.jmtext }}</td>"+
                    "<td>{{ xxx.jmtext.split(',')[0] }}</td>"+
                    "<td id='{{ xxx.rolemark }}'>{{ xxx.rolemark }}</td>"+
           "</tr>"+
                    "</table>"+
                    "</div><br>end loop"+
                    " </div><br><br><br><br><br>";
document.body.appendChild(elmBtdiv2);
addGlobalStyle('#angtable1{background:whitesmoke;position:absolute;left:10%;width:100%}');
addGlobalStyle('#maintable{border: 1px solid black;left:10%;}');
addGlobalStyle('tr,td {border: 1px solid black;}');

var app = angular.module("apptb1", []);
app.controller("ctr1", function($scope,$http) {

  $scope.cts = [];
  $scope.ctslocal = [];
  $scope.url_all = [];
  $scope.url_all[0] = "http://jishi.woniu.com/9yin/findSellingGoods.html?filterItem=4&pageIndex=";
  $scope.url_all[1] = "http://jishi.woniu.com/9yin/findNoticeGoods.html?pageIndex="

  //start main http
  var serverName=getCookie("serverName");
  $scope.mainhttp = function (url) {
    $http.get(url+1).success(function(data, status, headers, config){
      var ttpage = data[0].pageInfo.totalPages
      $scope.additemobj(data[0].pageData);
      for(var i = ttpage;i>1;i--){
        $http.get(url+i).success(function(data, status, headers, config){
         $scope.additemobj(data[0].pageData);
        });
      }
    });
  }

  $scope.fetchdata  = function (){
    $scope.cts = [];
    for(var i in $scope.url_all){
      $scope.mainhttp($scope.url_all[i]);
    }

  }
  //$scope.fetchdata();
  //end main http

  $scope.roleurl = "http://jishi.woniu.com/9yin/tradeItemDetail.html?catagory=2&itemId=";

  $scope.skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=SkillContainer&roleUid=";
  $scope.jmurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=JingMaiContainer"+"&roleUid=";
  $scope.equurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=EquipBox"+"&roleUid=";
  $scope.additemobj = function (p){
    for(var i in p){
      p[i]["skilltext"] = "";
      p[i]["equtext"] = "";
      p[i]["jmtext"] = "";

      $scope.getroledata(p[i],"skilltext",$scope.skillurl+p[i].sellerGameId,$scope.wantedskills);
      $scope.getroledata(p[i],"equtext",$scope.equurl+p[i].sellerGameId,$scope.chktxt);
      $scope.getroledata(p[i],"jmtext",$scope.jmurl+p[i].sellerGameId,"");
      p[i]["rolemark"] = $scope.matchrolej(p[i].itemName);
      $scope.cts.push(p[i]);
    }
  }
  $scope.getroledata = function (p,key,url,mtg){
    $http.get(url).success(function(data, status, headers, config){
        txt = data[0].msg;
        if(key == "skilltext" || key == "equtext"){
          txt = matchArr(mtg,txt);
        }
        if(key == "jmtext"){
          txt = fixjmtextj(txt).toString();
        }
        p[key] = txt;
    });
  }


  //init
  $scope.tborder = "price";
  $scope.chktxts = "";
  $scope.chktxts += "阴柔 太极 阳刚";
  $scope.chktxts += " 男 女";
  $scope.chktxts += " exprolename ngrolename okrolename unrolename";
  $scope.chktxt = $scope.chktxts.split(" ");
  $scope.wantedskills = localStorage.wantedskills.split(" ");

  $scope.q_txt = "";
  $scope.skb = {};
  $scope.q_price1 = 0;
  $scope.q_price2 = 1000;
  $scope.q_jmlen = 1;
  $scope.iformodel = true;

  $scope.uifilter1 = function (i){
    t=$scope.q_txt;
    i.rolemark = $scope.matchrolej(i.itemName);
    p=i.skilltext+" "+i.gender+" "+i.equtext+" "+i.rolemark;
    if(t.length == 0 && i.rolemark.match("ngrolename")){return false;}
    if(t.length == 0 && !i.rolemark.match("ngrolename")){return true;}

    t=t.split(" ");
    if(!$scope.iformodel){
      for(var ti in t){
        if(!p.match(t[ti])){return false;}
      }
      return true;
    }
    if(matchArr(t,p).trim()){
      return true;
    }
    return false;
  }

  $scope.uifilter2 = function (i){
    p=i.price;
    j=parseInt(i.jmtext.split(",")[0]);
    if(p>=$scope.q_price1 && p<=$scope.q_price2 && j>=$scope.q_jmlen){
      return true;
    }
    return false;
  }

  $scope.chkboxf = function (s){
    $scope.skb[s] = !$scope.skb[s];
    if(!$scope.q_txt.match(s) && $scope.skb[s]){
      $scope.q_txt+=" "+s;
    }
    if(!$scope.skb[s] && $scope.q_txt.match(s) ){
      $scope.q_txt=$scope.q_txt.replace(eval("/ "+s+"/g"),"");
    }
  }

  $scope.matchrolej = function (txt){
     return matchrolelist(txt);
  }
  $scope.ptable = function (){
    if($scope.cts.length == 0){
      $scope.fetchdata();
    }
    $scope.ctslocal = $scope.cts;
    markrolej();
  }


});




