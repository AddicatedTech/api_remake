"""
============================
Author:柠檬班-木森
Time:2020/3/12   21:53
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
import logging
from common.handle_config import conf
from common.handle_path import LOG_DIR

log_filepath =os.path.join(LOG_DIR,conf.get("log", "filename"))

class HandleLogger:
    """处理日志相关的模块"""
    @staticmethod
    def create_logger():
        """
        创建日志收集器
        :return: 日志收集器
        """
        # 第一步：创建一个日志收集器
        log = logging.getLogger("musen")

        # 第二步：设置收集器收集的等级
        log.setLevel(conf.get("log", "level"))

        # 第三步：设置输出渠道以及输出渠道的等级
        fh = logging.FileHandler(log_filepath, encoding="utf8")
        fh.setLevel(conf.get("log", "fh_level"))
        log.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(conf.get("log", "sh_level"))
        log.addHandler(sh)
        # 创建一个输出格式对象
        formats = '%(asctime)s -- [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        form = logging.Formatter(formats)
        # 将输出格式添加到输出渠道
        fh.setFormatter(form)
        sh.setFormatter(form)

        return log


log = HandleLogger.create_logger()
