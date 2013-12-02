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
          p.eq(0).html("还没有点评。快来抢沙发！");
          p.eq(1).html("");
          stack[fTop][i].most_popular_comment="还没有点评。快来抢沙发！";
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
var curcom=3;
$(document).ready(function(){
  $.ajaxSetup({async:false});
  comment_get_all();
  $.ajaxSetup({async:true});
  refresh_comment();
  setInterval("refresh_comment()",5000);
});
function decollect_get(that){
  $.get("/userpage/decollect/lecture/"+$(that).attr("data-lid")+"/",function(data){
    $(that).parentsUntil("li").parent().remove();
    var num=$("#collection_title").attr("data-number");
    $("#collection_title").attr("data-number",num-1);
    if ($("#hide_collection").html()=="收起"){
      if ($("#panel_collect li").length<=3)
        $("#hide_collection").remove();
    }
    else{
      if ($("#panel_collect li").length==0)
        $("#panel_collect").html('<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>');
      else{
        if ($("#panel_collect li").length>1&&$("#all_collection").html()=="显示全部"){
          $.get("/userpage/getallcollectionlectures/",function(data){
            var obj=JSON.parse(data),str='<ul class="list-group">',cl=obj.length;
            if (cl>3)
              cl=3;
            for (var i=0;i<cl;i++){
              str+='<li class="list-group-item" style="border-color:#AAAAAA"><div class="row"><div class="col-sm-3"><h5><a href="/lecture/'
              +obj[i].id+'/"><strong>'+obj[i].course_name+'</strong></a></h5><p>'+obj[i].professor_name+'</p><p><a href="#" data-lid="'+obj[i].id+'" class="decollect">取消收藏</a></p></div><div class="col-sm-9">';
              var comment=obj[i].most_popular_comment;
              if (comment=="")
                str+='<p>还没有点评。快来抢沙发！</p>';
              else{
                str+='<h5 style="text-indent:2em;line-height:20pt;border:solid 1px #DDDDDD;border-radius:10px;padding:10px;word-break:break-all;">'+comment.comment_content+'</h5>';
                str+='<h4 style="text-align:right;white-space:pre;"><small>'+comment.comment_user+'      '+comment.comment_time+'      有用 ('+comment.comment_super_number+')</small></h4>';
              }
              str+='</div></div></li>';
            }
            str+='</ul>';
            if (obj.length==0)
              str='<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>';
            if (obj.length>3)
              str+='<p style="text-align:right;"><a href="#" id="all_collection">显示全部</a></p>';
            $("#panel_collect").html(str);
            $("#collection_title").attr("data-number",obj.length);
            $("#all_collection").click(function(e){
              e.preventDefault();
              all_collection_get();
            });
            $(".decollect").click(function(e){
              e.preventDefault();
              decollect_get(this);
            });
          });
        }
      }
    }
    var title="收藏的课";
    if ($("#collection_title").attr("data-number")>0)
      title+="（"+$("#collection_title").attr("data-number")+"）";
    $("#collection_title").html(title);
  });
}
function all_collection_get(){
  $.get("/userpage/getallcollectionlectures/",function(data){
    var obj=JSON.parse(data),str='<ul class="list-group">',title="收藏的课";
    for (var i=0;i<obj.length;i++){
      str+='<li class="list-group-item" style="border-color:#AAAAAA"><div class="row"><div class="col-sm-3"><h5><a href="/lecture/'
      +obj[i].id+'/"><strong>'+obj[i].course_name+'</strong></a></h5><p>'+obj[i].professor_name+'</p><p><a href="#" data-lid="'+obj[i].id+'" class="decollect">取消收藏</a></p></div><div class="col-sm-9">';
      var comment=obj[i].most_popular_comment;
      if (comment=="")
        str+='<p>还没有点评。快来抢沙发！</p>';
      else{
        str+='<h5 style="text-indent:2em;line-height:20pt;border:solid 1px #DDDDDD;border-radius:10px;padding:10px;word-break:break-all;">'+comment.comment_content+'</h5>';
        str+='<h4 style="text-align:right;white-space:pre;"><small>'+comment.comment_user+'      '+comment.comment_time+'      有用 ('+comment.comment_super_number+')</small></h4>';
      }
      str+='</div></div></li>';
    }
    str+='</ul>';
    if (obj.length==0)
      str='<p>还没有收藏的课程。</p><p>快去课程页面收藏喜欢的课吧！</p>';
    else
      title+="（"+obj.length+"）";
    if (obj.length>3)
      str+='<p style="text-align:right;"><a href="#" id="hide_collection">收起</a></p>';
    $("#panel_collect").html(str);
    $("#collection_title").html(title);
    $("#collection_title").attr("data-number",obj.length);
    $("#hide_collection").click(function(e){
      e.preventDefault();
      $("#panel_collect").children("p").remove();
      $("#panel_collect").find("li").eq(2).nextAll().remove();
      $("#panel_collect").append('<p style="text-align:right;"><a href="#" id="all_collection">显示全部</a></p>');
      $("#all_collection").click(function(e){
        e.preventDefault();
        all_collection_get();
      });
    });
    $(".decollect").click(function(e){
      e.preventDefault();
      decollect_get(this);
    });
  });
}
function comment_get_all(){
  for (var i=1;i<=3;i++){
    $.get("/userpage/getrandomcomment/",
      function(data){
        var obj=JSON.parse(data);
        $("#course_name"+i+" strong").html(obj.lecture.course_name);
        $("#course_name"+i).attr("href","/lecture/"+obj.lecture.id+"/");
        $("#professor_name"+i).html(obj.lecture.professor_name);
        $("#course_level"+i).html(obj.lecture.level);
        $("#comment_content"+i).html(obj.comment_content);
        $("#comment_info"+i).html(obj.comment_user+"      "+obj.comment_time+"      有用 ("+obj.comment_super_number+")");
      }
    );
  }
}
function comment_get_one(){
  $.get("/userpage/getrandomcomment/",function(data){
    var obj=JSON.parse(data);
    $("#course_name"+curcom+" strong").html(obj.lecture.course_name);
    $("#course_name"+curcom).attr("href","/lecture/"+obj.lecture.id+"/");
    $("#professor_name"+curcom).html(obj.lecture.professor_name);
    $("#course_level"+curcom).html(obj.lecture.level);
    $("#comment_content"+curcom).html(obj.comment_content);
    $("#comment_info"+curcom).html(obj.comment_user+"      "+obj.comment_time+"      有用 ("+obj.comment_super_number+")");
    var tmpcom=curcom-1,height=$("#comment"+curcom).innerHeight();
    if (tmpcom==0)
      tmpcom=3;
    $("#comment"+tmpcom).animate({
      top:'+='+height+'px'
    },"slow");
    if (--tmpcom==0)
      tmpcom=3;
    $("#comment"+tmpcom).animate({
      top:'+='+height+'px'
    },"slow",function(){
      var s=$("#comment"+curcom).clone();
      $("#comment"+curcom).remove();
      $("#float_comment").prepend(s);
      $("#comment"+curcom).animate({
        opacity:'1'
      },"slow");
      tmpcom=curcom-1;
      if (tmpcom==0)
        tmpcom=3;
      $("#comment"+tmpcom).animate({
        top:'-='+height+'px'
      },0);
      if (--tmpcom==0)
        tmpcom=3;
      $("#comment"+tmpcom).animate({
        top:'-='+height+'px'
      },0);
      if (--curcom==0)
        curcom=3;
    });
  });
}
function refresh_comment(){
  $("#comment"+curcom).animate({
    opacity:'0'
  },"slow",function(){
    comment_get_one();
  });
}
/*$("#cPrevious").click(function(){
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
});*/
$("#all_collection").click(function(e){
  e.preventDefault();
  all_collection_get();
});
$(".decollect").click(function(e){
  e.preventDefault();
  decollect_get(this);
});