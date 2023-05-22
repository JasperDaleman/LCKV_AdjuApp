from PyQt5 import QtWidgets


class HomeScreen(QtWidgets.QWidget):
    def __init__(self, master):
        QtWidgets.QWidget.__init__(self)
        self.master = master

        self.layout = QtWidgets.QGridLayout()

        kamp = QtWidgets.QPushButton(self, text="Kamp omgeving")
        kamp.pressed.connect(self.kamp)
        kamp.setFocus()
        kamp.setAutoDefault(True)

        kantine = QtWidgets.QPushButton(self, text="Kantine omgeving")
        kantine.pressed.connect(self.kantine)
        kantine.setAutoDefault(True)

        self.layout.addWidget(kamp, 0, 0)
        self.layout.addWidget(kantine, 0, 1)

        afsl = QtWidgets.QPushButton(self, text="Afsluiten")
        afsl.pressed.connect(self.master.master.close)
        self.layout.addWidget(afsl, 1, 0, 1, 2)

        self.setLayout(self.layout)

    def kantine(self):
        self.master.change_screens("KantineHome")

    def kamp(self):
        self.master.change_screens("KampHome")
