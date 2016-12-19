#!/usr/bin/env python3

from datetime import datetime
import json
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import dottorrent
import humanfriendly

from dottorrentGUI import Ui_MainWindow
from dottorrentGUI import Ui_AboutDialog
from dottorrentGUI import __version__


PROGRAM_NAME = "dottorrent-gui"
PROGRAM_NAME_VERSION = "{} {}".format(PROGRAM_NAME, __version__)
CREATOR = "dottorrent-gui/{} dottorrent/{}".format(
    __version__, dottorrent.__version__)

PIECE_SIZES = [None] + [2 ** i for i in range(14, 23)]


class CreateTorrentQThread(QtCore.QThread):

    progress_update = QtCore.pyqtSignal(str, int, int)
    onError = QtCore.pyqtSignal(str)

    def __init__(self, torrent, save_path):
        super().__init__()
        self.torrent = torrent
        self.save_path = save_path

    def run(self):
        def progress_callback(*args):
            self.progress_update.emit(*args)
            return self.isInterruptionRequested()

        self.torrent.creation_date = datetime.now()
        self.torrent.created_by = CREATOR
        try:
            self.success = self.torrent.generate(callback=progress_callback)
        except Exception as exc:
            self.onError.emit(str(exc))
            return
        if self.success:
            with open(self.save_path, 'wb') as f:
                self.torrent.save(f)


class CreateTorrentBatchQThread(QtCore.QThread):

    progress_update = QtCore.pyqtSignal(str, int, int)
    onError = QtCore.pyqtSignal(str)

    def __init__(self, path, save_dir, trackers, web_seeds,
                 private, source, comment, include_md5):
        super().__init__()
        self.path = path
        self.save_dir = save_dir
        self.trackers = trackers
        self.web_seeds = web_seeds
        self.private = private
        self.source = source
        self.comment = comment
        self.include_md5 = include_md5

    def run(self):
        def callback(*args):
            return self.isInterruptionRequested()

        entries = os.listdir(self.path)
        for i, p in enumerate(entries):
            p = os.path.join(self.path, p)
            if not dottorrent.is_hidden_file(p):
                sfn = os.path.split(p)[1] + '.torrent'
                self.progress_update.emit(sfn, i, len(entries))
                t = dottorrent.Torrent(
                    p,
                    trackers=self.trackers,
                    web_seeds=self.web_seeds,
                    private=self.private,
                    source=self.source,
                    comment=self.comment,
                    include_md5=self.include_md5,
                    creation_date=datetime.now(),
                    created_by=CREATOR
                )
                try:
                    self.success = t.generate(callback=callback)
                # ignore empty inputs
                except dottorrent.exceptions.EmptyInputException:
                    continue
                except Exception as exc:
                    self.onError.emit(str(exc))
                    return
                if self.isInterruptionRequested():
                    return
                if self.success:
                    with open(os.path.join(self.save_dir, sfn), 'wb') as f:
                        t.save(f)


class DottorrentGUI(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle(PROGRAM_NAME_VERSION)

        self.torrent = None
        self.MainWindow = MainWindow

        self.actionImportTrackers.triggered.connect(self.import_trackers)
        self.actionExportTrackers.triggered.connect(self.export_trackers)
        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.actionQuit.triggered.connect(self.MainWindow.close)

        self.fileRadioButton.toggled.connect(self.inputTypeToggle)
        self.fileRadioButton.setChecked(True)
        self.directoryRadioButton.toggled.connect(self.inputTypeToggle)

        self.browseButton.clicked.connect(self.browseInput)
        self.batchModeCheckBox.stateChanged.connect(self.batchModeChanged)

        self.pieceCountLabel.hide()
        self.pieceSizeComboBox.addItem('Auto')
        for x in PIECE_SIZES[1:]:
            self.pieceSizeComboBox.addItem(
                humanfriendly.format_size(x, binary=True))

        self.pieceSizeComboBox.currentIndexChanged.connect(
            self.pieceSizeChanged)

        self.privateTorrentCheckBox.stateChanged.connect(
            self.privateTorrentChanged)

        self.commentEdit.textEdited.connect(
            self.commentEdited)

        self.sourceEdit.textEdited.connect(
            self.sourceEdited)

        self.md5CheckBox.stateChanged.connect(
            self.md5Changed)

        self.progressBar.hide()
        self.createButton.setEnabled(False)
        self.createButton.clicked.connect(self.createButtonClicked)
        self.cancelButton.hide()
        self.cancelButton.clicked.connect(self.cancel_creation)
        self.resetButton.clicked.connect(lambda: self.setupUi(MainWindow))

    def getSettings(self):
        return QtCore.QSettings(
            QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            PROGRAM_NAME,
            PROGRAM_NAME
        )

    def loadSettings(self):
        settings = self.getSettings()
        trackers = settings.value('seeding/trackers')
        if trackers:
            self.trackerEdit.setPlainText(trackers)
        web_seeds = settings.value('seeding/web_seeds')
        if web_seeds:
            self.webSeedEdit.setPlainText(web_seeds)
        private = bool(int(settings.value('options/private') or 0))
        self.privateTorrentCheckBox.setChecked(private)
        source = settings.value('options/source')
        if source:
            self.sourceEdit.setText(source)
        self.last_input_dir = settings.value('history/last_input_dir') or None
        self.last_output_dir = settings.value(
            'history/last_output_dir') or None

    def saveSettings(self):
        settings = self.getSettings()
        settings.setValue('seeding/trackers', self.trackerEdit.toPlainText())
        settings.setValue('seeding/web_seeds', self.webSeedEdit.toPlainText())
        settings.setValue('options/private',
                          int(self.privateTorrentCheckBox.isChecked()))
        settings.setValue('options/source', self.sourceEdit.text())
        if self.last_input_dir:
            settings.setValue('history/last_input_dir', self.last_input_dir)
        if self.last_output_dir:
            settings.setValue('history/last_output_dir', self.last_output_dir)

    def _statusBarMsg(self, msg):
        self.MainWindow.statusBar().showMessage(msg)

    def _showError(self, msg):
        errdlg = QtWidgets.QErrorMessage()
        errdlg.setWindowTitle('Error')
        errdlg.showMessage(msg)
        errdlg.exec_()

    def showAboutDialog(self):
        qdlg = QtWidgets.QDialog()
        ad = Ui_AboutDialog()
        ad.setupUi(qdlg)
        ad.programVersionLabel.setText("version {}".format(__version__))
        ad.dtVersionLabel.setText("(dottorrent {})".format(
            dottorrent.__version__))
        qdlg.exec_()

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
        qfd = QtWidgets.QFileDialog(self.MainWindow)
        if self.last_input_dir:
            qfd.setDirectory(self.last_input_dir)
        if self.inputType == 'file':
            qfd.setWindowTitle('Select file')
            qfd.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        else:
            qfd.setWindowTitle('Select directory')
            qfd.setFileMode(QtWidgets.QFileDialog.Directory)
        if qfd.exec_():
            fn = qfd.selectedFiles()[0]
            self.inputEdit.setText(fn)
            self.last_input_dir = os.path.split(fn)[0]
            self.initializeTorrent()

    def batchModeChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.pieceSizeComboBox.setCurrentIndex(0)
            self.pieceSizeComboBox.setEnabled(False)
            self.pieceCountLabel.hide()
        else:
            self.pieceSizeComboBox.setEnabled(True)
            self.pieceCountLabel.show()

    def initializeTorrent(self):
        self.torrent = dottorrent.Torrent(self.inputEdit.text())
        try:
            t_info = self.torrent.get_info()
        except Exception as e:
            self.torrent = None
            self._showError(str(e))
            return
        ptail = os.path.split(self.torrent.path)[1]
        if self.inputType == 'file':
            self._statusBarMsg(
                "{}: {}".format(ptail, humanfriendly.format_size(
                    t_info[0], binary=True)))
        else:
            self._statusBarMsg(
                "{}: {} files, {}".format(
                    ptail, t_info[1], humanfriendly.format_size(
                        t_info[0], binary=True)))
        self.pieceSizeComboBox.setCurrentIndex(0)
        self.updatePieceCountLabel(t_info[2], t_info[3])
        self.pieceCountLabel.show()
        self.createButton.setEnabled(True)

    def commentEdited(self, comment):
        if getattr(self, 'torrent', None):
            self.torrent.comment = comment

    def sourceEdited(self, source):
        if getattr(self, 'torrent', None):
            self.torrent.source = source

    def pieceSizeChanged(self, index):
        if getattr(self, 'torrent', None):
            self.torrent.piece_size = PIECE_SIZES[index]
            t_info = self.torrent.get_info()
            self.updatePieceCountLabel(t_info[2], t_info[3])

    def updatePieceCountLabel(self, ps, pc):
        ps = humanfriendly.format_size(ps, binary=True)
        self.pieceCountLabel.setText("{} pieces @ {} each".format(pc, ps))

    def privateTorrentChanged(self, state):
        if getattr(self, 'torrent', None):
            self.torrent.private = (state == QtCore.Qt.Checked)

    def md5Changed(self, state):
        if getattr(self, 'torrent', None):
            self.torrent.include_md5 = (state == QtCore.Qt.Checked)

    def createButtonClicked(self):
        # Validate trackers and web seed URLs
        trackers = self.trackerEdit.toPlainText().strip().split()
        web_seeds = self.webSeedEdit.toPlainText().strip().split()
        try:
            self.torrent.trackers = trackers
            self.torrent.web_seeds = web_seeds
        except Exception as e:
            self._showError(str(e))
            return
        self.torrent.private = self.privateTorrentCheckBox.isChecked()
        self.torrent.comment = self.commentEdit.text() or None
        self.torrent.source = self.sourceEdit.text() or None
        self.torrent.include_md5 = self.md5CheckBox.isChecked()
        if self.batchModeCheckBox.isChecked():
            self.createTorrentBatch()
        else:
            self.createTorrent()

    def createTorrent(self):
        if os.path.isfile(self.inputEdit.text()):
            save_fn = os.path.splitext(
                os.path.split(self.inputEdit.text())[1])[0] + '.torrent'
        else:
            save_fn = self.inputEdit.text().split(os.sep)[-1] + '.torrent'
        if self.last_output_dir:
            save_fn = os.path.join(self.last_output_dir, save_fn)
        fn = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, 'Save torrent', save_fn,
            filter=('Torrent file (*.torrent)'))[0]
        if fn:
            self.last_output_dir = os.path.split(fn)[0]
            self.creation_thread = CreateTorrentQThread(
                self.torrent,
                fn)
            self.creation_thread.started.connect(
                self.creation_started)
            self.creation_thread.progress_update.connect(
                self._progress_update)
            self.creation_thread.finished.connect(
                self.creation_finished)
            self.creation_thread.onError.connect(
                self._showError)
            self.creation_thread.start()

    def createTorrentBatch(self):
        save_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.MainWindow, 'Select output directory', self.last_output_dir)
        if save_dir:
            self.last_output_dir = save_dir
            trackers = self.trackerEdit.toPlainText().strip().split()
            web_seeds = self.webSeedEdit.toPlainText().strip().split()
            self.creation_thread = CreateTorrentBatchQThread(
                path=self.inputEdit.text(),
                save_dir=save_dir,
                trackers=trackers,
                web_seeds=web_seeds,
                private=self.privateTorrentCheckBox.isChecked(),
                source=self.sourceEdit.text(),
                comment=self.commentEdit.text(),
                include_md5=self.md5CheckBox.isChecked(),
            )
            self.creation_thread.started.connect(
                self.creation_started)
            self.creation_thread.progress_update.connect(
                self._progress_update_batch)
            self.creation_thread.finished.connect(
                self.creation_finished)
            self.creation_thread.onError.connect(
                self._showError)
            self.creation_thread.start()

    def cancel_creation(self):
        self.creation_thread.requestInterruption()

    def _progress_update(self, fn, pc, pt):
        fn = os.path.split(fn)[1]
        msg = "{} ({}/{})".format(fn, pc, pt)
        self.updateProgress(msg, int(round(100 * pc / pt)))

    def _progress_update_batch(self, fn, tc, tt):
        msg = "({}/{}) {}".format(tc, tt, fn)
        self.updateProgress(msg, int(round(100 * tc / tt)))

    def updateProgress(self, statusMsg, pv):
        self._statusBarMsg(statusMsg)
        self.progressBar.setValue(pv)

    def creation_started(self):
        self.inputGroupBox.setEnabled(False)
        self.seedingGroupBox.setEnabled(False)
        self.optionGroupBox.setEnabled(False)
        self.progressBar.show()
        self.createButton.hide()
        self.cancelButton.show()
        self.resetButton.setEnabled(False)

    def creation_finished(self):
        self.inputGroupBox.setEnabled(True)
        self.seedingGroupBox.setEnabled(True)
        self.optionGroupBox.setEnabled(True)
        self.progressBar.hide()
        self.createButton.show()
        self.cancelButton.hide()
        self.resetButton.setEnabled(True)
        if self.creation_thread.success:
            self._statusBarMsg('Finished')
        else:
            self._statusBarMsg('Canceled')
        self.creation_thread = None

    def export_trackers(self):

        fn = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, 'Save tracker profile', self.last_output_dir,
            filter=('JSON configuration file (*.json)'))[0]
        if fn:
            trackers = self.trackerEdit.toPlainText().strip().split()
            web_seeds = self.webSeedEdit.toPlainText().strip().split()
            private = self.privateTorrentCheckBox.isChecked()
            source = self.sourceEdit.text()
            data = {
                'trackers': trackers,
                'web_seeds': web_seeds,
                'private': private,
                'source': source
            }
            with open(fn, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)
            self._statusBarMsg("Tracker profile saved to " + fn)

    def import_trackers(self):
        fn = QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow, 'Open tracker profile', self.last_input_dir,
            filter=('JSON configuration file (*.json)'))[0]
        if fn:
            with open(fn) as f:
                data = json.load(f)
            trackers = data.get('trackers', [])
            web_seeds = data.get('web_seeds', [])
            private = data.get('private', False)
            source = data.get('source', '')
            try:
                ts = os.linesep.join(trackers)
                self.trackerEdit.setPlainText(ts)
                ws = os.linesep.join(web_seeds)
                self.webSeedEdit.setPlainText(ws)
                self.privateTorrentCheckBox.setChecked(private)
                self.sourceEdit.setText(source)
            except Exception as e:
                self._showError(str(e))
                return
            self._statusBarMsg("Tracker profile {} loaded".format(
                os.path.split(fn)[1]))


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DottorrentGUI()
    ui.setupUi(MainWindow)
    ui.loadSettings()
    app.aboutToQuit.connect(lambda: ui.saveSettings())
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
