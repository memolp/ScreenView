# -*- coding:utf-8 -*-

"""
  录制的设置主界面
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import gzip

from ui.QTrayIcon import QSysTrayIcon
from core.CaptureDesktop import CaptureDesktop
from core.NetService import NetService
from core.BMP import Bmp

class QMainDialog(QDialog):
    def __init__(self, parent=None):
        """
        主界面
        :param parent:
        """
        super(QMainDialog, self).__init__(parent)
        # 初始化组件
        self.init_component()
        self.mCapture = CaptureDesktop()
        self.mNetClient = NetService()
        self.mTimer = QTimer()
        self.mTimer.setInterval(200)
        self.mTimer.timeout.connect(self.update_img)


    def init_component(self):
        """
        初始化组件
        :return:
        """
        self.mTrayIcon = QSysTrayIcon(self)
        self.mToggleAction = self.mTrayIcon.add_menu_action("隐藏界面", self, self.on_toggle_widget)
        self.mTrayIcon.show()
        self.mView = QLabel()
        self.mView.setMaximumSize(800, 600)
        hLayout = QVBoxLayout()
        btn_s = QPushButton("开始")
        btn_s.clicked.connect(self.on_start)
        hLayout.addWidget(btn_s)
        hLayout.addWidget(self.mView)
        self.setLayout(hLayout)

    def closeEvent(self, event):
        # QMessageBox.information(self, "aaa","bbb")
        super(QMainDialog, self).closeEvent(event)
        self.mTrayIcon.quit()
        self.mTimer.stop()
        self.mNetClient.stop()

    def on_toggle_widget(self):
        if self.isVisible():
            self.hide()
            self.mToggleAction.setText("显示界面")
            self.mTrayIcon.send_message("提示", "界面已经隐藏")
        else:
            self.show()
            self.mToggleAction.setText("隐藏界面")
            self.mTrayIcon.send_message("提示", "界面已经显示")

    def update_img(self):

        bitmap_data, w, h = self.mCapture.Capture()
        # 实验BMP压缩后发送
        # bmp = Bmp()
        # bmp.parse_from_buff(bitmap_data)
        # bmp.resize(w*0.4, h*0.4)
        # bitmap_data = gzip.compress(bitmap_data)
        # print("bitmap_data:size:", len(d))
        # pixmap = QImage(bitmap_data, w, h, QImage.Format_ARGB32)
        # pixmap = QPixmap.fromImage(pixmap)
        # self.mView.setPixmap(pixmap)
        self.mNetClient.send_data(bitmap_data)


    def on_start(self):
        self.mNetClient.setup()
        self.mTimer.start()