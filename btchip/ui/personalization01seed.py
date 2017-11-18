# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'personalization-01-seed.ui'
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
        self.TitleLabel.setGeometry(QtCore.QRect(50, 20, 311, 31))
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
        self.NewWalletButton = QtWidgets.QRadioButton(Dialog)
        self.NewWalletButton.setGeometry(QtCore.QRect(20, 130, 94, 21))
        self.NewWalletButton.setChecked(True)
        self.NewWalletButton.setObjectName("NewWalletButton")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.NewWalletButton)
        self.RestoreWalletButton = QtWidgets.QRadioButton(Dialog)
        self.RestoreWalletButton.setGeometry(QtCore.QRect(20, 180, 171, 21))
        self.RestoreWalletButton.setObjectName("RestoreWalletButton")
        self.buttonGroup.addButton(self.RestoreWalletButton)
        self.seed = QtWidgets.QLineEdit(Dialog)
        self.seed.setEnabled(False)
        self.seed.setGeometry(QtCore.QRect(50, 210, 331, 21))
        self.seed.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.seed.setObjectName("seed")
        self.CancelButton = QtWidgets.QPushButton(Dialog)
        self.CancelButton.setGeometry(QtCore.QRect(10, 270, 75, 25))
        self.CancelButton.setObjectName("CancelButton")
        self.NextButton = QtWidgets.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(320, 270, 75, 25))
        self.NextButton.setObjectName("NextButton")
        self.mnemonicNotAvailableLabel = QtWidgets.QLabel(Dialog)
        self.mnemonicNotAvailableLabel.setGeometry(QtCore.QRect(130, 240, 171, 31))
        font = QtGui.QFont()
        font.setItalic(True)
        self.mnemonicNotAvailableLabel.setFont(font)
        self.mnemonicNotAvailableLabel.setWordWrap(True)
        self.mnemonicNotAvailableLabel.setObjectName("mnemonicNotAvailableLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BTChip setup - seed"))
        self.TitleLabel.setText(_translate("Dialog", "BTChip setup - seed (1/3)"))
        self.IntroLabel.setText(_translate("Dialog", "Please select an option : either create a new wallet or restore an existing one"))
        self.NewWalletButton.setText(_translate("Dialog", "New Wallet"))
        self.RestoreWalletButton.setText(_translate("Dialog", "Restore wallet backup"))
        self.seed.setPlaceholderText(_translate("Dialog", "Enter an hexadecimal seed or a BIP 39 mnemonic code"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.NextButton.setText(_translate("Dialog", "Next"))
        self.mnemonicNotAvailableLabel.setText(_translate("Dialog", "Mnemonic API is not available"))

