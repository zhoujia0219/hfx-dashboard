// 导入
//function uploadPicture(obj) {
//    var file = $(obj).attr("id");
//    alert(file)
//                        $.ajax({
//                        url: "/data_transfe/",
//                        type: "post",
//                        contentType: "application/json",
//                        data: file,
////                        data:  JSON.stringify(params),
//                        success: function (resp) {
//                            return false
//                        },
//                        error:function(res){
//                        }
//                    })
//}
function to_lead(){
    var fileinfo = document.getElementById("uploadFile").files[0];
    alert(fileinfo);
//    var reader = new FileReader();
//    reader.readAsDataURL(fileinfo);
//    data = reader.result.split(",")[1]  #　这样才是完整的数据
    var params = {
        "a": 1,
    }
    $.ajax({
    url: "/data_transfe/",
    type: "post",
    contentType: "application/json",
//    data: file,
  data:JSON.stringify(params),
//  data:fileinfo,

    success: function (resp) {
        return false
    },
    error:function(res){
    }
})

//$("#upload").on("change",function(){
//        $.ajaxFileUpload({
//            url : '/data_transfe/',//后台请求地址
//            type: 'post',//请求方式  当要提交自定义参数时，这个参数要设置成post
//            secureuri : false,//是否启用安全提交，默认为false。
//            fileElementId : 'upload',// 需要上传的文件域的ID，即<input type="file">的ID。
//            dataType : 'json',//服务器返回的数据类型。可以为xml,script,json,html。如果不填写，jQuery会自动判断。如果json返回的带pre,这里修改为json即可解决。
//            success : function (json, status) {//提交成功后自动执行的处理函数，参数data就是服务器返回的数据。
//                  alert(json.retMsg);
//            },
//            error : function (json, status, e) {//提交失败自动执行的处理函数。
//
//            }
//        });
//    });
}




//function to_lead(){
//        var objFile = document.getElementById("id1");
//        if(objFile.value == "") {
//            alert("请先选择文件！")
//        }
//        console.log(objFile.files[0].size); // 文件字节数
//        var files = $('#id1').prop('files');//获取到文件列表
//        if(files.length == 0){
//            alert('请选择文件');
//        }else{
//            var reader = new FileReader();//新建一个FileReader
//            reader.readAsText(files[0], "UTF-8");//读取文件
//            reader.onload = function(evt){ //读取完文件之后会回来这里
//                var fileString = evt.target.result; // 读取文件内容
//                if (fileString.length!=0){
//                        alert(fileString)
//                        $.ajax({
//                        url: "/data_transfe/",
//                        type: "post",
//                        contentType: "application/json",
//                        data: JSON.stringify(fileString),
//                        success: function (resp) {
//                            return false
//                        },
//                        error:function(res){
//                        }
//                    })
//                }
//
//
//        }
//    }
//
//}

//function UpladFile(fileObj) {
//                var form = new FormData(); // FormData 对象
//                form.append("file", fileObj); // 文件对象
//                $.ajax({
//                    url: '/data_transfe/',                      //url地址
//                    type: 'POST',                 //上传方式
//                    data: form,                   // 上传formdata封装的数据
//                    dataType: 'JSON',
//                    cache: false,                  // 不缓存
//                    processData: false,        // jQuery不要去处理发送的数据
//                    contentType: false,         // jQuery不要去设置Content-Type请求头
//                    success:function (data) {           //成功回调
//                        console.log(data);
//                    },
//                   error:function (data) {           //失败回调
//                        console.log(data);
//                    }
//                });
//             }
//
//function to_lead() {
//    alert(131421)
//    $("#file").click();
//    $('#file').change(function (e) {
//     var fileName = e.target.files[0];//js 获取文件对象
//     if(fileName !== undefined){
//       var file_typename =   fileName.name.substring(fileName.name.lastIndexOf('.'));
//       if (file_typename === '.xlsx' || file_typename === '.xls') {
//        $("#filename").css("display","block");
//        $("#filename").val(fileName.name);
//       UpladFile(fileName);
//       }else {
//        console.log("请选择正确的文件类型！")
//        }
//     }else{
//   console.log("请选择正确的文件！")
//    }
//}

// 导出
function export_data(){

}

// function check() {
//
//        var objFile = document.getElementById("fileId");
//        if(objFile.value == "") {
//            alert("不能空")
//        }
//
//        console.log(objFile.files[0].size); // 文件字节数
//
//        var files = $('#fileId').prop('files');//获取到文件列表
//        if(files.length == 0){
//            alert('请选择文件');
//        }else{
//            var reader = new FileReader();//新建一个FileReader
//            reader.readAsText(files[0], "UTF-8");//读取文件
//            reader.onload = function(evt){ //读取完文件之后会回来这里
//                var fileString = evt.target.result; // 读取文件内容
//        }
//    }
//
//}
