// 导入
function to_lead(){
    $(function () {
               $("#btn_uploadimg1").click(function () {
                   var fileObj = document.getElementById("FileUpload1").files[0]; // js 获取文件对象
                   if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                       alert("请选择图片");
                       return;
                   }
                   var formFile = new FormData();
                   formFile.append("action", "UploadVMKImagePath");
                   formFile.append("file", fileObj); //加入文件对象

                   // ajax 提交
                   var data = formFile;
                   $.ajax({
                       url: "/data_transfe/",
                       data: data,
                       type: "Post",
                       dataType: "json",
                       cache: false,//上传文件无需缓存
                       processData: false,//用于对data参数进行序列化处理 这里必须false
                       contentType: false, //必须
                       success: function (result) {
                       if (result.code==1){

                       alert(result.msg)
                       }else{
                        alert(0)
                       }

                       alert(result);
                           alert("上传完成!");
                       },
                   })
               })
           })
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
