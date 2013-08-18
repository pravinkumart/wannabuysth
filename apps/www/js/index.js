

$(function(){
	help_init() //帮助页面
})

function help_init(){
  var obj = $('#wrapper_help');
  var width = $(window).width();
  var count = obj.find('.thelist li').length;
  	  obj.find('.thelist li').width(width);
  	  obj.find('.scroller').width(count*width);
  var myScroll = new iScroll('wrapper_help',{
    snap: true,
    momentum: false,
    hScrollbar: false
  });
	
}
