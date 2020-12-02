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
        self.mClientSocket = None

    def setup(self, host="127.0.0.1", port=8089):
        """
        设置监控环境
        :param host:
        :param port:
        :return:
        """
        self.mClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.mClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8294400)
        self.mClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8294400)
        self.mClientSocket.connect((host, port))
        self.mSelector.register(self.mClientSocket, selectors.EVENT_READ)
        self.mRunning = True
        print("connect ............")
        # self.start()

    def send_data(self, data, address=None):
        size = len(data)
        block = round(size / BLOCK_SIZE + 0.5)
        print("send_data size:%s, block:%s" % (size, block))
        self.mClientSocket.sendto(b"APM:"+struct.pack(">ii", size, block), ("127.0.0.1", 8089))
        for i in range(block):
            end_index = i * BLOCK_SIZE + BLOCK_SIZE
            if end_index >= size:
                end_index = -1
            self.mClientSocket.sendto(data[i * BLOCK_SIZE: end_index], ("127.0.0.1", 8089))

    def run(self):
        """
        线程执行方法
        :return:
        """
        pass
        # while self.mRunning:
        #     socks = self.mSelector.select(1)
            # for mask, obj in socks:
            #     if mask & selectors.EVENT_READ == 1:
            #         self.receiver_data(obj.fileobj)

    def receiver_data(self, sock):
        data, address = sock.recvfrom(8294400)
        self.receiver.emit(data)

    def stop(self):
        self.mRunning = False
        if self.mClientSocket:
            self.mClientSocket.close()