var index_page = {}
$(document).ready(function() {
    help_init() //帮助页面nts_init() //登录注册选择页面
	//index_init() 
});

$(document).bind('pageinit', function() {
	// myScroll.refresh()
});

$(document).bind('pageshow', function() {
	
});
function gopage(page_id){
	$.mobile.changePage(page_id,{transition:'slide'})
}
function help_init(){
	 $('#help_href').click();
}

$("#index").live("pagecreate",function(){
 	// index_init()
})
$("#index").bind('pageshow', function() {
	index_init()
	// myScroll.refresh()
});
function index_init(){
  get_index_types_data()
  var obj = $('#wrapper_index');
  var width = 230;
  var count = obj.find('.thelist li').length;
  	  obj.find('.thelist li').width(width);
  	  obj.find('.scroller').width(count*width);
  if(index_page.myScroll){
  		index_page.myScroll.refresh()
  		return false;
  	}
  var myScroll = new iScroll('wrapper_index',{
    snap: true,
    momentum: false,
    hScrollbar: false
  });
  index_page.myScroll = myScroll;
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
