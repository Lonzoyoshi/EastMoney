# -*- coding: utf-8 -*-
import sys
import time
import webbrowser
import os

import SpiderWithOpt
from SpiderWithOpt import SpiderEastMM
import showAnalysis
from showAnalysis import show_analysis
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

listOfModule = ['沪深京A股',
            '上证A股',
            '深证A股',
            '北证A股',
            '新股',
            '创业板',
            '科创板',
            '沪股通',
            '深股通',
            'B股',
            '上证AB股比价',
            '深证AB股比价',
            '风险警示板',
            '两网及退市']
ModuleChoice = 0
PageChoice = 1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.setWindowIcon(QIcon('./favicon.ico'))
        self.resize(600, 400)
        self.mainUI()
        self.buttonUI()


    def mainUI(self):
        self.setWindowTitle("东方财富股票信息爬取和分析")
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)



    def buttonUI(self):
        self.button1 = QPushButton("选择板块", self)
        self.button2 = QPushButton("选择页码", self)
        self.button3 = QPushButton("开始爬取", self)
        self.button4 = QPushButton("退出程序", self)
        self.button1.move(100, 100)
        self.button2.move(100, 150)
        self.button3.move(100, 200)
        self.button4.move(100, 250)
        self.button1.clicked.connect(self.clickButton)
        self.button1.clicked.connect(self.close)
        self.button2.clicked.connect(self.clickButton)
        self.button2.clicked.connect(self.close)
        self.button3.clicked.connect(self.clickButton)
        self.button3.clicked.connect(self.close)
        self.button4.clicked.connect(self.clickButton)
        self.show()

    # 跳转至相应模块的界面
    def clickButton(self):
        sender = self.sender()
        if sender.text() == "选择板块":
            self.module_choice_ui = ModuleChoiceUI()
            self.module_choice_ui.show()
            print("进入选择板块模块")
        elif sender.text() == "选择页码":
            self.page_choice_ui = PageChoiceUI()
            self.page_choice_ui.show()
            print("进入选择页码模块")
        elif sender.text() == "开始爬取":
            self.spider_ui = SpiderUI()
            self.spider_ui.show()
            print("进入爬取模块")
        elif sender.text() == "退出程序":
            self.close()

class ModuleChoiceUI(QMainWindow):
    def __init__(self):
        super(ModuleChoiceUI, self).__init__(parent=None)
        self.resize(600, 400)
        self.setWindowTitle("选择需要爬取的证券板块")
        self.buttonUI()
    def buttonUI(self):
        self.button1 = QPushButton("沪深京A股", self)
        self.button2 = QPushButton("上证A股", self)
        self.button3 = QPushButton("深证A股", self)
        self.button4 = QPushButton("北证A股", self)
        self.button5 = QPushButton("新股", self)
        self.button6 = QPushButton("创业板", self)
        self.button7 = QPushButton("科创板", self)
        self.button8 = QPushButton("沪股通", self)
        self.button9 = QPushButton("深股通", self)
        self.button10 = QPushButton("B股", self)
        self.button11 = QPushButton("上证AB股比价", self)
        self.button12 = QPushButton("深证AB股比价", self)
        self.button13 = QPushButton("风险警示板", self)
        self.button14 = QPushButton("两网及退市", self)
        self.button1.move(100, 100)
        self.button2.move(100, 150)
        self.button3.move(100, 200)
        self.button4.move(100, 250)
        self.button5.move(100, 300)
        self.button6.move(200, 100)
        self.button7.move(200, 150)
        self.button8.move(200, 200)
        self.button9.move(200, 250)
        self.button10.move(200, 300)
        self.button11.move(300, 100)
        self.button12.move(300, 150)
        self.button13.move(300, 200)
        self.button14.move(300, 250)
        self.button1.clicked.connect(self.clickButton)
        self.button1.clicked.connect(self.close)
        self.button2.clicked.connect(self.clickButton)
        self.button2.clicked.connect(self.close)
        self.button3.clicked.connect(self.clickButton)
        self.button3.clicked.connect(self.close)
        self.button4.clicked.connect(self.clickButton)
        self.button4.clicked.connect(self.close)
        self.button5.clicked.connect(self.clickButton)
        self.button5.clicked.connect(self.close)
        self.button6.clicked.connect(self.clickButton)
        self.button6.clicked.connect(self.close)
        self.button7.clicked.connect(self.clickButton)
        self.button7.clicked.connect(self.close)
        self.button8.clicked.connect(self.clickButton)
        self.button8.clicked.connect(self.close)
        self.button9.clicked.connect(self.clickButton)
        self.button9.clicked.connect(self.close)
        self.button10.clicked.connect(self.clickButton)
        self.button10.clicked.connect(self.close)
        self.button11.clicked.connect(self.clickButton)
        self.button11.clicked.connect(self.close)
        self.button12.clicked.connect(self.clickButton)
        self.button12.clicked.connect(self.close)
        self.button13.clicked.connect(self.clickButton)
        self.button13.clicked.connect(self.close)
        self.button14.clicked.connect(self.clickButton)
        self.button14.clicked.connect(self.close)



    def clickButton(self):
        global ModuleChoice
        sender = self.sender()
        print(sender.text() + "按钮被点击了")
        ModuleChoice = int(listOfModule.index(sender.text()))
        print("您选择的板块为：" + str(ModuleChoice))
        self.main_window = MainWindow()
        self.main_window.show()
class PageChoiceUI(QMainWindow):
    def __init__(self):
        super(PageChoiceUI, self).__init__(parent=None)
        self.resize(600, 400)
        self.setWindowTitle("选择需要爬取的页码")
        self.buttonUI()
        self.QlineUI()
    def QlineUI(self):
        self.Qline = QLineEdit(self)
        self.Qline.move(100, 100)
        self.Qline.resize(200, 30)
        self.Qline.setPlaceholderText("请输入页码(1-10)")
        self.Qline.setValidator(QIntValidator())
        self.Qline.textChanged.connect(self.setPageChoice)
    def buttonUI(self):
        self.button1 = QPushButton("确定", self)
        self.button1.move(100, 150)
        self.button1.clicked.connect(self.clickedOK)
        self.button1.clicked.connect(self.close)

    def setPageChoice(self, value):
        global PageChoice
        PageChoice = int(value)
        print("您选择的页码为：" + str(PageChoice))
    def clickedOK(self):
        print("确定按钮被点击了")
        self.main_window = MainWindow()
        self.main_window.show()


class SpiderUI(QMainWindow):
    def __init__(self):
        super(SpiderUI, self).__init__(parent=None)
        self.resize(600, 400)
        self.setWindowTitle("东方财富股票信息爬取和分析")
        self.buttonUI()


    def buttonUI(self):
        self.button1 = QPushButton("开始爬取", self)
        self.button2 = QPushButton("显示分析结果", self)
        self.button1.move(100, 100)
        self.button2.move(100, 150)
        self.button1.clicked.connect(self.clickButton)
        self.button1.clicked.connect(self.close)
        self.button2.clicked.connect(self.clickButton)
        self.button2.clicked.connect(self.close)

    def clickButton(self):
        global ModuleChoice
        global PageChoice
        sender = self.sender()
        if sender.text() == "开始爬取":
            SpiderEastMM(ModuleChoice, PageChoice)
            print("爬取完成")
            self.spider_ui = SpiderUI()
            self.spider_ui.show()
        elif sender.text() == "显示分析结果":
            show_analysis(listOfModule[ModuleChoice], PageChoice)
            path_root = os.path.dirname(os.getcwd())
            print(path_root)
            html_path = os.path.join(path_root, 'EastMoney/eastmm_EastMoney.html')
            #打开html文件
            webbrowser.open(html_path)
            print("显示分析结果")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
