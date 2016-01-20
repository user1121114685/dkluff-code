function pricetable(prc){
    var a = ""+prc;
    var b = ""+prc;
    var maxp = 10;
    for(i=1;i<=10;i++){
        a=a+" | "+(prc*(100+i)/100).toFixed(2)+"(+"+i+"%)"
        b=b+" | "+(prc*(100-i)/100).toFixed(2)+"(-"+i+"%)"
    }
    return "<strong _ntesquote_='code:0600415;attr:price;fixed:2;color:updown' class='cRed'>"+a+"</strong>" + "<br>"+ 
            "<strong _ntesquote_='code:0600415;attr:price;fixed:2;color:updown' class='cGreen'>"+b+"</strong>"

}



var div_stock_detail = document.getElementsByClassName("stock_detail")[0]
var yestclose = parseFloat(document.getElementsByClassName("stock_detail")[0].getElementsByTagName("strong")[2].innerHTML)

var price_tool = document.createElement('div');
price_tool.id = "pricetool";
price_tool.innerHTML = pricetable(yestclose);

var calcer = document.createElement('div');
calcer.innerHTML = "<div ng-app='appcalcer' ng-controller='ctr1'>"+
                   "<input type='text' ng-model='q_prc'/> : "+ 
                   "<table><tr>"+
                   "<td><ul>"+
                   "<li ng-repeat='x in prcs(q_prc)'>"+
                   "<strong class='cRed'>{{ x }}</strong>"+
                   "</li>"+
                   "</ul></td>"+
                   "<td><ul>"+
                   "<li ng-repeat='y in prcsdown(q_prc)'>"+
                   "<strong class='cGreen'>{{ y }}</strong>"+
                   "</li>"+
                   "</ul></td></tr></table>"+
                   "</div>"

div_stock_detail.appendChild(price_tool);
div_stock_detail.appendChild(calcer);

var app = angular.module("appcalcer", []);
app.controller("ctr1", function($scope) {
        $scope.q_prc = "";
        $scope.prcs = function (v){
            p=parseFloat(v)
            arr = [];
            for(i=1;i<=10;i++){
                arr[i] = (p*(100+i)/100).toFixed(2) + "( +"+i+"%)" 
            }
            return arr;
        };
        $scope.prcsdown = function (v){
            p=parseFloat(v)
            arr = [];
            for(i=-1;i>=-10;i--){
                arr[-1*i] = (p*(100+i)/100).toFixed(2) + "( "+i+"%)" 
            }
            return arr;
        };
});

