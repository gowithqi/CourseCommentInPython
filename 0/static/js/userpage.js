var clr=0,cur=0,hid=0,len=0,laststr="",origin_val="";
var stack,fTop=0,tTop=0;
$(document).ready(function(){
  /*var trs1=$("#rank1").children(),
      trs2=$("#rank2").children();
  for (var i=0;i<10;i++){
    trs1.eq(i).children().eq(0).html(i+1);
    trs2.eq(i).children().eq(0).html(i+1);
  }*/
  $("#cPrevious").prop('disabled',true);
  stack=new Array();
  stack[0]=new Array();
  for (var i=0;i<3;i++){
    var h3=$("#panel_change").find(".panel-title").eq(i);
    stack[0][i]=new Object();
    stack[0][i].id=h3.find("a").attr("href").replace("/","").replace("lecture","");
    stack[0][i].course_name=h3.find("a").html();
    stack[0][i].professor_name=h3.find("p").html();
    var p=$("#panel_change").find(".panel-body").eq(i).find("p");
    stack[0][i].most_popular_comment=p.eq(0).html();
    stack[0][i].user=p.eq(1).html();
  }
  fTop=1;
  tTop=1;
  $.csrftoken();
  $.ajaxSetup({async:false});
});
function auto_complete_post(){
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
          ss+="</tbody></table>";
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
function change_course_get(){
  if (tTop==fTop){
    stack[fTop]=new Array();
    $.get("/userpage/change/",function(data){
      obj=JSON.parse(data);
      for (var i=0;i<3;i++){
        var h3=$("#panel_change").find(".panel-title").eq(i);
        h3.find("a").attr("href","/lecture/"+obj[i].id+"/");
        h3.find("a").html(obj[i].course_name);
        h3.find("p").html(obj[i].professor_name);
        stack[fTop][i]=new Object();
        var p=$("#panel_change").find(".panel-body").eq(i).find("p"),comment=obj[i].most_popular_comment;
        if (comment==""){
          p.eq(0).html("还没有评论。快来抢沙发！");
          p.eq(1).html("");
          stack[fTop][i].most_popular_comment="还没有评论。快来抢沙发！";
          stack[fTop][i].user="";
        }
        else{
          p.eq(0).html(comment.comment_content);
          p.eq(1).html(comment.comment_user+"       "+comment.time+"   有用 ("+comment.comment_super_number+")");
          stack[fTop][i].most_popular_comment=comment.comment_content;
          stack[fTop][i].user=p[1].html;
        }
        stack[fTop][i].id=obj[i].id;
        stack[fTop][i].course_name=obj[i].course_name;
        stack[fTop][i].professor_name=obj[i].professor_name;
      }
    });
    tTop++;
    fTop++;
  }
  else{
    for (var i=0;i<3;i++){
      var h3=$("#panel_change").find(".panel-title").eq(i);
      h3.find("a").attr("href","/lecture/"+stack[fTop][i].id+"/");
      h3.find("a").html(stack[fTop][i].course_name);
      h3.find("p").html(stack[fTop][i].professor_name);
      var p=$("#panel_change").find(".panel-body").eq(i).find("p");
      p.eq(0).html(stack[fTop][i].most_popular_comment);
      p.eq(1).html(stack[fTop][i].user)
    }
    fTop++;
  }
  $("#cPrevious").find("span").attr("style","");
  $("#cPrevious").prop('disabled',false);
}
function decollect_get(lid){
  $.get("/userpage/decollect/lecture/"+lid+"/",function(data){
    if (data=="yes"){
      window.location.assign("/");
    }
  });
}
function all_collection_get(){
  $.get("/userpage/getallcollectionlectures/",function(data){
    var obj=JSON.parse(data);
    
  });
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
$("#cPrevious").click(function(){
  if (fTop!=1){
    fTop--;
    for (var i=0;i<3;i++){
      var h3=$("#panel_change").find(".panel-title").eq(i);
      h3.find("a").attr("href","/lecture/"+stack[fTop-1][i].id+"/");
      h3.find("a").html(stack[fTop-1][i].course_name);
      h3.find("p").html(stack[fTop-1][i].professor_name);
      var p=$("#panel_change").find(".panel-body").eq(i).find("p");
      p.eq(0).html(stack[fTop-1][i].most_popular_comment);
      p.eq(1).html(stack[fTop-1][i].user);
    }
    if (fTop==1){
      $("#cPrevious").prop('disabled',true);
      $("#cPrevious").find("span").attr("style","color:#DDDDDD;");
    }
  }
});