

function login_out(){
	if(!confirm('确定退出登录？')){
		return false;
	}
	return true;
}

function filter_re(el,index){
	var min = $('#min_val').val();
	var max = $('#max_val').val();
	var url = '/mc/requirment/0?min='+min+'&max='+max+'&index='+index;
	$(el).attr('href',url);
	return true;
	
}

function reply(el,id,fee){
	var my_fee = $('#reply_'+id).val();
		my_fee = parseFloat(my_fee);
		if(!my_fee||my_fee>fee){alert('金额错误');return false;}
	var url = $(el).attr('href')+'?my_fee='+my_fee;
	$(el).attr('href',url);
	return true;
}

function get_or_create_id(el){
	var obj = jQ(el).eq(0);
	var id = obj.attr('id');
	if(id){return id;}
	var id = 'auto_'+(new Date()).getTime();
		obj.attr('id',id);
	return id;
}

function auto_img(el){
	function callback(data){
		if(data.succeed){
			var id = $(el).attr('for_ref');
			$('#'+id+'_value').val(data.erro);
			$('#'+id+'_show').attr('src',data.erro);
		}
	}
	upload_img(el,callback);
}

function upload_img(el,callback){
	var id = get_or_create_id(el);
	$.ajaxFileUpload({
          url:'/mc/update_img', 
          secureuri:true,
          fileElementId:id,
          type:'POST',
          dataType:'content',
          success: function (data, status) {
          	var start = data.indexOf(">");   
	             if(start != -1) {   
	               var end = data.indexOf("<", start + 1);   
	               if(end != -1) {   
	                 data = data.substring(start + 1, end);   
	                }   
	             }   
             eval( "data = " + data);   
          	callback(data);
          },
          error:function(data){
          	callback(data);
          }});
}

function add_product_img(el){
	function callback(data){
		if(data.succeed){
			$('#cropbox_wap').show();
			$('#cropbox').attr('src',data.erro);
			$('#icon_large').val(data.erro);
			show_crop(data.erro);
			var img_info = cropbox.getWidgetSize();
	    	// if((img_info[0]>200)&&(img_info[1]>120)){
	    		// $('#icon_large').val(data.erro);
	    	// }else{
	    		// alert('图片太小，请重新上传');
	    	// }
		}
	}
	upload_img(el,callback);
}


var  cropbox = null;
	    
function show_crop(src){
	if(cropbox){
		cropbox.setImage(src);
		return false;
	}
   	var jcrop_api, boundx, boundy;
   	
   	function update_crop(c)
		{
		  if (parseInt(c.w) > 0)
		  {
			var rx = 100 / c.w;
			var ry = 100 / c.h;
		
			$('#preview').css({
			  width: Math.round(rx * boundx) + 'px',
			  height: Math.round(ry * boundy) + 'px',
			  marginLeft: '-' + Math.round(rx * c.x) + 'px',
			  marginTop: '-' + Math.round(ry * c.y) + 'px'
			});
		
			$("#crop_x").val(Math.round(c.x));
			$("#crop_y").val(Math.round(c.y));
			$("#crop_w").val(Math.round(c.w));
			$("#crop_h").val(Math.round(c.h));
		  }
		};

    $('#cropbox').Jcrop({
	      onChange: update_crop,
	      onSelect: update_crop,
	      aspectRatio:100/60,
	      minSize: [200,120],
	      maxSize:[200,120],
	      allowResize:false,
    }, function(){
    	cropbox = this;
    });
  }


function alert(msg){
	$('#alertTest .modal-body').html(msg);
	$('#alertTest').modal({
	    backdrop:true,
	    keyboard:true,
	    show:true
	});
}
