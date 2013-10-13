var current_page = '';
var user_is_first = true;
var is_init_main = false;
var my_navigator = [];
var pre_domin = ''; //强制指定后退回到的页面
//$.mobile.changePage($.mobile.activePage.jqmData('url'),{reloadPage :true});
$(document).bind('pagechangefailed',function(){
	$('.header_b').removeClass('on');
	alert('获取数据失败，请检查网络');
	current_page = '';
});

$(document).bind('pageshow',function(e){
	if(!current_page){return false;}
	my_navigator.push(current_page);
	current_page = '';
});

function get_data(key){
	return	window.localStorage.getItem(key);
}

function set_data(key,data){
	window.localStorage.setItem(key, data);
}

function del_data(key){
	return	window.localStorage.removeItem(key);
}

//初始化数据
(function() {
	$.mobile.allowCrossDomainPages=true;
	if(is_init_main){return false;}
	 is_init_main =true;
	 init_main();
	 if(get_data('user_is_first')){
	 	 gopage('home/accounts')
	 }else{
		 gopage('home/help');
	 	 set_data('user_is_first','true')
	 }
})();


document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
	window.device.overrideBackButton();
	document.addEventListener("backbutton", function(){
		if(go_back()){return false;}
		if(!confirm('是否退出?')){return false;}
		window.device.exitApp();
	}, false);
}

//全局init
function init_main(){
	$('.me_tap').live('fastClick',function(){
		var obj = $(this);
		var me_event = obj.attr('me_event');
		var me_data = obj.attr('me_data');
		if(!me_event){return false;}
		var me_event = eval(me_event);
			me_event(me_data)
		
	})
	$('.header_b').live('fastClick',function(){
		if($(this).hasClass('on')){return false;}
		$.mobile.loading('show', {text : 'test', theme : 'a'});
		$(this).addClass('on');
		if(pre_domin){
			gopage(pre_domin);
		}else{
			go_back()
		}
		return false;
	})
}


$('#accounts').live('pageshow',function() {
	if(pre_domin== 'accounts'){
		pre_domin = '';
	}
	
});

function getPicture(){
	if(!confirm('是否修改头像？')){return  false;}
	navigator.camera.getPicture(onSuccess, onFail, { quality: 50,
	    destinationType: Camera.DestinationType.DATA_URL
	});
}

function onSuccess(imageData) {
    var image = document.getElementById('myImage');
    image.src = "data:image/jpeg;base64," + imageData;
    update_user_portrait(imageData);
}

function update_user_portrait(imageData){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	$.post(www+'home/update_user_portrait',{'image':imageData},function(datas){
		$.mobile.loading('hide');
		alert('头像保存成功')
	})
}

function onFail(message) {
    console.log('Failed because: ' + message);
}

function update_user_name(){
	var username = $('#username').val();
	if(!username){
		alert('昵称不能为空');
		return false;
	}
	$.post(www+'home/update_user_name',{'username':username},function(data){
		$.mobile.loading('hide');
		alert(data.erro)
		if(data.succeed){
			go_back();
		}
	})
}

function go_back(){
	if(my_navigator.length==1&&my_navigator[0]=="home/help"){
		my_navigator.pop()
		gopage('home/accounts');
		return true
	}
	if(my_navigator.length <= 1){
		return false
	}
	var current = my_navigator.pop();
	if(current=="home/index"){return false}
	gopage(my_navigator.pop(),true);
	return true
}

function gopage(page_id,reverse){
	if(current_page){return false;}
	var reverse = reverse?true:false;
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	if(page_id.indexOf('home')==-1&&www){
		page_id = 'home/'+page_id
	}
	current_page = page_id
	$.mobile.changePage(www+page_id,{
			transition:'slide',
			data:{v:(new Date()).getTime()},
			showLoadMsg:false,
			reverse:reverse
	});
	
}

$("#index").live('pageshow', function() {
	index_init()
});

var index_page = {};
function index_init(){
  var obj = $('#wrapper_index');
  var width = 230;
  var count = obj.find('.thelist li').length;
  	  obj.find('.thelist li').width(width);
  	  obj.find('.scroller').width(count*width);
  if(index_page.myScroll){
  		index_page.myScroll.destroy();
  	}
  var myScroll = new iScroll('wrapper_index',{
    snap: true,
    momentum: false,
    hScrollbar: false
  });
  index_page.myScroll = myScroll;
  index_page.myScroll.refresh()
}


$("#login").live('pageshow', function() {
	window.need_login = $('#need_login_el').val();
});

function login_ok(){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#login_form').serializeArray();
	$.post(www+'home/login_do',data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('登录成功!')
			if(window.need_login){
				gopage(window.need_login);
			}else{
				gopage('index');
			}
		}else{
			alert(datas.erro)
		}
	})
}
function regedit_ok(){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#regedit_form').serializeArray();
	$.post(www+'home/regedit_do',data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('注册成功!')
			if(window.need_login){
				gopage(window.need_login);
			}else{
				gopage('index');
			}
		}else{
			alert(datas.erro)
		}
	})
}

function forget_ok(){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#forget_form').serializeArray();
	$.post(www+'home/forget_do',data,function(datas){
		$.mobile.loading('hide');
		alert(datas.erro);
	})
}

/*  二级分类 */
var second_lv_page = {}

$("#second_lv").live('pageshow', function() {
	second_lv_init()
});

function second_lv_init(){
  var obj = $('#wrapper_second_lv');
  var width = $('#wrapper_second_lv').width();
  if(second_lv_page.myScroll){
  		second_lv_page.myScroll.destroy();
  	}
  function pullUpAction () {
  	setTimeout(function(){
		$('.thelist').append($('.thelist li').eq(0).clone())
		myScroll.refresh();	
		  		
  	},3000)
	}
	pullUpEl = document.getElementById('pullUp');	
	if(!pullUpEl){
		return false;
	}
	pullUpOffset = pullUpEl.offsetHeight;
  var myScroll = new iScroll('wrapper_second_lv',{
		useTransition: true,
		onRefresh: function () {
			if (pullUpEl.className.match('loading')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
			}
		},
		onScrollMove: function () {
			if (this.y < (this.maxScrollY - 5) && !pullUpEl.className.match('flip')) {
				pullUpEl.className = 'flip';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Release to refresh...';
				this.maxScrollY = this.maxScrollY;
			} else if (this.y > (this.maxScrollY + 5) && pullUpEl.className.match('flip')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
				this.maxScrollY = pullUpOffset;
			}
		},
		onScrollEnd: function () {
			if (pullUpEl.className.match('flip')) {
				pullUpEl.className = 'loading';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Loading...';				
				pullUpAction();	// Execute custom function (ajax call?)
			}
		}
  });
  second_lv_page.myScroll = myScroll;
}

/* 商品列表 */
var item_list_page = {}
$("#item_list").live('pageshow', function() {
	item_list_init()
});


function item_list_init(){
  if(item_list_page.myScroll){
  		item_list_page.myScroll.destroy();
  	}
  function pullUpAction () {
  	setTimeout(function(){
		$('.item_list').append($('.item_list li').eq(0).clone())
		myScroll.refresh();	
		  		
  	},3000)
	}
	pullUpEl = document.getElementById('pullUp');	
	pullUpOffset = pullUpEl.offsetHeight;
	if($('.item_list li').length < 5){
		$('#pullUp').hide();
		return false;
		}
	
  var myScroll = new iScroll('item_list_wrapper',{
  	
  		useTransition: true,
		onRefresh: function () {
			if (pullUpEl.className.match('loading')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
			}
		},
		onScrollMove: function () {
			if (this.y < (this.maxScrollY - 2) && !pullUpEl.className.match('flip')) {
				pullUpEl.className = 'flip';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Release to refresh...';
				this.maxScrollY = this.maxScrollY;
			} else if (this.y > (this.maxScrollY + 2) && pullUpEl.className.match('flip')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
				this.maxScrollY = pullUpOffset;
			}
		},
		onScrollEnd: function () {
			if (pullUpEl.className.match('flip')) {
				pullUpEl.className = 'loading';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Loading...';				
				pullUpAction();	// Execute custom function (ajax call?)
			}
		}
  });
  item_list_page.myScroll = myScroll;
}

/* 购买列表 */
var sell_list_page = {}
$("#sell_list").live('pageshow', function() {
	sell_list_init()
});


function sell_list_init(){
	return false;
  if(sell_list_page.myScroll){
  		sell_list_page.myScroll.destroy();
  	}
  function pullUpAction () {
  	setTimeout(function(){
		$('.thelist').append($('.thelist li').eq(0).clone())
		myScroll.refresh();	
		  		
  	},3000)
	}
  var pullUpEl = document.getElementById('pullUp');	
  var pullUpOffset = pullUpEl.offsetHeight;
	
  var myScroll = new iScroll('sell_list_wrapper',{
  		useTransition: true,
		onRefresh: function () {
			if (pullUpEl.className.match('loading')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
			}
		},
		onScrollMove: function () {
			if (this.y < (this.maxScrollY - 5) && !pullUpEl.className.match('flip')) {
				pullUpEl.className = 'flip';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Release to refresh...';
				this.maxScrollY = this.maxScrollY;
			} else if (this.y > (this.maxScrollY + 5) && pullUpEl.className.match('flip')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
				this.maxScrollY = pullUpOffset;
			}
		},
		onScrollEnd: function () {
			if (pullUpEl.className.match('flip')) {
				pullUpEl.className = 'loading';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Loading...';				
				pullUpAction();	// Execute custom function (ajax call?)
			}
		}
  });
  sell_list_page.myScroll = myScroll;
}


/* 管一管 */
var history_list_page = {}
$("#history_list").live('pageshow', function() {
	history_list_init()
});


function history_list_init(){
	return false;
  if(history_list_page.myScroll){
  		history_list_page.myScroll.destroy();
  	}
  function pullUpAction () {
  	setTimeout(function(){
		$('.thelist').append($('.thelist li').eq(0).clone())
		myScroll.refresh();	
		  		
  	},3000)
	}
  var pullUpEl = document.getElementById('pullUp');	
  var pullUpOffset = pullUpEl.offsetHeight;
	
  var myScroll = new iScroll('history_list_wrapper',{
  		useTransition: true,
		onRefresh: function () {
			if (pullUpEl.className.match('loading')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
			}
		},
		onScrollMove: function () {
			if (this.y < (this.maxScrollY - 5) && !pullUpEl.className.match('flip')) {
				pullUpEl.className = 'flip';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Release to refresh...';
				this.maxScrollY = this.maxScrollY;
			} else if (this.y > (this.maxScrollY + 5) && pullUpEl.className.match('flip')) {
				pullUpEl.className = '';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Pull up to load more...';
				this.maxScrollY = pullUpOffset;
			}
		},
		onScrollEnd: function () {
			if (pullUpEl.className.match('flip')) {
				pullUpEl.className = 'loading';
				pullUpEl.querySelector('.pullUpLabel').innerHTML = 'Loading...';				
				pullUpAction();	// Execute custom function (ajax call?)
			}
		}
  });
  history_list_page.myScroll = myScroll;
}

function reload_js(){
	$.getScript('/static/js/index.js')
}

function apply_item_ok(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#apply_item_form').serializeArray();
	$.post('/home/apply_item_do',data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('申请成功!')
			gopage('item_list/'+id)
		}else{
			alert(datas.erro)
		}
	})
	
}

function wating(){
	alert('功能正在开发中。。')
}

function select_reply(replay_id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {replay_id:replay_id}
	$.post('/home/select_reply/'+replay_id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('选择商家成功!')
			gopage('decide_list')
		}else{
			alert(datas.erro)
		}
	})
	
}

function choose_s(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {id:id}
	$.post('/home/choose_s/'+id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('执行成功!')
			gopage('choose_list')
		}else{
			alert(datas.erro)
		}
	})
}

function choose_d(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {id:id}
	$.post('/home/choose_d/'+id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('执行成功!')
			gopage('history_list')
		}else{
			alert(datas.erro)
		}
	})
}

$( window ).hashchange(function() {
	var hash = location.hash;
});

$("#apply_item").live('pageshow', function() {
	var a = {display:"modal",lang:"zh",mode:"scroller",preset:"date",theme:"default"}
    $('#test_default').val('').scroller('destroy').scroller(a);
});



