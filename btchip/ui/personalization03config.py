# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-03-config.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 243)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(30, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.IntroLabel = QtWidgets.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(20, 50, 351, 61))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName("IntroLabel")
        self.qwertyButton = QtWidgets.QRadioButton(Dialog)
        self.qwertyButton.setGeometry(QtCore.QRect(50, 110, 94, 21))
        self.qwertyButton.setChecked(True)
        self.qwertyButton.setObjectName("qwertyButton")
        self.keyboardGroup = QtWidgets.QButtonGroup(Dialog)
        self.keyboardGroup.setObjectName("keyboardGroup")
        self.keyboardGroup.addButton(self.qwertyButton)
        self.qwertzButton = QtWidgets.QRadioButton(Dialog)
        self.qwertzButton.setGeometry(QtCore.QRect(50, 140, 94, 21))
        self.qwertzButton.setObjectName("qwertzButton")
        self.keyboardGroup.addButton(self.qwertzButton)
        self.azertyButton = QtWidgets.QRadioButton(Dialog)
        self.azertyButton.setGeometry(QtCore.QRect(50, 170, 94, 21))
        self.azertyButton.setObjectName("azertyButton")
        self.keyboardGroup.addButton(self.azertyButton)
        self.CancelButton = QtWidgets.QPushButton(Dialog)
        self.CancelButton.setGeometry(QtCore.QRect(10, 210, 75, 25))
        self.CancelButton.setObjectName("CancelButton")
        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(320, 210, 75, 25))
        self.NextButton.setObjectName("NextButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup - config (3/3)"))
        self.IntroLabel.setText(_translate("Dialog", "Please select your keyboard type to type the second factor confirmation"))
        self.qwertyButton.setText(_translate("Dialog", "QWERTY"))
        self.qwertzButton.setText(_translate("Dialog", "QWERTZ"))
        self.azertyButton.setText(_translate("Dialog", "AZERTY"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.NextButton.setText(_translate("Dialog", "Next"))

