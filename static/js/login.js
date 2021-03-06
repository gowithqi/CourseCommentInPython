var curcom=3;
$(document).ready(function(){
  $.csrftoken();
  $.ajaxSetup({async:false});
  comment_get_all();
  $.ajaxSetup({async:true});
  refresh_comment();
  setInterval("refresh_comment()",5000);
});
function login_post(){
  $.post("/",
  {
    username:$("#username").val().toLowerCase(),
    password:hex_md5($("#passwordl").val())
  },
  function(data){
    if (data=='password'){
      $("#psw_prompt").html("密码错误！");
      $("#psw_prompt").attr("class","text-danger");
      $("#psw_prompt").attr("style","margin-bottom:-0.7em;");
      $("#un_prompt").html("");
    }
    else
      if (data=='username'){
        $("#un_prompt").html("昵称或邮箱不存在！");
        $("#un_prompt").attr("class","text-danger");
        $("#psw_prompt").html("");
        $("#psw_prompt").attr("style","");
      }
    else{
      window.location.assign("/"+data+"/");
    }
  });
}
function comment_get_all(){
  for (var i=1;i<=3;i++){
    $.get("/userpage/getrandomcomment/60",
      function(data){
        var obj=JSON.parse(data);
        $("#course_name"+i).html(obj.lecture.course_name);
        $("#professor_name"+i).html(obj.lecture.professor_name);
        $("#course_level"+i).html(obj.lecture.level);
        $("#comment_content"+i).html(obj.comment_content);
        $("#comment_info"+i).html(obj.comment_user+"      "+obj.comment_time+"      有用 ("+obj.comment_super_number+")");
      }
    );
  }
}
function comment_get_one(){
  $.get("/userpage/getrandomcomment/60",function(data){
    var obj=JSON.parse(data);
    $("#course_name"+curcom).html(obj.lecture.course_name);
    $("#professor_name"+curcom).html(obj.lecture.professor_name);
    $("#course_level"+curcom).html(obj.lecture.level);
    $("#comment_content"+curcom).html(obj.comment_content);
    $("#comment_info"+curcom).html(obj.comment_user+"      "+obj.comment_time+"      有用 ("+obj.comment_super_number+")");
    var tmpcom=curcom-1,height=$("#comment"+curcom).innerHeight();
    if (tmpcom==0)
      tmpcom=3;
    $("#comment"+tmpcom).animate({
      top:'+='+height+'px',
      backgroundColor:'#AAC0BB'
    },"slow");
    if (--tmpcom==0)
      tmpcom=3;
    $("#comment"+tmpcom).animate({
      top:'+='+height+'px',
      backgroundColor:'#88A099'
    },"slow",function(){
      var s=$("#comment"+curcom).clone();
      $("#comment"+curcom).remove();
      $("#float_comment").prepend(s);
      $("#comment"+curcom).animate({
        opacity:'1',
        backgroundColor:'#708380'
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
$("#username").change(function(){
  $("#un_prompt").html("");
  $("#psw_prompt").html("");
  $("#psw_prompt").attr("style","");
});
$("#passwordl").change(function(){
  $("#psw_prompt").html("");
  $("#psw_prompt").attr("style","");
});
function checkl(){
  var blank=0;
  if ($("#username").val()==""){
    $("#un_prompt").html("请填写昵称或邮箱！");
    $("#un_prompt").attr("class","text-warning control-label");
    blank=1;
  }
  if ($("#passwordl").val()==""){
    $("#psw_prompt").html("请输入密码！");
    $("#psw_prompt").attr("class","text-warning control-label");
    $("#psw_prompt").attr("style","margin-bottom:-0.7em;");
    blank=1;
  }
  if (blank)
    return false;
  return true;
}
function refresh_comment(){
  $("#comment"+curcom).animate({
    opacity:'0'
  },"slow",function(){
    comment_get_one();
  });
}
var last=0;
$(".enterl").keydown(function(e){
  if (e.keyCode==40||e.keyCode==38)
    last=1;
  else{
    if (e.keyCode==13&&last==0)
    {
      e.preventDefault();
      $("#username").trigger("blur");
      $("#passwordl").trigger("blur");
      if (checkl())
        login_post();
    }
    last=0;
  }
});
$("#login").click(function(e){
  e.preventDefault();
  if (checkl())
    login_post();
});