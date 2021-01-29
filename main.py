# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QDesktopWidget


class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.edit_src = QLineEdit()

		grid = QGridLayout()
		self.setLayout(grid)

		grid.addWidget(QLabel('Source'), 0, 0)
		grid.addWidget(QLabel('For Raw'), 1, 0)
		grid.addWidget(QLabel('For Etc'), 2, 0)
		grid.addWidget(QLabel('message'), 4, 0)

		self.edit_src = QLineEdit()
		self.edit_raw = QLineEdit()
		self.edit_etc = QLineEdit()
		grid.addWidget(self.edit_src, 0, 1)
		grid.addWidget(self.edit_raw, 1, 1)
		grid.addWidget(self.edit_etc, 2, 1)

		self.btn_start = QPushButton('Start')
		self.btn_stop = QPushButton('Stop')
		grid_inner = QGridLayout()
		grid_inner.addWidget(self.btn_start, 0, 0)
		grid_inner.addWidget(self.btn_stop, 0, 1)
		grid.addLayout(grid_inner, 3, 1)

		self.lbl_message = QLabel()
		grid.addWidget(self.lbl_message, 4, 1)

		self.btn_src = QPushButton('...')
		self.btn_src.clicked.connect(self.btn_src_clicked)
		self.btn_raw = QPushButton('...')
		self.btn_raw.clicked.connect(self.btn_raw_clicked)
		self.btn_etc = QPushButton('...')
		self.btn_etc.clicked.connect(self.btn_etc_clicked)
		grid.addWidget(self.btn_src, 0, 2)
		grid.addWidget(self.btn_raw, 1, 2)
		grid.addWidget(self.btn_etc, 2, 2)

		self.setWindowTitle('Vrism Content Backup')
		# self.move(300, 300)
		self.center()
		self.resize(800, 400)
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def btn_src_clicked(self):
		self.edit_src.setText(self.show_file_dialog())

	def btn_raw_clicked(self):
		self.edit_raw.setText(self.show_file_dialog())

	def btn_etc_clicked(self):
		self.edit_etc.setText(self.show_file_dialog())

	def show_file_dialog(self):
		return QFileDialog.getExistingDirectory(self, 'Select a folder', '.')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())
