# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time : 2022/8/9 15:00
# @Author : yufeng.wang@we-med.com
# @Site :
# @File : screen_shot.py
# @Software : PyCharm
import time,os
import pyautogui
import uiautomation
# 截图整个桌面
import win32gui
import win32ui
import win32con
import win32api

def save_screenshot(Windows):
    """
    调用uiautomation模块的截图功能
    :param Windows:窗口对象
    :return:
    """
    # 获取当前时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 图片存放路径
    pic_path = "../screenshot/" + now + '_screen.png'
    Windows.CaptureToImage(savePath=pic_path)



def screen_shot():
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()
    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    screenshot.SaveBitmapFile(mem_dc, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\screenshot\screen.png')
    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())



if __name__ == '__main__':
    screen_shot()
