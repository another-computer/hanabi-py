# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChatClientSplitterUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 650)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        self.splitter_2.setGeometry(QtCore.QRect(0, 0, 1191, 541))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.address_label = QtWidgets.QLabel(self.splitter)
        self.address_label.setObjectName("address_label")
        self.chat_log = QtWidgets.QListWidget(self.splitter)
        self.chat_log.setObjectName("chat_log")
        self.input_box = QtWidgets.QLineEdit(self.splitter)
        self.input_box.setObjectName("input_box")
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 17))
        self.menuBar.setObjectName("menuBar")
        self.menuClient = QtWidgets.QMenu(self.menuBar)
        self.menuClient.setObjectName("menuClient")
        self.menuThemes = QtWidgets.QMenu(self.menuBar)
        self.menuThemes.setObjectName("menuThemes")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionBookmark = QtWidgets.QAction(MainWindow)
        self.actionBookmark.setObjectName("actionBookmark")
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.action1337 = QtWidgets.QAction(MainWindow)
        self.action1337.setObjectName("action1337")
        self.menuClient.addAction(self.actionConnect)
        self.menuClient.addAction(self.actionBookmark)
        self.menuThemes.addAction(self.actionLight)
        self.menuThemes.addAction(self.actionDark)
        self.menuThemes.addAction(self.action1337)
        self.menuBar.addAction(self.menuClient.menuAction())
        self.menuBar.addAction(self.menuThemes.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.address_label.setText(_translate("MainWindow", "No Connection Established"))
        self.menuClient.setTitle(_translate("MainWindow", "Connections"))
        self.menuThemes.setTitle(_translate("MainWindow", "Themes"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionBookmark.setText(_translate("MainWindow", "Bookmark"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.action1337.setText(_translate("MainWindow", "1337"))
