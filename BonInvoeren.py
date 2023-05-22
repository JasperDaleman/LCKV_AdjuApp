from PyQt5 import QtWidgets
import numpy as np
import pandas as pd
from datetime import datetime


class BonInvoeren(QtWidgets.QWidget):
    def __init__(self, master):
        self.master = master
        QtWidgets.QWidget.__init__(self)

        self.layout = QtWidgets.QGridLayout()

        self.receipt_label = QtWidgets.QLabel(self, text="Bonnummer")
        self.new_receipt_number = max(self.master.master.bonnen["Bonnummer"], default=1)
        self.receipt_number = QtWidgets.QLabel(self, text=str(self.new_receipt_number))
        self.layout.addWidget(self.receipt_label, 0, 0)
        self.layout.addWidget(self.receipt_number, 0, 1)

        # Date
        dt = datetime.now()

        self.date_label = QtWidgets.QLabel(self, text="Datum")

        self.date_day = QtWidgets.QComboBox(self)
        for d in np.arange(1, 32):
            self.date_day.addItem(str(d))
        self.date_day.setCurrentText(str(dt.day))

        self.date_month = QtWidgets.QComboBox(self)
        for m in np.arange(1, 13):
            self.date_month.addItem(str(m))
        self.date_month.setCurrentText(str(dt.month))

        self.date_year = QtWidgets.QLineEdit(self)
        self.date_year.setText(str(dt.year))

        self.layout.addWidget(self.date_label, 1, 0)
        self.layout.addWidget(self.date_day, 1, 1)
        self.layout.addWidget(self.date_month, 1, 2)
        self.layout.addWidget(self.date_year, 1, 3)

        # Description
        self.desc_label = QtWidgets.QLabel(self, text="Omschrijving")
        self.desc = QtWidgets.QLineEdit(self)

        self.layout.addWidget(self.desc_label, 2, 0)
        self.layout.addWidget(self.desc, 2, 1, 1, 3)

        # Pot
        self.source = QtWidgets.QComboBox(self)
        for v in [
            "Voeding",
            "Vrije besteding",
            "Fietsverhuur_Outdoor",
            "Brandstof",
            "Overig",
            "Kantine",
            "Statiegeld",
            "Stafhap",
            "PBs",
        ]:
            self.source.addItem(str(v))

        self.source_label = QtWidgets.QLabel(self, text="Pot")
        self.layout.addWidget(self.source_label, 3, 0)
        self.layout.addWidget(self.source, 3, 1)

        # Amount
        self.amount_label = QtWidgets.QLabel(self, text="Bedrag")
        self.amount = QtWidgets.QLineEdit(self)

        self.layout.addWidget(self.amount_label, 4, 0)
        self.layout.addWidget(self.amount, 4, 1)

        # Invoeren / afsluiten
        self.confirm = QtWidgets.QPushButton(self, text="Bevestigen Bon")
        self.confirm.clicked.connect(self.conf)

        self.ex = QtWidgets.QPushButton(self, text="Terugkeren")
        self.ex.clicked.connect(self.exit)

        self.layout.addWidget(self.ex, 5, 0)
        self.layout.addWidget(self.confirm, 5, 1)

        self.setLayout(self.layout)

        self.widgets = [
            self.date_day,
            self.date_month,
            self.date_year,
            self.desc,
            self.source,
            self.amount,
        ]

        self.amount.returnPressed.connect(self.conf)

    def conf(self):
        self.date = "{}-{}-{}".format(
            self.date_day.currentText(),
            self.date_month.currentText(),
            self.date_year.text(),
        )

        print(
            self.date, self.desc.text(), self.amount.text(), self.source.currentText()
        )

        s = pd.Series(
            [
                self.new_receipt_number,
                self.date,
                self.desc.text(),
                self.source.currentText(),
                float(self.amount.text().replace(",", ".")),
            ],
            index=["Bonnummer", "Datum", "Omschrijving", "Pot", "Bedrag"],
            name=str(len(self.master.master.bonnen)),
        )

        self.master.master.bonnen = self.master.master.bonnen.append(
            s, sort=False, ignore_index=False
        )

        self.desc.clear()
        self.amount.clear()
        self.desc.setFocus()

    def exit(self):
        self.master.change_screens("KampHome")
