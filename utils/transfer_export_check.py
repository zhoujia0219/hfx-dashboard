"""
数据导入导出页面的校验逻辑文件
"""
from pyparsing import basestring
from services.srv_sales_bymonth import default_dbname
from utils.clickhouse_conn import clickHouseConn
from utils.db_util import just_execute
from typing import List, Dict


class dataToImportFYJH(object):
    """
    费用计划数据导入类：文件验证（公共和私有），数据验证（公共和私有），数据入库
    """

    def __init__(self):
        self.sql = ''  # sql字符串
        self.flag_has_first = True  # 是否是第一条数据
        self.clickhouse = clickHouseConn()  # clickhouse得连接client

    @staticmethod
    def check_file_data(file_row_data: list, row_num: int) -> List:
        """
        校验excel的每一行数据是否合格
        params file_row_data:每行数据，列表形式
               row_num:行数，从1开始计算的，此处为2表示表头是第一行
               table_name_key:用的哪一组数据表的信息键

        return:1.是否通过（True，False），2.未通过时候的原因
        """
        # 校验数据列数是否足够
        if len(file_row_data) < 7:
            return [False, "文件中缺少【%s】列!" % (7 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [basestring, basestring, basestring, basestring, basestring, basestring, int]
        for index, data in enumerate(file_row_data):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[3][index])]
        return [True, "OK!"]

    def check_fyjh(self, table) -> Dict:
        """
        费用计划处理数据验证后拼接sql
        params table:加载的excel数据
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if self.flag_has_first:
                # 第一条数据创建插入语句
                self.sql = """
               insert into  chunbaiwei.data_transfer (column_1,column_2,column_3,column_4,column_5,column_6,column_7,column_8) 
                          values {}
                  """.format(tuple(current_row_data[0:8]))
                self.flag_has_first = False
            else:
                self.sql += ','
                self.sql += '{}'.format(tuple(current_row_data[0:8]))  # 对后续的数据拼接到插入语句
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql}

    def main(self, table, file) -> Dict:
        """
        brand数据入库
        """
        sql_str = self.check_fyjh(table)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            # 当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            just_execute(sql_str["sql"], default_dbname)  # 执行批量插入
            print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}


class dataToImportBrand(object):
    """
    品牌数据导入类：文件验证（公共和私有），数据验证（公共和私有），数据入库
    """

    def __init__(self):
        self.sql = ''  # sql字符串
        self.flag_has_first = True  # 是否是第一条数据
        self.clickhouse = clickHouseConn()  # clickhouse得连接client

    @staticmethod
    def check_file_data(file_row_data: list, row_num: int) -> List:
        """
        校验excel的每一行数据是否合格
        params file_row_data:每行数据，列表形式
               row_num:行数，从1开始计算的，此处为2表示表头是第一行
               table_name_key:用的哪一组数据表的信息键

        return:1.是否通过（True，False），2.未通过时候的原因
        """
        # table_key_data = self.table_field_info[table_name_key]
        # 校验数据列数是否足够
        if len(file_row_data) < 7:
            return [False, "文件中缺少【%s】列!" % (7 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [basestring, basestring, basestring, basestring, basestring, basestring, int]
        for index, data in enumerate(file_row_data):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[3][index])]
        return [True, "OK!"]

    def check_brand(self, table) -> Dict:
        """
        品牌验证
        params table:加载的excel数据
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if self.flag_has_first:
                # 第一条数据创建插入语句
                self.sql = """
                       INSERT INTO cdp.pdim_brand (brand_code,std_brand_code,db_schema,brand_name,trade_code,company_code,version_time)
            VALUES {}
                  """.format(tuple(current_row_data[0:7]))
                self.flag_has_first = False
            else:
                self.sql += ','
                self.sql += '{}'.format(tuple(current_row_data[0:7]))  # 对后续的数据拼接到插入语句
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql}

    def main(self, table, file) -> Dict:
        """
        brand数据入库
        """
        sql_str = self.check_brand(table)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            # 3.当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            self.clickhouse.execute_sql(sql_str["sql"])  # 执行批量插入
            print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}
