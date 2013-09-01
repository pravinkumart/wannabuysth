var index_page = {};
var is_init_main = false;
$(document).bind('pageinit',function() {
	if(is_init_main){return false;}
	is_init_main =true;
	init_main();
});

function init_main(){
	$('.me_tap').live('tap',function(){
		var obj = $(this);
		var me_event = obj.attr('me_event');
		var me_data = obj.attr('me_data');
		if(!me_event){return false;}
		var me_event = eval(me_event);
			me_event(me_data)
		
	})
	$('.header_b').live('tap',function(){
		$.mobile.back();
		return false;
	})
}

$("#accounts").bind('pageinit', function() {
	gopage('home/my_keeper')
	// gopage('home/help')
});

$(document).bind('pagebeforechange',function(e,data){ 
	console.log(e)
}); 

function gopage(page_id){
	$.mobile.changePage(page_id+'.html',{transition:'slide'})
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