"""
数据导入导出页面的校验逻辑文件
"""
from flask import jsonify
from pyparsing import basestring

# 数据导出导入的表名和字段名
EXPORT_LOAD_TABLENAME_FIELD = {
    "fyjh": ["data_transfer",  # 对应的数据表名
             ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6', 'column_7', 'column_8'],  # 数据库字段
             [int, int, int, basestring, int, int, basestring, int],  # 对应每个字段的python类型
             ['整数', '整数', '整数', '字符串', '整数', '整数', '字符串', '整数'],  # 类型的中文
             ["字段1", '字段2', '字段3', '字段4', '字段5', '字段6', '字段7', '字段8']  # excel表格数据中的表头
             ]
}


class dataToLead(object):
    """
    数据导入类
    """

    def __init__(self):
        self.table_field_info = EXPORT_LOAD_TABLENAME_FIELD  # 数据库的相关基本常量信息
        self.filed_str = ''  # sql字符串中的字段字符串
        self.sql = ''  # sql字符串
        self.flag_is_first = True  # 是否是第一条数据

    def check_file_transfer_excel(self, file):
        """
                校验excel文件一些验证是否合格,公共的检测方法
        params
        return:1.是否通过（True，False），2.未通过时候的原因
        """
        if file:  # 判断前端是否发送文件过来
            return False, '请选择文件!'
        file_name = file.filename  # 文件名
        if file_name.split('.')[1] not in ["xls", 'xlsx']:
            return False, "请选择正确格式的文件！"

        return True, ""

    def check_row_data(self, row_data, table_name_key, row_num):
        """
        校验excel的每一行数据是否合格,公共的检测方法
        params row_data:每行数据，列表形式
        params table_name_key:用的哪一组数据表的信息键
        params row_num:行数，从1开始计算的，此处为2表示表头是第一行
        return:1.是否通过（True，False），2.未通过时候的原因
        """
        table_key_data = self.table_field_info[table_name_key]
        # 校验数据列数是否足够
        if len(row_data) != len(table_key_data[1]):
            return False, "文件中缺少列"
        type_list = table_key_data[2]  # 一条数据对应的类型

        # 判断每条数据的数据格式是否正确
        for index, data in enumerate(row_data):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data, ((int, float) if type_list[index] == int else type_list[index]))
            if not is_type_correct:
                return False, "第{}行第{}列应该是{}！".format(row_num, index + 1, table_key_data[3][index])

        return True, "OK!"

    def fyjh(self, table):
        """
        费用计划处理
        params table:加载的excel数据
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row = table.row_values(row_num)  # 列表形式的每一行数据
            check_data, msg = self.check_row_data(current_row, 'fyjh', row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_data:  # 校验未通过
                return {"code": 0, "msg": msg}
                # return render_template('data_transfer.html', data={"code": 0, "msg": msg})
            if self.flag_is_first:
                # 第一条数据创建插入语句
                self.sql = """
                      insert into  chunbaiwei.data_transfer (column_1,column_2,column_3,column_4,column_5,column_6,column_7,column_8) 
                          values {}
                  """.format(tuple(current_row))
                self.flag_is_first = False
            else:
                self.sql += ','
                self.sql += '{}'.format(tuple(current_row))  # 对后续的数据拼接到插入语句
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql}
