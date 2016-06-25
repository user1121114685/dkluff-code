var app = angular.module("trackstockapp", []);

app.controller("tsctrlmain", function($scope,$http) {
//adata = ["stockname *** price amount date", ]
    $scope.adata = [];

    $scope.logger = function (data,opt) {
        //console.log(data);
    }

    $scope.addData = function () {
        for(i=0;i<tmpdata.length;i++){
            var d = parseData(tmpdata[i]);
            $scope.adata = $scope.adata.concat(d);
            $scope.logger(d,"+");
        }
        tmpdata = [];
        
    }

    $scope.removeItem = function (x) {
        $scope.logger($scope.adata[x],"-");
        $scope.adata.splice(x, 1);
        
    }

    $scope.addItem = function () {
        //org addMe "stockname price amount" 
        if (!$scope.addMe) {return;}
        if ($scope.adata.indexOf($scope.addMe) == -1) {
            //format addMe to "stockname *** price amount date"

            
            $scope.adata.push($scope.addMe);
            $scope.logger($scope.addMe,"+");
            $scope.addMe = "";
        }
    }

    $scope.saveFile = function () {
        var d = $scope.adata.join();
        var blob = new Blob(d, {type: 'text/plain; charset=gbk'});
        var url = URL.createObjectURL(blob);
        node = document.createElement('a');
        node.href = url;
        node.download = outputfilename;
        node.click();
    }
       
    
});
