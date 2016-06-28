//massive org files -->tmpdata-->split to adata 
function removebadline(line){
  line = line.trim();
    //remove bad line
  if(line.length <3 ){return "";}
  if(line.includes("证券名称")){return "";}
  if(line.startsWith("---")){return "";}
  if(line.startsWith("#")){return "";}
  return line;
}
function zsDatafmt(line,isDbfile) {
  
  line = removebadline(line);
  if(isDbfile){
    return line;
  }
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
  
  var isDbfile = false;
  if(a[0].startsWith("#new-db-stock.txt")){
    isDbfile = true;
  }
  for(i=0;i<a.length;i++){
    var s = zsDatafmt(a[i],isDbfile);
    if(s.length <3){continue;}
    r.push(s);
  }
  
  return r;

}
function datatoJSON(adata) {
  var r = [];
  for(i=0;i<adata.length;i++){
    if(adata[i].startsWith("#")){continue;}
    var d = adata[i].split(" ");
    var fee=Math.abs(parseFloat(d[3])*parseInt(d[4])/1000)+5;
  
    r.push({
      "cid":i,
      "stockname":d[1],
      "price":parseFloat(d[3]),
      "amount":parseInt(d[4]),
      "date":d[5],
      "money":parseFloat(d[3])*parseInt(d[4])+fee,
    });
  }
  //console.log(r);
  return r;
}





function getStock(jarr){
  var r = {};

  for(i=0;i<jarr.length;i++){
    r[jarr[i].stockname] = 0;
  }
  return r;

}

function dataByStock(jarr){
  var r =[];
  var s = getStock(jarr);
  for(i=0;i<jarr.length;i++){
    s[jarr[i].stockname] += jarr[i].amount;  
    r.push(cpdic(s));  
  }
  return r;
}

function bStock(jarr){
  var r = [];
  var s = getStock(jarr);
  var sp = getStock(jarr);
  for(i=0;i<jarr.length;i++){
    s[jarr[i].stockname] += jarr[i].amount;
    sp[jarr[i].stockname] += jarr[i].money;  
          
  }
  for(k in s){
    var t = {};
    if(s[k] <100){ continue;}
    t.stockname = k;
    t.amount = s[k];
    t.price = 0;
    t.code= "";
    t.money=sp[k];
    t.cost=sp[k]/s[k];
    r.push(t);
  }

  return r;
}

function cpdic(d){
  var a = {};
  for(k in d){
    a[k] = d[k];
  }
  return a;
}