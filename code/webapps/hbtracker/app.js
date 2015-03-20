var app = angular.module("hbRecorder", []);
// to convert js time to python: time.strptime("Wed Mar 18 2015 01:13:06",'%a %b %d %Y %H:%M:%S')

//common lib
function chkv_time(min,max){
  n = new Date();
  k = n.getHours();
  if(k>=min && k<=max){
    return true;
  }
  return false;
}

app.controller("hbCtrlMain", function($scope,$http) {
  //init
  $scope.Chkfunc = function (){
    this.extcount = 0;
    this.extinfo = "";
    this.setextinfo = function(){
      this.extinfo = " - /Good:"+this.extcount+"/";
    }
    this.chcount = function (t,c){
      return c;
    }
    this.chweight = function(t,w){
      return w;
    }
  }


  $scope.hbs =  [
    {"name":"smoking","count":0,"weight":-10,"basecount":10,"chkfname":"smokingchkf"},
    {"name":"mt","count":0,"weight":-50,"basecount":1},
    {"name":"badthing","count":0,"weight":-10,"basecount":0},
    {"name":"test","count":0,"weight":0,"basecount":10,"chkfname":""},
    {"name":"gym","count":0,"weight":50,"basecount":3},
    {"name":"goodthing","count":0,"weight":10,"basecount":0},
    {"name":"sleep","count":0,"weight":-50,"basecount":0,"chkfname":"sleepchkf"},
  ];



  //set sleep chk
  $scope.Sleepchkf = new $scope.Chkfunc();
  $scope.Sleepchkf.chweight = function (t,w){
    var ww = 1;
    if(chkv_time(12,23)){
      ww = -1;
    }
    return ww*w;
  }

  $scope.Sleepchkf.chcount = function (t,c){
    if(chkv_time(12,23)){ this.extcount+=c;}
    this.setextinfo();

    //day check
    if($scope.ifcalchk){
      this.daycheck_smoking(t,c);
    }
    return c;
  }

  $scope.Sleepchkf.tmpsmoking = [];
  $scope.Sleepchkf.daycheck_smoking = function (t,c){
    //day count smoking
    b=$scope.hbs[0];
    bf = $scope.chkflist[b.chkfname]
    awd = 0;
    if(c>0){
      if(b.count<=b.basecount){
        bf.extcount+=c;
        awd = c*bf.award;
      }
      this.tmpsmoking.push(b.count);
      b.count = 0;
    }
    if(c<0){
      l=this.tmpsmoking.pop()
      if(l<=b.basecount){
        bf.extcount+=c;
        b.count = l;
        awd = c*bf.award;
      }
    }
    bf.setextinfo();
    $scope.curmoney += awd;
  }

  $scope.Smokingchkf = new $scope.Chkfunc();
  $scope.Smokingchkf.award = 50;


  $scope.chkflist = {
    "sleepchkf":$scope.Sleepchkf,
    "smokingchkf":$scope.Smokingchkf,
  }

  $scope.accperiod = 6;
  $scope.startdate = new Date();
  $scope.nowdate = $scope.startdate;
  $scope.curmoney = 300;
  $scope.targetmoney = 600;
  $scope.ifcalchk = true;
  $scope.ifcalchktxt = "";

  function savevars(){
    localStorage.curmoney = $scope.curmoney;
    localStorage.startdate = $scope.startdate;
    localStorage.hbs = JSON.stringify($scope.hbs);
  }
  function readvars(){
    $scope.curmoney = parseInt(localStorage.curmoney);
    $scope.startdate = new Date(localStorage.startdate);
    $scope.hbs = JSON.parse(localStorage.hbs);
  }
  if(localStorage.curmoney) {readvars()};

  //End init

  $scope.updatevars = function (){
    if($scope.tmpdate){$scope.startdate = new Date($scope.tmpdate);}
    if($scope.tmpcurm){$scope.curmoney = parseInt($scope.tmpcurm);}
    if($scope.tmptgtm){$scope.targetmoney = parseInt($scope.tmptgtm);}
    if($scope.tmpacc){$scope.accperiod = parseInt($scope.tmpacc);}
    savevars();
  }

  $scope.settheme = function (t){
    if((t.basecount-t.count)*t.weight >0){
      return "btn-danger"; 
    }
    return "btn-success";
  }

  $scope.hblog = "";
  $scope.dohblog = function (t,c){
    $scope.hblog += t.name+","+Date()+","+c+","+$scope.curmoney+"\n";
  }
  


  $scope.chkbox = function (){
    if(!$scope.ifcalchk){
      $scope.ifcalchktxt = "Cal Off";
      return
    }
    $scope.ifcalchktxt = "";
  }

  $scope.calmoney = function (t,c){
    if(!$scope.ifcalchk){
      return
    }
    w=t.weight;
    if(t.chkfname){ w=$scope.chkflist[t.chkfname].chweight(t,w);}
    if(t.basecount >= t.count+(c<0?1:0)){w=0;}
    $scope.curmoney += c*w;
    $scope.dohblog(t,c);
    $scope.nowdate = new Date();
  }


  $scope.recordHB = function (t,c){
    if(t.chkfname){c=$scope.chkflist[t.chkfname].chcount(t,c);}
    t.count+=c;
    if(t.count <= 0){ t.count = 0;}
    t.theme = $scope.settheme(t);
    $scope.calmoney(t,c);
    savevars();
  }

  $scope.resetHB = function (t) {
    t.count = 0;
    if(t.chkfname){$scope.chkflist[t.chkfname].extcount=0;}
    savevars();
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
