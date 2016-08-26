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


class CreateTorrentQThread(QtCore.QThread):

    progress_update = QtCore.pyqtSignal(str, int, int)

    def __init__(self, torrent, save_path, include_md5=False):
        super().__init__()
        self.torrent = torrent
        self.save_path = save_path
        self.include_md5 = include_md5

    def run(self):
        def progress_callback(*args):
            self.progress_update.emit(*args)

        self.torrent.generate(include_md5=self.include_md5,
                              callback=progress_callback)
        with open(self.save_path, 'wb') as f:
            self.torrent.save(f)


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

        self.progressBar.hide()
        self.createButton.setEnabled(False)
        self.createButton.clicked.connect(self.createButtonClicked)
        self.cancelButton.hide()
        self.cancelButton.clicked.connect(self.cancel_creation)
        self.resetButton.clicked.connect(lambda: self.setupUi(MainWindow))

    def _statusBarMsg(self, msg):
        self.MainWindow.statusBar().showMessage(msg)

    def inputTypeToggle(self):
        if self.fileRadioButton.isChecked():
            self.inputType = 'file'
            self.batchModeCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.batchModeCheckBox.setEnabled(False)
            self.batchModeCheckBox.hide()
        else:
            self.inputType = 'directory'
            self.batchModeCheckBox.setEnabled(True)
            self.batchModeCheckBox.show()
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
            self._statusBarMsg(
                "{}: {}".format(ptail, humanfriendly.format_size(t_info[0])))
        else:
            self._statusBarMsg(
                "{}: {} files, {}".format(
                    ptail, t_info[1], humanfriendly.format_size(t_info[0])))
        self.pieceSizeComboBox.setCurrentIndex(PIECE_SIZES.index(t_info[2]))
        self.updatePieceCountLabel(t_info[3])
        self.pieceCountLabel.show()
        self.createButton.setEnabled(True)

    def pieceSizeChanged(self, index):
        if getattr(self, 'torrent', None):
            self.torrent.piece_size = PIECE_SIZES[index]
            t_info = self.torrent.get_info()
            self.updatePieceCountLabel(t_info[3])

    def updatePieceCountLabel(self, pc):
        self.pieceCountLabel.setText("{} pieces".format(pc))

    def privateTorrentChanged(self, state):
        if getattr(self, 'torrent', None):
            self.torrent.private = (state == QtCore.Qt.Checked)

    def createButtonClicked(self):
        if _isChecked(self.batchModeCheckBox):
            pass
        else:
            self.createTorrent()

    def createTorrent(self):
        fn = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, 'Save torrent', None,
            filter=('Torrent (*.torrent)'))
        if fn[0]:
            self.creation_thread = CreateTorrentQThread(
                self.torrent,
                fn[0],
                _isChecked(self.md5CheckBox))
            self.creation_thread.started.connect(
                self.creation_started)
            self.creation_thread.progress_update.connect(
                self._progress_update)
            self.creation_thread.finished.connect(
                self.creation_finished)
            self.creation_thread.start()

    def cancel_creation(self):
        thread = getattr(self, 'creation_thread', None)

    def _progress_update(self, fn, pc, pt):
        fn = os.path.split(fn)[1]
        msg = "{} ({}/{})".format(fn, pc, pt)
        self.updateProgress(msg, int(round(100 * pc / pt)))

    def _progress_update_batch(self, fn, tc, tt):
        pass

    def updateProgress(self, statusMsg, pv):
        self._statusBarMsg(statusMsg)
        self.progressBar.setValue(pv)

    def creation_started(self):
        self.progressBar.show()
        self.createButton.hide()
        self.cancelButton.show()
        self.resetButton.setEnabled(False)

    def creation_finished(self):
        self.progressBar.hide()
        self.createButton.show()
        self.cancelButton.hide()
        self.resetButton.setEnabled(True)
        self._statusBarMsg('Finished')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DottorrentGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
