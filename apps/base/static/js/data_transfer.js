// 导入
function to_lead(){
        var objFile = document.getElementById("id1");
        if(objFile.value == "") {
            alert("请先选择文件！")
        }
        console.log(objFile.files[0].size); // 文件字节数
        var files = $('#id1').prop('files');//获取到文件列表
        if(files.length == 0){
            alert('请选择文件');
        }else{
            var reader = new FileReader();//新建一个FileReader
            reader.readAsText(files[0], "UTF-8");//读取文件
            reader.onload = function(evt){ //读取完文件之后会回来这里
                var fileString = evt.target.result; // 读取文件内容
                alert(fileString)

                $.ajax({
                url: "/data_transfe/",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify(fileString),
                success: function (resp) {
                },
                error:function(res){
                }
            })

        }
    }

}

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
