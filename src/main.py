# coding=utf-8

import sys

from PyQt5.QtCore import pyqtSlot, Qt, QPointF
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence, QBrush, QColor, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem, QShortcut, QFileDialog, QGraphicsItem

APP_TITLE = '照片-桌面'
TABLE_SIZE = (650, 650)
PAPER_SIZE = (500, 350)
PHOTO_SIZE_MAX = (450, 315)


class WindowWidget(QWidget):
	def __init__(self):
		super(WindowWidget, self).__init__()
		self.main_layout = None
		self.table_view = None
		self.table_scene = None
		self.setAcceptDrops(True)
		self.init_layout()
		self.reg_hotkey()

	def init_layout(self):
		self.setWindowIcon(QIcon(res_path('res/ico.ico')))
		self.setWindowTitle(APP_TITLE)
		self.setStyleSheet('background-color: #303030')
		self.setMinimumSize(*TABLE_SIZE)

		self.table_scene = QGraphicsScene()
		self.table_scene.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
		self.table_view = QGraphicsView()
		self.table_view.setStyleSheet('border: 0px')
		self.table_view.setScene(self.table_scene)

		self.main_layout = QVBoxLayout()
		self.main_layout.addWidget(self.table_view)

		self.setLayout(self.main_layout)

	def reg_hotkey(self):
		hotkey_open = QShortcut(QKeySequence('Ctrl+O'), self)
		hotkey_open.activated.connect(self.on_hotkey_open)

	@pyqtSlot()
	def on_hotkey_open(self):
		file = QFileDialog.getOpenFileName(self, '打开照片', '', '*.jpg;*.png;*.jpeg;*.bmp')
		if file[0]:
			self.add_photo(file[0])

	def add_photo(self, path):
		paper = QPixmap(*PAPER_SIZE)
		paper.fill(QColor(255, 255, 255))
		photo = QPixmap(path).scaled(PHOTO_SIZE_MAX[0], PHOTO_SIZE_MAX[1], Qt.KeepAspectRatio)
		offset_x = (PAPER_SIZE[0] - photo.width()) / 2
		offset_y = (PAPER_SIZE[1] - photo.height()) / 2
		painter = QPainter(paper)
		painter.drawPixmap(QPointF(offset_x, offset_y), photo)
		painter.end()

		item = QGraphicsPixmapItem()
		item.setPixmap(paper)
		item.setFlag(QGraphicsItem.ItemIsMovable, True)

		self.table_scene.addItem(item)


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
