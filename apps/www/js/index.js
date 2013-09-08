var www = 'http://192.168.1.251:8000/';
var index_page = {};
var is_init_main = false;
var pre_domin = ''; //强制指定后退回到的页面
//$.mobile.changePage($.mobile.activePage.jqmData('url'),{reloadPage :true});
//jQuery( ".selector" ).on( "pagechangefailed", function( event ) { ... } )
$(document).bind('pageinit',function() {
	$.mobile.allowCrossDomainPages=true;
	if(is_init_main){return false;}
	is_init_main =true;
	init_main();
});

document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
	window.device.overrideBackButton();
	document.addEventListener("backbutton", function(){
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
		$.mobile.loading('show', {text : 'test', theme : 'a'});
		if(pre_domin){
			gopage(pre_domin);
			pre_domin = '';
		}else{
			$.mobile.back();
		}
		return false;
	})
}

$("#loading").bind('pageshow', function() {
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	pre_domin = 'accounts'
	gopage('help')
	// gopage('home/help')
});

// $(document).bind('pagebeforechange',function(e,data){ 
	// console.log(e)
// }); 
function getPicture(){
	navigator.camera.getPicture(onSuccess, onFail, { quality: 50,
	    destinationType: Camera.DestinationType.DATA_URL
	});
}

function onSuccess(imageData) {
    var image = document.getElementById('myImage');
    image.src = "data:image/jpeg;base64," + imageData;
}

function onFail(message) {
    alert('Failed because: ' + message);
}


function gopage(page_id,changeHash){
	$.mobile.loading('show', {text : 'test', theme : 'a'});
	if(page_id.indexOf('home')==-1){
		page_id = 'home/'+page_id
	}
	$.mobile.changePage(www+page_id+'.html?v='+(new Date()).getTime(),{
			transition:'slide'
		})
}

$("#index").live('pageshow', function() {
	index_init()
});
function index_init(){
  get_index_types_data()
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

//首页类型数据填充
function get_index_types_data(){
	var html = ''
	
	
}

function accounts_init(){
	$('.vertical').height($(window).height());
	
}

function login_ok(){
	alert('....')
}
function regedit_ok(){
	alert('.....')
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
	
  var myScroll = new iScroll('item_list_wrapper',{
  	
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
  item_list_page.myScroll = myScroll;
}

/* 购买列表 */
var sell_list_page = {}
$("#sell_list").live('pageshow', function() {
	sell_list_init()
});


function sell_list_init(){
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