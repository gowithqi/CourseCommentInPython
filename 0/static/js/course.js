$("#confirm_ok").click(function(){
	if (this.getAttribute("address")!="no_jump")
	{
		window.location.replace(this.getAttribute("address"));
	}
});

//level
$(".forall .star").click(function(){
	var level=parseInt(($(this).index()+2)/2);
	$("#trinity1").html("");
	$("#trinity1").rating({maxvalue:5,curvalue:level,increment:0.5,change:1});
	$("#trinity1").attr("data-value",level);
	$("#trinity").attr("data-id",$(this).parent().attr("data-id"));
	$("#trinity").modal('show');
});

//score
$(".rs_submit").click(function(){
	var x = $(".rs_content").val();
	$("#trinity2").val(x);
	$("#trinity1").html("");
	$("#trinity1").rating({maxvalue:5,curvalue:0,increment:0.5,change:1});
	$("#trinity1").attr("data-value",0);
	$("#trinity").attr("data-id",$(this).attr("data-id"));
	$("#trinity").modal('show');
});

//comment
$(".comment_submit").click(function(){
	var x = $(this).parent().parent().parent().children("textarea.comment_content").val();
	$("#trinity3").val(x);
	$("#trinity1").html("");
	$("#trinity1").rating({maxvalue:5,curvalue:0,increment:0.5,change:1});
	$("#trinity1").attr("data-value",0);
	$("#trinity").attr("data-id",$(this).attr("data-id"));
	$('#trinity').modal('show');
});

$("#trinity_submit").click(function(){
	var s=parseInt($("#trinity1").attr("data-value")),lid=$("#trinity").attr("data-id");
	var ss=$("#trinity2").val();
	var int_ss=parseInt(ss)
	var sss=$("#trinity3").val();
	if ((s>0) && (sss.length<=300)) {
		$.post("/lecture/recordall/"+lid+"/",
		{
			level:s,
			score:ss,
			content:sss
		},
		function(status){
			window.location.reload();
		});
	}
	// if (s>0){
	// 	$.post("/lecture/recordlevel/"+lid+"/",
	// 	{
	// 		level:s
	// 	},
	// 	function(status){
	// 		window.location.reload();
	// 	});
	// }
	// var ss=$("#trinity2").val();
	// if (ss.search(/^\d+$/)==-1){
		
	// }
	// else{
	// 	s=parseInt(ss);
	// 	if ((40<=s)&&(s<=100))
	// 	{
	// 		$.post("/lecture/recordscore/"+lid+"/",
	// 		{
	// 			score:s
	// 		},
	// 		function(status){
	// 			window.location.reload();
	// 		});
	// 	}
	// 	else {
			
	// 	}
	// }
	// ss=$("#trinity3").val();
	// if (ss.length>0){
	// 	if (ss.length<=300){
	// 	  	$.post("/comment/lecture/"+lid+"/",
	// 		{
	// 			content:ss
	// 		},
	// 		function(status){
	// 			if (status=="yes")
	// 			{
	// 				window.location.reload();
	// 			}
	// 			else
	// 			{
	// 				$('#failed_content').html(status);
	// 				$('#failed').modal('toggle');
	// 			}
	// 		});
	//   	}
	//   	else{
			
	//   	}
	// }
});

$("#trinity").on('hidden.bs.modal',function(){
	$("#trinity2").val("");
	$("#trinity3").val("");
});

//收藏按钮
function collect(id){
	var y = $(id).parent().children("input.l_id");
	var tmp = id.innerHTML;
	if (tmp == "收藏")
	{
		id.innerHTML = "取消收藏";
		$(id).attr('class','btn btn-warning btn-lg collect');
		$.get("/userpage/collect/lecture/"+y.val()+"/",function(status){
			if (status == "yes"){
				$('#confirm_content').html("收藏成功！");
				$('#confirm').modal('toggle');
				$('#confirm_ok').attr('address','no_jump');
			}
			else{
				$('#failed_content').html(status);
				$('#failed').modal('toggle');
			}
		}); 
	}
	else {
		id.innerHTML = "收藏";
		$(id).attr('class','btn btn-success btn-lg collect');
		$.get("/userpage/decollect/lecture/"+y.val()+"/",function(status){
			if (status == "yes"){
				$('#confirm_content').html("取消成功！");
				$('#confirm').modal('toggle');
				$('#confirm_ok').attr('address','no_jump');
			}
			else{
				$('#failed_content').html(status);
				$('#failed').modal('toggle');
			}
		});
	};
}

//点评点有用部分的js
function comment_good(id)
{
	var x = id.innerHTML;	//检测当前是否已经点过有用
	var y = $(id).parent().children("input.comment_id");
	var ss = "comment_"+y.val();
	var z = document.getElementById(ss);
	var num = parseInt(z.innerHTML);
	if (x == "有用")
	{
		x = "取消";
		id.innerHTML = x;
		num = num + 1;
		z.innerHTML = String(num);
		$.get("/comment/super/"+y.val()+"/",function(status){
			if (status!="yes") alert(status);
		});

	}
	else
	{
		x = "有用";
		id.innerHTML = x;
		num = num - 1;
		z.innerHTML = String(num);
		$.get("/comment/desuper/"+y.val()+"/",function(status){
			if (status!="yes") alert(status);
		});
	}
}

//吐槽点赞部分的js
function gossip_good(id)
{
	var x = id.innerHTML;	//检测当前是否已经赞过
	var y = $(id).parent().children("input.gossip_id");
	var ss = "gossip_"+y.val();
	var z = document.getElementById(ss);
	var num = parseInt(z.innerHTML);
	if (x == "点赞")
	{
		x = "取消";
		id.innerHTML = x;
		num = num + 1;
		z.innerHTML = String(num);
		$.get("/gossip/super/"+y.val()+"/",function(status){
			if (status!="yes") alert(status);
		});

	}
	else
	{
		x = "点赞";
		id.innerHTML = x;
		num = num - 1;
		z.innerHTML = String(num);
		$.get("/gossip/desuper/"+y.val()+"/",function(status){
			if (status!="yes") alert(status);
		});
	}
}

//吐槽submit
$(".wall_submit").click(function(){
	var x = $(this).parent().parent().parent().children("textarea.wall_content");
	var y = $(this).parent().parent().parent().children("input.l_id");
	if ((x.val().length<300) && (x.val().length>0))
	{
		$.post("/gossip/record/",
		{
			content:x.val(),
			lecture_id:y.val()
		},
		function(status){
			if (status=="yes")
			{
				$('#confirm_content').html("您的吐槽已经提交成功，查看请刷新页面。");
				$('#confirm').modal('toggle');
				$('#confirm_ok').attr('address','/lecture/'+ y.val() +'/');
			}
			else
			{
				$('#failed_content').html(status);
				$('#failed').modal('toggle');
			}
		});
	}
	else {
		if (x.val().length>300)
		{
			$('#failed_content').html("请不要超过300字");
  		}
		else
	    {
	    	$('#failed_content').html("请填写吐槽");
	    }
		$('#failed').modal('toggle');
	}
});
