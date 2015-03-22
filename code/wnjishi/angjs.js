
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
                    "<a  href='#angtable'>[GoTO Top]</a>  "+
                    "<button id='angtable' ng-click='runangtable()'>[Ang Table]</button>"+
                    "<br>start loop<br><div>"+

                    "<label ng-repeat='w in wantedskills'>"+
                    "<input type='checkbox' ng-click='chkboxf(w)' >{{ w }}"+
                    "</label><br>--------------------------------------<br>"+

                    "<label ng-repeat='w in chktxt'>"+
                    "<input type='checkbox' ng-click='chkboxf(w)' >{{ w }}"+
                    "</label><br>--------------------------------------<br>"+

                    "Checkbox_txt:<input type='text' ng-model='q_txt'/> - "+
                    "Comtxt:<input type='text' ng-model='q_comtxt'/> - "+

                    "Price:<input type='number' ng-model='q_price1'/> - "+
                    "<input type='number' ng-model='q_price2'/><br>"+

                    "JM: <input type='number' ng-model='q_jmlen'/><br>"+

                    "<input type='checkbox' ng-model='hdtxt' >Hide Txt:"+
                    "<p ng-show='hdtxt'>{{ctslocal}}</p><br>"+

                    "Table:<br><table id='maintable'>"+
          "<tr ng-repeat='xxx in ctslocal | filter:uifilter1 | filter:uifilter2 | filter:q_comtxt | orderBy:tborder ' >"+
                    "<td class='titjj' rolename='{{ xxx.itemName }}'>{{ xxx.itemName }}</td>"+
    "<td id='{{xxx.rolemark}}'>[{{$index+1}}]<a href='{{roleurl+xxx.id}}' target='_blank'>{{ xxx.itemName }}</a></td>"+
                    "<td>{{ xxx.gender }}<br></td>"+
                    "<td>{{ xxx.gradeName }}</td>"+
                    "<td>{{ xxx.price }}</td>"+
                    "<td>{{ xxx.guild }}</td>"+
                    "<td id='{{ xxx.rolemark }}'>{{ xxx.skilltext.gettxt() }}</td>"+
                    "<td>- {{ xxx.equtext.gettxt() }}</td>"+
                    "<td>{{ xxx.jmtext.gettxt() }}</td>"+
                    "<td>{{ xxx.jmtext.getjmlen() }}</td>"+
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
  $scope.runangtable = function (){
    $scope.ctslocal  = $scope.cts;
    markrolej();
  }

  $scope.cts = [];
  $scope.url_all = "http://jishi.woniu.com/9yin/findSellingGoods.html?filterItem=4&pageIndex=";
  $scope.ttpage = 1;

  //start main http
  var serverName=getCookie("serverName");
  $http.get($scope.url_all+1).success(function(data, status, headers, config){
    $scope.ttpage = data[0].pageInfo.totalPages
    $scope.additemobj(data[0].pageData);
    for(var i = $scope.ttpage;i>1;i--){
      $http.get($scope.url_all+i).success(function(data, status, headers, config){
       $scope.additemobj(data[0].pageData);
      });
    }
  });
  //end main http

  $scope.roleurl = "http://jishi.woniu.com/9yin/tradeItemDetail.html?catagory=2&itemId=";

  $scope.skillurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=SkillContainer&roleUid=";
  $scope.jmurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=JingMaiContainer"+"&roleUid=";
  $scope.equurl="http://jishi.woniu.com/9yin/roleMsg.html?serverId="+serverName+"&type=EquipBox"+"&roleUid=";
  $scope.additemobj = function (p){
    for(var i in p){
      p[i]["skilltext"] = new $scope.getroledata($scope.skillurl+p[i].sellerGameId,$scope.wantedskills,0);
      p[i]["equtext"] = new $scope.getroledata($scope.equurl+p[i].sellerGameId,$scope.chktxt,0);
      p[i]["jmtext"] = new $scope.getroledata($scope.jmurl+p[i].sellerGameId,"",1)
      p[i]["rolemark"] = $scope.matchrolej(p[i].itemName);
      $scope.cts.push(p[i]);
    }
  }
  $scope.getroledata = function (url,mtg,j){
    var txt = "";
    var len = 0;
    this.gettxt = function (){
      return txt;
    }
    this.getjmlen = function (){
      return len;
    }
    $http.get(url).success(function(data, status, headers, config){
        if(j==0){
          txt = matchArr(mtg,data[0].msg);
        }
        if(j==1){
          t = fixjmtextj(data[0].msg);
          txt = t[1];
          len = t[0];
        }
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

  $scope.uifilter1 = function (i){
    t=$scope.q_txt;
    p=i.skilltext.gettxt()+" "+i.gender+" "+i.equtext.gettxt()+" "+i.rolemark;
    if(t.length == 0 && i.rolemark.match("ngrolename")){return true;}
    t=t.split(" ");
    if(matchArr(t,p).trim()){
      return true;
    }
    return false;
  }

  $scope.uifilter2 = function (i){
    p=i.price;
    j=parseInt(i.jmtext.getjmlen());
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

});




