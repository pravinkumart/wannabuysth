

function login_out(){
	if(!confirm('确定退出登录？')){
		return false;
	}
	return true;
}



function reply(el,fee){
	if(!confirm('投标价格不能高于该消费者的报价，若要继续投标请等于或低于'+fee+'元')){
		return false;
	}
	var my_fee = window.prompt('请输入投标金额');
		my_fee = parseFloat(my_fee);
		if(!my_fee||my_fee>fee){alert('金额错误');return false;}
	var url = $(el).attr('href')+'?my_fee='+my_fee;
	$(el).attr('href',url);
	return true;
}

