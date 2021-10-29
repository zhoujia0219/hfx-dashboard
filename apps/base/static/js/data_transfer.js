// 导入 1.自定义城市区划
// 替换导入
$(function () {
           $("#btn_uploadimg11").click(function () {
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
               var res = {
                    "file":data,
                    "table_key":"CustDistrict"
               }
               $.ajax({
                   url: "/to_import/CustDistrict_1",
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
//忽略导入
$(function () {
           $("#btn_uploadimg12").click(function () {
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
               var res = {
                    "file":data,
                    "table_key":"CustDistrict"
               }
               $.ajax({
                   url: "/to_import/CustDistrict_2",
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
//不重复导入
$(function () {
           $("#btn_uploadimg13").click(function () {
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
               var res = {
                    "file":data,
                    "table_key":"CustDistrict"
               }
               $.ajax({
                   url: "/to_import/CustDistrict_3",
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

// 导入 2.支付渠道
// 替换导入
$(function () {
           $("#btn_uploadimg21").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"payChannel "
               }
               $.ajax({
                   url: "/to_import/payChannel_1",
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
//忽略导入
$(function () {
           $("#btn_uploadimg22").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"payChannel"
               }
               $.ajax({
                   url: "/to_import/payChannel_2",
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
//不重复导入
$(function () {
           $("#btn_uploadimg23").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"payChannel"
               }
               $.ajax({
                   url: "/to_import/payChannel_3",
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

// 导入 3.支付方式
// 替换导入
$(function () {
           $("#btn_uploadimg31").click(function () {
               var fileObj = document.getElementById("FileUpload3").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"PayMode"
               }
               $.ajax({
                   url: "/to_import/PayMode_1",
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
//忽略导入
$(function () {
           $("#btn_uploadimg32").click(function () {
               var fileObj = document.getElementById("FileUpload3").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"PayMode"
               }
               $.ajax({
                   url: "/to_import/PayMode_2",
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
//不重复导入
$(function () {
           $("#btn_uploadimg33").click(function () {
               var fileObj = document.getElementById("FileUpload3").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"PayMode"
               }
               $.ajax({
                   url: "/to_import/PayMode_3",
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

// 导入 4.费用
// 替换导入
$(function () {
           $("#btn_uploadimg41").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"Charge"
               }
               $.ajax({
                   url: "/to_import/Charge_1",
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
//忽略导入
$(function () {
           $("#btn_uploadimg42").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"Charge"
               }
               $.ajax({
                   url: "/to_import/Charge_2",
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
//不重复导入
$(function () {
           $("#btn_uploadimg43").click(function () {
               var fileObj = document.getElementById("FileUpload2").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象

               // ajax 提交
               var data = formFile;
               var res = {
                    "file":data,
                    "table_key":"Charge"
               }
               $.ajax({
                   url: "/to_import/Charge_3",
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



// 导出1.自定义城市区划
function export_data1(){
    // 发起导出请求
                var params = {
                    "file_path": 'C:\\Users\\ruipos\\Desktop\\',
                }
            $.ajax({
                    type: 'POST',
                    url: "/export_data/CustDistrict",
                    data: params,
                    dataType: 'text',
                    success: function (resp) {
                            alert('导出成功！');
                            return false
                        },
            });
}
// 导出2.支付渠道
function export_data2(){
    // 发起导出请求
                var params = {
                    "file_path": 'C:\\Users\\ruipos\\Desktop\\',
                }
            $.ajax({
                    type: 'POST',
                    url: "/export_data/payChannel",
                    data: params,
                    dataType: 'text',
                    success: function (resp) {
                                        alert(resp);
                            alert('导出成功！');
                            return false
                        },
            });
}
// 导出3.支付方式
function export_data3(){
    // 发起导出请求
                var params = {
                    "file_path": 'C:\\Users\\ruipos\\Desktop\\',
                }
            $.ajax({
                    type: 'POST',
                    url: "/export_data/PayMode",
                    data: params,
                    dataType: 'text',
                    success: function (resp) {
                            alert('导出成功！');
                            return false
                        },
            });
}
// 导出4.费用
function export_data4(){
    // 发起导出请求
                var params = {
                    "file_path": 'C:\\Users\\ruipos\\Desktop\\',
                }
            $.ajax({
                    type: 'POST',
                    url: "/export_data/Charge",
                    data: params,
                    dataType: 'text',
                    success: function (resp) {
                            alert('导出成功！');
                            return false
                        },
            });
}