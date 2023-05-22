from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QComboBox,
    QGridLayout,
    QLabel,
    QRadioButton,
    QMessageBox,
)


import pandas as pd


class InvullenBegroting(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        # Kamp
        self.kamp_label = QLabel(self, text="Kampgegevens")
        self.kamp_nummer = QLineEdit(self)
        self.kamp_locatie = QComboBox(self)
        for l in self.master.master.locaties:
            self.kamp_locatie.addItem(l)
        self.layout.addWidget(self.kamp_label, 0, 0, 1, 2)
        self.layout.addWidget(self.kamp_nummer, 0, 2)
        self.layout.addWidget(self.kamp_locatie, 0, 3)

        # Voeding (per deelnemer)
        self.voeding_label = QLabel(self, text="Voedingsbudget per deelnemer")
        self.voeding = QLineEdit(self)
        self.layout.addWidget(self.voeding_label, 1, 0, 1, 2)
        self.layout.addWidget(self.voeding, 1, 2, 1, 2)

        # Vrije besteding (per deelnemer)
        self.vrije_besteding = QLabel(self, text="Vrij budget per deelnemer")
        self.vb = QLineEdit(self)
        self.layout.addWidget(self.vrije_besteding, 2, 0, 1, 2)
        self.layout.addWidget(self.vb, 2, 2, 1, 2)

        # Outdoor/Fietsverhuur, totaal of per persoon vinken
        self.outdoor_label = QLabel(self, text="Budget Outdoor/fietsverhuur")
        self.outdoor_budget = QLineEdit(self)
        self.outdoor_rb1 = QRadioButton(self, text="Totaal")
        self.outdoor_rb1.setChecked(True)
        self.outdoor_rb2 = QRadioButton(self, text="Per deelnemer")
        self.layout.addWidget(self.outdoor_label, 3, 0)
        self.layout.addWidget(self.outdoor_budget, 3, 1)
        self.layout.addWidget(self.outdoor_rb1, 3, 2)
        self.layout.addWidget(self.outdoor_rb2, 3, 3)

        self.stafsupport_label = QLabel(self, text="Hoe veel staf als support?")
        self.stafsupport = QLineEdit(self, text="9")
        self.layout.addWidget(self.stafsupport_label, 4, 0, 1, 2)
        self.layout.addWidget(self.stafsupport, 4, 2, 1, 2)

        # Fooi
        self.fooi_label = QLabel(self, text="Fooi")
        self.fooi = QLineEdit(self)
        self.layout.addWidget(self.fooi_label, 5, 0, 1, 2)
        self.layout.addWidget(self.fooi, 5, 2, 1, 2)

        # Brandstof
        self.brandstof_label = QLabel(self, text="Brandstof")
        self.brandstof = QLineEdit(self)
        self.layout.addWidget(self.brandstof_label, 6, 0, 1, 2)
        self.layout.addWidget(self.brandstof, 6, 2, 1, 2)

        # Stafpresentje (20e)
        self.pres_label = QLabel(self, text="Stafpresentje")
        self.pres = QLineEdit(self)
        self.layout.addWidget(self.pres_label, 7, 0, 1, 2)
        self.layout.addWidget(self.pres, 7, 2, 1, 2)

        self.keer_terug = QPushButton(self, text="Keer terug")
        self.keer_terug.clicked.connect(self.kt)
        self.layout.addWidget(self.keer_terug, 8, 0, 1, 2)

        self.bevestigen = QPushButton(self, text="Bevestigen")
        self.bevestigen.clicked.connect(self.bev)
        self.layout.addWidget(self.bevestigen, 8, 2, 1, 2)

        self.setLayout(self.layout)

        self.check_file()

    def kt(self):
        self.master.change_screens("HomeScreen")

    def bev(self):
        kampn = self.kamp_nummer.text()
        kampl = self.kamp_locatie.currentText()

        try:
            voeding = int(self.voeding.text()) * len(self.master.master.personen)
            vb = int(self.vb.text())

            outdoor = int(self.outdoor_budget.text())
            if self.outdoor_rb2.isChecked():
                outdoor *= len(
                    self.master.master.personen[
                        self.master.master.personen.Functie == "Deelnemer"
                    ]
                ) + int(self.stafsupport.text())

            fooi = int(self.fooi.text())
            fuel = int(self.brandstof.text())

            pres = int(self.pres.text())

            s = pd.Series(
                [kampn, kampl, voeding, vb, outdoor, fooi, fuel, pres],
                index=[
                    "Kampnummer",
                    "Locatie",
                    "Voeding",
                    "Vrije besteding",
                    "Fietsverhuur_outdoor",
                    "Fooi",
                    "Brandstof",
                    "Stafpresentje",
                ],
            )
            self.master.master.begroting = s

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle("Ingevoerd")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setText("Begroting is ingevoerd")
            msgbox.exec_()

            self.kt()

        except ValueError:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle("Foute waarde ingevoerd")
            msgbox.setText(
                "Er is ergens een foute waarde ingevoerd, controleer gegevens"
            )
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def check_file(self):
        if not self.master.master.begroting.empty:
            # print(self.master.master.begroting.index)
            kampn = self.master.master.begroting.loc["Kampnummer", 1]
            kampl = self.master.master.begroting.loc["Locatie", 1]
            vd = self.master.master.begroting.loc["Voeding", 1]
            vb = self.master.master.begroting.loc["Vrije besteding", 1]
            fo = self.master.master.begroting.loc["Fietsverhuur_Outdoor", 1]
            fi = self.master.master.begroting.loc["Fooi", 1]
            bs = self.master.master.begroting.loc["Brandstof", 1]
            ps = self.master.master.begroting.loc["Stafpresentje", 1]

            self.kamp_nummer.setText(str(kampn))
            self.kamp_locatie.setCurrentText(str(kampl))
            self.voeding.setText(str(vd))
            self.vb.setText(str(vb))
            self.outdoor_budget.setText(str(fo))
            self.fooi.setText(str(fi))
            self.brandstof.setText(str(bs))
            self.pres.setText(str(ps))

        else:
            pass
