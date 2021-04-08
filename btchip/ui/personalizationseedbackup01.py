# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-seedbackup-01.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(30, 20, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(320, 270, 75, 25))
        self.NextButton.setObjectName("NextButton")
        self.IntroLabel = QtWidgets.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(10, 100, 351, 31))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName("IntroLabel")
        self.IntroLabel_2 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_2.setGeometry(QtCore.QRect(10, 140, 351, 31))
        self.IntroLabel_2.setWordWrap(True)
        self.IntroLabel_2.setObjectName("IntroLabel_2")
        self.IntroLabel_3 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_3.setGeometry(QtCore.QRect(10, 180, 351, 41))
        self.IntroLabel_3.setWordWrap(True)
        self.IntroLabel_3.setObjectName("IntroLabel_3")
        self.TitleLabel_2 = QtWidgets.QLabel(Dialog)
        self.TitleLabel_2.setGeometry(QtCore.QRect(90, 60, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel_2.setFont(font)
        self.TitleLabel_2.setObjectName("TitleLabel_2")
        self.IntroLabel_4 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_4.setGeometry(QtCore.QRect(10, 220, 351, 41))
        self.IntroLabel_4.setWordWrap(True)
        self.IntroLabel_4.setObjectName("IntroLabel_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup  - seed backup"))
        self.NextButton.setText(_translate("Dialog", "Next"))
        self.IntroLabel.setText(_translate("Dialog", "A new seed has been generated for your wallet."))
        self.IntroLabel_2.setText(_translate("Dialog", "You must backup this seed and keep it out of reach of hackers (typically by keeping it on paper)."))
        self.IntroLabel_3.setText(_translate("Dialog", "You can use this seed to restore your dongle if you lose it or access your funds with any other compatible wallet."))
        self.TitleLabel_2.setText(_translate("Dialog", "READ CAREFULLY"))
        self.IntroLabel_4.setText(_translate("Dialog", "Press Next to start the backuping process."))

