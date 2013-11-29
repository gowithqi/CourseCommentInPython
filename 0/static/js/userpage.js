/*var stack,fTop=0,tTop=0;
$(document).ready(function(){
  var trs1=$("#rank1").children(),
      trs2=$("#rank2").children();
  for (var i=0;i<10;i++){
    trs1.eq(i).children().eq(0).html(i+1);
    trs2.eq(i).children().eq(0).html(i+1);
  }
  $("#cPrevious").prop('disabled',true);
  stack=new Array();
  stack[0]=new Array();
  for (var i=0;i<3;i++){
    var h3=$("#panel_change").find(".panel-title").eq(i);
    stack[0][i]=new Object();
    stack[0][i].id=h3.find("a").attr("href").replace("/","").replace("/","").replace("/","").replace("lecture","");
    stack[0][i].course_name=h3.find("a").html();
    stack[0][i].professor_name=h3.find("p").html();
    var p=$("#panel_change").find(".panel-body").eq(i).find("p");
    stack[0][i].most_popular_comment=p.eq(0).html();
    stack[0][i].user=p.eq(1).html();
  }
  fTop=1;
  tTop=1;
});
function change_course_get(){
  $.ajaxSetup({async:false});
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
          p.eq(1).html(comment.comment_user+"       "+comment.comment_time+"       有用 ("+comment.comment_super_number+")");
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
}*/
function decollect_get(lid){
  $.get("/userpage/decollect/lecture/"+lid+"/",function(data){
    if (data=="yes"){
      if ($("#hide_collection").html()=="收起")
        all_collection_get();
      else{
        $.get("/userpage/getallcollectionlectures/",function(data){
          var obj=JSON.parse(data),str="",l=3;
          if (obj.length<3)
            l=obj.length;
          for (var i=0;i<l;i++){
            str+='<p style="white-space:pre;"><a href="/lecture/'+obj[i].id+'/">'+obj[i].course_name+'</a>     '+obj[i].professor_name+'     <a href="#" data-lid="'+obj[i].id+'" class="decollect">取消收藏</a></p>';
            var comment=obj[i].most_popular_comment;
            if (comment=="")
              str+='<p>还没有评论。快来抢沙发！</p>';
            else{
              str+='<p>'+comment.comment_content+'</p>';
              str+='<p style="text-align:right;white-space:pre;">'+comment.comment_user+'  '+comment.comment_time+'  有用 ('+comment.comment_super_number+')</p>';
            }
          }
          if (l==0)
            str+='<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>';
          else
          if (obj.length>3)
            str+='<p style="text-align:right;"><a href="#" id="all_collection">显示全部</a></p>';
          $("#panel_collect").html(str);
          $("#all_collection").click(function(e){
            e.preventDefault();
            all_collection_get();
          });
          $(".decollect").click(function(e){
            e.preventDefault();
            decollect_get($(this).attr("data-lid"));
          });
        });
      }
    }
  });
}
function all_collection_get(){
  $.get("/userpage/getallcollectionlectures/",function(data){
    var obj=JSON.parse(data),str="";
    for (var i=0;i<obj.length;i++){
      str+='<p style="white-space:pre;"><a href="/lecture/'+obj[i].id+'/">'+obj[i].course_name+'</a>     '+obj[i].professor_name+'     <a href="#" data-lid="'+obj[i].id+'" class="decollect">取消收藏</a></p>';
      var comment=obj[i].most_popular_comment;
      if (comment=="")
        str+='<p>还没有评论。快来抢沙发！</p>';
      else{
        str+='<p>'+comment.comment_content+'</p>';
        str+='<p style="text-align:right;white-space:pre;">'+comment.comment_user+'  '+comment.comment_time+'  有用 ('+comment.comment_super_number+')</p>';
      }
    }
    if (obj.length==0)
      str+='<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>';
    else
    if (obj.length>3)
      str+='<p style="text-align:right;"><a href="#" id="hide_collection">收起</a></p>';
    $("#panel_collect").html(str);
  });
  $("#hide_collection").click(function(e){
    e.preventDefault();
    $.get("/userpage/getallcollectionlectures/",function(data){
      var obj=JSON.parse(data),str="",l=3;
      if (obj.length<3)
        l=obj.length;
      for (var i=0;i<l;i++){
        str+='<p style="white-space:pre;"><a href="/lecture/'+obj[i].id+'/">'+obj[i].course_name+'</a>     '+obj[i].professor_name+'     <a href="#" data-lid="'+obj[i].id+'" class="decollect">取消收藏</a></p>';
        var comment=obj[i].most_popular_comment;
        if (comment=="")
          str+='<p>还没有评论。快来抢沙发！</p>';
        else{
          str+='<p>'+comment.comment_content+'</p>';
          str+='<p style="text-align:right;white-space:pre;">'+comment.comment_user+'  '+comment.comment_time+'  有用 ('+comment.comment_super_number+')</p>';
        }
      }
      if (l==0)
        str+='<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>';
      else
      if (obj.length>3)
        str+='<p style="text-align:right;"><a href="#" id="all_collection">显示全部</a></p>';
      $("#panel_collect").html(str);
      $("#all_collection").click(function(e){
        e.preventDefault();
        all_collection_get();
      });
      $(".decollect").click(function(e){
        e.preventDefault();
        decollect_get($(this).attr("data-lid"));
      });
    });
  });
  $(".decollect").click(function(e){
    e.preventDefault();
    decollect_get($(this).attr("data-lid"));
  });
}
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
$("#all_collection").click(function(e){
  e.preventDefault();
  all_collection_get();
});
$(".decollect").click(function(e){
  e.preventDefault();
  decollect_get($(this).attr("data-lid"));
});