var www = 'http://app.bangban.com/';
var $ = jQuery;
$.mobile.allowCrossDomainPages=true;

Raven.config('http://53b9b800c28741fda2fda2107f96dbfc@error.codoon.com/3', {
     whitelistUrls: []
 }).install();
 
Raven.setUser({
     email: '155214685@qq.com',
     id: '3'
});


(function(win){
	Raven.captureMessage('加载index.js 文件');
	var e = document.createElement("script");
	e.setAttribute("src",www+'static/js/index.js?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	Raven.captureMessage('加载index.css 文件');
	var e = document.createElement("link");
	e.setAttribute("rel",'stylesheet');
	e.setAttribute("href",www+'static/css/index.css?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
})(window);

if(navigator.onLine==false){
	Raven.captureMessage('网络断开');
	$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
	$('#loading').fastClick(function(){
		window.location.href = window.location.href;
	});
}
else{
	Raven.captureMessage('测试state');
	$("#loading").live('pageshow', function() {
		$.mobile.loading('show', {text : 'test', theme : 'a'});
		$.ajax({
			url:www + "state",
			dataType:'json',
			success:function(){},
			error:function(){
				Raven.captureMessage('测试state失败');
				$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
				$('#loading').fastClick(function(){
					window.location.href = window.location.href;
				});
				$.mobile.loading('hide');
			}
		});
	});
}
