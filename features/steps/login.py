# -*- coding: UTF-8 -*-
import os
from time import sleep
import uiautomation as auto
from assertpy import assert_that
from behave import *
from common.control_element import OperateWindow
from common.log import logger
from page.login_page import LoginPage, LoginPageAction
from common.image_match import ImageMatch
from common.screen_shot import screen_shot


@given(u'启动软件')
def step_impl(context):
    context.login_action = LoginPageAction()


@given(u'输入用户名{name}和密码{pswd}')
def step_impl(context, name, pswd):
    context.login_action.login_page_username_edit_click()
    context.login_action.login_page_username_edit_sendkeys(name)
    context.login_action.login_page_password_edit_click()
    context.login_action.login_page_password_edit_sendkeys(pswd)


@given(u'选择用户类型{type}')
def step_impl(context, type):
    if type == "admin":
        context.login_action.login_page_admin_button_click()
    elif type == "user":
        context.login_action.login_page_user_button_click()
    elif type == "service":
        context.login_action.login_page_service_button_click()


@when(u'点击按钮登录')
def step_impl(context):
    context.login_action.login_page_login_button_click()


@then(u'进入软件主界面')
def step_impl(context):
    sleep(5)
    try:
        patient_window = auto.StatusBarControl(Name="进入病例管理", Depth=2)
        status = OperateWindow().window_exists(patient_window)
        if status:
            logger.info("软件登录成功，进入病人管理界面")
    except Exception as e:
        pass
    finally:
        assert_that(status).is_true()


@then(u'提示错误信息{error}')
def step_impl(context, error):
    sleep(2)
    # 截取全屏
    screen_shot()
    # 文字识别
    screen_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\screenshot\screen.png'
    text = ImageMatch().get_picture_str(screen_path)
    # 判断识别出的文本与期望结果是否一致
    assert_that(text).contains(str(error))
