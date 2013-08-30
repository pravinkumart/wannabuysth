var index_page = {}
$(document).ready(function() {
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
}

$("#accounts").bind('pageinit', function() {
	gopage('home/help')
});

$(document).bind('pageshow', function() {
	
});

$(document).bind('pagebeforechange',function(e,data){ 
	console.log(e)
}); 

function gopage(page_id){
	$.mobile.changePage(page_id+'.html',{transition:'slide'})
}

$("#index").live("pagecreate",function(){
 	 index_init()
})
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
