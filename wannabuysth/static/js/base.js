var www = 'http://192.168.1.120:5000/';
var www = 'http://www.qp197.com:8000/';
var $ = jQuery;
$.mobile.allowCrossDomainPages=true;
if(!navigator.onLine){
	$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
	$('#loading').fastClick(function(){
		window.location.href = window.location.href;
	});
}
else{
	$("#loading").live('pageshow', function() {
		$.mobile.loading('show', {text : 'test', theme : 'a'});
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
	
	if(www.indexOf('5000')>-1){
		var e = document.createElement("script");
		e.setAttribute("src","http://192.168.1.120:8080/target/target-script-min.js#anonymous");
		document.getElementsByTagName("body")[0].appendChild(e);
	}

})(window);