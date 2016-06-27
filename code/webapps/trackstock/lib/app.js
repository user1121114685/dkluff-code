var app = angular.module("trackstockapp", []);

app.controller("tsctrlmain", function($scope,$http) {
//adata = ["RMB stockname *** price amount date", ]
    $scope.adata = [];
    

    $scope.logger = function (data,opt) {
        //console.log(data.length);
    }


    $scope.addData = function () {
        var d = [];
        var i = tmpdata.length-1;
        //for(i=0;i<tmpdata.length;i++){ //--bug
        while(i>=0){
          
            d = parseData(tmpdata[i]);
            $scope.adata = $scope.adata.concat(d);
            //$scope.logger(tmpdata);
            i--;

        }
        
        $scope.clearQueue();
        $scope.paint();
        
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
        if ($scope.adata.indexOf($scope.addMe) == -1) {
            //format addMe to "*** stockname *** price amount date"
            var r=$scope.addMe.replace(/ +|\t/g," ").split(" ");
            
            $scope.addMe = ["人民币",r[0],"***",r[1],r[2],d.toLocaleDateString()].join(" ");

            $scope.adata.push($scope.addMe);
            $scope.logger($scope.addMe,"+");
            $scope.addMe = "";
            $scope.paint();
        }
    }

    $scope.saveFile = function () {
        localStorage.adata = $scope.adata;
        var d = ["#new-db-stock.txt\r\n"];
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
    $scope.clear = function () {
        r=confirm("Clear&Save?");
        if(r){
            $scope.saveFile();
            localStorage.clear();
        }
        
    }


    $scope.paint = function () {
        g2paint_c1($scope.adata,16250);
        g2paint_c2($scope.adata,[{"中国动力":32}]);
        //TODO
        /*
        $http.get(url).success(function(response){
            g2paint_c1($scope.adata,);
        });
        */
        
    }
       
    if(localStorage.adata){
        $scope.adata = localStorage.adata.split(",");
        $scope.addData();
    }

});
