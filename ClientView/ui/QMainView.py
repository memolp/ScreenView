# -*- coding:utf-8 -*-

"""
  显示界面
"""
import gzip

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.NetService import NetService


class QMainView(QWidget):
    def __init__(self):
        super(QMainView, self).__init__()
        self.init_component()
        self.mNetService = NetService()
        self.mNetService.receiver.connect(self.on_receive_data)

    def init_component(self):
        """
        初始化界面
        :return:
        """
        self.mViewCanvas = QLabel()
        self.mViewCanvas.setMaximumSize(800, 600)
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.mViewCanvas)
        btn_s = QPushButton("开始")
        btn_s.clicked.connect(self.on_start)
        vLayout.addWidget(btn_s)
        self.setLayout(vLayout)

    def on_receive_data(self, data):
        """
        收到数据
        :param data:
        :return:
        """
        print("on_receive_dataon_receive_dataon_receive_data")
        # data = gzip.decompress(data)
        bitmap_data, w, h = data, 1920, 1080
        pixmap = QImage(bitmap_data, w, h, QImage.Format_Alpha8)
        pixmap = QPixmap.fromImage(pixmap)
        self.mViewCanvas.setPixmap(pixmap)

    def on_start(self):
        self.mNetService.setup()