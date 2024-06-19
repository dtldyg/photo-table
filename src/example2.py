# coding=utf-8

import sys
import time

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QKeySequence, QTransform
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QShortcut, QFileDialog, QApplication

WINDOW_TITLE = '照片-桌面'
WINDOW_SIZE = (650, 650)
PHOTO_SIZE = (500, 350)
PRINT_SIZE = (450, 315)


class WindowWidget(QWidget):
	def __init__(self):
		super(WindowWidget, self).__init__()
		self.layout_table = None
		self.label_photo = None
		self.pixmap = None
		self.photo_rotate = 0
		self.setAcceptDrops(True)
		self.init_table()
		self.reg_hotkey()

	def init_table(self):
		self.label_photo = QLabel(self)
		self.label_photo.setFixedSize(*PHOTO_SIZE)
		self.label_photo.setAlignment(Qt.AlignCenter)
		self.label_photo.setStyleSheet('background-color: #ffffff')

		# layout
		self.layout_table = QVBoxLayout()
		self.layout_table.addWidget(self.label_photo)
		self.layout_table.setAlignment(Qt.AlignCenter)

		self.setLayout(self.layout_table)
		self.setFixedSize(*WINDOW_SIZE)
		self.setWindowTitle(WINDOW_TITLE)
		self.setStyleSheet('background-color: #303030')
		self.setWindowIcon(QIcon(res_path('res/ico.ico')))

	def reg_hotkey(self):
		hotkey_open = QShortcut(QKeySequence('Ctrl+O'), self)
		hotkey_open.activated.connect(self.on_open)

	# ↓↓ event: drop
	def dragEnterEvent(self, event):
		text = event.mimeData().text()
		if text.endswith('.jpg') or text.endswith('.png') or text.endswith('.jpeg') or text.endswith('.bmp'):
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		path = event.mimeData().text().replace('file:///', '')
		self.load_image(path)

	# ↓↓ event: mouse
	def mousePressEvent(self, event):
		pass

	def mouseReleaseEvent(self, event):
		pass

	def wheelEvent(self, event):
		transform = QTransform().rotate(10)
		self.pixmap = self.pixmap.transformed(transform)
		self.label_photo.setPixmap(self.pixmap)

	# ↓↓ event: open
	@pyqtSlot()
	def on_open(self):
		file = QFileDialog.getOpenFileName(self, '打开照片', '', '*.jpg;*.png;*.jpeg;*.bmp')
		if file[0]:
			self.load_image(file[0])

	# ↓↓ new image
	def load_image(self, path):
		photo = QImage(path)
		self.pixmap = QPixmap(photo).scaled(PRINT_SIZE[0], PRINT_SIZE[1], Qt.KeepAspectRatio)
		self.label_photo.setPixmap(self.pixmap)


def res_path(path):
	if hasattr(sys, '_MEIPASS'):
		return getattr(sys, '_MEIPASS') + '/' + path
	else:
		return path


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = WindowWidget()
	window.show()
	sys.exit(app.exec_())
