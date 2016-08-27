# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(372, 226)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.programNameLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.programNameLabel.setFont(font)
        self.programNameLabel.setObjectName("programNameLabel")
        self.verticalLayout.addWidget(self.programNameLabel)
        self.programVersionLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.programVersionLabel.setFont(font)
        self.programVersionLabel.setObjectName("programVersionLabel")
        self.verticalLayout.addWidget(self.programVersionLabel)
        self.dtVersionLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.dtVersionLabel.setFont(font)
        self.dtVersionLabel.setObjectName("dtVersionLabel")
        self.verticalLayout.addWidget(self.dtVersionLabel)
        self.infoLabel = QtWidgets.QLabel(AboutDialog)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setOpenExternalLinks(True)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.programNameLabel.setText(_translate("AboutDialog", "dottorrent-gui"))
        self.programVersionLabel.setText(_translate("AboutDialog", "PROGRAM_VERSION"))
        self.dtVersionLabel.setText(_translate("AboutDialog", "DOTTORRENT_VERSION"))
        self.infoLabel.setText(_translate("AboutDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">© 2016 Kevin Zhang</span></p><p><span style=\" font-size:10pt;\">dottorrent-gui is made available under the terms of the </span><a href=\"http://choosealicense.com/licenses/gpl-3.0/\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">GNU General Public License, version 3</span></a><span style=\" font-size:10pt;\">.</span></p><p><a href=\"https://github.com/kz26/dottorrent-gui\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://github.com/kz26/dottorrent-gui</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AboutDialog = QtWidgets.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec_())

