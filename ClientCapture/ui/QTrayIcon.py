# -*- coding:utf-8 -*-

"""
   系统托盘
"""


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class QSysTrayIcon(QSystemTrayIcon):
    """ 系统托盘图标功能 """
    def __init__(self, parent=None):
        super(QSysTrayIcon, self).__init__(parent)
        # 初始化
        self.init_component()

    def init_component(self):
        """
        初始化组件信息
        :return:
        """
        # 系统菜单
        self.mContextMenu = QMenu()
        # 设置系统菜单
        self.setContextMenu(self.mContextMenu)
        # 托盘的图标
        self.setIcon(QIcon("capture.png"))

    def send_message(self, title, content, icon_=0, delay_=10000):
        """
        显示一条消息通知
        :param title:
        :param content:
        :param icon_: （0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        :param delay_: 持续间隔（毫秒）
        :return:
        """
        self.showMessage(title, content, icon=icon_, msecs=delay_)

    def add_menu_action(self, label_, parent_, triggered_):
        """
        添加操作按钮
        :param label_:
        :param parent_:
        :param triggered_:
        :return:
        """
        action = QAction(label_, parent_, triggered=triggered_)
        self.mContextMenu.addAction(action)
        return action

    def quit(self):
        """
        退出
        :return:
        """
        self.setVisible(False)
