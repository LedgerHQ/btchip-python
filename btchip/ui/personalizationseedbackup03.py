# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-seedbackup-03.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 513)
        self.TitleLabel = QtWidgets.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(20, 10, 351, 31))
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
        self.IntroLabel_2 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_2.setGeometry(QtCore.QRect(20, 120, 351, 31))
        self.IntroLabel_2.setWordWrap(True)
        self.IntroLabel_2.setObjectName("IntroLabel_2")
        self.IntroLabel_3 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_3.setGeometry(QtCore.QRect(20, 160, 351, 51))
        self.IntroLabel_3.setWordWrap(True)
        self.IntroLabel_3.setObjectName("IntroLabel_3")
        self.IntroLabel_4 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_4.setGeometry(QtCore.QRect(20, 220, 351, 51))
        self.IntroLabel_4.setWordWrap(True)
        self.IntroLabel_4.setObjectName("IntroLabel_4")
        self.IntroLabel_5 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_5.setGeometry(QtCore.QRect(20, 280, 351, 71))
        self.IntroLabel_5.setWordWrap(True)
        self.IntroLabel_5.setObjectName("IntroLabel_5")
        self.IntroLabel_6 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_6.setGeometry(QtCore.QRect(20, 350, 351, 51))
        self.IntroLabel_6.setWordWrap(True)
        self.IntroLabel_6.setObjectName("IntroLabel_6")
        self.IntroLabel_7 = QtWidgets.QLabel(Dialog)
        self.IntroLabel_7.setGeometry(QtCore.QRect(20, 410, 351, 51))
        self.IntroLabel_7.setWordWrap(True)
        self.IntroLabel_7.setObjectName("IntroLabel_7")
        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(310, 480, 75, 25))
        self.NextButton.setObjectName("NextButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup  - seed backup"))
        self.IntroLabel.setText(_translate("Dialog", "If you do not trust this computer, perform the following steps on a trusted one or a different device. Anything supporting keyboard input will work (smartphone, TV box ...)"))
        self.IntroLabel_2.setText(_translate("Dialog", "Open a text editor, set the focus on the text editor, then insert the dongle"))
        self.IntroLabel_3.setText(_translate("Dialog", "After a very short time, the dongle will type the seed as hexadecimal (0..9 A..F) characters, starting with \"seed\" and ending with \"X\""))
        self.IntroLabel_4.setText(_translate("Dialog", "If you perform those steps on Windows, a new device driver will be loaded the first time and the seed will not be typed. This is normal."))
        self.IntroLabel_5.setText(_translate("Dialog", "If you perform those steps on Mac, you\'ll get a popup asking you to select a keyboard type the first time and the seed will not be typed. This is normal, just close the popup."))
        self.IntroLabel_6.setText(_translate("Dialog", "If you did not see the seed for any reason, keep the focus on the text editor, unplug and plug the dongle again twice."))
        self.IntroLabel_7.setText(_translate("Dialog", "Then press Next once you wrote the seed to a safe medium (i.e. paper) and unplugged the dongle"))
        self.NextButton.setText(_translate("Dialog", "Next"))

