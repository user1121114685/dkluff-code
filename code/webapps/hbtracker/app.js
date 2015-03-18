var app = angular.module("hbRecorder", []);

//common lib

app.controller("hbCtrlMain", function($scope,$http) {
  //init
  $scope.ChkSleep =  function (){
    var goodcount = 0;
    var ttcount = 0;
    //to reverse sleep weight
    this.chk = function (){
      ttcount+=1;
      n = new Date();
      k = n.getHours();
      $scope.hblog += "TotalSmoked,"+$scope.hbs[0].count+","+n.toDateString()+"\n";
      $scope.hbs[0].count = 0; //new day,reset smoking count
      if(k <= 23 && k>12){
        goodcount+=1;
        $scope.hblog += "TotalGoodSleep,"+goodcount+"/"+ttcount+","+n.toDateString()+"\n";
        return -1;
      }
      return 1;
    }
  }


  $scope.hbs =  [
    {"name":"smoking","count":0,"weight":-10,"goal":10},
    {"name":"mt","count":0,"weight":-50,"goal":1},
    {"name":"badthing","count":0,"weight":-10,"goal":0},
    {"name":"test","count":0,"weight":0,"goal":10},
    {"name":"gym","count":0,"weight":50,"goal":3},
    {"name":"goodthing","count":0,"weight":10,"goal":1},
    {"name":"sleep","count":0,"weight":-50,"goal":1,"fchk":new $scope.ChkSleep()},
  ];

  $scope.accperiod = 6;
  $scope.startdate = new Date();
  $scope.nowdate = $scope.startdate;
  $scope.curmoney = 300;
  $scope.targetmoney = $scope.curmoney*2;


  function savevars(){
    localStorage.curmoney = $scope.curmoney;
    localStorage.startdate = $scope.startdate;
  }
  function readvars(){
    $scope.curmoney = localStorage.curmoney
    $scope.startdate = new Date(localStorage.startdate);
  }
  if(localStorage.curmoney) {readvars()};

  //End init

  $scope.updatevars = function (){
    if($scope.tmpdate){$scope.startdate = new Date($scope.tmpdate);}
    if($scope.tmpcurm){$scope.curmoney = parseInt($scope.tmpcurm);}
    if($scope.tmptargetmoney){$scope.targetmoney = parseInt($scope.tmptartgetm);}
    if($scope.tmpacc){$scope.accperiod = parseInt($scope.tmpacc);}
    savevars();
  }

  $scope.settheme = function (t){
    if((t.goal-t.count)*t.weight >0){
      return "btn-danger"; 
    }
    return "btn-success";
  }

  $scope.hblog = "";
  $scope.dohblog = function (c,t){
    $scope.hblog += t.name+","+Date()+","+c+","+$scope.curmoney+"\n";
  }

  $scope.calmoney = function (c,t){
    w=t.weight;
    if(t.fchk){ w*=t.fchk.chk();}
    if(t.goal >= t.count+(c<0?1:0)){w=0;}
    $scope.curmoney += c*w;
    $scope.dohblog(c,t);
    $scope.nowdate = new Date();
  }


  $scope.recordHB = function (t,c){
    t.count+=c;
    if(t.count <= 0){ t.count = 0;}
    t.theme = $scope.settheme(t);
    $scope.calmoney(c,t);
  }

  $scope.resetHB = function (t) {
    t.count = 0;
  }


  $scope.savelog = function (){
    $http.post('/htcgi/savelog.py', $scope.hblog).success(function (){
      $scope.hblog = "Log Saved\n";
    });
  }

  $scope.resetAll = function (c) {
    r=confirm("ResetALL? Are you sure?");
    if(r){
      localStorage.clear();
      if(c<0){
        location.reload();
        return 1;
      }
      $http.post('/htcgi/savelog.py', $scope.hblog).success(function (){
        location.reload();
      });
    }
  }

}); //hbCtrlMain
