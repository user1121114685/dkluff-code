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
    oFReader.onload = function (oFREvent) {
      console.log("Loaded successfully")
      tmpdata.push(oFREvent.target.result);
      //append data to datainqueue
      var e = document.getElementById("datainqueue");
      e.innerHTML = e.innerHTML+oFREvent.target.result;
            
    };
  
    
    oFReader.readAsText(files[i],charset);
    //oFReader.readAsArrayBuffer(files[0]);
  }  
}