# -*- coding:utf-8 -*-

"""
  网络服务器，采用UDP协议 线程采用PyQT5， 也可以很快的换成原始的线程
"""

import socket
import struct
import selectors

from PyQt5.QtCore import *

BLOCK_SIZE = 1024 * 30

class NetService(QThread):
    # 派发事件
    receiver = pyqtSignal(object)

    def __init__(self):
        super(NetService, self).__init__()
        # 默认的select
        self.mSelector = selectors.DefaultSelector()
        self.mRunning = False

    def setup(self, port=8089):
        """
        设置监控环境
        :param port:
        :return:
        """
        self.mServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.mServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8294400)
        self.mServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8294400)
        self.mServerSock.bind(("0.0.0.0", port))
        self.mSelector.register(self.mServerSock, selectors.EVENT_READ)
        self.mRunning = True
        self.start()
        print("bind ..................")

    def run(self):
        """
        线程执行方法
        :return:
        """
        while self.mRunning:
            self.receiver_data(self.mServerSock)
            # socks = self.mSelector.select()
            # for obj, mask in socks:
                #if mask & selectors.EVENT_READ == 1:
                # self.receiver_data(obj.fileobj)

    def receiver_data(self, sock):
        print("33333")
        data, address = sock.recvfrom(BLOCK_SIZE)
        if data.find(b"APM:") == 0:
            temp_img = b""
            size, block = struct.unpack(">ii", data[4:])
            for i in range(block):
                data, address = sock.recvfrom(BLOCK_SIZE)
                temp_img += data
            print(">?>>>>>>>>>>>")
            self.receiver.emit(temp_img)
