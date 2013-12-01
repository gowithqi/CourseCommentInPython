$.ajaxSetup({async:false});
$("#regInfo").modal({
  keyboard:false,
  backdrop:'static'
});
$("#regInfo").modal("hide");
function register_post(){
  $.post("/register/",
  {
    account:$("#account").val()+"@sjtu.edu.cn",
    name:$("#name").val(),
    password:hex_md5($("#password").val())
  },
  function(){
    $(".modal-title").html("还差一步！");
    $(".modal-body").html("<h5><b>我们已向您的邮箱发送验证邮件</b></h5>");
    $(".modal-body").append("<h5><b>请登录<a href='http://mail.sjtu.edu.cn'> mail.sjtu.edu.cn </a>查询（可能在垃圾邮箱T_T）</b></h5>");
  });
}
function account_get(){
  $.get("/register/account/"+$("#account").val()+"@sjtu.edu.cn"+"/",function(data){
    if (data=="no"){
      $("#ac_prompt").html("此邮箱已被注册！");
      $("#ac_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#account_ok").attr("class","");
    }
    else{
      $("#account_ok").attr("class","glyphicon glyphicon-ok");
      $("#ac_prompt").html("");
      $("#ac_prompt").attr("style","");
    }
  });
}
function name_get(str){
  $.get("/register/name/"+$("#name").val().toLowerCase()+"/",function(data){
    if (data=="no"){
      $("#nm_prompt").html("昵称已存在！");
      $("#nm_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#name_ok").attr("class","");
    }
    else{
      $("#name_ok").attr("class","glyphicon glyphicon-ok");
      $("#nm_prompt").html("");
      $("#nm_prompt").attr("style","");
    }
  });
}
$("#account").focus(function(){
  if ($("#ac_prompt").html()==""&&$("#account_ok").attr("class")==""){
    $("#ac_prompt").attr("style","color:#666666;margin-bottom:-10px");
    $("#ac_prompt").html("即jaccount帐号");
  }
});
$("#name").focus(function(){
  if ($("#nm_prompt").html()==""&&$("#name_ok").attr("class")==""){
    $("#nm_prompt").attr("style","color:#666666;margin-bottom:-10px");
    $("#nm_prompt").html("3-15位中英字符和数字 不区分大小写");
  }
})
$("#account").blur(function(){
  if ($("#ac_prompt").attr("style")=="color:#666666;margin-bottom:-10px"){
    $("#ac_prompt").html("");
    $("#ac_prompt").attr("style","");
  }
  if ($(this).val()!=""){
    account_get();
    if ($("#name").val()=="")
      $("#name").val($(this).val());
  }
  else
    if ($("#ac_prompt").attr("style")!="color:#888800;margin-bottom:-10px"){
      $("#ac_prompt").html("");
      $("#ac_prompt").attr("style","");
      $("#account_ok").attr("class","");
    }
});
$("#name").blur(function(){
  if ($("#nm_prompt").attr("style")=="color:#666666;margin-bottom:-10px"){
    $("#nm_prompt").html("");
    $("#nm_prompt").attr("style","");
  }
  if ($(this).val()!="")
    if ($(this).val().length<3){
      $("#nm_prompt").html("昵称名太短！");
      $("#nm_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#name_ok").attr("class","");
    }
    else if ($(this).val().length>15){
      $("#nm_prompt").html("昵称名太长！");
      $("#nm_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#name_ok").attr("class","");
    }
    else{
      var s=$(this).val(),ok=1;
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
        $("#nm_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
        $("#name_ok").attr("class","");
      }
    }
  else
    if ($("#nm_prompt").attr("style")!="color:#888800;margin-bottom:-10px"){
      $("#nm_prompt").html("");
      $("#nm_prompt").attr("style","");
      $("#name_ok").attr("class","");
    }
});
$("#password").focus(function(){
  if ($("#pw_prompt").html()==""&&$("#password_ok").attr("class")==""){
    $("#pw_prompt").attr("style","color:#666666;margin-bottom:-10px");
    $("#pw_prompt").html("6-20位英文字符、数字和特殊符号，区分大小写");
  }
});
$("#password").blur(function(){
  if ($("#pw_prompt").attr("style")=="color:#666666;margin-bottom:-10px"){
    $("#pw_prompt").html("");
    $("#pw_prompt").attr("style","");
  }
  if ($(this).val()!="")
    if ($(this).val().length<6){
      $("#pw_prompt").html("密码长度不足！");
      $("#pw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#password_ok").attr("class","");
    }
    else
    if ($(this).val().length>20){
      $("#pw_prompt").html("密码长度超过限制！");
      $("#pw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#password_ok").attr("class","");
    }
    else
    if (/.*[\u4e00-\u9fa5]+.*$/.test($(this).val())){
      $("#pw_prompt").html("密码不能包含中文！");
      $("#pw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
      $("#password_ok").attr("class","");
    }
    else{
      var s=$(this).val(),ok=1;
      for (var i=0;i<s.length;i++){
        if (/[a-zA-Z0-9_:!@#$%^&*]/.test(s[i]))
          continue;
        ok=0;
        break;
      }
      if (ok==0){
        $("#pw_prompt").html("密码不能含有 _:!@#$%^&* 以外的特殊符号！");
        $("#pw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
        $("#password_ok").attr("class","");
      }
      else{
        $("#password_ok").attr("class","glyphicon glyphicon-ok");
        $("#pw_prompt").html("");
        $("#pw_prompt").attr("style","");
        if ($("#cpassword").val()!="")
          if ($("#cpassword").val()==$(this).val()){
            $("#cpassword_ok").attr("class","glyphicon glyphicon-ok");
            $("#cpw_prompt").html("");
            $("#cpw_prompt").attr("style","");
          }
          else{
            $("#cpw_prompt").html("密码不一致！");
            $("#cpw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
            $("#cpassword_ok").attr("class","");
          }
      }
    }
  else
    if ($("#pw_prompt").attr("style")!="color:#888800;margin-bottom:-10px"){
      $("#pw_prompt").html("");
      $("#pw_prompt").attr("style","");
      $("#password_ok").attr("class","");
    }
});
$("#cpassword").blur(function(){
  if ($("#password").val().length>=6 && $("#password").val().length<=16){
    if ($(this).val()==$("#password").val()){
      $("#cpassword_ok").attr("class","glyphicon glyphicon-ok");
      $("#cpw_prompt").html("");
      $("#cpw_prompt").attr("style","");
    }
    else
      if ($(this).val()!=""){
        $("#cpw_prompt").html("密码不一致！");
        $("#cpw_prompt").attr("style","color:#AA0000;margin-bottom:-10px");
        $("#cpassword_ok").attr("class","");
      }
      else
        if ($("#cpw_prompt").attr("style")!="color:#888800;margin-bottom:-10px"){
          $("#cpw_prompt").html("");
          $("#cpw_prompt").attr("style","");
          $("#cpassword_ok").attr("class","");
        }
  }
  else
    if ($("#cpw_prompt").attr("style")!="color:#888800;margin-bottom:-10px"){
      $("#cpw_prompt").html("");
      $("#cpw_prompt").attr("style","");
      $("#cpassword_ok").attr("class","");
    }
    else
      if ($(this).val()!=""){
        $("#cpw_prompt").html("");
        $("#cpw_prompt").attr("style","");
        $("#cpassword_ok").attr("class","");
      }
});
function check(){
  $("#account").trigger("blur");
  $("#name").trigger("blur");
  $("#password").trigger("blur");
  $("#cpassword").trigger("blur");
  if ($("#account").val()==""){
    $("#ac_prompt").html("请填写邮箱！");
    $("#ac_prompt").attr("style","color:#888800;margin-bottom:-10px");
    $("#account_ok").attr("class","");
  }
  if ($("#name").val()==""){
    $("#nm_prompt").html("请填写昵称！");
    $("#nm_prompt").attr("style","color:#888800;margin-bottom:-10px");
    $("#name_ok").attr("class","");
  }
  if ($("#password").val()==""){
    $("#pw_prompt").html("请填写密码！");
    $("#pw_prompt").attr("style","color:#888800;margin-bottom:-10px");
    $("#password_ok").attr("class","");
  }
  if ($("#cpassword").val()==""){
    $("#cpw_prompt").html("请确认密码！");
    $("#cpw_prompt").attr("style","color:#888800;margin-bottom:-10px");
    $("#cpassword_ok").attr("class","");
  }
  if ($("#account_ok").attr("class")!=""&&$("#name_ok").attr("class")!=""&&$("#password_ok").attr("class")!=""&&$("#cpassword_ok").attr("class")!="")
    return true;
  else
    return false;
}
var last=0;
$(".enter").keydown(function(e){
  if (e.keyCode==40||e.keyCode==38)
    last=1;
  else{
    if (e.keyCode==13&&last==0)
    {
      e.preventDefault();
      if (check()){
        $(".modal-body").html("<h5><b>邮箱 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+$("#account").val()+"@sjtu.edu.cn</b></h5>");
        $(".modal-body").append("<h5><b>昵称 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+$("#name").val()+"</b></h5>");
        $("#regInfo").modal("show");
        $("#confirm").click(function(){
          $(".modal-title").html("请稍侯");
          $(".modal-body").html("<h5><b>正在向您的邮箱发送验证邮件</b></h5>");
          $(".modal-body").append("<h5><b>请等待几秒钟。。。</b></h5>");
          $(".modal-footer").hide();
          register_post();
        });
      }
    }
    last=0;
  }
});
$("#register").click(function(e){
  e.preventDefault();
  if (check()){
    $(".modal-body").html("<h5><b>邮箱 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+$("#account").val()+"@sjtu.edu.cn</b></h5>");
    $(".modal-body").append("<h5><b>昵称 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+$("#name").val()+"</b></h5>");
    $("#regInfo").modal("show");
    $("#confirm").click(function(){
      $(".modal-title").html("请稍侯");
      $(".modal-body").html("<h4>正在向您的邮箱发送确认信息</h4>");
      $(".modal-body").append("<h4>请等待几秒钟。。。</h4>");
      $(".modal-footer").hide();
      register_post();
    });
  }
});