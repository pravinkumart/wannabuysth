var current_user = ''
var current_page = '';  //正在处理的页面
var is_init_main = false;
var my_navigator = [];
var pre_domin = ''; //强制指定后退回到的页面
$.mobile.ajaxEnabled = false;
$.mobile.pageLoadErrorMessage = "获取数据失败";
$(document).bind('pagechangefailed',function(){
	$('.header_b').removeClass('on');
	$.mobile.loading('hide');
	alert('获取数据失败，请检查网络');
	current_page = '';
});

$(document).bind('pageshow',function(e){
	if(!current_page){return false;}
	if(my_navigator.indexOf(current_page)>-1){
		my_navigator = my_navigator.slice(0,my_navigator.indexOf(current_page)+1);
	}else{
		my_navigator.push(current_page);
	}
	current_page = '';
});

function get_data(key){
	return	window.localStorage.getItem(key);
}

function set_data(key,data){
	if(typeof window.localStorage.setItem == "string"){
		window.localStorage.setItem[key] = data;
	}else{
		window.localStorage.setItem(key, data);
	}
}

function del_data(key){
	return	window.localStorage.removeItem(key);
}


document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
	navigator.app.overrideBackbutton();
	document.addEventListener("backbutton", function(){
		if(current_page){return false;}
		if(go_back()){return false;}
		showConfirm('是否退出?',function(data){
			if(data == 1){
				navigator.app.exitApp();
			}
		});
	}, false);
	if(navigator.notification&&navigator.notification.alert){
		window.alert = function(message, alertCallback,title){
			if(!title){title='提示';}
			navigator.notification.alert(message, alertCallback, title, '确定')
		};

	}
}

function showConfirm(message, completeCallback, title){
	if(!confirm(message)){return false;}
		completeCallback(1);
	return 
	if(navigator.notification&&navigator.notification.confirm){
			if(!title){title = '提示';}
			navigator.notification.confirm(message, completeCallback, title, ['确定','取消'])
	}else{
		if(!confirm(message)){return false;}
		completeCallback();
	}
}


var onmessage = function(e) {
       var data = e.data.split(':');
       if(data[0]=='next'){
       		gopage(data[1]);
       }
       
};

//监听postMessage消息事件
if (typeof window.addEventListener != 'undefined') {
  window.addEventListener('message', onmessage, false);
} else if (typeof window.attachEvent != 'undefined') {
  window.attachEvent('onmessage', onmessage);
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
	showConfirm('是否修改头像？',function(ok){
		if(ok!=1){return false;}
		navigator.camera.getPicture(onSuccess, onFail, { quality: 50,
		    destinationType: Camera.DestinationType.DATA_URL
		});
	})
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

function update_user_mobile(me_data){
	var data = $('#update_mobile_form').serializeArray();
	$.post(www+'home/update_user_mobile',data,function(data){
		$.mobile.loading('hide');
		alert(data.erro)
		if(data.succeed){
			if(me_data=='bind'){
				my_navigator = [];
				gopage('index')
			}else{
				go_back();
			}
		}
	})
}

function update_user_password(){
	var data = $('#update_password_form').serializeArray();
	$.post(www+'home/update_user_password',data,function(data){
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
	if(current=="home/index"){
		my_navigator.push(current);
		return false;
	}
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
$("#guide").live('pageshow', function() {
	$('#loading_lv li').width($(window).width());
  	$('#loading_lv .scroller').width($(window).width()*$('#loading_lv li').length);
  	$('#loading_lv .thelist').width($(window).width()*$('#loading_lv li').length);
  	var max_height = $(window).height()
  	var imgs = $('#loading_lv li img');
  	for(var i = 0;i<imgs.length;i++){
  		// var height =  imgs.eq(i).height();
  		// if (max_height > height){
  			// imgs.eq(i).css('margin-top',(max_height-height)/2)
  		// }
  	}
  	var myScroll = new iScroll('loading_lv',{
  			snap: true,
		    momentum: false,
		    hScrollbar: false
  		});
  	myScroll.refresh();
  	$.mobile.loading('hide');
  	$('#loading_lv li img').show();
  	my_navigator = [];
});


$("#index").live('pageshow', function() {
	index_init()
});

var index_page = {};
function index_init(){
  var obj = $('#wrapper_index');
  if(index_page.myScroll){
  		index_page.myScroll.destroy();
  	}
  var myScroll = new iScroll('wrapper_index',{hideScrollbar: true});
  index_page.myScroll = myScroll;
  index_page.myScroll.refresh()
}

var item_detail_page = {};
$("#item_detail").live('pageshow', function() {
	
  var obj = $('#wrapper_item_detail');
  if(item_detail_page.myScroll){
  		index_page.myScroll.destroy();
  	}
  var myScroll = new iScroll('wrapper_item_detail',{hideScrollbar: true});
  item_detail_page.myScroll = myScroll;
  item_detail_page.myScroll.refresh()
  
});


$("#login").live('pageshow', function() {
	var username = get_data('username');
		if(username){
			$('.username').val(username);
		}
	window.need_login = $('#need_login_el').val();
});

function login_ok(){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#login_form').serializeArray();
	$.post(www+'home/login_do',data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			var username = $('.username').val();
			set_data('username',username)			
			current_user = data.erro;
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
		myScroll.refresh();	
  	},0)
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
		myScroll.refresh();	
  	},0)
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


$("#notification").live('pageshow', function() {
	$.post(www+'home/notification/read',{},function(datas){});
	bijia_list_init();
});

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
		myScroll.refresh();	
  	},0)
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
		myScroll.refresh();	
  	},0)
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

function apply_item_ok(type_data){
	var data = $('#apply_item_form').serializeArray();
	var id = type_data.split(' ')[0];
	var type = type_data.split(' ')[1];
	if($('.place_text').val()==$('.place_text').attr('placeholder')){
		alert('内容不能为空!');
		return false;
	}
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	$.post('/home/apply_item_do',data,function(datas){
		$.mobile.loading('hide');
		my_navigator.pop();
		if(datas.succeed){
			if(type==0){
				alert('提交成功!');
				go_back();
			}else{
				alert('发布成功!');
				go_back();
			}
			
		}else{
			alert(datas.erro);
		}
	});
	
}

function wating(){
	alert('功能正在开发中。。')
}

function select_reply(replay_id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {replay_id:replay_id};
	$.post('/home/select_reply/'+replay_id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('选择商家成功!')
			gopage('decide_list')
		}else{
			alert(datas.erro)
		}
	});
	
}

function choose_s(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {id:id};
	$.post('/home/choose_s/'+id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('执行成功!');
			gopage('choose_list');
		}else{
			alert(datas.erro);
		}
	});
}

function choose_d(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	data = {id:id};
	$.post('/home/choose_d/'+id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('执行成功!');
			gopage('history_list');
		}else{
			alert(datas.erro);
		}
	});
}

$( window ).hashchange(function() {
	var hash = location.hash;
});

$("#apply_item").live('pageshow', function() {
	var a = {display:"modal",lang:"zh",mode:"scroller",preset:"date",theme:"default"};
    $('#test_default').val('').scroller('destroy').scroller(a);
});


function login_out(){
	showConfirm('确定要退出登录吗？',function(ok){
		if(ok!=1){return false;}
		$.mobile.loading('show', {text : 'test', theme : 'a'});
		$.get('/home/login_out/',{},function(datas){
			$.mobile.loading('hide');
			if(datas.succeed){
				alert('注销成功');
				my_navigator = [];
				gopage('home/accounts');
			}else{
				alert(datas.erro);
			}
		});
	});
}



function update_choose_item(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#choose_item_form').serializeArray();
	$.post('/home/update_choose_item/'+id,data,function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('请求成功!');
			gopage('choose_list');
		}else{
			alert(datas.erro);
		}
	});
}


/* 分享 */
var share_requirment_page = {};
$("#share_requirment").live('pageshow', function() {
	share_requirment_init();
});


function share_requirment_init(){
  if(share_requirment_page.myScroll){
  		share_requirment_page.myScroll.destroy();
  	}
	
  var myScroll = new iScroll('share_requirment_wrapper',{});
  share_requirment_page.myScroll = myScroll;
}


var bijia_list_page = {};
$("#bijia_list").live('pageshow', function() {
	bijia_list_init();
});


function bijia_list_init(){
  if(bijia_list_page.myScroll){
  		bijia_list_page.myScroll.destroy();
  	}
	
  var myScroll = new iScroll('bijia_list_wrapper',{});
  bijia_list_page.myScroll = myScroll;
}

function share_requirment(id){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	var data = $('#choose_item_form').serializeArray();
	$.post('/home/share_requirment/'+id,{},function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('发布成功!');
			$('#requirment_'+id).html('状态:<span class="fb">已发布</spa>');
		}else{
			alert(datas.erro);
		}
	});
}

var bijia_detail_page = {};
$("#bijia_detail").live('pageshow', function() {
	bijia_detail_init();
});


function bijia_detail_init(){
  if(bijia_detail_page.myScroll){
  		bijia_detail_page.myScroll.destroy();
  	}
	
  var myScroll = new iScroll('bijia_detail_wrapper',{
  	onBeforeScrollStart : function(e){
	　　var nodeType = e.explicitOriginalTarget ? e.explicitOriginalTarget.nodeName.toLowerCase() : (e.target ? e.target.nodeName.toLowerCase() : '');
	　　if(nodeType != 'select' && nodeType != 'option' && nodeType != 'input' && nodeType != 'textarea'){
	　　 　　e.preventDefault();
	　　}
	}
  });
  bijia_detail_page.myScroll = myScroll;
}

function comment_ok(showcase_id){
	var comment_content = $('#comment_content').val();
		comment_content = $.trim(comment_content);
	if(!comment_content){alert('内容不能为空');return false;}
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	$.post('/home/comment/'+showcase_id,{content:comment_content},function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('发表成功!');
			gopage(my_navigator[my_navigator.length-1])
		}else{
			alert(datas.erro);
		}
	});
	
}


var bijia_casereplay_page = {};
$("#bijia_casereplay").live('pageshow', function() {
	
	if(bijia_casereplay_page.myScroll){
  		bijia_casereplay_page.myScroll.destroy();
  	}
	
	  var myScroll = new iScroll('bijia_casereplay_wrapper',{});
	  bijia_casereplay_page.myScroll = myScroll;

});

function bijia_casereplay_ok(data){
	var showcase_id = data.split(',')[0];
	var showcase_re_id  = data.split(',')[1];
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	$.post('/home/re_showcase/'+showcase_id+'/'+showcase_re_id,{},function(datas){
		$.mobile.loading('hide');
		if(datas.succeed){
			alert('比价成功!');
			go_back();
		}else{
			alert(datas.erro);
		}
	});
}

function clear_data(){
	window.localStorage.clear();
	alert('清除成功');
}

function check_update(){
	alert('已经是最新版本了')
}

$(function (){
	$('.place_text').live('focus',function(){
		if($(this).val()==$(this).attr('placeholder')){
			$(this).val('');
			$(this).css('color','');
		}
		
	});
	
	$('.place_text').live('blur',function(){
		if($(this).val()==''){
			$(this).val($(this).attr('placeholder'));
			$(this).css('color','#D1D1D1');
		}else{
			$(this).css('color','');
		}
		
	});
	
	$('.like_msg span').live('fastClick',function(el){
		var index = $(this).attr('v');
		for(var i=0;i<=4;i++){
			if(i<=index){
				$('.like_msg span').eq(i).find('img').attr('src','/static/images/star1.png')
			}else{
				$('.like_msg span').eq(i).find('img').attr('src','/static/images/star0.png')
			}
		}
		$('input[name=like]').val(1+ parseInt(index))
	})
})

$(function() {
	$.mobile.allowCrossDomainPages=true;
	if(is_init_main){return false;}
	 is_init_main =true;
	 init_main();
});

$(function(){
	setTimeout(function() {
		if(get_data('user_is_first')){
			 gopage('home/accounts');
		 }else{
			 gopage('home/loading');
		 	 set_data('user_is_first','false')
		 }
	}, 1000);
})



function befor_catalog_search(){
	var my_fee = $('#my_fee').val();
		my_fee = parseFloat(my_fee);
		if(my_fee){
			gopage('home/catalog_list/'+my_fee);
		}else{
			alert('请输入正确金额。');
		}
	
}

















