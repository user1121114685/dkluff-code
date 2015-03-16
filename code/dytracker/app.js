var app = angular.module("hbRecorder", []);

//common lib
function matcharr(tg,txt){
  for(k=0;k<tg.length;k++){
    if (tg[k].match(txt)){
      return true;
    }
  }
  return false;
}

app.controller("hbCtrlMain", function($scope,$http) {
  //init
  $scope.hbs =  [
    {"name":"smoking","count":0,"isBadhb":true,"weight":-1},
    {"name":"lsleep","count":0,"isBadhb":true,"weight":-10},
    {"name":"mt","count":0,"isBadhb":true,"weight":-50},
    {"name":"badthing-10","count":0,"isBadhb":true,"weight":-10},
    {"name":"test","count":0,"isBadhb":false,"weight":0},
    {"name":"gym","count":0,"isBadhb":false,"weight":10},
    {"name":"esleep","count":0,"isBadhb":false,"weight":10},
    {"name":"goodthing+10","count":0,"isBadhb":false,"weight":10},
  ];
  if(!localStorage.startmoney){
        localStorage.startmoney=200;
  }
  if(!localStorage.targetmoney){
    localStorage.targetmoney=parseInt(localStorage.startmoney)+300;
  }
  if(!localStorage.curmoney | localStorage.curmoney<=0){
    localStorage.curmoney=localStorage.startmoney
  }

  function readmoney(){
    $scope.curmoney = localStorage.curmoney;
    $scope.targetmoney = localStorage.targetmoney;
    $scope.startmoney = localStorage.startmoney;
  }
  readmoney();
  $scope.chgstartmoney = function () { 
    localStorage.startmoney = $scope.istartm;
    readmoney();
  }
  $scope.chgtargetmoney = function (){
    localStorage.targetmoney = $scope.itargetm;
    readmoney();
  }


  $scope.gettheme = function (t){
    if(t){ return "btn-danger"; }
    return "btn-success";
  }
  
  $scope.hblog = "";
  $scope.dohblog = function (c,t){
    $scope.hblog += t.name+","+Date()+","+c+"\r\n";
  }

  $scope.calmoney = function (c,t){
    $scope.curmoney = parseInt($scope.curmoney)+c*t.weight;
    localStorage.curmoney = $scope.curmoney;
    $scope.dohblog(c,t);
  }

  $scope.recordHB = function (t){
    t.count+=1;
    $scope.calmoney(1,t);
  }
  $scope.undoHB = function (t) {
    t.count-=1;
    if(t.count <= 0){ t.count = 0;}
    $scope.calmoney(-1,t);
  }
  $scope.resetHB = function (t) {
    t.count = 0;
  }

  $scope.resetAll = function () {
    r=confirm("ResetALL? Are you sure?");
    if(r){
      localStorage.clear();
      $http.post('/htcgi/savelog.py', $scope.hblog).success(function (){
        location.reload();
      });
    }
  }

});
