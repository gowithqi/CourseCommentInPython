var clr=0,cur=0,hid=0,len=0,laststr="",origin_val="";
$(document).ready(function(){
  $.csrftoken();
});
function auto_complete_post(){
  $.ajaxSetup({async:true});
  $.post("/search/lecture/autocomplete/",
    {
      content:$("#search").val()
    },
    function(data){
      var s=data.split("\n");
      $("#complete").html(function(){
        var list="",l=$("#search").val().length;
        if (/[\u4e00-\u9fa5]/.test($("#search").val())){
          for (var i=0;i<s.length;i++){
            list=list+"<li><a href='#' style='padding-left:13px;'>";
            for (var j=0;j<l;j++)
              list=list+s[i][j];
            list=list+"<b>";
            for (var j=l;j<s[i].length;j++)
              list=list+s[i][j];
            list=list+"</b></a></li>";
          }
        }
        else{
          for (var i=0;i<s.length;i++)
            list=list+"<li><a href='#' style='padding-left:13px;'>"+s[i]+"</a></li>";
        }
        return list;
      });
      $("#complete").find("a").mousedown(function(){
        $("#search").val($(this).html().replace("<b>","").replace("</b>",""));
        $("#complete").hide();
        hid=1;
        search_post();
      });
      $("#complete").children().mouseenter(function(){
        $(this).parent().children().eq(cur).find("a").attr("style","padding-left:13px;color:#333333;background-color:#ffffff;");
        $(this).find("a").attr("style","padding-left:13px;color:#333333;background-color:#ebebeb;");
        cur=$(this).index();
      });
      if (s[0]==""||(s.length==1&&s[0]==$("#search").val())){
        len=0;
        $("#complete").hide();
        hid=1;
      }
      else{
        len=s.length;
        cur=-1;
        origin_val=$("#search").val();
        $("#complete").show();
        hid=0;
      }
    }
  );
}
function search_post(){
  if ($("#search").val()!="")
    $.post("/search/lecture/",
      {
        content:$("#search").val()
      },
      function(data){
        if (data[0]=="/")
          if (/[-]/.test(data)){
            $("#search").trigger("blur");
            $("#eSearch").find("h4").html("无法找到该课程");
            $("#eSearch").find(".modal-body").html('<h5><b>抱歉，没有找到名为《'+$("#search").val()+'》的课程。</b></h5>');
            $("#eSearch").find(".modal-body").append('<h5><b>请检查课程名是否正确。</b></h5>');
            $("#eSearch").modal("show");
          }
          else
            window.location.assign(data);
        else{
          var s=data.split("\n");
          $("#search").trigger("blur");
          $("#eSearch").find("h4").html("选择课程");
          $("#eSearch").find("button").html("取消");
          var mb=$("#eSearch").find(".modal-body"), ss="";
          mb.attr("data-length",s.length-1);
          ss="<table class='table table-hover table-bordered'><thead><tr><th>课程名</th><th>课号</th><th>学分</th><th>开课院系</th></tr></thead><tbody>";
          for (var i=0;i<s.length-1;i++){
            var cou=s[i].split(":");
            ss+="<tr><td><a href='#' onclick='search_get("+cou[0]+")'>"+cou[1]+"</a></td>";
            for (var j=2;j<=4;j++)
              ss+="<td>"+cou[j]+"</td>";
            ss+="</tr>";
          }
          ss+="</tbody></table><p><span class='glyphicon glyphicon-info-sign'></span> 没有找到？试试更完整的课程名</p>";
          mb.html(ss);
          $("#eSearch").modal("show");
        }
      }
    );
}
function search_get(cid){
  $.get("/search/lecture/courseid/"+cid+"/",function(data){
    window.location.assign(data);
  });
}
function name_get(){
  $.ajaxSetup({async:false});
  $.get("/register/name/"+$("#newname").val().toLowerCase()+"/",function(data){
    if (data=="no"){
      $("#nm_prompt").html("昵称已存在！");
      $("#nm_prompt").attr("class","text-danger control-label");
    }
    else{
      $("#nm_prompt").html("正确");
      $("#nm_prompt").attr("class","text-success control-label");
    }
  });
  $.ajaxSetup({async:true});
}
function setname_post(){
  if (checkname()){
    $("#sName").modal('hide');
    $.post("/userpage/setnickname/",
      {
        new_nickname:$("#newname").val()
      },
      function(){
        window.location.assign("/");
      }
    );
  }
}
function checkname(){
  if ($("#newname").val()!=""){
    if ($("#newname").val().length<3){
      $("#nm_prompt").html("昵称名太短！");
      $("#nm_prompt").attr("class","text-danger control-label");
    }
    else if ($("#newname").val().length>15){
      $("#nm_prompt").html("昵称名太长！");
      $("#nm_prompt").attr("class","text-danger control-label");
    }
    else{
      var s=$("#newname").val(),ok=1;
      for (var i=0;i<s.length;i++){
        if (/.*[\u4e00-\u9fa5]+.*$/.test(s[i]))
          continue;
        if (s[i]>='a'&&s[i]<='z')
          continue;
        if (s[i]>='0'&&s[i]<='9')
          continue;
        if (s[i]>='A'&&s[i]<='Z'){
          continue;
        }
        ok=0;
        break;
      }
      if (ok==1)
        name_get();
      else{
        $("#nm_prompt").html("昵称不能含有中英字符和数字以外的字符！");
        $("#nm_prompt").attr("class","text-danger control-label");
      }
    }
  }
  else{
    if ($("#nm_prompt").attr("class")!="text-warning control-label")
      $("#nm_prompt").html("");
  }
  if ($("#newname").val()==""){
    $("#nm_prompt").html("请填写昵称！");
    $("#nm_prompt").attr("class","text-warning control-label");
  }
  return ($("#nm_prompt").html()=="正确");
}
function auto_complete(){
  if ($("#search").val()==""){
    $("#complete").hide();
    hid=1;
    laststr="";
  }
  else
  if (laststr!=$("#search").val()){
    laststr=$("#search").val();
    auto_complete_post();
  }
}
$("#search").focus(function(){
  clr=setInterval("auto_complete()",500);
});
$("#search").blur(function(){
  clearInterval(clr);
  $("#complete").hide();
  hid=1;
});
$("#search").keydown(function(e){
  if (e.keyCode==40||e.keyCode==38){
    e.preventDefault();
    if (hid==1){
      laststr="";
      return;
    }
    var nxt;
    if (e.keyCode==40){
      nxt=cur+1;
      if(nxt==len)
        nxt=-1;
    }
    else{
      nxt=cur-1;
      if (nxt<-1)
        nxt=len-1;
    }
    if (cur>=0)
      $("#complete").children().eq(cur).find("a").attr("style","padding-left:13px;color:#333333;background-color:#ffffff;");
    if (nxt>=0){
      var li=$("#complete").children().eq(nxt).find("a");
      li.attr("style","padding-left:13px;color:#333333;background-color:#ebebeb;");
      $("#search").val(li.html().replace("<b>","").replace("</b>",""));
    }
    else
      $("#search").val(origin_val);
    laststr=$("#search").val();
    cur=nxt;
  }
  else if (e.keyCode==13){
    e.preventDefault();
    search_post();
  }
  else if (e.keyCode==27){
    if (hid==0){
      hid=1;
      $("#complete").hide();
    }
  }
});
$("#submit").click(function(e){
  e.preventDefault();
  search_post();
});
$("#eSearch").keydown(function(e){
  if (e.keyCode==13)
    $(this).modal("hide");
});
$("#newname").focus(function(){
  $("#helpname").html("3-15位中英字符和数字 不区分大小写");
})
$("#newname").keydown(function(e){
  if (e.keyCode==13)
    e.preventDefault();
});
$("#sName").on('hidden.bs.modal',function(){
  $("#newname").val("");
  $("#helpname").html("");
  $("#nm_prompt").html("");
});