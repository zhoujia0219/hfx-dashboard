// 登录表单提交
function login(){
    var username = $("#username").val()
    var password = $("#password").val()
    var brand = $("#brand").val()

　　if(password == null || password == ''){
　　　　alert("密码不能为空!");
　　　　return false;
　　}
　　if(brand == null || brand == ''){
　　　　alert("品牌不能为空!");
　　　　return false;
　　}
　　if(username == null || username == ''){
　　　　alert("用户名不能为空!");
　　　　return false;
　　}
    // 发起登录请求
    var params = {
        "username": username,
        "password": password,
        "brand":brand
    }
    console.log(params)
    $.ajax({
        url: "http://127.0.0.1:8011/login",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(params),
        success: function (resp) {
            return false
        },
//        error:function(res){
//        }
    })
}