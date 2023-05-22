import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGridLayout,
    QLabel,
)


class InlegEnTentindeling(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        self.naam_label = QLabel(self, text="Naam")
        self.layout.addWidget(self.naam_label, 0, 0)
        self.naam = QComboBox(self)
        for n in self.master.personen.Naam.sort_values():
            self.naam.addItem(n)
        self.layout.addWidget(self.naam, 0, 1)

        self.tent = QComboBox(self)
        for t in ["Tent 1", "Tent 2", "Tent 3", "Tent 4", "Tent 5", "Tent 6", "Staf"]:
            self.tent.addItem(t)
        self.layout.addWidget(self.tent, 1, 1)
        self.layout.addWidget(QLabel(self, text="Tent"), 1, 0)

        self.inleg_label = QLabel(self, text="Inleg")
        self.inleg = QLineEdit(self)
        self.inleg.returnPressed.connect(self.nxt)
        self.layout.addWidget(self.inleg_label, 2, 0)
        self.layout.addWidget(self.inleg, 2, 1)

        self.barcode_label = QLabel(self, text="Barcode bonuskaart")
        self.layout.addWidget(self.barcode_label, 3, 0)
        self.bc = QLineEdit(self)
        self.bc.returnPressed.connect(self.conf)
        self.layout.addWidget(self.bc, 3, 1)

        self.keer_terug = QPushButton(self, text="Keer terug")
        self.keer_terug.pressed.connect(self.kt)
        self.layout.addWidget(self.keer_terug, 4, 0)
        self.bevestigen = QPushButton(self, text="Bevestigen")
        self.bevestigen.pressed.connect(self.conf)
        self.layout.addWidget(self.bevestigen, 4, 1)

        self.setLayout(self.layout)

    def kt(self):
        self.close()

    def nxt(self):
        self.bc.setFocus()

    def conf(self):
        naam = self.naam.currentText()

        row = self.master.personen[self.master.personen.Naam == naam]

        self.master.personen.at[
            self.master.personen[self.master.personen.Naam == naam].index, "Tent"
        ] = self.tent.currentText()
        self.master.personen.at[
            self.master.personen[self.master.personen.Naam == naam].index, "Barcode"
        ] = self.bc.text()
        inleg = self.inleg.text()
        try:
            inleg = float(inleg)

            s = pd.Series(
                [self.bc.text(), self.inleg.text()], index=["Barcode", "Inleg"]
            )
            self.master.inleg = self.master.inleg.append(s, ignore_index=True)

            self.inleg.clear()
            self.bc.clear()
        except ValueError:
            print("Geen goede waarde ingevoerd")

        self.inleg.setFocus()
