#!/usr/bin/env python3

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_mainwindow import Ui_MainWindow



class DottorrentGUI(Ui_MainWindow):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		self.MainWindow = MainWindow

		self.fileRadioButton.toggled.connect(self.inputTypeToggle)
		self.fileRadioButton.setChecked(True)

		self.browseButton.clicked.connect(self.browseInput)


	def inputTypeToggle(self):
		if self.MainWindow.sender() == self.fileRadioButton:
			self.inputType = 'file'
		else:
			self.inputType = 'directory'
		self.inputEdit.setText('')

	def browseInput(self):
		if self.inputType == 'file':
			fn = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Select file')
			if fn[0]:
				self.inputEdit.setText(fn[0])
		else:
			dn = QtWidgets.QFileDialog.getExistingDirectory(self.MainWindow, 'Select directory')
			if dn[0]:
				self.inputEdit.text.setText(fn[0])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DottorrentGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())