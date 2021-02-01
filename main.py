# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import os
import shbackup
import json
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, \
	QDesktopWidget, QMessageBox


RECENT_DIR_JSON = 'recent_dir.json'


class RecentDirJson:
	SRC = "src"
	RAW = "raw"
	ETC = "etc"


class MyApp(QWidget):

	is_job_running = False
	t = None

	def __init__(self):
		super().__init__()

		grid = QGridLayout()
		self.setLayout(grid)

		grid.addWidget(QLabel('Source'), 0, 0)
		grid.addWidget(QLabel('For Raw'), 1, 0)
		grid.addWidget(QLabel('For Etc'), 2, 0)
		grid.addWidget(QLabel(), 4, 0)

		# get/set recent used directory
		with open(RECENT_DIR_JSON, 'r') as cf:
			self.recent = json.load(cf)
			self.recent_src = self.recent[RecentDirJson.SRC]
			self.recent_raw = self.recent[RecentDirJson.RAW]
			self.recent_etc = self.recent[RecentDirJson.ETC]

		if self.recent_src:
			self.edit_src = QLineEdit(self.recent_src)
		else:
			self.edit_src = QLineEdit(os.getcwd())

		if self.recent_raw:
			self.edit_raw = QLineEdit(self.recent_raw)
		else:
			self.edit_raw = QLineEdit(os.getcwd())

		if self.recent_etc:
			self.edit_etc = QLineEdit(self.recent_etc)
		else:
			self.edit_etc = QLineEdit(os.getcwd())

		grid.addWidget(self.edit_src, 0, 1)
		grid.addWidget(self.edit_raw, 1, 1)
		grid.addWidget(self.edit_etc, 2, 1)

		self.btn_start = QPushButton('Start')
		self.btn_start.clicked.connect(self.btn_start_clicked)
		self.btn_stop = QPushButton('Stop')
		self.btn_stop.clicked.connect(self.btn_stop_clicked)
		grid_inner = QGridLayout()
		grid_inner.addWidget(self.btn_start, 0, 0)
		grid_inner.addWidget(self.btn_stop, 0, 1)
		grid.addLayout(grid_inner, 3, 1)
		self.btn_start.setEnabled(True)
		self.btn_stop.setEnabled(False)

		self.lbl_message = QLabel('')
		grid.addWidget(self.lbl_message, 4, 1)

		self.btn_src = QPushButton('...')
		self.btn_raw = QPushButton('...')
		self.btn_etc = QPushButton('...')
		self.btn_src.clicked.connect(self.btn_src_clicked)
		self.btn_raw.clicked.connect(self.btn_raw_clicked)
		self.btn_etc.clicked.connect(self.btn_etc_clicked)
		grid.addWidget(self.btn_src, 0, 2)
		grid.addWidget(self.btn_raw, 1, 2)
		grid.addWidget(self.btn_etc, 2, 2)

		self.setWindowTitle('Vrism Content Backup Tool')
		# self.move(300, 300)
		self.center()
		self.resize(600, 200)
		self.show()

	def closeEvent(self, event) -> None:
		if self.is_job_running:
			reply = QMessageBox.question(self,
										 'Message',
					    			     'now on you task, Are sure to Quit?',
										 QMessageBox.Yes | QMessageBox.No,
										 QMessageBox.No)
			if reply == QMessageBox.Yes:
				event.accept()
				shbackup.stop = True
				self.t.join()
			else:
				event.ignore()
		else:
			event.accept()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def set_status(self, msg, running = True):
		self.lbl_message.setText(msg)
		self.is_job_running = running
		if running:
			self.btn_start.setEnabled(False)
			self.btn_stop.setEnabled(True)
		else:
			self.btn_start.setEnabled(True)
			self.btn_stop.setEnabled(False)

	def btn_start_clicked(self):
		if self.is_job_running:
			return
		self.t = threading.Thread(target = shbackup.run,
							 args = (self.edit_src.text(),
									 self.edit_raw.text(),
									 self.edit_etc.text(),
									 self.set_status))
		self.t.start()
		with open(RECENT_DIR_JSON, 'w') as cf:
			self.recent[RecentDirJson.SRC] = self.edit_src.text()
			self.recent[RecentDirJson.RAW] = self.edit_raw.text()
			self.recent[RecentDirJson.ETC] = self.edit_etc.text()
			json.dump(self.recent, cf, indent = 4)

	def btn_stop_clicked(self):
		if not self.is_job_running:
			return
		shbackup.stop = True
		self.t.join()
		self.t = None

	def btn_src_clicked(self):
		sel = self.show_file_dialog()
		if sel:
			self.edit_src.setText(sel)

	def btn_raw_clicked(self):
		sel = self.show_file_dialog()
		if sel:
			self.edit_raw.setText(sel)

	def btn_etc_clicked(self):
		sel = self.show_file_dialog()
		if sel:
			self.edit_etc.setText(sel)

	def show_file_dialog(self):
		return QFileDialog.getExistingDirectory(self, 'Select a folder', '.')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())
