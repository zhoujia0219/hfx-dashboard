import os
import time
import xlrd
import xlwt
from flask import request

from utils.db_util import just_execute, query_list
from utils.transfer_export_check import dataToLead, EXPORT_LOAD_TABLENAME_FIELD

default_dbname = "data_analysis"


def to_lead_view():
    """
    数据导入视图
    """
    data_to_lead = dataToLead()  # 创建数据导入类对象
    file = request.files.get('file')
    table_key = 'fyjh'  # 将决定是用哪组数据库表数据
    file_status, msg = data_to_lead.check_file_transfer_excel(file)
    if not file_status:
        return {"code": 0, "msg": "文件格式错误!"}
    # 1.加载excel的数据
    f = file.read()
    clinic_file = xlrd.open_workbook(file_contents=f)
    table = clinic_file.sheet_by_index(0)
    # 2.对相应的导入做逻辑处理(每一行的数据验证+验证之后所需执行的sql拼接)
    if table_key == 'fyjh':
        sql_str = data_to_lead.fyjh(table)
        if sql_str['code'] == 0:
            # 验证失败
            return {"code": 0, "msg": sql_str['msg']}
        try:
            # 3.当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            just_execute(sql_str["sql"], default_dbname)  # 执行批量插入
        except:
            return {"code": 0, "msg": "数据库错误!"}
    print('文件【%s】导入成功' % file.filename)
    return {"code": 1, "msg": "导入成功！"}


def export_data_view():
    """
    数据导出视图
    """
    try:
        # 拼接路径
        parama_dict = request.form
        file_path = parama_dict.get("file_path")
        file_path = file_path + r'fyjh_{}.xls'.format(int(time.time()))

        table_key = 'fyjh'  # 将决定是用哪组数据库表数据
        filed_str = ''  # sql字符串中的字段字符串
        excel_header = EXPORT_LOAD_TABLENAME_FIELD[table_key][4]  # 表头
        for i in EXPORT_LOAD_TABLENAME_FIELD[table_key][1]:
            # 拼接sql中的字段组成
            if filed_str:
                filed_str += ','
                filed_str += i
            else:
                filed_str += i
        # 1.查询数据
        sql = """
               select {} from chunbaiwei.{} 
           """.format(filed_str, EXPORT_LOAD_TABLENAME_FIELD[table_key][0])  # sql字符串
        all_data = query_list(sql, default_dbname)
        # 2.创建表格
        new_workbook = xlwt.Workbook()
        worksheet = new_workbook.add_sheet("sheet1")  # 创建sheet
        # 3.写入数据
        for row in range(len(all_data) + 1):  # 数据的行数+表头行
            for col in range(len(excel_header)):  # 列
                if row == 0:
                    worksheet.write(row, col, excel_header[col])  # 写入表头
                else:
                    worksheet.write(row, col, all_data[row - 1][col])  # 写入数据
        # 4.保存excel
        new_workbook.save(file_path)
        return {"code": 1, "msg": "导出成功！"}
    except:
        return {"code": 0, "msg": "文件导出错误！"}
