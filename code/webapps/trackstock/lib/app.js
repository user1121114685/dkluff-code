var app = angular.module("trackstockapp", []);

app.controller("tsctrlmain", function($scope,$http) {
//adata = ["stockname amount price date", ]
    $scope.adata = [];

    $scope.logger = function (data,opt) {
        
    }

    $scope.addData = function () {
        for(i=0;i<tmpdata.length;i++){
            var d = parseData(tmpdata[i]);
            $scope.adata = $scope.adata.concat(d);
            $scope.logger(d,"+");
        }
        
    }

    $scope.removeItem = function (x) {
        $scope.adata.splice(x, 1);
        $scope.logger(x,"-")
    }

    $scope.addItem = function () {
        if (!$scope.addMe) {return;}
        if ($scope.adata.indexOf($scope.addMe) == -1) {
            $scope.adata.push($scope.addMe);
            $scope.logger(addMe,"+");
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
