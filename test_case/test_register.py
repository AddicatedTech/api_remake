### login 测试case类


''''''
import pytest
import random
from common.handle_excel import HandleExcel
from lib.myddt import ddt, data
from common.handle_config import conf
from requests import request
from common.handle_logging import log
from common.handle_yaml import Handle_Yml
from common.handle_db import HandleMysql


# excel_path = r"F:\py_27class\api_frame\data\apicases.xlsx"

# 在需要使用数据驱动框架的类上添加 @ddt装饰器
class TestRegisterCase:
	# excel = HandleExcel(excel_path,"login")
	# cases = excel.read_data()
	obj_yml = Handle_Yml("register_case.yml")
	cases = obj_yml.read_yml()
	db = HandleMysql()

	@classmethod
	def gen_acc(cls):
		# 生成一个数据库里面未注册的手机号码用作用户名
		while True:  # 设定为死循环，设定生成一个db中没有的手机号即跳出循环
			username = "155"
			for i in range(8):
				r = random.randint(0, 9)
				username += str(r)
			sql = F"SELECT * FROM futureloan.member WHERE mobile_phone = {username}"
			res = cls.db.find_count(sql)
			if res == 0:
				return username

	@pytest.mark.parametrize("case",cases)
	def test_register(self, case):
		method = case["method"]
		# 请求地址
		url = case["url"]
		# 请求参数
		data = case["data"]
		# 请求头
		headers = eval(conf.get("env", "headers"))
		# 预期结果
		expected = case["expected"]
		# row =case["case_id"]+1
		# 惨痛教训，，竟然忘了传data = =
		# 替换生成手机号
		if "#phone#" in data.values():
			phone = self.gen_acc()
			data["mobile_phone"] = phone
		print(data.values())

		response = request(method=method, url=url, json=data, headers=headers)

		# 获得实际结果
		res = response.json()

		print("预期：", expected)
		print("实际", res)

		# 进行断言， 输出到日志
		try:
			assert expected['code'] == res["code"]
			assert expected['msg'] == res["msg"]
			# self.assertEqual(expected['code'], res['code'])
			# self.assertEqual(expected["msg"], res['msg'])
		except AssertionError as e:
			# 结果会写到excel中
			log.error(F"用例{case['title']}---执行不通过")
			log.debug(F"预期结果：{expected}")
			log.debug(F"实际结果：{res}")
			log.exception(e)
			# self.excel.write_data(row=row,column=8,value="未通过")
			raise e
		else:
			# 结果回写到excel中
			log.info(F"用例--{case['title']}---执行通过")
	# self.excel.write_data(row=row,column=8,value="通过")
if __name__ == '__main__':
	pytest.main()