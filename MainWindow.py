from PyQt5 import QtWidgets

from HomeScreen import HomeScreen
from KampHome import KampHome
from KantineHome import KantineHome
from BonInvoeren import BonInvoeren
from BonWijzigen import BonWijzigen
from OrderIngeven import OrderIngeven
from InlegEnTentindeling import InlegEnTentindeling
from InvoerenPersonen import InvoerenPersonen
from ArtikelBeheer import ArtikelBeheer
from ArtikelAanmaken import ArtikelAanmaken
from TentWijzigen import TentWijzigen
from PersonenWijzigen import PersonenWijzigen
from PersoonToevoegen import PersoonToevoegen
from StafhapEnPB import StafhapEnPB
from InvullenBegroting import InvullenBegroting


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, master):
        QtWidgets.QMainWindow.__init__(self)
        self.master = master
        self.geo = (0, 0, 640, 480)  # self.master.geo

        self.setGeometry(self.geo[0], self.geo[1], self.geo[2], self.geo[3])

        self.setWindowTitle("LCKV ADJU App")

        self.screens = {
            "HomeScreen": HomeScreen,
            "KampHome": KampHome,
            "KantineHome": KantineHome,
            "BonInvoeren": BonInvoeren,
            "BonWijzigen": BonWijzigen,
            "OrderIngeven": OrderIngeven,
            "ArtikelBeheer": ArtikelBeheer,
            "ArtikelAanmaken": ArtikelAanmaken,
            "TentWijzigen": TentWijzigen,
            "PersonenWijzigen": PersonenWijzigen,
            "PersoonToevoegen": PersoonToevoegen,
            "StafhapEnPB": StafhapEnPB,
            "InvullenBegroting": InvullenBegroting,
        }

        self.setup_menus()
        self.change_screens("HomeScreen")
        self.show()

    def change_screens(self, screen):
        self.setCentralWidget(self.screens[screen](self))

    def setup_menus(self):
        self.mb = self.menuBar()
        self.fm = self.mb.addMenu("&File")

        self.c = QtWidgets.QAction("&Close", self)
        self.c.triggered.connect(self.master.close)

        self.adn = QtWidgets.QAction("&Invoeren Deelnemers...", self)
        self.adn.triggered.connect(self.enter_dn)

        self.ti = QtWidgets.QAction("&Tentenindeling...", self)
        self.ti.triggered.connect(self.enter_tents)

        self.tw = QtWidgets.QAction("&Tentindeling Wijzigen", self)
        self.tw.triggered.connect(self.change_tents)

        self.begr = QtWidgets.QAction("&Begroting Invoeren", self)
        self.begr.triggered.connect(self.begrotingInvoeren)

        self.fm.addAction(self.begr)
        self.fm.addAction(self.adn)
        self.fm.addAction(self.ti)
        self.fm.addAction(self.tw)
        self.fm.addAction(self.c)

    def begrotingInvoeren(self):
        self.change_screens("InvullenBegroting")

    def enter_dn(self):
        self.wdg = InvoerenPersonen(self.master)
        self.wdg.show()

    def enter_tents(self):
        self.indeling = InlegEnTentindeling(self.master)
        self.indeling.show()

    def change_tents(self):
        self.wijzig_tent = TentWijzigen(self.master)
        self.wijzig_tent.show()
        # self.change_screens('TentWijzigen')

    def inleggen_geld(self):
        self.inlg = Inleggen(self.master)
        self.inlg.show()
