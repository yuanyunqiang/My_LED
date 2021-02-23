import sys
import time
import qdarkgraystyle
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_main import Ui_MainWindow
from PyQt5.QtCore import QTimer

    
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self) 
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time_)
        self.timer.start(100)
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
    App.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ex.show()
    sys.exit(App.exec_())


