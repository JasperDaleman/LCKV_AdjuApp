import PyQt5
from PyQt5 import QtWidgets


class KampHome(QtWidgets.QWidget):
    def __init__(self, master):
        QtWidgets.QWidget.__init__(self)
        self.master = master

        self.layout = QtWidgets.QGridLayout()

        kt = QtWidgets.QPushButton(self, text='Keer terug')
        kt.setAutoDefault(True)
        kt.clicked.connect(self.ret)

        bi = QtWidgets.QPushButton(self, text='Bon Ingeven')
        bi.setAutoDefault(True)
        bi.clicked.connect(self.bon_invoeren)

        bw = QtWidgets.QPushButton(self, text='Bon Wijzigen')
        bw.setAutoDefault(True)
        bw.clicked.connect(self.bon_wijzigen)

        sp = QtWidgets.QPushButton(self, text='Stafhap && PB\'s')
        sp.setAutoDefault(True)
        sp.clicked.connect(self.stafhap_pb)

        inzienPersonen = QtWidgets.QPushButton(self, text='Inzien/Wijzigen Personen')
        inzienPersonen.clicked.connect(self.pers)

        self.layout.addWidget(bi, 2, 0)
        self.layout.addWidget(bw, 2, 1)
        self.layout.addWidget(kt, 3, 0, 1, 2)
        self.layout.addWidget(inzienPersonen, 0, 0, 1, 2)
        self.layout.addWidget(sp, 1, 0)

        self.setLayout(self.layout)

    def ret(self):
        self.master.change_screens('HomeScreen')

    def bon_invoeren(self):
        self.master.change_screens('BonInvoeren')

    def bon_wijzigen(self):
        self.master.change_screens('BonWijzigen')

    def pers(self):
        self.master.change_screens('PersonenWijzigen')

    def stafhap_pb(self):
        self.master.change_screens('StafhapEnPB')
