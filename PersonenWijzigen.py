import pandas as pd

pd.options.mode.chained_assignment = None

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QTableWidget,
    QComboBox,
)


class PersonenWijzigen(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.setGeometry(0, 0, 640, 480)

        self.layout = QGridLayout()

        self.setup_table()

        self.kt = QPushButton(self, text="Keer terug")
        self.kt.clicked.connect(self.ret)
        self.layout.addWidget(self.kt, 1, 0)

        self.new = QPushButton(self, text="Nieuw persoon toevoegen")
        self.new.clicked.connect(self.addNew)
        self.layout.addWidget(self.new, 1, 2)

        self.verw = QPushButton(self, text="Verwijder regel")
        self.verw.pressed.connect(self.verwijder_regel)
        self.layout.addWidget(self.verw, 1, 1)

        self.setLayout(self.layout)

    def setup_table(self):
        self.cols = len(self.master.master.personen.columns)
        self.rows = len(self.master.master.personen)

        self.table = QTableWidget(self.rows, self.cols, self)
        self.header = self.table.horizontalHeader()
        self.table.setHorizontalHeaderLabels(list(self.master.master.personen.columns))

        for i in range(self.cols):
            if i == 0 or i == self.cols - 1:
                self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                self.header.setSectionResizeMode(
                    i, QtWidgets.QHeaderView.ResizeToContents
                )

        self.layout.addWidget(self.table, 0, 0, 1, 3)

        self.fill_table()
        self.table.cellChanged.connect(self.on_changed)

    def fill_table(self):
        self.boxes = []

        for i, row in self.master.master.personen.iterrows():
            # self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))

            combGesl = QComboBox(self)
            combFunctie = QComboBox(self)
            combTent = QComboBox(self)

            for s in self.master.master.geslachten:
                combGesl.addItem(s)
            for s in self.master.master.tenten:
                combTent.addItem(s)
            for s in self.master.master.functies:
                combFunctie.addItem(s)

            combGesl.setCurrentText(row.Geslacht)
            combGesl.currentTextChanged.connect(self.on_changed_combo)
            combGesl.setProperty("Row", i)
            combGesl.setProperty("Column", 1)
            self.boxes.append(combGesl)

            combFunctie.setCurrentText(row.Functie)
            combFunctie.currentTextChanged.connect(self.on_changed_combo)
            combFunctie.setProperty("Row", i)
            combFunctie.setProperty("Column", 2)
            self.boxes.append(combFunctie)

            combTent.setCurrentText(row.Tent)
            combTent.currentTextChanged.connect(self.on_changed_combo)
            combTent.setProperty("Row", i)
            combTent.setProperty("Column", 3)
            self.boxes.append(combTent)

            self.table.setCellWidget(i, 1, combGesl)
            self.table.setCellWidget(i, 2, combFunctie)
            self.table.setCellWidget(i, 3, combTent)

            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row.Naam)))
            # self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.Geslacht)))
            # self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(row.Functie)))
            # self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(row.Tent)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(row.Barcode)))

    def on_changed_combo(self):
        self.master.master.personen.iloc[
            self.sender().property("Row"), self.sender().property("Column")
        ] = self.sender().currentText()

        print(self.master.master.personen)

    def on_changed(self):
        self.master.master.personen.iloc[
            self.table.currentRow(), self.table.currentColumn()
        ] = self.table.currentItem().text()
        print(self.master.master.personen)

    def ret(self):
        self.master.change_screens("KampHome")

    def addNew(self):
        self.master.change_screens("PersoonToevoegen")

    def verwijder_regel(self):
        row = self.table.currentRow()
        self.master.master.personen.drop(row, inplace=True)
        self.master.master.personen.reset_index(drop=True, inplace=True)
        self.table.clear()
        print(self.master.master.personen)
        self.setup_table()
