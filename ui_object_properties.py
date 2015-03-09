# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_object_properties.ui'
#
# Created: Wed Feb 25 11:38:14 2015
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

class Ui_ObjectProperties(object):
    def setupUi(self, ObjectProperties):
        ObjectProperties.setObjectName(_fromUtf8("ObjectProperties"))
        ObjectProperties.resize(258, 232)
        self.group_connected_to = QtGui.QGroupBox(ObjectProperties)
        self.group_connected_to.setGeometry(QtCore.QRect(0, 0, 251, 211))
        self.group_connected_to.setFlat(False)
        self.group_connected_to.setCheckable(False)
        self.group_connected_to.setObjectName(_fromUtf8("group_connected_to"))
        self.gridLayoutWidget = QtGui.QWidget(self.group_connected_to)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 181, 161))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.down = QtGui.QPushButton(self.gridLayoutWidget)
        self.down.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.down.setCheckable(True)
        self.down.setAutoExclusive(False)
        self.down.setObjectName(_fromUtf8("down"))
        self.gridLayout.addWidget(self.down, 3, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 0, 1, 1)
        self.up = QtGui.QPushButton(self.gridLayoutWidget)
        self.up.setCheckable(True)
        self.up.setChecked(False)
        self.up.setAutoExclusive(False)
        self.up.setFlat(False)
        self.up.setObjectName(_fromUtf8("up"))
        self.gridLayout.addWidget(self.up, 0, 1, 1, 1)
        self.left = QtGui.QPushButton(self.gridLayoutWidget)
        self.left.setCheckable(True)
        self.left.setAutoExclusive(False)
        self.left.setObjectName(_fromUtf8("left"))
        self.gridLayout.addWidget(self.left, 2, 0, 1, 1)
        self.right = QtGui.QPushButton(self.gridLayoutWidget)
        self.right.setCheckable(True)
        self.right.setAutoExclusive(False)
        self.right.setObjectName(_fromUtf8("right"))
        self.gridLayout.addWidget(self.right, 2, 2, 1, 1)

        self.retranslateUi(ObjectProperties)
        QtCore.QMetaObject.connectSlotsByName(ObjectProperties)

    def retranslateUi(self, ObjectProperties):
        ObjectProperties.setWindowTitle(_translate("ObjectProperties", "Właściwości obiektu", None))
        self.group_connected_to.setTitle(_translate("ObjectProperties", "Połączenia do sąsiędnich obiektów", None))
        self.down.setText(_translate("ObjectProperties", "Dół", None))
        self.up.setText(_translate("ObjectProperties", "Góra", None))
        self.left.setText(_translate("ObjectProperties", "Lewo", None))
        self.right.setText(_translate("ObjectProperties", "Prawo", None))

