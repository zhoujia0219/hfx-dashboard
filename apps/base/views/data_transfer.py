import time
import xlrd
import xlwt
from flask import request

from conf.basic_const import IMPORT_EXPORT_TABLENAME_FIELD
from services.srv_to_import import pay_mode_all_data_code
from utils.clickhouse_conn import clickHouseConn
from utils.db_util import query_list
from utils.import_export_check import dataToImportFYJH, dataToImportBrand, dataImportPayMode

default_dbname = "data_analysis"

clickhouse = clickHouseConn()


def to_import_view(file, table_key, import_mode):
    """
    数据导入视图
    """
    # 1.文件参数的验证
    if not file:
        return {"code": 0, "msg": "请选择文件！"}
    if file.filename.split('.')[1] not in ["xls", 'xlsx']:
        return {"code": 0, "msg": "请选择正确格式的文件！"}

    # 2.加载文件数据
    file_data = file.read()
    clinic_file = xlrd.open_workbook(file_contents=file_data)
    table = clinic_file.sheet_by_index(0)

    # 3.对相应的导入做逻辑处理(每一行的数据验证+验证之后所需执行的sql拼接)
    result = {"code": 0, "msg": "参数错误！"}
    if table_key == 'fyjh':
        result = dataToImportFYJH().main(table, file)
    elif table_key == 'brand':
        result = dataToImportBrand().main(table, file)
    elif table_key == "PayMode":
        pay_mode_data = pay_mode_all_data_code()
        result = dataImportPayMode().main(table, file, pay_mode_data, import_mode)

    return result


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
        excel_header = IMPORT_EXPORT_TABLENAME_FIELD[table_key][2]  # 表头
        for i in IMPORT_EXPORT_TABLENAME_FIELD[table_key][1]:
            # 拼接sql中的字段组成
            if filed_str:
                filed_str += ','
                filed_str += i
            else:
                filed_str += i
        # 1.查询数据
        sql = """
               select {} from chunbaiwei.{} 
           """.format(filed_str, IMPORT_EXPORT_TABLENAME_FIELD[table_key][0])  # sql字符串
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
