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
import json
import re

class Runthread(QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    _signal1 = pyqtSignal(str)
    def __init__(self):
        super(Runthread, self).__init__()
        self.id='0'
    def __del__(self):
        self.wait()
 
    def run(self):
        HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
        response = requests.get('https://geoapi.qweather.com/v2/city/lookup?location=zhongshan&key=04fe891110264bfd89f9c57ab0c64169')
        response.encoding = response.apparent_encoding
        data=json.loads(response.text)
        for i in data['location']:
            if i['adm1']=="广东省":
                self.id=i['id']
                print(self.id)
        response1 = requests.get('https://devapi.qweather.com/v7/weather/now?location='+self.id+'&key=04fe891110264bfd89f9c57ab0c64169').json()
        #print(response1)
        response2 = requests.get('https://devapi.qweather.com/v7/astronomy/sunmoon?location='+self.id+'&key=04fe891110264bfd89f9c57ab0c64169'+"&date="+time.strftime("%Y%m%d", time.localtime()) ).json()
        print(response2['sunrise'])
        pattern = re.compile('T+\d{2}:\d{2}')
        str1 = response2['sunrise']
        sun1=pattern.search(str1).group().replace("T","")
        self._signal.emit(sun1)
        print(response2['sunset'])
        pattern = re.compile('T+\d{2}:\d{2}')
        str2 = response2['sunset']
        sun2=pattern.search(str2).group().replace("T","")
        self._signal1.emit(sun2)


os.environ['QT_API'] = 'pyqt5'
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self) 
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time_)
        self.timer.start(100)
        self.thread = Runthread() # 创建线程
        self.thread._signal.connect(self.callbacklog) # 连接信号
        self.thread._signal1.connect(self.callbacklog1)
        self.thread.start() # 开始线程
    def time_(self):
        h=time.strftime("%H", time.localtime())
        m=time.strftime("%M", time.localtime())
        s=time.strftime("%S", time.localtime())
        h1=time.strftime("%I", time.localtime())
        ow=int(h)*60*60+int(m)*60+int(s)
        self.label.setText(h1+":"+m+":"+s)
        self.progressBar.setValue(ow)
    def callbacklog(self,sun1):
        self.label_5.setText(sun1)
    def callbacklog1(self,sun2):
        self.label_6.setText(sun2)
    


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = MainWindow()
    App.setStyleSheet(qdarkstyle.load_stylesheet())
    ex.show()
    sys.exit(App.exec_())


