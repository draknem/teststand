#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is a simple test results visualiser.

Author: Draknem Flishkin
Last edited: April 24, 2018
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QDesktopWidget, QApplication, QAction, QMessageBox, QTabWidget, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QInputDialog
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap
import sys, sqlite3, hashlib

class settings(QMainWindow):
    def __init__(self, parent=None):
        super(settings, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.table_widget = tabsWidget(self)
        self.setCentralWidget(self.table_widget)
        self.resize(640, 480)
        self.center()
        self.setWindowTitle('Настройки')
        self.setWindowIcon(QIcon('set.svg'))
        self.setFixedSize(640, 480)

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class m0d3l(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.wbch = Wbench(self)
        self.setCentralWidget(self.wbch)
        self.wbch.resize(640, 480)

        self.set = settings(self)

        self.resize(640, 480)
        self.center()
        self.setWindowTitle('Модель')
        self.setWindowIcon(QIcon('main.svg'))

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit.svg'), 'Выход', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Выход из программы')
        exitButton.triggered.connect(self.exapp)
        fileMenu.addAction(exitButton)

        settingsButton = QAction(QIcon('set.svg'), 'Настройки', self)
        settingsButton.setShortcut('Ctrl+S')
        settingsButton.triggered.connect(lambda: self.sett())
        editMenu.addAction(settingsButton)

        aboutButton = QAction(QIcon('about.svg'), 'О работе', self)
        aboutButton.setShortcut('Ctrl+A')
        aboutButton.setStatusTip('Информация о лабораторной работе')
        aboutButton.triggered.connect(self.close)
        helpMenu.addAction(aboutButton)

        verButton = QAction(QIcon('ver.svg'), 'О прогарамме', self)
        verButton.setShortcut('Ctrl+V')
        verButton.triggered.connect(self.ver)
        helpMenu.addAction(verButton)

        self.show()

    def sett(self):
        text, okPressed = QInputDialog.getText(self, "Настройки", "Введите пароль:", QLineEdit.Password, "")
        self.set.show()
        """
        if okPressed and text != '':
            m = hashlib.md5()
            m.update(text.encode('utf-8'))
            if m.hexdigest() == '62643c77b55c30c790d577452c9440ce':
                self.set.show()
            else:
                QMessageBox.critical(self, 'Настройки', "Введён неверный пароль")
                print(m.hexdigest())
        """

    def exapp(self):
        buttonReply = QMessageBox.question(self, 'Выход из программы', "Прогресс выполнения работы не будет сохранён. Выйти?", QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Yes:
            self.close()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)

    def ver(self):
        QMessageBox.about(self, 'О прогарамме', "Первая, тестовая версия программы")

class Wbench(QFrame):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    db=str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    num = int(c.execute('SELECT models FROM list WHERE num=' + str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    dataname=db+'_data'
    imagesname = db + '_images'
    infoname = db + '_info'
    c.execute('SELECT * FROM {tn}'. format(tn=dataname))
    states = c.execute('SELECT * FROM {tn}'.format(tn=dataname)).fetchall()
    states=states.__len__()
    meters=int(c.execute("SELECT text FROM "+infoname+" WHERE name='Meters'").fetchone()[0])
    conn.close()
    meterlist=[]

    def __init__(self, parent):
        super().__init__(parent)
        ssw1 = stateSwitcher(self)
        ssw1.resize(200, 100)
        ssw1.move(230, 260)
        self.mdl = model(self)
        self.mdl.resize(400, 240)
        self.mdl.move(125, 10)
        self.meterlist = []
        for i in range(0, 4):
            metertmp = meter(self, i + 1)
            self.meterlist.append(metertmp)
            self.meterlist[i].resize(120, 180)
            self.meterlist[i].move(5, 20)
            if i == 1:
                self.meterlist[i].move(520, 20)
                if self.meters > 2:
                    self.meterlist[i].move(5, 200)
            if i > 1:
                self.meterlist[i].move(520, 20)
                if i == 3:
                    self.meterlist[i].move(520, 200)
        self.hidemeters(4-self.meters)
        ssw1.updatemeters()

    def refresh(self):
        self.oldmeters=self.meters
        self.conn = sqlite3.connect('settings.db')
        self.c = self.conn.cursor()
        self.db = str(self.c.execute('SELECT name FROM list WHERE num=' + str(
            self.c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(self.c.execute('SELECT models FROM list WHERE num=' + str(
            self.c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        self.infoname = self.db + '_info'
        self.meters = int(self.c.execute("SELECT text FROM " + self.infoname + " WHERE name='Meters'").fetchone()[0])
        self.conn.close()
        self.mdl.refresh()
        if self.oldmeters>self.meters:
            self.hidemeters(self.oldmeters-self.meters)
        elif self.meters>self.oldmeters:
            self.showmeters(self.meters-self.oldmeters)

    def refrcont(self):
        for i in range(0,self.meters):
            self.meterlist[i].newing(i+1)

    def hidemeters(self,n):
        for i in range(0, n):
            self.meterlist[4 - i - 1].hide()
        if 4 - n < 3:
            self.meterlist[1].move(520, 20)

    def showmeters(self,n):
        for i in range(self.oldmeters, self.meters):
            self.meterlist[i].show()
        if self.meters > 2:
            self.meterlist[1].move(5, 200)

class meter(QWidget):
    def __init__(self, parent, n):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        c.execute('SELECT * FROM {tn}'.format(tn=dataname))
        meters = int(c.execute("SELECT text FROM "+infoname+" WHERE name='Meters'").fetchone()[0])
        super(QWidget, self).__init__(parent)
        self.label1 = QLabel()
        self.label1.setText(c.execute('SELECT text FROM ' + infoname + ' WHERE name=' + str(n)).fetchone()[0])
        self.label2 = QLabel()
        self.image = QPixmap()
        self.image.loadFromData(c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=' + str(n)).fetchone()[0])
        self.image=self.image.scaledToWidth(120)
        self.label2.setPixmap(self.image)
        self.label3 = QLabel()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        conn.close()

    def newing(self, n):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        imagesname = db + '_images'
        infoname = db + '_info'
        self.label1.setText(c.execute('SELECT text FROM ' + infoname + ' WHERE name=' + str(n)).fetchone()[0])
        self.image.loadFromData(c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=' + str(n)).fetchone()[0])
        self.image=self.image.scaledToWidth(120)
        self.label2.setPixmap(self.image)
        conn.close()

    def update(self, r):
        self.label3.setText(str(r))

class model(QWidget):
    def __init__(self, parent):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        c.execute('SELECT * FROM {tn}'.format(tn=dataname))
        super(QWidget, self).__init__(parent)
        self.label1 = QLabel()
        self.label1.setText(c.execute('SELECT text FROM ' + infoname + ' WHERE name=Name').fetchone()[0])
        self.label2 = QLabel()
        self.image = QPixmap()
        self.image.loadFromData(c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=5').fetchone()[0])
        self.image=self.image.scaledToWidth(440)
        self.label2.setPixmap(self.image)
        #self.label3 = QLabel()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        #self.layout.addWidget(self.label3)
        conn.close()
    def refresh(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        c.execute('SELECT * FROM {tn}'.format(tn=dataname))
        self.label1.setText(c.execute('SELECT text FROM ' + infoname + ' WHERE name=Name').fetchone()[0])
        self.image.loadFromData(c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=5').fetchone()[0])
        self.image = self.image.scaledToWidth(440)
        self.label2.setPixmap(self.image)
        # self.label3 = QLabel()
        conn.close()

class stateSwitcher(QWidget):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    db=str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    num = int(c.execute('SELECT models FROM list WHERE num=' + str(
        c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    dataname=db+'_data'
    imagesname = db + '_images'
    infoname = db + '_info'
    c.execute('SELECT * FROM {tn}'. format(tn=dataname))
    states = c.execute('SELECT * FROM {tn}'.format(tn=dataname)).fetchall()
    states = states.__len__()
    cursta=1
    conn.close()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        label = QLabel('Переключение состояний')
        label2 = QLabel()
        image = QPixmap('test.jpg')
        image=image.scaledToHeight(64)
        label2.setPixmap(image)
        statesLine = QLineEdit('1')
        upButton = QPushButton('Предыдущее')
        downButton = QPushButton('Следующее')

        upButton.clicked.connect(lambda: self.prev(statesLine))
        downButton.clicked.connect(lambda: self.next(statesLine))

        self.updatemeters()
        self.layout=QGridLayout(self)
        self.layout.activate()
        self.layout.update()
        self.layout.addWidget(label,0,0,1,2)
        self.layout.addWidget(label2,1,0,3,1)
        self.layout.addWidget(upButton,1,1,1,1)
        self.layout.addWidget(statesLine,2,1,1,1)
        self.layout.addWidget(downButton,3,1,1,1)

    def next(self, line):
        if int(line.text()) < self.states:
            line.setText(str(int(line.text()) + 1))
            self.cursta=self.cursta + 1
        else:
            line.setText('1')
            self.cursta=1
        self.parent().refresh()
        self.updatemeters()

    def prev(self, line):
        if int(line.text()) > 1:
            line.setText(str(int(line.text())-1))
            self.cursta = self.cursta - 1
        else:
            line.setText(str(self.states))
            self.cursta = self.states
        self.parent().refresh()
        self.updatemeters()

    def refresh(self):
        self.conn = sqlite3.connect('settings.db')
        self.c = self.conn.cursor()
        self.db = str(self.c.execute('SELECT name FROM list WHERE num=' + str(
            self.c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(self.c.execute('SELECT models FROM list WHERE num=' + str(
            self.c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        self.dataname = self.db + '_data'
        self.imagesname = self.db + '_images'
        self.infoname = self.db + '_info'
        self.c.execute('SELECT * FROM {tn}'.format(tn=self.dataname))
        self.states = self.c.execute('SELECT * FROM {tn}'.format(tn=self.dataname)).fetchall()
        self.states = self.states.__len__()
        self.meters = int(self.c.execute("SELECT text FROM " + self.infoname + " WHERE name='Meters'").fetchone()[0])
        self.conn.close()

    def updatemeters(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        for i in range(0, len(self.parent().meterlist)):
            self.parent().meterlist[i].update(str(c.execute(
                'SELECT m' + str(i + 1) + ' FROM ' + dataname + ' WHERE state=' + str(self.cursta)).fetchone()[0]))
        conn.close()

class tabsWidget(QWidget):
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    db=str(c.execute('SELECT name FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    num=int(c.execute('SELECT models FROM list WHERE num='+str(c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
    dataname=db+'_data'
    imagesname = db + '_images'
    infoname = db + '_info'
    c.execute('SELECT * FROM {tn}'. format(tn=dataname))
    states = c.execute('SELECT * FROM {tn}'.format(tn=dataname)).fetchall()
    states=states.__len__()
    meters=int(c.execute("SELECT text FROM "+infoname+" WHERE name='Meters'").fetchone()[0])
    conn.close()
    mlbllist = []
    mlinelist = []
    mimglist = []

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        c.execute('SELECT * FROM {tn}'.format(tn=dataname))
        states = c.execute('SELECT * FROM {tn}'.format(tn=dataname)).fetchall()
        states = states.__len__()
        meters = int(c.execute("SELECT text FROM "+infoname+" WHERE name='Meters'").fetchone()[0])

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        #self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Настройки")
        self.tabs.addTab(self.tab2, "Таблица")
        #self.tabs.addTab(self.tab3, "Предпросмотр")

        # Create first tab

        self.tab1.layout = QGridLayout(self)
        self.tab1.layout.addWidget(QLabel('Количество состояний'), 1, 0)
        self.tab1.layout.addWidget(QLabel('Количество измерителей'), 2, 0)
        self.tab1.layout.addWidget(QLabel('Установка'), 4, 0)
        self.tab1.layout.addWidget(QLabel('Название'), 3, 0)
        self.statesline=QLineEdit(str(states))
        self.metersline=QLineEdit(str(meters))
        self.nameline = QLineEdit(str(c.execute('SELECT text FROM '+infoname+' WHERE name=Name').fetchone()[0]))
        imgline=QLineEdit('')
        self.tab1.layout.addWidget(self.statesline, 1, 1)
        self.tab1.layout.addWidget(self.metersline, 2, 1)
        self.tab1.layout.addWidget(self.nameline, 3, 1)
        self.tab1.layout.addWidget(imgline, 4, 1)

        self.labelm = QLabel()
        self.image = QPixmap()
        self.image.loadFromData(c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=5').fetchone()[0])
        self.image=self.image.scaledToWidth(120)
        self.labelm.setPixmap(self.image)
        self.tab1.layout.addWidget(self.labelm, 4, 2)

        for i in range(0, 4):
            self.mlinelist.append(QLineEdit(''))
            self.tab1.layout.addWidget(self.mlinelist[i], 5+i, 1)
            self.mlbllist.append(QLabel('Измеритель '+ str(i+1)))
            self.tab1.layout.addWidget(self.mlbllist[i], 5 + i, 0)

            imgtmp = QPixmap()
            labeltmp = QLabel()
            imgtmp.loadFromData(
                c.execute('SELECT image FROM ' + imagesname + ' WHERE meter=' + str(i+1)).fetchone()[0])
            imgtmp = imgtmp.scaledToWidth(120)
            labeltmp.setPixmap(imgtmp)
            self.mimglist.append(labeltmp)
            self.tab1.layout.addWidget(self.mimglist[i], 5 + i, 2)

        for i in range(meters,4):
            self.mlinelist[i].hide()
            self.mlbllist[i].hide()
            self.mimglist[i].hide()

        applyButton = QPushButton('Применить')
        applyButton.clicked.connect(lambda: self.read(self.statesline.text(), self.metersline.text(), self.nameline.text(), imgline.text()))
        self.tab1.layout.addWidget(applyButton, 9, 2)
        newButton = QPushButton('Новая работа')
        newButton.clicked.connect(lambda: self.newtable())
        self.tab1.layout.addWidget(newButton, 9, 0)
        self.listWidget = QListWidget()

        for i in range(0,c.execute("SELECT num FROM list").fetchall().__len__()-1):
            self.listWidget.addItem(str(c.execute("SELECT text FROM "+(c.execute("SELECT name FROM list WHERE num="+str(i+2)).fetchone()[0])+"_info WHERE name='Name'").fetchone()[0]))
        self.listWidget.currentItemChanged.connect(lambda: self.workswitch())
        self.tab1.layout.addWidget(self.listWidget, 9, 1)

        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QGridLayout(self)
        self.createTable(self.states,self.meters)
        self.tab2.layout.addWidget(self.tab2.tableWidget,1,0)
        applyTableButton = QPushButton('Применить')
        applyTableButton.clicked.connect(lambda: self.savetable())
        self.tab2.layout.addWidget(applyTableButton, 2, 0)
        resetTableButton = QPushButton('Сброс')
        resetTableButton.clicked.connect(lambda: self.fillTable())
        self.tab2.layout.addWidget(resetTableButton, 3, 0)
        self.tab2.setLayout(self.tab2.layout)
        self.fillTable()
        '''
        # Create third tab
        self.tab3.wbch = Wbench(self.tab3)
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.tab3.wbch)
        self.tab3.setLayout(self.tab3.layout)
        '''
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        conn.close()

    def workswitch(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        print(str(self.listWidget.currentRow()))
        print(self.listWidget.currentRow())
        c.execute("UPDATE list SET name=" + str(self.listWidget.currentRow() + 2) + " WHERE num=1")
        conn.commit()
        self.parent().parent().wbch.refresh()
        self.parent().parent().wbch.refrcont()
        self.refresh()
        self.tab2.tableWidget.setRowCount(self.states)
        self.tab2.tableWidget.setColumnCount(self.meters)
        self.fillTable()
        conn.close()

    def newtable(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        text, okPressed = QInputDialog.getText(self, "Новая таблица", "Введите название:")
        if okPressed and text != '':
            newdb=str(text)
            newdataname = newdb + '_data'
            newimagesname = newdb + '_images'
            newinfoname = newdb + '_info'
            c.execute(
                "CREATE TABLE " + newdataname + " ( `state` INTEGER NOT NULL UNIQUE, `m1` NUMERIC, `m2` NUMERIC, `m3` NUMERIC, `m4` NUMERIC, PRIMARY KEY(`state`) )")
            c.execute(
                "CREATE TABLE " + newimagesname + " ( `meter` INTEGER NOT NULL UNIQUE, `image` BLOB, PRIMARY KEY(`meter`) )")
            c.execute(
                "CREATE TABLE " + newinfoname + " ( `name` TEXT NOT NULL UNIQUE, `text` TEXT, PRIMARY KEY(`name`) )")
            c.execute("INSERT INTO " + newdataname + " SELECT * FROM " + dataname)
            c.execute("INSERT INTO " + newimagesname + " SELECT * FROM " + imagesname)
            c.execute("INSERT INTO " + newinfoname + " SELECT * FROM " + infoname)
            n=int(c.execute('SELECT num FROM list').fetchall().__len__())
            c.execute("INSERT INTO list (num,name,models) VALUES ("+str(n+1)+",'"+newdb+"', 1)")
            c.execute("UPDATE list SET name=" + str(n+1) + " WHERE num=1")
            self.parent().parent().wbch.refresh()
            self.parent().parent().wbch.refrcont()
            self.refresh()
            self.tab2.tableWidget.setRowCount(self.states)
            self.tab2.tableWidget.setColumnCount(self.meters)
            self.fillTable()
            conn.commit()
        conn.close()

    def read(self, statesline, metersline, nameline, imgline):
        self.states = int(self.statesline.text())
        self.meters = int(self.metersline.text())
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        dataname = db + '_data'
        imagesname = db + '_images'
        infoname = db + '_info'
        statescur = c.execute('SELECT * FROM {tn}'.format(tn=dataname)).fetchall()
        statescur = statescur.__len__()
        meterscur = int(c.execute("SELECT text FROM "+infoname+" WHERE name='Meters'").fetchone()[0])

        if statescur>self.states:
            for i in range(self.states, statescur):
                c.execute('DELETE FROM ' + dataname + ' WHERE state=' + str(i+1))
        elif statescur<self.states:
            for i in range(statescur, self.states):
                c.execute('INSERT INTO ' + dataname + ' (state) VALUES ('+str(i+1)+')')

        c.execute("UPDATE " + infoname + " SET text='" + nameline + "' WHERE name='Name'")
        c.execute("UPDATE " + infoname + " SET text=" + str(self.meters) + " WHERE name='Meters'")
        if imgline!='':
            with open(imgline, 'rb') as f:
                ablob = f.read()
            c.execute(("UPDATE " + imagesname + " SET image=? WHERE meter=5"),[sqlite3.Binary(ablob)])
            f.close()
            conn.commit()
        for i in range(0,4):
            if self.mlinelist[i].text() !='':
                with open(self.mlinelist[i].text(), 'rb') as f:
                    ablob = f.read()
                c.execute(("UPDATE " + imagesname + " SET image=? WHERE meter="+str(i+1)),[sqlite3.Binary(ablob)])
                f.close()
                conn.commit()
        conn.commit()
        conn.close()
        self.tab2.tableWidget.setRowCount(self.states)
        self.tab2.tableWidget.setColumnCount(self.meters)
        self.parent().parent().wbch.refresh()
        self.parent().parent().wbch.refrcont()
        self.refresh()
        self.fillTable()

    def refresh(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        db = str(c.execute('SELECT name FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        num = int(c.execute('SELECT models FROM list WHERE num=' + str(
            c.execute('SELECT name FROM list WHERE num=1').fetchone()[0])).fetchone()[0])
        self.dataname = db + '_data'
        self.imagesname = db + '_images'
        self.infoname = db + '_info'
        self.states = c.execute('SELECT * FROM {tn}'.format(tn=self.dataname)).fetchall()
        self.states = self.states.__len__()
        self.meters = int(c.execute("SELECT text FROM "+self.infoname+" WHERE name='Meters'").fetchone()[0])
        self.statesline.setText(str(self.states))
        self.metersline.setText(str(self.meters))
        self.nameline.setText(str(c.execute('SELECT text FROM '+self.infoname+' WHERE name=Name').fetchone()[0]))
        self.image.loadFromData(c.execute('SELECT image FROM ' + self.imagesname + ' WHERE meter=5').fetchone()[0])
        self.image=self.image.scaledToWidth(120)
        self.labelm.setPixmap(self.image)
        for i in range(0,self.meters):
            self.mlinelist[i].show()
            self.mlbllist[i].show()
            self.mimglist[i].show()
            imgtmp = QPixmap()
            labeltmp = QLabel()
            imgtmp.loadFromData(
                c.execute('SELECT image FROM ' + self.imagesname + ' WHERE meter=' + str(i+1)).fetchone()[0])
            imgtmp = imgtmp.scaledToWidth(120)
            self.mimglist[i].setPixmap(imgtmp)
            if self.meters>2:
                self.parent().setFixedSize(640, 510)
                self.parent().resize(640, 510)
                if self.meters>3:
                    self.parent().setFixedSize(640, 640)
                    self.parent().resize(640, 640)
        for i in range(self.meters,4):
            self.mlinelist[i].hide()
            self.mlbllist[i].hide()
            self.mimglist[i].hide()
            if self.meters<4:
                self.parent().setFixedSize(640, 510)
                self.parent().resize(640, 510)
                if self.meters<3:
                    self.parent().setFixedSize(640, 480)
                    self.parent().resize(640, 480)
        k=self.listWidget.currentRow()
        if k!=-1:
            self.listWidget.item(k).setText(str(c.execute("SELECT text FROM "+self.infoname+" WHERE name='Name'").fetchone()[0]))
        conn.close()

    def createTable(self,r,c):
            self.tab2.tableWidget = QTableWidget()
            self.tab2.tableWidget.setRowCount(r)
            self.tab2.tableWidget.setColumnCount(c)
            self.tab2.tableWidget.move(0, 0)
            #self.tab2.tableWidget.doubleClicked.connect(self.on_click)

    def fillTable(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        for i in range(0, self.states):
            for j in range(0, self.meters):
                self.tab2.tableWidget.setItem(i,j, QTableWidgetItem(str(c.execute('SELECT m'+str(j+1)+' FROM '+ self.dataname +' WHERE state='+str(i+1)).fetchone()[0])))
        conn.close()

    def savetable(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        for i in range(0, self.states):
            for j in range(0, self.meters):
                c.execute("UPDATE "+self.dataname+" SET m"+str(j+1)+"="+str(self.tab2.tableWidget.item(i,j).text())+" WHERE state="+str(i+1))
                #self.tab2.tableWidget.setItem(i,j, QTableWidgetItem(str(c.execute('SELECT m'+str(j+1)+' FROM '+ self.dataname +' WHERE state='+str(i+1)).fetchone()[0])))
        conn.commit()
        conn.close()

'''
    @pyqtSlot()
    def on_click(self):
        print("\ n")
        for currentQTableWidgetItem in self.tab2.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
'''

if __name__ == '__main__':

    app = QApplication([])
    model = m0d3l()
    sys.exit(app.exec_())
