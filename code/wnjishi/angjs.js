
var elmBtdiv3 = document.createElement('div');
elmBtdiv3.className="controllbar2";
elmBtdiv3.innerHTML="<a  href='#angtable1'>[GoTO Ang Table]</a>";
document.body.appendChild(elmBtdiv3);
addGlobalStyle('.controllbar2{position:absolute;right:10%;top:20%;}');
//document.getElementById('angtable').addEventListener('click',function(){alert(1);},false);

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
                    "<td>{{ xxx.gender }}<br></td>"+
                    "<td>{{ xxx.gradeName }}</td>"+
                    "<td>{{ xxx.price }}</td>"+
                    "<td>{{ xxx.guild }}</td>"+
                    "<td id='{{ xxx.rolemark }}'>{{ xxx.skilltext }}</td>"+
                    "<td>- {{ xxx.equtext }}</td>"+
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




