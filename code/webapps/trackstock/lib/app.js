var app = angular.module("trackstockapp", []);

app.controller("tsctrlmain", function($scope,$http) {
//adata = ["RMB stockname *** price amount date", ]
    $scope.adata = [];
    $scope.stock = [];
    $scope.stockcodes = [];
    $scope.datalog = [];
    $scope.totalhold = 0;
    $scope.totalcash = 0;
    $scope.startcash = 0;


    $scope.logger = function (data,opt) {
        $scope.datalog.push(data+" opt :"+opt);
    }


    $scope.addData = function () {
        var d = [];
        var i = tmpdata.length-1;
        //for(i=0;i<tmpdata.length;i++){ //--bug
        while(i>=0){         
            d = parseData(tmpdata[i]);
            $scope.adata = $scope.adata.concat(d);
            $scope.logger(tmpdata,"+");
            i--;
        }
        var j = datatoJSON($scope.adata)
        $scope.stock = bStock(j);

        $scope.clearQueue();
        $scope.paint();
        $scope.totalcash = -1*datasum(j);
        $scope.startcash = -1*datasum(j,col='money',filter='stockname/现金');
        
    }
    $scope.clearQueue = function () {
        tmpdata = [];
        var e = document.getElementById("datainqueue");
        e.innerHTML = "";       
    }
    

    $scope.removeItem = function (x) {
        $scope.logger($scope.adata[x],"-");
        $scope.adata.splice(x, 1);
        $scope.paint();
        
    }
    

    $scope.addItem = function () {
        var d = new Date();
        //org addMe "stockname price amount" 
        if (!$scope.addMe) {return;}

         //format addMe to "*** stockname *** price amount date"
         var r=$scope.addMe.replace(/ +|\t/g," ").split(" ");
         
         $scope.addMe = ["人民币",r[0],"***",r[1],r[2],d.toLocaleDateString()].join(" ");

         $scope.adata.push($scope.addMe);
         $scope.logger($scope.addMe,"+");
         $scope.addMe = "";
         $scope.paint();
        
    }

    $scope.saveFile = function () {
        localStorage.adata = $scope.adata;
        var d = [];
        $scope.adata.forEach(function(e) {
            d.push(e+"\r\n")
        }, this);
        var blob = new Blob(d, {type: "text/plain"});
        //var blob = new File(d,{type: "text/plain;charset=gbk"});
       
        var url = URL.createObjectURL(blob);
        node = document.createElement('a');
        node.href = url;
        node.download = outputfilename;
        node.click();
    }
    $scope.clearAll = function () {
        r=confirm("Clear&Save?");
        if(r){
            $scope.saveFile();
            localStorage.clear();
        }
        
    }
    $scope.clearData = function () {
        r=confirm("Clear? - Pleas Save Before clear");
        if(r){
            $scope.saveFile();
            localStorage.adata="";
                       
        }
        
    }

    $scope.getPrice = function () {
        for(k=0;k<$scope.stock.length;k++){
            try {
                
                var v = eval("hq_str_"+$scope.stock[k].code);      
                $scope.stock[k].price=parseFloat(v.split(",")[3]);
            } catch (error) {
                console.log(error);
                continue;
            }
        }

        $scope.totalhold = 0;
        
        for(k=0;k<$scope.stock.length;k++){
            $scope.totalhold+=$scope.stock[k].price*$scope.stock[k].amount;
        }
       
    }


    $scope.paint = function () {
        
        g2paint_c0($scope.adata);
        g2paint_c1($scope.adata,$scope.totalhold);
        g2paint_c2($scope.adata);
        
    }
    $scope.updateCode = function () {
        
        if ($scope.tmpstcode) {
            if ($scope.stockcodes.indexOf($scope.tmpstcode) == -1) {
                
                var c= $scope.tmpstcode.replace(/ +|\t+/g," ").split(" ");
                var k = {};
                for(s=0;s<$scope.stockcodes.length;s++){
                    var a = $scope.stockcodes[s].split(" ");
                    
                    if(a.length>1){k[a[0]] = a[1];}
                }
                k[c[0]] = c[1];
                
                $scope.stockcodes=[];
                for(key in k){
                    $scope.stockcodes.push(key+" "+k[key]);
                }
                
            }
        }
        for(i=0;i<$scope.stockcodes.length;i++){
            var n = $scope.stockcodes[i].split(" ");
            for(k=0;k<$scope.stock.length;k++){
                if($scope.stock[k].stockname==n[0]){
                    $scope.stock[k].code=n[1];
                }
            }
            
        }

        $scope.getPrice(); 

        //archive index
        try{
            
            var s = "#p1"
                +"|"+($scope.totalcash +$scope.totalhold)
                +"|"+parseFloat(hq_str_sh000001.split(",")[3]);
            $scope.adata.push(s);
            localStorage.adata=$scope.adata;
        
        }catch (error) {
            console.log(error);
        }


        
        localStorage.stockcodes = $scope.stockcodes;
        $scope.paint();
    }

    //---for ui
    $scope.getlabelcolor= function (i){
        if(i>0){ return "label-success"}
        return "label-danger";
    }
    //end -- for ui
       
    if(localStorage.adata){
        $scope.adata = localStorage.adata.split(",");
        $scope.addData();
    }
    
    if(localStorage.stockcodes){
        $scope.stockcodes = localStorage.stockcodes.split(",");
    }


});
