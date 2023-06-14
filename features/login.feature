Feature: 登录系统
    Background: 启动软件
        Given 启动软件

    Scenario Outline: 登录系统成功
        Given 输入用户名<name>和密码<pswd>
        And 选择用户类型<type>
        When 点击按钮登录
        Then 进入软件主界面
    Examples:
        |name | pswd | type |
        |admin |123 |admin |
        |user |123 |user |
        |service |123 |service |

    Scenario Outline: 登录系统失败
        Given 输入用户名<name>和密码<pswd>
        And 选择用户类型<type>
        When 点击按钮登录
        Then 提示错误信息<error>
    Examples:
        | name | pswd | type | error |
        | admin | 111 | admin | 用户不存在 |
        | user | 111 | user | 用户密码错误 |
        | service | 111 | service | 用户类型错误 |



