# -*- coding:utf-8 -*-

"""
  桌面截图
"""

from PIL import Image
import win32gui, win32ui, win32con, win32api


class CaptureDesktop(object):
    """ 桌面截图 """
    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79

    def __init__(self):
        super(CaptureDesktop, self).__init__()
        self.mHwnd = None
        self.mHwndDC = None
        self.mMfcDC = None
        self.mSaveDC = None
        self.init_env()

    def init_env(self):
        self.mHwnd = win32gui.GetDesktopWindow()
        self.mHwndDC = win32gui.GetWindowDC(self.mHwnd)
        self.mMfcDC = win32ui.CreateDCFromHandle(self.mHwndDC)
        self.mSaveDC = self.mMfcDC.CreateCompatibleDC()

    def Capture(self):
        w = win32api.GetSystemMetrics(self.SM_CXVIRTUALSCREEN)
        h = win32api.GetSystemMetrics(self.SM_CYVIRTUALSCREEN)
        l = win32api.GetSystemMetrics(self.SM_XVIRTUALSCREEN)
        t = win32api.GetSystemMetrics(self.SM_YVIRTUALSCREEN)
        r = l + w
        b = t + h
        # 左、上、右、下
        print(l, t, r, b, ' -> ', w, h)

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.mMfcDC , w, h)
        self.mSaveDC.SelectObject(saveBitMap)
        self.mSaveDC.BitBlt((0, 0), (w, h), self.mMfcDC , (l, t), win32con.SRCCOPY)
        # 保存为文件
        # saveBitMap.SaveBitmapFile(self.mSaveDC, 'screencapture.bmp')

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        # BMP原始数据， 图片的宽高
        return bmpstr, bmpinfo['bmWidth'], bmpinfo['bmHeight']

        # 使用PIL将BMP进行转码
        # im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        # pdata = im.convert("P")
        # return pdata.tobytes(), bmpinfo['bmWidth'], bmpinfo['bmHeight']

        # 使用PIL将BMP存储为png或者jpg
        # import Image
        # im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        # im.save('screencapture.jpg', format='jpeg', quality=85)
        # im.save('screencapture.png', format='png')


if __name__ == "__main__":
    CaptureDesktop().Capture()