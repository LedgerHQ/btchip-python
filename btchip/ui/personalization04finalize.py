# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-04-finalize.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 267)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(20, 20, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.FinishButton = QtWidgets.QPushButton(Dialog)
        self.FinishButton.setGeometry(QtCore.QRect(320, 230, 75, 25))
        self.FinishButton.setObjectName("FinishButton")
        self.IntroLabel_4 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_4.setGeometry(QtCore.QRect(10, 70, 351, 61))
        self.IntroLabel_4.setWordWrap(True)
        self.IntroLabel_4.setObjectName("IntroLabel_4")
        self.IntroLabel_5 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_5.setGeometry(QtCore.QRect(50, 140, 121, 21))
        self.IntroLabel_5.setWordWrap(True)
        self.IntroLabel_5.setObjectName("IntroLabel_5")
        self.pin1 = QtWidgets.QLineEdit(Dialog)
        self.pin1.setGeometry(QtCore.QRect(200, 140, 181, 21))
        self.pin1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin1.setObjectName("pin1")
        self.remainingAttemptsLabel = QtWidgets.QLabel(Dialog)
        self.remainingAttemptsLabel.setGeometry(QtCore.QRect(120, 170, 171, 31))
        font = QtGui.QFont()
        font.setItalic(True)
        self.remainingAttemptsLabel.setFont(font)
        self.remainingAttemptsLabel.setWordWrap(True)
        self.remainingAttemptsLabel.setObjectName("remainingAttemptsLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup - security"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup - completed"))
        self.FinishButton.setText(_translate("Dialog", "Finish"))
        self.IntroLabel_4.setText(_translate("Dialog", "BTChip setup is completed. Please enter your PIN to validate it then press Finish"))
        self.IntroLabel_5.setText(_translate("Dialog", "BTChip PIN :"))
        self.remainingAttemptsLabel.setText(_translate("Dialog", "Remaining attempts"))

