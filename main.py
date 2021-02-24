import sys
import time
import qdarkstyle
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_main import Ui_MainWindow
from PyQt5.QtCore import QTimer,QThread
import requests
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from lxml import etree

class Runthread(QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()
 
    def run(self):
        response = requests.get('https://tianqi.qq.com/index.htm')
        response.encoding = response.apparent_encoding
        print(response.text)
        data=self.xpath_parse_movies(response.text)
        for i in data:
            print(i)

    def xpath_parse_movies(self,html):
        et_html = etree.HTML(html)
        urls = et_html.xpath('//*[@id="txt-temperature"]')
        print(urls)
        for index in range(len(urls)):
            print(urls[index].text)
        return urls





os.environ['QT_API'] = 'pyqt5'
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self) 
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time_)
        self.timer.start(100)
        self.thread = Runthread() # 创建线程
        #self.thread._signal.connect(self.callbacklog) # 连接信号
        self.thread.start() # 开始线程
    def time_(self):
        h=time.strftime("%H", time.localtime())
        m=time.strftime("%M", time.localtime())
        s=time.strftime("%S", time.localtime())
        h1=time.strftime("%I", time.localtime())
        ow=int(h)*60*60+int(m)*60+int(s)
        self.label.setText(h1+":"+m+":"+s)
        self.progressBar.setValue(ow)

    


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = MainWindow()
    App.setStyleSheet(qdarkstyle.load_stylesheet())
    ex.show()
    sys.exit(App.exec_())


