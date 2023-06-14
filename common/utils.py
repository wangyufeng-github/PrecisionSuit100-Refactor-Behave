# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time : 2022/8/5 16:20
# @Author : yufeng.wang@we-med.com
# @Site :
# @File : utils.py
# @Software : PyCharm
import configparser
import os
import subprocess
import time
from pathlib import Path
from common.log import logger

# 配置文件路径
CONFIG_FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\config\config.ini'


##################################
#    Utils: 工具类，定义为单例模式
##################################
class Utils:
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self):
        pass

    def start_app(self):
        """
        通过将软件快捷方式增加到dock栏，利用图像识别方式打开软件
        :return:
        """
        subprocess.Popen(r"C:\wemed\PrecisionSuit100\PrecisionSuit.exe", cwd=r"C:\wemed\PrecisionSuit100")
        # subprocess.Popen(r"D:\Product3D\My3DApp.exe",cwd="D:\Product3D")
        # ImageMatch().image_to_click("app_icon")
        time.sleep(3)
        login_state = self.get_process_state("PrecisionSuit.exe")
        if login_state:
            logger.info("软件成功启动")
            return True
        else:
            print("未获取到后台进程，请检查程序是否启动")
            logger.info("软件启动失败")
            return False

    def stop_application(self):
        """
        强制退出软件
        :return:
        """
        os.system("taskkill /im PrecisionSuit.exe -f")
        time.sleep(2)
        return True

    def get_process_state(self, process_name):
        """
        判断程序是否运行
        :param process_name:
        :return:
        """
        result = os.system(f"tasklist | findstr {process_name}")
        if result is not None:
            return True
        else:
            return False

    def get_config(self, section, option):
        """
        读取配置文件中的用户名和密码信息
        :param section:
        :param value:
        :return:
        """
        config = configparser.ConfigParser()
        filename = CONFIG_FILE_DIR
        print(filename)
        config.read(filename, encoding='utf-8')
        result = config.get(section, option)
        return result

    def delete_html_files(self, file_path):
        """
        清空文件夹
        :param file_path:html文件路径，不包含具体文件名
        :return:
        """
        try:
            for file in os.listdir(file_path):
                if file.endswith('html'):
                    full_path = (os.path.join(file_path, file))
                    full_path = '/'.join(full_path.split('\\'))
                    os.remove(full_path)
                    logger.info("reports文件夹删除html文件成功！")
        except PermissionError as e:
            print("reports文件夹暂时未生成html文件")

    def delete_automationlog_txt(self):
        """
        遍历工程路径的方式删除所有的@AutomationLog.txt文件
        :return:
        """
        path = Path.cwd().parent
        for name in path.rglob('@AutomationLog.txt'):
            os.remove(name)


if __name__ == '__main__':
    # Tool().delete_automationlog_txt()
    path = Path.cwd().parent
    for i1 in path.rglob('@AutomationLog.txt'):
        os.remove(i1)
