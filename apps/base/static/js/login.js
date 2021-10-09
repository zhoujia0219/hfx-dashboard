//// 登录表单提交
//$(".login_form_con").submit(function (e) {
//    e.preventDefault()
//    var username = $(".login_form #username").val()
//    var passport = $(".login_form #password").val()
//
//    if (!username) {
//        $("#login-mobile-err").show();
//        return;
//    }
//
//    if (!passport) {
//        $("#login-password-err").show();
//        return;
//    }
//
//    // 发起登录请求
//    var params = {
//        "mobile": mobile,
//        "passport": passport
//    }
//
//    $.ajax({
//        url: "http://127.0.0.1:8011/login1",
//        type: "post",
//        contentType: "application/json",
//        data: JSON.stringify(params),
//        success: function (resp) {
//            if (resp.errno == "0") {
//                // 代表登录成功
//                window.location.href="http://127.0.0.1:8011/"
//            }else {
//                alert(resp.errmsg)
//                $("#login-password-err").html(resp.errmsg)
//                $("#login-password-err").show()
//            }
//        }
//    })
//})