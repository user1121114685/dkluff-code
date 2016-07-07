function requrl(url,chkfunc){
  xp=new XMLHttpRequest();
  xp.onreadystatechange = chkfunc;
  xp.open("GET",url,true);
  xp.send();
}//if (this.readyState==4 && this.status==200)

function fmtdata_c0(d) {
    var p = d[0].property
    var sh = d[0].sh000001
    var r = []
    d.forEach(function(element) {
        r.push({
            "cid":element.cid,
            "property":100*(element.property-p)/p,
            "sh000001":100*(element.sh000001-sh)/sh,
        })
    }, this);
    return r;
}

function fmtframe_c1(frame){
    //add curcash
    var m = 0;
    var arrm=[];
    frame.colArray('money').forEach(function(e) {
      m+=e;
      arrm.push(-1*m);
    }, this);
    frame.addCol('curcash',arrm);

    //add stockchk
    m = 0;
    arrm=[];
    frame.colArray('amount').forEach(function(e) {
      m+=e;
      if(m==0){arrm.push(1);}
      arrm.push(0);
    }, this);
    frame.addCol('stockchk',arrm);
    
    

    return frame;

}

function g2paint_c0(d) {
    bid = 'c0'
    var e = document.getElementById(bid);
    e.innerHTML = "";
    
    var data = fmtdata_c0(getHistoryData(d,"#p1"));
    
    var Stat = G2.Stat;
    var Frame = G2.Frame;
    var frame = new Frame(data);
    var chart = new G2.Chart({ // 声明一个图表
        id: bid,
        width: 800,
        height: 400,
        forceFit:true,
        
    });

    
    chart.source(frame);
    chart.line().position('cid*property');
    chart.line().position('cid*sh000001').color('red');
    chart.render();



  
}

function g2paint_c1(d,totalhold) {
    bid = 'c1'
    var e = document.getElementById(bid);
    e.innerHTML = "";
    
    var data = datatoJSON(d);
    
    var Stat = G2.Stat;
    var Frame = G2.Frame;
    var frame = new Frame(data);
    var chart = new G2.Chart({ // 声明一个图表
        id: bid,
        width: 800,
        height: 400,
        forceFit:true,
        
    });
    


    //test
    //console.log(frame.cell(frame.rowCount()-1,'curcash'));
    //end-test
    frame = fmtframe_c1(frame);
    chart.source(frame);
    totalhold += frame.cell(frame.rowCount()-1,'curcash');
    //chart.interval().position(Stat.summary.sum('stockname*money'));
    chart.line().position('cid*curcash');
    chart.interval().position('cid*stockchk').size(1).color('red');
    chart.guide().line([0,totalhold],[totalhold,totalhold]);
    chart.render();
}





function g2paint_c2(d) {
    bid = 'c2'
    var e = document.getElementById(bid);
    e.innerHTML = "";
    
    var data = datatoJSON(d);
    
    var Stat = G2.Stat;
    var Frame = G2.Frame;
    var frame = new Frame(data);
    var chart = new G2.Chart({ // 声明一个图表
        id: bid,
        width: 800,
        height: 400,
        forceFit:true,
        
    });

    
    var defs = {
      money:{
        min:-2000,
        max:2000,
      },
      
    };
    chart.source(frame,defs);
  
    chart.interval().position(Stat.summary.sum('stockname*money')).size(25).color('stockname');
    
    chart.interval().position(Stat.summary.sum('stockname*amount')).shape('hollowRect').size(35);

    chart.render();

    
}
