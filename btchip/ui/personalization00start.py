# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-00-start.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 231)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(120, 20, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.IntroLabel = QtWidgets.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(20, 60, 351, 61))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName("IntroLabel")
        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(310, 200, 75, 25))
        self.NextButton.setObjectName("NextButton")
        self.arningLabel = QtWidgets.QLabel(Dialog)
        self.arningLabel.setGeometry(QtCore.QRect(20, 120, 351, 81))
        self.arningLabel.setWordWrap(True)
        self.arningLabel.setObjectName("arningLabel")
        self.CancelButton = QtWidgets.QPushButton(Dialog)
        self.CancelButton.setGeometry(QtCore.QRect(20, 200, 75, 25))
        self.CancelButton.setObjectName("CancelButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup"))
        self.IntroLabel.setText(_translate("Dialog", "Your BTChip dongle is not set up - you\'ll be able to create a new wallet, or restore an existing one, and choose your security profile."))
        self.NextButton.setText(_translate("Dialog", "Next"))
        self.arningLabel.setText(_translate("Dialog", "Sensitive information including your dongle PIN will be exchanged during this setup phase - it is recommended to execute it on a secure computer, disconnected from any network, especially if you restore a wallet backup."))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))

