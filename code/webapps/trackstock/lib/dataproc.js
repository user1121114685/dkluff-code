//massive org files -->tmpdata-->split to adata 
function zsDatafmt(line) {

  line = line.trim();

  //remove bad line
  if(line.length <3 ){return "";}
  if(line.includes("证券名称")){return "";}
  if(line.startsWith("---")){return "";}
  if(line.startsWith("#")){return "";}
  //fmt data
  var r = line.replace(/ +|\t/g," ").split(" ");
  var d = new Date();
  //type 资金流水
  if(r[0] == "人民币" && !line.includes("---")){
    r=r.slice(0,5);
    r.push(d.toLocaleDateString());
    return r.join(" ");
  }
  //type 当日成交
  if(r[2] == "买入" || r[2] == "卖出" ){
    var nr = [];
    nr[0] = "人民币";
    nr[1] = r[0];
    nr[2] = "***";
    nr[3] = r[3];
    nr[4] = r[4];
    if(r[2] == "卖出"){ nr[4] = nr[4]*-1; }
    nr.push(d.toLocaleDateString());
    return nr.join(" ");
  }
  //type 历史成交
  if(r[3] == "买入" || r[3] == "卖出" ){
    var nr = [];
    nr[0] = "人民币";
    nr[1] = r[0];
    nr[2] = r[1];
    nr[3] = r[4];
    nr[4] = r[5];
    if(r[3] == "卖出"){ nr[4] = nr[4]*-1; }
    nr.push(d.toLocaleDateString());
    return nr.join(" ");
  }
  return "";
}

function parseData(tmpdatablock) {
  //tmpdata to $scope.adata,return ["stockname *** price amount date", ]
  var a = tmpdatablock.split("\n");
  var r = [];

  if(a[0].startsWith("#new-db-stock.txt")){
    return a;
  }
  for(i=0;i<a.length;i++){
    var s = zsDatafmt(a[i]);
    if(s.length <3){continue;}
    r.push(s);
  }
  
  return r;

}
function datatoJSON(adata) {
  
}
