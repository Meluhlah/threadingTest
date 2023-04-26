from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QDialog, QMainWindow
import threading
import gui
import sys
import serial.tools.list_ports


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopThread = threading.Event()

    def stop(self):
        self.stopThread.set()
        self.join()

    def stopped(self):
        return self.stopThread.is_set()


class mainWindow(gui.Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ports = []
        self.t1Alive = False
        self.t2Alive = False
        self.getPorts()
        self.t1 = MyThread(target=self.t1Func)
        self.t2 = MyThread(target=self.t2Func)
        self.thread1.clicked.connect(self.start_thread1)
        self.thread2.clicked.connect(self.start_thread2)
        self.t1off.clicked.connect(self.stop_thread1)
        self.t2off.clicked.connect(self.stop_thread2)

    def getPorts(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.ports.append(port.name)
            self.comboBox.addItem(port.name)

    def stop_thread1(self):
        self.t1.stop()
        if self.t1.is_alive():
            del self.t1
        self.t1Alive = False

    def stop_thread2(self):
        self.t2.stop()
        if self.t2.is_alive():
            del self.t2
        self.t2Alive = False

    def start_thread1(self):
        if not self.t1Alive:
            self.t1 = MyThread(target=self.t1Func)
            self.t1.start()
        elif not self.t1.is_alive():
            self.t1.start()
        self.t1Alive = True

    def start_thread2(self):
        if not self.t2Alive:
            self.t2 = MyThread(target=self.t2Func)
            self.t2.start()
        elif not self.t2.is_alive():
            self.t2.start()
        self.t2Alive = True

    def t1Func(self):
        while not self.t1.stopped():
            print('T1')

    def t2Func(self):
        while not self.t2.stopped():
            print('T2')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()
