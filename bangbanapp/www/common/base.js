var www = 'http://app.bangban.com/';
var $ = jQuery;
$.mobile.allowCrossDomainPages=true;

// Raven.config('http://53b9b800c28741fda2fda2107f96dbfc@error.codoon.com/3', {
    // whitelistUrls: []
// }).install();
// 
// Raven.setUser({
    // email: '155214685@qq.com',
    // id: '3'
// });



if(navigator.onLine==false){
	$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
	$('#loading').fastClick(function(){
		window.location.href = window.location.href;
	});
}
else{
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
(function(win){
	var e = document.createElement("script");
	e.setAttribute("src",www+'static/js/index.js?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	var e = document.createElement("link");
	e.setAttribute("rel",'stylesheet');
	e.setAttribute("href",www+'static/css/index.css?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	
	var e = document.createElement("script");
	e.setAttribute("src","http://192.168.1.120:8080/target/target-script-min.js#anonymous");
	document.getElementsByTagName("body")[0].appendChild(e);

})(window);