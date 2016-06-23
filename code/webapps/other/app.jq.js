        //init code
        button='<li class="list-group-item"><div class="btn-group"> \
        <button type="button" class="btn btn-lg _btnstyle" id="_btnid">_BNTTEXT <span class="badge" id="_bgid">0</span></button> \
        <button type="button" class="btn btn-lg dropdown-toggle _btnstyle" data-toggle="dropdown" aria-expanded="false"> \
          <span class="caret"></span> \
          <span class="sr-only">Toggle Dropdown</span> \
        </button> \
        <ul class="dropdown-menu" role="menu"> \
          <li><a href="#" id="_undoid">Undo</a></li> \
          <li class="_divider"></li> \
          <li><a href="#" id="resetid">Reset</a></li> \
        </ul> \
      </div>    </li>';


      goodhb = ["gym","esleep"];
      badhb = {"smoking":0,"mt":0,"lsleep":0,"test":0,"gym":0,"esleep":0};

      if(!localStorage.startmoney){
        localStorage.startmoney=200
      }
      if(!localStorage.targetmoney){
        localStorage.targetmoney=parseInt(localStorage.startmoney)+300
      }
      if(!localStorage.curmoney | localStorage.curmoney<=0){
        localStorage.curmoney=localStorage.startmoney
      }

      function matcharr(tg,txt){
        for(k=0;k<tg.length;k++){
          if (tg[k].match(txt)){
            return true;
          }
        }
        return false;

      }

      for( var i in badhb ){
        var b1="";
        var btntheme="btn-danger"
        if(matcharr(goodhb,i)){
          btntheme = "btn-success";
        }
        //console.log(k); 这里有个奇怪的现象

        b1=button.replace(/_btnstyle/g, btntheme);
        b1=b1.replace("_bgid","bg"+i);
        b1=b1.replace("_btnid","btn"+i);
        b1=b1.replace("_BNTTEXT", i.toUpperCase());
        $("#btns").append(b1);
      }
      //---func start---

      function calcurmoney(bid){
        var curmoney = parseInt(localStorage.curmoney);
        m=badhb[bid];
        //smoking pre-proc
        if(bid == 'smoking'){
          m = (m-10)/10;
        }
        curmoney += m*10;
        localStorage.curmoney = curmoney;
      }

      function updateMoneyBar(){
        var curmoney = parseInt(localStorage.curmoney);
        var progress = curmoney*100.00/parseInt(localStorage.targetmoney);
        $(".progress-bar").css('width', progress+'%');
        $("#curmoney").html(localStorage.curmoney+"/"+localStorage.targetmoney);
        $("#prgbar-span").html(progress.toFixed(2)+"% Completed");
      }

      //---func end---

      updateMoneyBar();

      $("#changestartmoney").on( "click", function( event ) {
        localStorage.startmoney=$("#txtmoney").val();
        updateMoneyBar();
      });
      $("#changetargetmoney").on( "click", function( event ) {
        localStorage.targetmoney=$("#txtmoney2").val();
        updateMoneyBar();
      });
      $("#resetall").on( "click", function( event ) {
        r=confirm("Are you sure?");
        if(r){
          localStorage.clear();
          location.reload();
        }
      });

