function showCheck(a){
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
	ctx.clearRect(0,0,1000,1000);
	ctx.font = "80px 'Microsoft Yahei'";
	ctx.fillText(a,0,100);
	ctx.fillStyle = "white";
}

function createCode(){
    $.ajax({
        url: '/admin/code',
        type: 'POST',
        dataType: 'json',
        success: function (e) {
            if (e.code === 200) {
                showCheck(e.checkcode)
            } else {
                showCheck("error")
            }
        }
    })
}