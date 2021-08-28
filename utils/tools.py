# 其他的类型工具
from copy import copy


def big_number_conduct(numb, decimal_point: int):
    """大的数字的处理
    param numb:传入的数字
    param decimal_point:保留小数的位数
    return:带单位万或者亿的字符串
    """
    try:
        result = float(copy(numb))
    except Exception:
        return numb
    numb_constant = float(copy(numb))
    million_1 = 1000000  # 100万
    million_100 = 100000000  # 1亿
    # 先处理成为万的单位(小于1亿大于等于1百万)
    if numb_constant < million_100 and numb_constant >= million_1:
        result = format(round((numb_constant / 10000), decimal_point), ',') + "万"
        result = result if len(result.split('.')[1]) == decimal_point + 1 else result.replace("万", '0' * (
                decimal_point - (len(result.split('.')[1]) - 1)) + "万")
    # 再如果可以处理成为亿的单位则处理成为亿的单位
    elif numb_constant > million_100:
        result = format(round((numb_constant / million_100), decimal_point), ',') + "亿"
        result = result if len(result.split('.')[1]) == 3 else result.replace("亿", '0' * (
                decimal_point - (len(result.split('.')[1]) - 1)) + "亿")
    else:
        result = format(result, ',')
    return result


if __name__ == '__main__':
    a = big_number_conduct(round(1111114.48, 2), 1)
    print(a)
