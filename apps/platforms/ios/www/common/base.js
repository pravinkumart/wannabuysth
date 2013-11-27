var www = 'http://192.168.1.120:5000/';
var www = 'http://www.qp197.com:8000/';
var $ = jQuery;
$.mobile.allowCrossDomainPages=true;

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

function takePhoto(){
    setTimeout(function(){
               navigator.camera.getPicture(onSuccess, onFail, { quality: 50,
                                           destinationType: Camera.DestinationType.DATA_URL
                                           });
               
               function onSuccess(imageData) {
               var image = document.getElementById('myImage');
               image.src = "data:image/jpeg;base64," + imageData;
               }
               
               function onFail(message) {
               alert('Failed because: ' + message);
               }
               },0);
}


(function(win){
	var e = document.createElement("script");
	e.setAttribute("src",www+'static/js/index.js?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
	
	var e = document.createElement("link");
	e.setAttribute("rel",'stylesheet');
	e.setAttribute("href",www+'static/css/index.css?v='+(new Date()).getTime());
	document.getElementsByTagName("body")[0].appendChild(e);
    takePhoto();
	
	if(www.indexOf('5000')>-1){
		var e = document.createElement("script");
		e.setAttribute("src","http://192.168.1.120:8080/target/target-script-min.js#anonymous");
		document.getElementsByTagName("body")[0].appendChild(e);
	}

})(window);