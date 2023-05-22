from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QLineEdit,
    QWidget,
    QComboBox,
    QGridLayout,
    QPushButton,
    QLabel,
    QMessageBox,
)

import sys
import pandas as pd


class ArtikelAanmaken(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        # Product barcode
        self.prodcode = QLineEdit(self)
        self.prodcode.returnPressed.connect(self.nxt)
        self.product_label = QLabel(self, text="Barcode: ")
        self.layout.addWidget(self.product_label, 0, 0)
        self.layout.addWidget(self.prodcode, 0, 1)

        # Product omschrijving
        self.prodomsc = QLineEdit(self)
        self.prodomsc.returnPressed.connect(self.nxt)
        self.prodomsc_label = QLabel(self, text="Omschrijving: ")
        self.layout.addWidget(self.prodomsc_label, 1, 0)
        self.layout.addWidget(self.prodomsc, 1, 1)

        # Productgroep selectie
        self.pgcombo = QComboBox(self)
        self.prodgr = ["Dranken", "Chips", "Snoep"]
        for pg in self.prodgr:
            self.pgcombo.addItem(pg)

        self.prodomsc_label = QLabel(self, text="Groep: ")
        self.layout.addWidget(self.prodomsc_label, 2, 0)
        self.layout.addWidget(self.pgcombo, 2, 1)

        # Prijs
        self.prijs = QLineEdit(self)
        self.prijs.returnPressed.connect(self.nxt)
        self.prijs_label = QLabel(self, text="Prijs: ")
        self.layout.addWidget(self.prijs_label, 3, 0)
        self.layout.addWidget(self.prijs, 3, 1)

        # Inhoud
        self.inhoud = QLineEdit(self)
        self.inhoud.returnPressed.connect(self.nxt)
        self.inhoud_label = QLabel(self, text="Inhoud: ")
        self.layout.addWidget(self.inhoud_label, 4, 0)
        self.layout.addWidget(self.inhoud, 4, 1)

        # Suiker
        self.suiker = QLineEdit(self)
        self.suiker.returnPressed.connect(self.nxt)
        self.suiker_label = QLabel(self, text="Suiker: ")
        self.layout.addWidget(self.suiker_label, 5, 0)
        self.layout.addWidget(self.suiker, 5, 1)

        # Calorieen
        self.calorieen = QLineEdit(self)
        self.calorieen.returnPressed.connect(self.confirm_artikel)
        self.calorieen_label = QLabel(self, text="Calorieën: ")
        self.layout.addWidget(self.calorieen_label, 6, 0)
        self.layout.addWidget(self.calorieen, 6, 1)

        # Bevestigen Buttons en terug
        self.conf_artk = QPushButton(self, text="Maak artikel")
        self.keer_terug = QPushButton(self, text="Keer terug")

        self.conf_artk.clicked.connect(self.confirm_artikel)
        self.keer_terug.clicked.connect(self.kt)

        self.layout.addWidget(self.conf_artk, 8, 1)
        self.layout.addWidget(self.keer_terug, 8, 0)

        # Opzetten artikeldata
        self.artikeldata = pd.DataFrame(columns=self.master.master.kantine.columns)

    def confirm_artikel(self):
        self.msgInfo = QMessageBox()
        self.msgInfo.setIcon(QMessageBox.Information)
        self.msgInfo.setStandardButtons(QMessageBox.Ok)

        self.msgWarn = QMessageBox()
        self.msgWarn.setIcon(QMessageBox.Warning)
        self.msgWarn.setStandardButtons(QMessageBox.Ok)

        pc = self.prodcode.text()
        pg = self.pgcombo.currentText()
        po = self.prodomsc.text()
        pr = float(self.prijs.text().replace(",", "."))
        ih = float(self.inhoud.text().replace(",", "."))
        sk = float(self.suiker.text().replace(",", "."))
        cl = float(self.calorieen.text().replace(",", "."))

        if pc == "" or po == "":
            self.msgWarn.setText("Barcode en artikel omschrijving zijn verplicht.")
            self.msgWarn.setWindowTitle("Aanmaken mislukt")
            self.msgWarn.show()

        elif self.master.master.kantine.Productcode.astype(str).str.contains(pc).any():
            self.msgWarn.setText("Barcode " + pc + " bestaat al. Aanmaken mislukt.")
            self.msgWarn.setWindowTitle("Aanmaken mislukt")
            self.msgWarn.show()

        else:
            s = pd.Series([pg, po, pc, pr, ih, sk, cl], index=self.artikeldata.columns)
            self.artikeldata = self.artikeldata.append(s, ignore_index=True, sort=False)

            # print(self.artikeldata)

            self.master.master.kantine = self.master.master.kantine.append(
                self.artikeldata, ignore_index=True, sort=False
            )
            self.artikeldata.drop(self.artikeldata.index, inplace=True)

            self.msgInfo.setText(po + " is aangemaakt.")
            self.msgInfo.setWindowTitle("Artikel aangemaakt")
            self.msgInfo.show()

            self.prodcode.clear()
            self.prodomsc.clear()
            # self.pgcombo.clear()
            self.prijs.clear()
            self.inhoud.clear()
            self.suiker.clear()
            self.calorieen.clear()

            self.prodcode.setFocus()

    def kt(self):
        self.master.change_screens("ArtikelBeheer")

    def nxt(self):
        self.prodcode.setFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = ArtikelAanmaken(None)
    screen.show()
    sys.exit(app.exec_())
