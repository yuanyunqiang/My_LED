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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QMovie

class Runthread(QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    _signal1 = pyqtSignal(str)
    _signal2 = pyqtSignal(str)
    _signal3 = pyqtSignal(str)
    _signal4 = pyqtSignal(str)
    _signal5 = pyqtSignal(str)
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
        #print(response1['now']['humidity'])
        shidu=response1['now']['humidity']
        self._signal2.emit(shidu)
        wendu=response1['now']['temp']
        self._signal3.emit(wendu)
        tian=response1['now']['text']
        self._signal4.emit(tian)
        ico=response1['now']['icon']
        self._signal5.emit(ico)
        response2 = requests.get('https://devapi.qweather.com/v7/astronomy/sunmoon?location='+self.id+'&key=04fe891110264bfd89f9c57ab0c64169'+"&date="+time.strftime("%Y%m%d", time.localtime()) ).json()
        #print(response2['sunrise'])
        pattern = re.compile('T+\d{2}:\d{2}')
        str1 = response2['sunrise']
        sun1=pattern.search(str1).group().replace("T","")
        self._signal.emit(sun1)
        #print(response2['sunset'])
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
        self.timer1 = QTimer()  # 初始化定时器
        self.timer1.timeout.connect(self.tianqi_)
        self.timer1.start(2*60*1000)
        self.thread = Runthread() # 创建线程
        self.thread._signal.connect(self.callbacklog) # 连接信号
        self.thread._signal1.connect(self.callbacklog1)
        self.thread._signal2.connect(self.callbacklog2)
        self.thread._signal3.connect(self.callbacklog3)
        self.thread._signal4.connect(self.callbacklog4)
        self.thread._signal5.connect(self.callbacklog5)
        self.thread.start() # 开始线程
        self.m_movie()
    def m_movie(self):
        movie = QMovie("static\one.gif")
        self.label_9.setMovie(movie)
        movie.start() 
    def tianqi_(self):
        self.thread.start() # 开始线程
        print("开始更新数据！")
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
    def callbacklog2(self,shidu):
        self.label_7.setText(shidu+"%")
    def callbacklog3(self,wendu):
        self.label_3.setText(wendu)
    def callbacklog4(self,tian):
        if 1<len(tian)<7:
            p=150
        elif len(tian)<2:
            p=100
        else:
            p=205
        font = QtGui.QFont()
        font.setFamily("华光行书_CNKI")
        font.setPointSize(p/len(tian))
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setText(tian)    
    def callbacklog5(self,ico):
        print(ico)
        #self.label_4.setStyleSheet("image: url(:/tianqi/static/"+ico+".png);")
        jpg = QtGui.QPixmap('static/'+ico+'.png').scaled(self.label_4.width(), self.label_4.height())
        self.label_4.setPixmap(jpg)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = MainWindow()
    App.setStyleSheet(qdarkstyle.load_stylesheet())
    ex.show()
    sys.exit(App.exec_())


