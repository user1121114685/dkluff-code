var tmpdata=[];
var outputfilename = "db-stock.txt";
var dropbox;
dropbox = document.getElementById("dropbox");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);
function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}
function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  var dt = e.dataTransfer;
  var files = dt.files;

  readData(files);
}    
     
function chksave(){
  //return "save to file?";
}

function readData(files,charset='gbk'){
  for(i=0;i<files.length;i++){
    oFReader = new FileReader();
    oFReader.readAsArrayBuffer(files[i]);


    oFReader.onload = function (e) {
      er = e.target.result;
      var g = new TextDecoder('gbk');
      var u = new TextDecoder();
      var gd = g.decode(er);
      var ud = u.decode(er);
      var r = "输入文件有误！";
      var c = ["现金","人民币","买","卖"];
      for(i=0;i<c.length;i++){
        if(gd.search(c[i])>-1){
          r=gd;
          break;
        }
        if(ud.search(c[i])>-1){
          r=ud;
          break
        }
      }
      tmpdata.push(r);
      //append data to datainqueue
      var e = document.getElementById("datainqueue");
      e.innerHTML = e.innerHTML+r;
      
    }
  
    
    //oFReader.readAsText(files[i],charset);
    
   //oFReader.readAsBinaryString(files[i]);
  }  
}
function sinaApi() {
  var url = "http://hq.sinajs.cn/list=";
  if(localStorage.stockcodes){
    var s=localStorage.stockcodes.split(",");
    for(i=0;i<s.length;i++){
      var u = url + s[i].split(" ")[1];
      var e=document.getElementsByTagName("body");				
      var node = document.createElement('script');
      node.type = "text/javascript";
      node.src = u;
      e[0].appendChild(node);
    }
  }
}
sinaApi();