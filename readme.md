## 对之前学过的项目进行重构
原项目架构为
excel + unittest + requests + httptestrunner生成测试报告

此次重构设想  
data 采用yaml的形式改造    
使用pytest代替unittest
使用allure代替httptestruner生成测试报告
开始日期 2020 614

yaml + pytest + alllure + CI jenkins mail

# ymal 控制case已经跑通，
剩下是采用pytest替代掉unittest，然后使用allure来生成测试报告
需要思考的一个问题，，比如说，用例通过或者失败，如何回写到yaml里面
