## 用作充值接口的测试类

# 接口地址 http://api.lemonban.com/futureloan/member/recharge
# post方法
# 请求类型为json  响应格式也为json
# 请求数据为  member_id  int  会员id amount double  金额数量


""""""
import jsonpath

"""
充值测试用例类书写

excel中设计测试用例

编写测试用例类

创建类，继承unittest.TestCase

编写测试方法

导入ddt ，data 数据驱动

类上添加@ddt 注解

测试方法上 @data（读取的数据来源）

指明路径和表单名、

    测试方法
        1，准备用例数据
            url地址，方法，参数，请求头（从配置文件内读取出来
        2，发送请求获取实际结果
        3，断言预期结果和实际结果
            从excel中获取的结果格式是字符串，
        此次测试数据的url进行一些更改，因为测试环境和生产环境不同，所以把baseurl放到配置文件里
        在测试用例方法中进行拼接接口地址即可

        充值接口需要用户id，还有充值金额两个参数

        关于unittest的环境环境配置方法

            setUp  每条用例执行之前都会执行
            teadrdown 每条用例执行之后都会执行

            @classmethod
            setupClass 该测试用例类中的用例执行之前会执行

             @classmethod
             teardownclass  该测试用例类中的用例执行后会执行

    分析，充值之前需要登录，登录一次即可，
        即，在测试用例类运行之前登录一次，使用类前置方法调用登录接口进行一次登录
            登录用的账号和密码可以在配置文件内进行定义，之后读取。
            登录之后取出id，还有token方便之后进行鉴权
            jsonpath需要复习，jsonpath取到的数据格式为列表
            保存取到的数据可以直接定义为类属性  cls.属性名=属性值

            token有类型之分，后面调查， 
            然后提取到token之后要进行一下拼接
            替换从excel中读取到的 #member_id# 
            然后进行一次eval转换成字典

        准备请求头，请求头会发生改变
            需要添加一个新的字段Authorization 值为前面取到的token

        发请求，
        然后断言，
        错误 bool类型不可以取值 jsonpath 匹配不到数据的情况下返回的事false

        充值之前查询数据库
        充值之后查询数据库
        首先判断表中是有否有sql语句，有则进行DB校验，无则不用
            注意不要定义重复的变量
"""
import decimal
import pytest
from common.handle_config import conf
from requests import request
from common.handle_db import HandleMysql
from common.handle_logging import log
from common.handle_yaml import Handle_Yml

@pytest.fixture(scope='function')
def set_Up():
    # 登录所用的信息可以写到conf的配置中，然后通过工具类去读取
    url = conf.get("env", "url") + "/member/login"
    data = {
        "mobile_phone": conf.get("test_data", "phone"),
        "pwd": conf.get("test_data", "pwd")
    }
    # 因为取出是一个字符串，所以需要用eval
    headers = eval(conf.get("env", "headers"))
    # 发送请求拿到响应体
    response = request(method="post", url=url, json=data, headers=headers)
    res = response.json()
    print(res)
    member_id = str(jsonpath.jsonpath(res, "$..id")[0])  # 吧他们变成类变量方便引用
    token = "Bearer" + " " + jsonpath.jsonpath(res, "$..token")[0]
    yield member_id,token

class TestChargeCase():

    obj_yml =Handle_Yml('charge_case.yml')
    cases = obj_yml.read_yml()
    db = HandleMysql()

    # 思考：
    '''
    测试充值接口需要先进行登录，然后从登录成功返回的信息中取到测试接口要用的信息
    需要先登录，但是整体而言只需要登录一次即可，所以使用单元测试框架的类前置处理方法
    接口测试需要用到的信息有哪些？？
        member_id 
        token 信息。用来充值的时候来进行鉴权，
        
    '''

    # @classmethod
    # def setUpClass(cls):  # 测试类开始执行的时候执行一次，这个方法下写登录，登录完成后取信息
    #     # 登录所用的信息可以写到conf的配置中，然后通过工具类去读取
    #     url = conf.get("env", "url") + "/member/login"
    #     data = {
    #         "mobile_phone": conf.get("test_data", "phone"),
    #         "pwd": conf.get("test_data", "pwd")
    #     }
    #     # 因为取出是一个字符串，所以需要用eval
    #     headers = eval(conf.get("env", "headers"))
    #     # 发送请求拿到响应体
    #     response = request(method="post", url=url, json=data, headers=headers)
    #     res = response.json()
    #     cls.member_id = str(jsonpath.jsonpath(res, "$..id")[0])  # 吧他们变成类变量方便引用
    #     cls.token = "Bearer" + " " + jsonpath.jsonpath(res, "$..token")[0]

    @pytest.mark.parametrize("case",cases)
    def test_charge(self, case,set_Up):
        member_id,token = set_Up
        # 接口测试需要准备的测试数据 采用拼接的方式，取配置文件中的baseurl + excel中的
        url = conf.get("env", "url") + case["url"]
        # method
        print(url)
        method = case["method"]
        # data 需要传入用户的id ，excel 中使用 #member_id# 进行站位，需要进行替换
        # print(case["data"])
        data = case["data"]
        if "#member_id#" in data.values():
            data["member_id"] = member_id
        print(data)
        # 定义请求头信息
        headers = eval(conf.get("env", "headers"))
        # headers 从配置文件取出来是一个字典类型
        headers["Authorization"] = token
        expected = case["expected"]
        # 判断用例是否需要db校验，获取充值之前的账户余额是否
        # 调用requests库发送请求，
        if "check_sql" in case.keys():
            sql = case["check_sql"].format(member_id)
            # 获得充值之前的money量
            # 返回数据类型为dict 因为之前采用了dict游标
            # 所以可以直接进行取值 leave amount 为可用余额
            s_money = self.db.find_one(sql)["leave_amount"]
            print(F"充值之前的金额为：{s_money}")

        # 第二部： 发送请求获取实际结果
        response = request(url=url, method=method, json=data,
                           headers=headers)
        result = response.json()
        print(F"预期结果：{expected}")
        print(F"实际结果：{result}")
        # 取得返回结果进行断言用例是否通过
        # 断言预期结果和实际结果
        ## 判断该用例是否需要db校验，获取充值后的账户余额
        if "check_sql" in case.keys():
            sql = case["check_sql"].format(member_id)
            end_money = self.db.find_one(sql)["leave_amount"]
            print(F"充值之后的金额{end_money}")
        try:
            assert expected['code'] == result['code']
            assert expected['msg'] == result['msg']

            # 还要判断是否进行sql校验DB
            if "check_sql" in case.keys():
                # 将充值金额转换成decimal类型 db中的类型
                charge_money = decimal.Decimal(str(data["amount"]))
                assert charge_money == end_money -s_money
        except AssertionError as e:
            # 结果回写excel
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(result))
            log.exception(e)
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))

if __name__ == '__main__':
    pytest.main()