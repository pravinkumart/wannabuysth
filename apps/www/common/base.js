var www = 'http://app.bangban.com';
var $ = jQuery;
$.mobile.allowCrossDomainPages=true;

Raven.config('http://53b9b800c28741fda2fda2107f96dbfc@error.codoon.com/3', {
    whitelistUrls: []
}).install();

Raven.setUser({
    email: '155214685@qq.com',
    id: '3'
});
Raven.captureMessage('base js 读取成功');
if(navigator.onLine==false){
	Raven.captureMessage('网络未连接,点击屏幕，重新加载  navigator.onLine=false');
	$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
	$('#loading').fastClick(function(){
		window.location.href = window.location.href;
	});
}
else{
	Raven.captureMessage('现在执行loading state ');
	$("#loading").live('pageshow', function() {
		$.mobile.loading('show', {text : 'test', theme : 'a'});
		$.ajax({
			url:www + "state",
			dataType:'json',
			success:function(){},
			error:function(){
				$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
				$('#loading').fastClick(function(){
					window.location.href = window.location.href;
				});
				$.mobile.loading('hide');
			}
		});
	});
}
Raven.captureMessage('现在执行 加载 服务端 index.js ');
(function(win){
	var e = document.createElement("script");
	e.setAttribute("src",www+'static/js/index.js?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	Raven.captureMessage('服务端 index.js 加载代码完成');
	var e = document.createElement("link");
	e.setAttribute("rel",'stylesheet');
	e.setAttribute("href",www+'static/css/index.css?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	Raven.captureMessage('服务端 index.css 加载代码完成');
	
	if(www.indexOf('5000')>-1){
		var e = document.createElement("script");
		e.setAttribute("src","http://192.168.1.120:8080/target/target-script-min.js#anonymous");
		document.getElementsByTagName("body")[0].appendChild(e);
	}

})(window);