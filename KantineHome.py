import PyQt5
from PyQt5 import QtWidgets


class KantineHome(QtWidgets.QWidget):
    def __init__(self, master):
        QtWidgets.QWidget.__init__(self)
        self.master = master

        self.layout = QtWidgets.QGridLayout()

        kt = QtWidgets.QPushButton(self, text='Keer terug')
        kt.pressed.connect(self.ret)
        kt.setAutoDefault(True)

        bi = QtWidgets.QPushButton(self, text='Order ingeven')
        bi.pressed.connect(self.bon_ingeven)
        bi.setAutoDefault(True)

        ab = QtWidgets.QPushButton(self, text='Artikelbeheer')
        ab.pressed.connect(self.artikel_beheer)
        ab.setAutoDefault(True)

        self.layout.addWidget(kt, 2, 0)
        self.layout.addWidget(bi, 1, 0)
        self.layout.addWidget(ab, 0, 0)

        self.setLayout(self.layout)


    def ret(self):
        self.master.change_screens('HomeScreen')

    def bon_ingeven(self):
        self.master.change_screens('OrderIngeven')

    def artikel_beheer(self):
        self.master.change_screens('ArtikelBeheer')