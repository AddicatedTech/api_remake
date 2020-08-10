# 用来替换数据封装


# 此类中封装 环境变量类以及 re模块替换掉##括起来的数据方法

import  re
from common.handle_config import conf
class EnvData:
    pass


def replace_data(data):

#替换用例中# 括起来的数据
    while re.search("#(.*?)#", data):
        res = re.search("#(.*?)#", data)
        # 返回一个匹配对象
        # 然后可以通过对象的方法去得到匹配到的数据
        key = res.group()
        # 获取匹配规则中括号里面的内容，，（）是re表达式
        item = res.group(1)
        # 一般，m.group(N)
        # 返回第N组括号匹配的字符。
        # 而m.group() == m.group(0) == 所有匹配的字符，与括号无关，这个是API规定的。
        try:
            # 先去获取文件中对应的值，
            value = conf.get("test_data",item)
        except:
            # 发生异常的话就去EnvData这个类里面去寻找获取对应的值（环境变量类）
            value = getattr(EnvData,item)

        data = data.replace(key,value)
    return data