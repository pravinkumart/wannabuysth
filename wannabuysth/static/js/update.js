var last_version = '1.1.0';

function update_verson(){
	var request_url = 'http://app.bangban.com/app';
	if(last_version>Version){
			showConfirm("发现新版本"+last_version+',是否升级?',function(ok){
			if(ok!=1){return false;}
				window.open(request_url, "_system");
			});
		};
	
};


$(function(){
	setTimeout(update_verson,3000);
});
