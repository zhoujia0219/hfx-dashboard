// 登录表单提交
function login(){
    var username = $("#username").val()
    var password = $("#password").val()
    var brand = $("#brand").val()
    var verify_img = $("#verify_img").val()

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
        "verify_img": verify_img, // 验证码
        "brand":brand
    }
    console.log(params)
    $.ajax({
        url: "/login",
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

//验证码
//function verify_code(){
//    var params = {
//        "verify_img": verify_img,
//    }
//
//}



//var imageCodeId = ""
//function generateUUID(){
//         $.ajax({  // 验证码发给后端
//        url: "/verify_code/",
//        type: "get",
//        contentType: "application/json",
//        data: JSON.stringify(params),
//        success: function (resp) {
//            alert(111)
//            return resp
//        },
//        error:function(res){
//        alert(222)
//                    return resp
//
//        }
//    })
//}
//// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
//function generateImageCode() {
//    // 浏览器要发起图片验证码请求/image_code?imageCodeId=xxxxx
//    imageCodeId = generateUUID()
//    // 生成 url
//    var url = "/image_code?imageCodeId=" + imageCodeId
//    // 给指定img标签设置src,设置了地址之后，img标签就会去向这个地址发起请求，请求图片
//    $(".get_pic_code").attr("src", url)
//}


function change(){
    code=$("#code");
  // 验证码组成库
   var arrays=new Array(
       '1','2','3','4','5','6','7','8','9','0',
       'a','b','c','d','e','f','g','h','i','j',
       'k','l','m','n','o','p','q','r','s','t',
       'u','v','w','x','y','z',
       'A','B','C','D','E','F','G','H','I','J',
       'K','L','M','N','O','P','Q','R','S','T',
       'U','V','W','X','Y','Z'
       );
    codes='';// 重新初始化验证码
   for(var i = 0; i<4; i++){
   // 随机获取一个数组的下标
   var r = parseInt(Math.random()*arrays.length);
   codes += arrays[r];
  }
  // 验证码添加到input里
     code.val(codes);
    var params ={
        "code":codes
    }
    $.ajax({
        url: "/verify_code/",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(params),
        success: function (resp) {
            return false
        },
    })
  }

change();
code.click(change);
 //单击验证
$("#check").click(function(){
   var inputCode = $("#input").val().toUpperCase(); //取得输入的验证码并转化为大写
   console.log(inputCode);
  if(inputCode.length == 0) { //若输入的验证码长度为0
   alert("请输入验证码！"); //则弹出请输入验证码
  }
  else if(inputCode!=codes.toUpperCase()) { //若输入的验证码与产生的验证码不一致时
   alert("验证码输入错误!请重新输入"); //则弹出验证码输入错误
   change();//刷新验证码
   $("#input").val("");//清空文本框
  }else { //输入正确时
   alert("正确"); //弹出^-^
  }
});