'''
'''
"""
封装发送邮件的功能代码
       
        使用python发送邮箱测试报告
        qq邮箱为例，
            登录qq邮箱，然后smtp设置，保存授权码
            开启smtp服务 docvzkckifewbjcg

            qq邮箱 465
            163邮箱 465 25 端口号
           1， 导入smtplib
            2，连接smtp服务器并登录
            smtplib.SMTP_SSL(host="smtp.qq.com",port=465)
            3，登录smtp服务器，邮箱账号和授权码进行登录，非邮箱密
            添加付健的话
                首先打开报告，读取出来
                with open（） as f 
                    content = f.read()
                将content作为参数 传入到mimeText 方法中
        读取内容作为正文发送，显示特别不友好
            作为附件发送
            email.mime.application import MIMEApplication
            添加付健用的模块
            email.mime.multipart import MIMEultipart
            多组件话邮件模块
            
            构造一封多组件的邮件
            msg = MIMEMultipart（）
            msg[]
            msg[]
            msg[]
            
            构建邮件的文本内容
            text = MIMEText("邮件中的文本内容"，_charset="utf-8") 编码
            msg.attach(text)
            
            with open as f  使用rb模式
                content（f.read())
            构造邮件的付健
            report = MIMEApplication（content）确认一下参数是否需要传
            report.add_header(内有三个参数，需要自己学习一下
            4，构造一封邮件
            from mail.mime.text import mimetext
            msg = MIMEText("内容",charset字符编码
            msg["Subject"]  主题
            msg["To"]  收件人  是邮件里面所显示的信息
            msg["From"]  发件人 （自己） 同上
            
            5，发送邮件
            smtp.send_message(msg,from_addr = "发件人地址",to_addr="s收件人"
            群发的实现方式
            
"""
'''          1， 导入smtplib
            2，连接smtp服务器并登录
            smtplib.SMTP_SSL(host="smtp.qq.com",port=465)
            3，登录smtp服务器，邮箱账号和授权码进行登录，非邮箱密'''
import smtplib
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.handle_path import REPORT_DIR
def send_report():
    # 第一步连接到smtp 服务器并且登录
    smtp = smtplib.SMTP_SSL(host = "smtp.qq.com",port=465)
    # 登录smtp服务器，参数为邮箱地址还有smtp授权码
    smtp.login(user="414213352@qq.com",password="iqqfzicaxzzdcahh")
    #iqqfzicaxzzdcahh

    # 第二部，构建一封多组件的邮件，因为需要发送测试报告，所以需要多组件
    # 调用的事MIMEApplication
    msg= MIMEMultipart()
    msg["Subject"] = "----自动化测试报告-----"
    msg["To"] ="414213352@qq.com"
    msg["From"] ="414213352@qq.com"

    # 构建邮箱的文本内容
    text =  MIMEText("使用MIMEText对象进行邮件文本定制",_charset="utf8")
    # 在设置完成文本内容之后要调用MIMEMultipart对象将文本内容通过方法attach进对象中
    msg.attach(text)
    # 构建一下添加的付健
    # 使用流式打开，模式为rb
    with open(os.path.join(REPORT_DIR,"report.html"),"rb") as f:
        content = f.read()
    report = MIMEApplication(content)
    report.add_header("content-disposition","attachment",filename="python.html")
    msg.attach(report)
    # 进行邮件发送
    smtp.send_message(msg,
                      from_addr="414213352@qq.com",
                      to_addrs="414213352@qq.com")
