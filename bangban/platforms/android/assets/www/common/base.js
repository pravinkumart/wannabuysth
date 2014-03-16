var Version = '1.3.0';
var Debug = false;


var www = 'http://app.bangban.com/';
if(Debug){
	var www = 'http://192.168.1.150:5000/';	
}

var $ = jQuery;
$.mobile.allowCrossDomainPages=true;


if(navigator.onLine==false){
	$('#loading .tc').html('网络未连接,点击屏幕，重新加载');
	$('#loading').fastClick(function(){
		window.location.href = window.location.href;
	});
}

(function(win){
	
	var e = document.createElement("script");
	e.setAttribute("src",www+'static/js/update.js?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	
	if(Debug){
		var e = document.createElement("script");
		e.setAttribute("src","http://192.168.1.150:8080/target/target-script-min.js#anonymous");
		document.getElementsByTagName("body")[0].appendChild(e);
	}
})(window);








