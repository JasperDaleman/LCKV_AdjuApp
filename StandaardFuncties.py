from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QWidget, QComboBox, QGridLayout, QPushButton, QLabel, QMessageBox

def warning(cur_class, text, window_title):
    cur_class.msgBox = QMessageBox()
    cur_class.msgBox.setIcon(QMessageBox.Warning)
    cur_class.msgBox.setStandardButtons(QMessageBox.Ok)
    cur_class.msgBox.setText(text)
    cur_class.msgBox.setWindowTitle(window_title)
    cur_class.msgBox.show()
    cur_class.msgBox.exec_()