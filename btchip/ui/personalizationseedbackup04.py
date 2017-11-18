# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-seedbackup-04.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 190)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(30, 10, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.IntroLabel = QtWidgets.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(10, 50, 351, 51))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName("IntroLabel")
        self.seedOkButton = QtWidgets.QPushButton(Dialog)
        self.seedOkButton.setGeometry(QtCore.QRect(20, 140, 501, 25))
        self.seedOkButton.setObjectName("seedOkButton")
        self.seedKoButton = QtWidgets.QPushButton(Dialog)
        self.seedKoButton.setGeometry(QtCore.QRect(20, 110, 501, 25))
        self.seedKoButton.setObjectName("seedKoButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup  - seed backup"))
        self.IntroLabel.setText(_translate("Dialog", "Did you see the seed correctly displayed and did you backup it properly ?"))
        self.seedOkButton.setText(_translate("Dialog", "Yes, the seed is backed up properly and kept in a safe place, move on"))
        self.seedKoButton.setText(_translate("Dialog", "No, I didn\'t see the seed. Wipe the dongle and start over"))

