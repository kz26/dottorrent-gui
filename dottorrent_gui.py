#!/usr/bin/env python3

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from dottorrent import Torrent
import humanfriendly

from ui_mainwindow import Ui_MainWindow


PIECE_SIZES = [2 ** i for i in range(14, 23)]


def _isChecked(checkbox):
    return checkbox.checkState() == QtCore.Qt.Checked


class DottorrentGUI(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.torrent = None
        self.MainWindow = MainWindow

        self.fileRadioButton.toggled.connect(self.inputTypeToggle)
        self.fileRadioButton.setChecked(True)
        self.directoryRadioButton.toggled.connect(self.inputTypeToggle)

        self.browseButton.clicked.connect(self.browseInput)
        self.batchModeCheckBox.stateChanged.connect(self.batchModeChanged)

        self.pieceCountLabel.hide()
        for x in PIECE_SIZES:
            self.pieceSizeComboBox.addItem(humanfriendly.format_size(x))

        self.pieceSizeComboBox.currentIndexChanged.connect(
            self.pieceSizeChanged)

        self.privateTorrentCheckBox.stateChanged.connect(
            self.privateTorrentChanged)

        self.createButton.setEnabled(False)
        self.resetButton.clicked.connect(lambda: self.setupUi(MainWindow))

    def inputTypeToggle(self):
        if self.fileRadioButton.isChecked():
            self.inputType = 'file'
            self.batchModeCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.batchModeCheckBox.setEnabled(False)
        else:
            self.inputType = 'directory'
            self.batchModeCheckBox.setEnabled(True)
        self.inputEdit.setText('')

    def browseInput(self):
        if self.inputType == 'file':
            fn = QtWidgets.QFileDialog.getOpenFileName(
                self.MainWindow, 'Select file')
            if fn[0]:
                self.inputEdit.setText(fn[0])
        else:
            dn = QtWidgets.QFileDialog.getExistingDirectory(
                self.MainWindow, 'Select directory')
            if dn:
                self.inputEdit.setText(dn)
        self.initializeTorrent()

    def batchModeChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.pieceSizeLabel.hide()
            self.pieceSizeComboBox.hide()
            self.pieceCountLabel.hide()
        else:
            self.pieceSizeLabel.show()
            self.pieceSizeComboBox.show()
            self.pieceCountLabel.show()

    def initializeTorrent(self):
        self.torrent = Torrent(
            self.inputEdit.text(),
            private=_isChecked(self.privateTorrentCheckBox))
        try:
            t_info = self.torrent.get_info()
        except Exception as e:
            errdlg = QtWidgets.QErrorMessage()
            errdlg.showMessage(str(e))
            errdlg.exec_()
            return
        ptail = os.path.split(self.torrent.path)[1]
        if self.inputType == 'file':
            self.MainWindow.statusBar().showMessage(
                "{}: {}".format(ptail, humanfriendly.format_size(t_info[0])))
        else:
            self.MainWindow.statusBar().showMessage(
                "{}: {} files, {}".format(
                    ptail, t_info[1], humanfriendly.format_size(t_info[0])))
        self.pieceSizeComboBox.setCurrentIndex(PIECE_SIZES.index(t_info[2]))
        self.updatePieceCountDisplay(t_info[3])
        self.createButton.setEnabled(True)

    def pieceSizeChanged(self, index):
        if getattr(self, 'torrent', None):
            self.torrent.piece_size = PIECE_SIZES[index]
            t_info = self.torrent.get_info()
            self.updatePieceCountDisplay(t_info[3])

    def updatePieceCountDisplay(self, pc):
        self.pieceCountLabel.setText("{} pieces".format(pc))
        self.pieceCountLabel.show()

    def privateTorrentChanged(self, state):
        if getattr(self, 'torrent', None):
            self.torrent.private = (state == QtCore.Qt.Checked)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DottorrentGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
