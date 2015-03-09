# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created: Fri Feb 13 14:10:20 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_subStationSim(object):
    def setupUi(self, subStationSim):
        subStationSim.setObjectName(_fromUtf8("subStationSim"))
        subStationSim.resize(595, 372)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(subStationSim.sizePolicy().hasHeightForWidth())
        subStationSim.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(subStationSim)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 581, 351))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layout_list = QtGui.QListWidget(self.horizontalLayoutWidget)
        self.layout_list.setObjectName(_fromUtf8("layout_list"))
        self.horizontalLayout.addWidget(self.layout_list)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.open_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.open_button.setFlat(False)
        self.open_button.setObjectName(_fromUtf8("open_button"))
        self.verticalLayout.addWidget(self.open_button)
        self.edit_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.edit_button.setObjectName(_fromUtf8("edit_button"))
        self.verticalLayout.addWidget(self.edit_button)
        self.delete_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.delete_button.setObjectName(_fromUtf8("delete_button"))
        self.verticalLayout.addWidget(self.delete_button)
        self.new_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.new_button.setObjectName(_fromUtf8("new_button"))
        self.verticalLayout.addWidget(self.new_button)
        self.close_button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.close_button.setObjectName(_fromUtf8("close_button"))
        self.verticalLayout.addWidget(self.close_button)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        subStationSim.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(subStationSim)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        subStationSim.setStatusBar(self.statusbar)

        self.retranslateUi(subStationSim)
        QtCore.QObject.connect(self.close_button, QtCore.SIGNAL(_fromUtf8("clicked()")), subStationSim.close)
        QtCore.QMetaObject.connectSlotsByName(subStationSim)

    def retranslateUi(self, subStationSim):
        subStationSim.setWindowTitle(_translate("subStationSim", "MainWindow", None))
        self.open_button.setText(_translate("subStationSim", "Otwórz", None))
        self.edit_button.setText(_translate("subStationSim", "Edycja", None))
        self.delete_button.setText(_translate("subStationSim", "Usuń", None))
        self.new_button.setText(_translate("subStationSim", "Nowy", None))
        self.close_button.setText(_translate("subStationSim", "Zakończ", None))

