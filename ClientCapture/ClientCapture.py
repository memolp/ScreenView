# -*- coding:utf-8 -*-

"""
  主入口
"""


# -- import 模块
import sys
# -- 系统from import 模块
from PyQt5.Qt import QApplication
# -- 内部 from import 模块
from ui.QMainDialog import QMainDialog

# -- 主运行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #QApplication.setQuitOnLastWindowClosed(False)
    w = QMainDialog()
    w.show()
    sys.exit(app.exec_())
