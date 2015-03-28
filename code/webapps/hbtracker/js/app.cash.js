// to convert js time to python: time.strptime("Wed Mar 18 2015 01:13:06",'%a %b %d %Y %H:%M:%S')
var app = angular.module("hbRecorder", []);
app.filter('customfilter1',function (){
  return function (i){
    console.log("iput:"+i);
    return "a";
  }
});

//common lib
function chkv_time(min,max){
  n = new Date();
  k = n.getHours();
  if(k>=min && k<=max){
    return true;
  }
  return false;
}
function clearlocalvars(s){
  for(var i in localStorage){
    if(i.match(s+"$")){
      localStorage.removeItem(i);
    }
  }
}

app.controller("hbCtrlMain", function($scope,$http) {
  //init
  $scope.uifilter1 = function (i){
    if(!i.name.match("cash")){return true;}
    return false;
  }
  $scope.uifilter2 = function (i,b,m){
    return i%b==m?true:false;
  }
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
    {"name":"cig","count":0,"weight":-18,"basecount":0},
    {"name":"充值","count":0,"weight":-100,"basecount":0},
    {"name":"meal","count":0,"weight":-20,"basecount":0},
    {"name":"meal","count":0,"weight":-50,"basecount":0},
    {"name":"rent","count":0,"weight":-1500,"basecount":0},
    {"name":"ent","count":0,"weight":-500,"basecount":0},
    {"name":"cash$1","count":0,"weight":-100,"basecount":0},
    {"name":"cash$2","count":0,"weight":-50,"basecount":0},
    {"name":"cash$3","count":0,"weight":-20,"basecount":0},
    {"name":"cash$4","count":0,"weight":-10,"basecount":0},
    {"name":"cash$5","count":0,"weight":-5,"basecount":0},
    {"name":"cash$6","count":0,"weight":-1,"basecount":0},
  ];

  $scope.accperiod = 30;
  $scope.startdate = new Date();
  $scope.nowdate = $scope.startdate;
  $scope.curmoney = 0;
  $scope.targetmoney = 3000;
  $scope.ifcalchk = true;
  $scope.ifcalchktxt = "";

  function savevars(){
    localStorage.curmoney_cash = $scope.curmoney;
    localStorage.startdate_cash = $scope.startdate;
    localStorage.hbs_cash = JSON.stringify($scope.hbs);
  }
  function readvars(){
    $scope.curmoney = parseInt(localStorage.curmoney_cash);
    $scope.startdate = new Date(localStorage.startdate_cash);
    $scope.hbs = JSON.parse(localStorage.hbs_cash);
  }
  if(localStorage.curmoney_cash) {readvars()};

  //End init

  $scope.updatevars = function (){
    if($scope.tmpdate){$scope.startdate = new Date($scope.tmpdate);}
    if($scope.tmpcurm){$scope.curmoney = parseInt($scope.tmpcurm);}
    if($scope.tmptgtm){$scope.targetmoney = parseInt($scope.tmptgtm);}
    if($scope.tmpacc){$scope.accperiod = parseInt($scope.tmpacc);}
    savevars();
  }

  $scope.btn_c_theme = "";
  $scope.settheme = function (t){
    if(t){
      return "";
    }
    return "btn-success";
  }

  $scope.hblog = "";
  $scope.history = [ ];
  $scope.dohblog = function (t,c){
    if(!$scope.ifcalchk){return;}
    if(c<=0){
      $scope.hblog = $scope.hblog.replace(/#[^#]*\n$/,"");
      return
    }

    $scope.hblog += "#cash,"+t.name+","+Date()+","+$scope.ifcalchk+","+$scope.curmoney+"\n";
    h=$scope.history;
    h.push([t.name,c]);
    $scope.history = h;

  }



  $scope.chkbox = function (){
    $scope.btn_c_theme = $scope.settheme($scope.ifcalchk);
    if(!$scope.ifcalchk){
      $scope.ifcalchktxt = "Change Mode";
      return
    }
    $scope.ifcalchktxt = "";
  }

  $scope.calmoney = function (t,c){
    w=t.weight*($scope.ifcalchk?1:-1);
    //if(t.chkfname){ w=$scope.chkflist[t.chkfname].chweight(t,w);}
    //if(t.basecount >= t.count+(c<0?1:0)){w=0;}
    $scope.curmoney += c*w;
    $scope.nowdate = new Date();
  }


  $scope.recordHB = function (t,c){
    if(t.chkfname){c=$scope.chkflist[t.chkfname].chcount(t,c);}
    t.count+=c;
    if(t.count <= 0){ t.count = 0;}
    $scope.calmoney(t,c);
    $scope.dohblog(t,c);
    savevars();
  }

  $scope.Undo = function (){
    if($scope.history.length == 0){return;}
    x=$scope.history.pop();
    for(var i in $scope.hbs){
      k=$scope.hbs[i];
      if(k.name == x[0]){
        $scope.recordHB(k,-1*x[1]);
        break;
      }
    }
    return
  }


  $scope.savelog = function (){
    $http.post('/htcgi/savelog.py', $scope.hblog).success(function (){
      $scope.hblog = "#Info:Log Saved\n";
    });
  }

  $scope.resetAll = function (c) {
    r=confirm("ResetALL? Are you sure?");
    if(r){
      clearlocalvars("_cash");
      if(c<0){
        location.reload();
        return 1;
      }
      $http.post('/htcgi/savelog.py', $scope.hblog).success(function (){
        location.reload();
      });
    }
  }

  //lib2
  $scope.caltxt="";
  $scope.tochar = function (i){
    return String.fromCharCode(i);
  }
  $scope.inputchar = function (i){
    $scope.caltxt += i;

  }
  $scope.bkspace = function (i){
    if(i==0){
      $scope.caltxt="";
      return;
    }
    a=$scope.caltxt;
    $scope.caltxt = a.slice(0,a.length-1);
  }
  $scope.recordx = function (){
    s=$scope.caltxt
    for(;;){
      if(s.match(/[0-9]$/)){break;}
      s=s.replace(/[^0-9]*$/,"");
    }
    s=s.replace(/[^0-9\/*+-.]/,"");
    r=eval(s);
    console.log(r);
  }

}); //hbCtrlMain
