// 导入
$(function () {
           $("#btn_uploadimg1").click(function () {
               var fileObj = document.getElementById("FileUpload1").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               $.ajax({
                   url: "/to_import/",
                   data: data,
                   type: "Post",
                   dataType: "text",
                   cache: false,//上传文件无需缓存
                   processData: false,//用于对data参数进行序列化处理 这里必须false
                   contentType: false, //必须
                   success: function (result) {
                       alert("导入完成!");
                   },
               })
           })
       })

// 导出
function export_data(){
    // 发起导出请求
                var params = {
                    "file_path": 'C:\\Users\\ruipos\\Desktop\\',
                }
            $.ajax({
                    type: 'POST',
                    url: "/export_data/",
                    data: params,
                    dataType: 'text',
                    success: function (resp) {
                            alert('导出成功！');
//                    alert(resp)
//                    alert(resp.code)
                            return false
                        },

            });


}
