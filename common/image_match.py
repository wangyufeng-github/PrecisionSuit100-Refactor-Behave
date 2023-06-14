# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time : 2022/8/11 15:37
# @Author : yufeng.wang@we-med.com
# @Site :
# @File : image_match.py
# @Software : PyCharm


from ast import Return
import getpass
import pyautogui
import os
import sys
import subprocess
import random
import glob
import cv2 as cv
# import pandas as pd
from time import sleep
from time import time
import requests
import base64
import pytesseract
from PIL import ImageChops
from PIL import Image

from aip import AipOcr
import shutil
from common.screen_shot import screen_shot


class ImageMatch:
    def __init__(self):
        pass

    def check_images(self, pathone, filename1, pathtwo, filename2,
                     diffsavename):
        # Check Images ： robot关键字
        """robot自定义关键字: 比较两个长度和宽度一样大的图片【推荐使用】

        :Param pathone: <str> 存放第一个图片的路径，如：Pictures

        :Param filename1: <str> 第一个文件的名字

        :Param pathtwo: <str> 存放第二个图片的路径，如：Desktop

        :Param filename2: <str> 第二个文件的名字

        :Param diffsavename: <str> 图片校验后保存的名称，如：我们不一样

        :Return: <bool> 图片校对结果，True代表无差异，Flase代表有差异

        Example::

        | Check Images | Pictures | before | Desktop | after | 我们不一样 |
        """
        username = self.get_username()
        path_base = '/home/' + str(username) + '/' + str(pathone) + '/' + str(
            filename1) + '.png'
        path_compare = '/home/' + str(username) + '/' + str(
            pathtwo) + '/' + str(filename2) + '.png'
        diff_save_location = '/home/' + str(username) + '/' + str(
            pathtwo) + '/' + str(diffsavename) + '.png'
        image_one = Image.open(path_base)
        image_two = Image.open(path_compare)
        diff = ImageChops.difference(image_one, image_two)
        check_diff = diff.getbbox()
        try:
            if check_diff is None:
                return True
            else:
                diff.save(diff_save_location)
                return False
        except ValueError as e:
            text = ("图片大小和box对应的宽度不一致")
            print("【{0}】{1}".format(e, text))

    def get_picture_str(self,img_path: str) -> list:
        '''
        根据图片路径，将图片转为文字，返回识别到的字符串列表
        '''
        # 请求头
        headers = {
            'Host': 'cloud.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
            'Accept': '*/*',
            'Origin': 'https://cloud.baidu.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://cloud.baidu.com/product/ocr/general',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        # 打开图片并对其使用 base64 编码
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read())
        data = {
            'image': 'data:image/jpeg;base64,' + str(img)[2:-1],
            'image_url': '',
            'type': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
            'detect_direction': 'false'
        }
        # 开始调用 ocr 的 api
        response = requests.post(
            'https://cloud.baidu.com/aidemo', headers=headers, data=data)

        # 设置一个空的列表，后面用来存储识别到的字符串
        ocr_text = []
        result = response.json()['data']
        if not result.get('words_result'):
            return []

        # 将识别的字符串添加到列表里面
        for r in result['words_result']:
            text = r['words'].strip()
            ocr_text.append(text)
        # 返回字符串列表
        return ocr_text

    def matchImg(self,templateImage,confidencevalue=0.7):
        """
        原理：在待检测图像上，从左到右，从上向下计算模板图像与重叠子图像的匹配度，匹配程度越大，两者相同的可能性越大
        模板匹配图片
        :param image:大图
        :param templateImage: 模板图片
        :param confidencevalue: 识别精度
        :return: 字典 包含['rectangle']访问匹配到的图片左顶点图片宽高(left, top, width, height)  ['result']访问匹配到的图片中点 or None


        methods = [cv.TM_SQDIFF_NORMED,cv.TM_CCORR_NORMED,cv.TM_CCOEFF_NORMED]　　#各种匹配算法
        获取的是每种公式中计算出来的值，每个像素点都对应一个值
        min_val,max_val,min_loc,max_loc = cv.minMaxLoc(result)
        TM_CCOEFF_NORMED：1表示完美匹配,-1表示糟糕的匹配,0表示没有任何相关性(随机序列)
        """
        # 打开模板图片
        # screenImage.save(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\screenshot\screen.png')
        screenImage = cv.imread(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\screenshot\screen.png')
        templateImage = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + f'\image\\template\{templateImage}.png'
        templateImage = cv.imread(templateImage)
        # 调用matchTemplate方法进行匹配
        result = cv.matchTemplate(screenImage, templateImage, cv.TM_CCOEFF_NORMED)
        pos_start = cv.minMaxLoc(result)[3]
        # 匹配对象的中心坐标x y
        x = int(pos_start[0]) + int(templateImage.shape[1] / 2)
        y = int(pos_start[1]) + int(templateImage.shape[0] / 2)
        # 匹配度
        similarity = cv.minMaxLoc(result)[1]
        if similarity < confidencevalue:
            return None
        else:
            return {'result': (x, y),
                    'rectangle': (pos_start[0], pos_start[1], templateImage.shape[1], templateImage.shape[0])}

    def judge_image_exist(self, templateImage, confidencevalue=0.9):
        """
        Judge Image Exist
        判断当前截取的屏幕图片是否能够匹配到模板图片，返回bool值
        """
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screen_shot()
        obj_image = cv.imread(path + r'\screenshot\screen.png')
        template_path = path + f'\image\\template\{templateImage}.png'
        template = cv.imread(template_path)
        # 调用matchTemplate方法进行匹配
        result = cv.matchTemplate(obj_image, template, cv.TM_CCOEFF_NORMED)
        # 匹配度
        similarity = cv.minMaxLoc(result)[1]
        if similarity < confidencevalue:
            return False
        else:
            return True

    def image_to_click(self, templateImage):
        """
        Image To Click
        根据控件图片名称去操作控件
        """
        screen_shot()
        ret = self.matchImg(templateImage)
        if ret:
            pyautogui.click(ret['result'][0], ret['result'][1], duration=1)
        else:
            print("当前界面无该控件")

    def image_to_right_click(self, templateImage):
        """
        Image To Right Click
        根据控件图片名称去操作控件
        """
        img = pyautogui.screenshot()
        ret = self.matchImg(img, templateImage)
        if ret:
            pyautogui.rightClick(ret['result'][0], ret['result'][1], duration=1)
        else:
            print("当前界面无该控件")

    def image_to_double_click(self, templateImage):
        """
        Image To Right Click
        根据控件图片名称去操作控件
        """
        img = pyautogui.screenshot()
        ret = self.matchImg(img, templateImage)
        if ret:
            pyautogui.doubleClick(ret['result'][0], ret['result'][1], duration=1)
        else:
            print("当前界面无该控件")


if __name__ == '__main__':
    im = ImageMatch()
    # print(im.judge_image_exist("warning_1"))
    # print(im.get_picture_str(r"E:\project\PrecisionSuit100Test\screenshot\screen.PNG"))
    # text = pytesseract.image_to_string(Image.open(r'C:\Users\hello\AppData\Roaming\JetBrains\PyCharmCE2021.2\scratches\img.png'),
    #                                    lang="chi_sim").replace(" ", "").replace("\n", "")
    # print(text)