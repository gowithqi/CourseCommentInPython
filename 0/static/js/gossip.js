Array.prototype.S = String.fromCharCode(2); 
Array.prototype.in_array = function(e) { 
    var r = new RegExp(this.S+e+this.S); 
    return (r.test(this.S+this.join(this.S)+this.S)); 
};
var gossips = new Array();
var curPosition = 22, scrolling = 1, hasg = 1, fetchtime = 1;

$(document).ready(function(){
    for (var i=1;i<=3;i++){
        var col=$("#column"+i+" .panel");
        for (var j=0;j<col.length;j++)
            gossips.push(col.eq(j).find(".goss").attr("data-gosid"));
    }
});
function reachBottom() {
    var scrollTop = 0;
    var clientHeight = 0;
    var scrollHeight = 0;
    if (document.body.clientHeight && document.documentElement.clientHeight) {
        clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight: document.documentElement.clientHeight;
    } else {
        clientHeight = (document.body.clientHeight > document.documentElement.clientHeight) ? document.body.clientHeight: document.documentElement.clientHeight;
    }
    scrollHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    if (document.documentElement && document.documentElement.scrollTop) {
        scrollTop = document.documentElement.scrollTop;
    } else if (document.body) {
        scrollTop = document.body.scrollTop;
    }
    if (scrollTop + clientHeight >= scrollHeight) {
        return true;
    } else {
        return false;
    }
}
function load_more(){
    if (reachBottom()&&scrolling&&hasg){
        scrolling=0;
        $("#loading").html("加载中。。。");
        $(".well").attr('class','well');
        var nextPosition=curPosition+29,i=0,c=1;
        $.ajaxSetup({async:false});
        while (i<=30){
            $.get('/gossip/getgossips/'+curPosition+'/'+nextPosition+'/',function(data){
                var obj=JSON.parse(data),l=30;
                if (obj.length<30)
                    l=obj.length;
                for (var j=1;j<=l;j++)
                    if (!gossips.in_array(obj[j-1].gossip_id.toString())) {
                        $("#column"+c).append('<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title" style="color:#0066FF;"><a href="/lecture/'+obj[j-1].lecture.id+'/">'+obj[j-1].lecture.professor_name+' 《'+obj[j-1].lecture.course_name+'》</a></h3></div><div class="panel-body"><h4 style="text-indent:2em;">'+obj[j-1].gossip_content+'</h4><h4 style="text-align:right;white-space:pre;"><small>'+obj[j-1].gossip_time+'      <a href="#" class="goss'+fetchtime+'" data-gosid="'+obj[j-1].gossip_id+'" data-super="'+(obj[j-1].have_supered?'1':'0')+'">'+(obj[j-1].have_supered?'取消':'赞')+'</a> (<span id="s'+obj[j-1].gossip_id+'">'+obj[j-1].gossip_super_number+'</span>)</small></h4></div></div>');
                        c=c%3+1;
                        gossips.push(obj[j-1].gossip_id.toString());
                        i++;
                    }
                if (l<30){
                    $("#loading").html("没有更多吐槽了～");
                    hasg=0;
                }
            });
            if (hasg==0)
                break;
            curPosition+=30;
            nextPosition=curPosition+29-i;
        }
        $(".goss"+fetchtime).click(function(e){
            e.preventDefault();
            var id=$(this).attr("data-gosid");
            var nu=Number($("#s"+id).html());
            if ($(this).attr("data-super")==1){
                $.get("/gossip/desuper/"+id+"/");
                nu-=1;
                $(this).attr("data-super","0");
                $(this).html("赞");
            }
            else{
                $.get("/gossip/super/"+id+"/");
                nu+=1;
                $(this).attr("data-super","1");
                $(this).html("取消");
            }
            $("#s"+id).html(nu);
        });
        fetchtime++;
        if (hasg==1){
            $("#loading").html("");
            $(".well").attr('class','well hidden');
        }
        scrolling=1;
    }
}
$(document).scroll(function(){
	load_more();
});
$(".goss").click(function(e){
    e.preventDefault();
    var id=$(this).attr("data-gosid");
    var nu=Number($("#s"+id).html());
    if ($(this).attr("data-super")==1){
        $.get("/gossip/desuper/"+id+"/");
        nu-=1;
        $(this).attr("data-super","0");
        $(this).html("赞");
    }
    else{
        $.get("/gossip/super/"+id+"/");
        nu+=1;
        $(this).attr("data-super","1");
        $(this).html("取消");
    }
    $("#s"+id).html(nu);
});