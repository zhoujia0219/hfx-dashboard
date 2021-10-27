"""
数据导入导出页面的校验逻辑文件
"""
from pyparsing import basestring
from services.srv_to_import import pay_mode_all_data_other, pay_channel_all_data_other
from utils.clickhouse_conn import clickHouseConn
from typing import List, Dict


class dataImportPayMode(object):
    """
    支付方式导入类
    """

    def __init__(self):
        self.sql = ''  # sql插入字符串
        self.update_sql_list = []  # sql 更新字符串列表
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
        if len(file_row_data) < 2:
            return [False, "文件中缺少【%s】列!" % (2 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [int, basestring]
        for index, data in enumerate(file_row_data[0:2]):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[index])]
        return [True, "OK!"]

    def join_insert_sql(self, current_row_data):
        """
        拼接批量插入的sql
        """
        if self.flag_has_first:
            # 第一条数据创建插入语句
            self.sql = """
                   INSERT INTO cdp.cdim_pay_mode (pay_mode_code,pay_mode_name)
            VALUES {}
              """.format(tuple(current_row_data[0:2]))
            self.flag_has_first = False
        else:
            self.sql += ','
            self.sql += '{}'.format(tuple(current_row_data[0:2]))  # 对后续的数据拼接到插入语句

    def check_pay_mode(self, table, pay_mode_data, import_mode, pay_mode_other) -> Dict:
        """
        支付方式验证
        params table:加载的excel数据
                pay_mode_data:支付方式的数据
                import_mode：导入方式，1表示有的替换导入，2表示有的数据则跳过，其他默认是增加，3表示报错
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)[0:2]  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if import_mode in [1, '1']:
                # 已经有该编码数据并且支付方式修改了
                if (str(int(current_row_data[0])),) in pay_mode_data:
                    if (current_row_data[1],) not in pay_mode_other:
                        update_sql_str = """
                            ALTER TABLE cdp.cdim_pay_mode UPDATE pay_mode_name = '{}' WHERE pay_mode_code='{}'
                        """.format(current_row_data[1], str(int(current_row_data[0])))
                        self.update_sql_list.append(update_sql_str)
                # 没有该编码
                if (str(int(current_row_data[0])),) not in pay_mode_data:
                    self.join_insert_sql(current_row_data)
            elif import_mode in [2, '2']:
                # 忽略跳过
                if (str(int(current_row_data[0])),) not in pay_mode_data:
                    self.join_insert_sql(current_row_data)
            else:
                # 报错
                if (str(int(current_row_data[0])),) in pay_mode_data:
                    print("有重复值不支持导入!")
                    return {"code": 0, "msg": "有重复值不支持导入！"}
                self.join_insert_sql(current_row_data)
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql, "update_sql_list": self.update_sql_list}

    def main(self, table, file, pay_mode_data, import_mode) -> Dict:
        """
        数据入库
        """
        pay_mode_other = pay_mode_all_data_other()
        sql_str = self.check_pay_mode(table, pay_mode_data, import_mode, pay_mode_other)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            if sql_str["update_sql_list"]:
                for update_sql in sql_str["update_sql_list"]:
                    self.clickhouse.execute_sql(update_sql)  # 执行更新

            # 当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            if sql_str["sql"]:
                self.clickhouse.execute_sql(sql_str["sql"])  # 执行批量插入
                print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}


class dataImportPayChannel(object):
    """
    支付渠道导入类
    """

    def __init__(self):
        self.sql = ''  # sql插入字符串
        self.update_sql_list = []  # sql 更新字符串列表
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
        if len(file_row_data) < 2:
            return [False, "文件中缺少【%s】列!" % (2 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [int, basestring]
        for index, data in enumerate(file_row_data[0:2]):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[index])]
        return [True, "OK!"]

    def join_insert_sql(self, current_row_data):
        """
        拼接批量插入的sql
        """
        if self.flag_has_first:
            # 第一条数据创建插入语句
            self.sql = """
                   INSERT INTO cdp.cdim_pay_channel (pay_channel_code,pay_channel_name)
            VALUES {}
              """.format(tuple(current_row_data[0:2]))
            self.flag_has_first = False
        else:
            self.sql += ','
            self.sql += '{}'.format(tuple(current_row_data[0:2]))  # 对后续的数据拼接到插入语句

    def check_pay_channel(self, table, pay_channel_data, import_mode, pay_channel_other) -> Dict:
        """
        支付方式验证
        params table:加载的excel数据
                pay_channel_data:支付方式的数据
                import_channel：导入方式，1表示有的替换导入，2表示有的数据则跳过，其他默认是增加，3表示报错
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)[0:2]  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if import_mode in [1, '1']:
                # 已经有该编码数据并且支付方式修改了
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    if (current_row_data[1],) not in pay_channel_other:
                        update_sql_str = """
                            ALTER TABLE cdp.cdim_pay_channel UPDATE pay_channel_name = '{}' WHERE pay_channel_code='{}'
                        """.format(current_row_data[1], str(int(current_row_data[0])))
                        self.update_sql_list.append(update_sql_str)
                # 没有该编码
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            elif import_mode in [2, '2']:
                # 忽略跳过
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            else:
                # 报错
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    print("有重复值不支持导入!")
                    return {"code": 0, "msg": "有重复值不支持导入！"}
                self.join_insert_sql(current_row_data)
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql, "update_sql_list": self.update_sql_list}

    def main(self, table, file, pay_channel_data, import_mode) -> Dict:
        """
        数据入库
        """
        pay_channel_other = pay_channel_all_data_other()
        sql_str = self.check_pay_channel(table, pay_channel_data, import_mode, pay_channel_other)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            if sql_str["update_sql_list"]:
                for update_sql in sql_str["update_sql_list"]:
                    self.clickhouse.execute_sql(update_sql)  # 执行更新

            # 当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            if sql_str["sql"]:
                self.clickhouse.execute_sql(sql_str["sql"])  # 执行批量插入
                print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}


class dataImportCharge(object):
    """
    费用导入类
    """

    def __init__(self):
        self.sql = ''  # sql插入字符串
        self.update_sql_list = []  # sql 更新字符串列表
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
        if len(file_row_data) < 2:
            return [False, "文件中缺少【%s】列!" % (2 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [int, basestring]
        for index, data in enumerate(file_row_data[0:2]):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[index])]
        return [True, "OK!"]

    def join_insert_sql(self, current_row_data):
        """
        拼接批量插入的sql
        """
        if self.flag_has_first:
            # 第一条数据创建插入语句
            self.sql = """
                   INSERT INTO cdp.cdim_pay_channel (pay_channel_code,pay_channel_name)
            VALUES {}
              """.format(tuple(current_row_data[0:2]))
            self.flag_has_first = False
        else:
            self.sql += ','
            self.sql += '{}'.format(tuple(current_row_data[0:2]))  # 对后续的数据拼接到插入语句

    def check_pay_channel(self, table, pay_channel_data, import_mode, pay_channel_other) -> Dict:
        """
        支付方式验证
        params table:加载的excel数据
                pay_channel_data:支付方式的数据
                import_channel：导入方式，1表示有的替换导入，2表示有的数据则跳过，其他默认是增加，3表示报错
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)[0:2]  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if import_mode in [1, '1']:
                # 已经有该编码数据并且支付方式修改了
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    if (current_row_data[1],) not in pay_channel_other:
                        update_sql_str = """
                            ALTER TABLE cdp.cdim_pay_channel UPDATE pay_channel_name = '{}' WHERE pay_channel_code='{}'
                        """.format(current_row_data[1], str(int(current_row_data[0])))
                        self.update_sql_list.append(update_sql_str)
                # 没有该编码
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            elif import_mode in [2, '2']:
                # 忽略跳过
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            else:
                # 报错
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    print("有重复值不支持导入!")
                    return {"code": 0, "msg": "有重复值不支持导入！"}
                self.join_insert_sql(current_row_data)
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql, "update_sql_list": self.update_sql_list}

    def main(self, table, file, pay_channel_data, import_mode) -> Dict:
        """
        数据入库
        """
        pay_channel_other = pay_channel_all_data_other()
        sql_str = self.check_pay_channel(table, pay_channel_data, import_mode, pay_channel_other)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            if sql_str["update_sql_list"]:
                for update_sql in sql_str["update_sql_list"]:
                    self.clickhouse.execute_sql(update_sql)  # 执行更新

            # 当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            if sql_str["sql"]:
                self.clickhouse.execute_sql(sql_str["sql"])  # 执行批量插入
                print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}


class dataImportCustDistrict(object):
    """
    ⾃定义城市区划导入类
    """

    def __init__(self):
        self.sql = ''  # sql插入字符串
        self.update_sql_list = []  # sql 更新字符串列表
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
        if len(file_row_data) < 2:
            return [False, "文件中缺少【%s】列!" % (2 - len(file_row_data))]
        # 判断每条数据的数据格式是否正确
        field_type_list = [int, basestring]
        for index, data in enumerate(file_row_data[0:2]):
            # 如果是整型数据会在读取的时候变成float类型，所以需要转
            is_type_correct = isinstance(data,
                                         ((int, float) if field_type_list[index] == int else field_type_list[index]))
            if not is_type_correct:
                return [False, "第{}行第{}列应该是{}！".format(row_num, index + 1, field_type_list[index])]
        return [True, "OK!"]

    def join_insert_sql(self, current_row_data):
        """
        拼接批量插入的sql
        """
        if self.flag_has_first:
            # 第一条数据创建插入语句
            self.sql = """
                   INSERT INTO cdp.cdim_pay_channel (pay_channel_code,pay_channel_name)
            VALUES {}
              """.format(tuple(current_row_data[0:2]))
            self.flag_has_first = False
        else:
            self.sql += ','
            self.sql += '{}'.format(tuple(current_row_data[0:2]))  # 对后续的数据拼接到插入语句

    def check_pay_channel(self, table, pay_channel_data, import_mode, pay_channel_other) -> Dict:
        """
        支付方式验证
        params table:加载的excel数据
                pay_channel_data:支付方式的数据
                import_channel：导入方式，1表示有的替换导入，2表示有的数据则跳过，其他默认是增加，3表示报错
        return:
            {"code":0,msg:"","sql"}
            当通过校验则返回code为1,sql为拼接的sql字符串
            校验失败,则返回code为0,msg为未通过原因
        """
        for row_num in range(1, table.nrows):
            current_row_data = table.row_values(row_num)[0:2]  # 列表形式的每一行数据
            check_result_list = self.check_file_data(current_row_data, row_num + 1)  # 校验数据,返回的是True或False,校验结果信息字符串
            if not check_result_list[0]:  # 校验未通过
                return {"code": 0, "msg": check_result_list[1]}
            if import_mode in [1, '1']:
                # 已经有该编码数据并且支付方式修改了
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    if (current_row_data[1],) not in pay_channel_other:
                        update_sql_str = """
                            ALTER TABLE cdp.cdim_pay_channel UPDATE pay_channel_name = '{}' WHERE pay_channel_code='{}'
                        """.format(current_row_data[1], str(int(current_row_data[0])))
                        self.update_sql_list.append(update_sql_str)
                # 没有该编码
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            elif import_mode in [2, '2']:
                # 忽略跳过
                if (str(int(current_row_data[0])),) not in pay_channel_data:
                    self.join_insert_sql(current_row_data)
            else:
                # 报错
                if (str(int(current_row_data[0])),) in pay_channel_data:
                    print("有重复值不支持导入!")
                    return {"code": 0, "msg": "有重复值不支持导入！"}
                self.join_insert_sql(current_row_data)
            row_num += 1
        return {"code": 1, "msg": 'OK!', "sql": self.sql, "update_sql_list": self.update_sql_list}

    def main(self, table, file, pay_channel_data, import_mode) -> Dict:
        """
        数据入库
        """
        pay_channel_other = pay_channel_all_data_other()
        sql_str = self.check_pay_channel(table, pay_channel_data, import_mode, pay_channel_other)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            if sql_str["update_sql_list"]:
                for update_sql in sql_str["update_sql_list"]:
                    self.clickhouse.execute_sql(update_sql)  # 执行更新

            # 当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            if sql_str["sql"]:
                self.clickhouse.execute_sql(sql_str["sql"])  # 执行批量插入
                print('文件【%s】导入成功' % file.filename)
            return {"code": 1, "msg": "数据库导入成功!"}
        except:
            print("导入数据库失败")
            return {"code": 0, "msg": "数据库错误!"}
