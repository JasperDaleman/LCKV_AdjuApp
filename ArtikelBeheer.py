from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QComboBox,
    QGridLayout,
    QTableWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets

import sys


class ArtikelBeheer(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        self.setup_table()

        self.setGeometry(0, 0, 640, 480)

        new = QPushButton(self, text="Nieuw")
        new.clicked.connect(self.new_article)
        self.layout.addWidget(new, 1, 2)

        terug = QPushButton(self, text="Keer terug")
        terug.clicked.connect(self.ex)
        self.layout.addWidget(terug, 1, 0)

        delete = QPushButton(self, text="Verwijder")
        delete.clicked.connect(self.delete_article)
        self.layout.addWidget(delete, 1, 1)

        self.setLayout(self.layout)

    def setup_table(self):
        self.columns = len(self.master.master.kantine.columns)
        self.rows = len(self.master.master.kantine)

        self.table = QTableWidget(self.rows, self.columns, self)
        self.table.setGeometry(0, 0, 640, 400)
        self.table.setSortingEnabled(True)
        self.header = self.table.horizontalHeader()
        # self.headerList = [Productcode, Product, Productgroep, Prijs, Inhoud, Suiker, Calorieen]
        # self.headerList = [self.master.master.kantine.Productcode.name, self.master.master.kantine.Product.name, self.master.master.kantine.Productgroep.name, self.master.master.kantine.Prijs.name,
        # self.master.master.kantine.Inhoud.name, self.master.master.kantine.Suiker.name, self.master.master.kantine.Calorieen.name]
        # self.table.setHorizontalHeaderLabels([self.master.master.kantine.index.name] + list(self.master.master.kantine.columns))
        self.table.setHorizontalHeaderLabels(list(self.master.master.kantine.columns))
        # self.table.setRowCount(self.rows)

        for i in range(self.columns):
            if i == 0 or i == self.columns - 1:
                self.header.setSectionResizeMode(
                    i, QtWidgets.QHeaderView.ResizeToContents
                )  # Stretch)
            else:
                self.header.setSectionResizeMode(
                    i, QtWidgets.QHeaderView.ResizeToContents
                )

        self.layout.addWidget(self.table, 0, 0, 1, 3)

        self.fill_table()
        self.table.cellChanged.connect(self.on_changed)

    def fill_table(self):
        self.prodgr = ["Dranken", "Chips", "Snoep"]

        self.boxes = []

        rowCount = 0

        for i, row in self.master.master.kantine.iterrows():
            print(row)

            comb = QComboBox(self)
            for s in self.prodgr:
                comb.addItem(s)

            comb.setCurrentText(row.Productgroep)
            comb.currentTextChanged.connect(self.on_changed_combo)
            comb.setProperty("Row", rowCount)
            comb.setProperty("Column", 0)
            self.boxes.append(comb)
            self.table.setCellWidget(rowCount, 0, comb)

            # self.table.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(row.Productgroep)))
            self.table.setItem(
                rowCount, 1, QtWidgets.QTableWidgetItem(str(row.Productomschrijving))
            )
            self.table.setItem(
                rowCount, 2, QtWidgets.QTableWidgetItem(str(row.Productcode))
            )
            self.table.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(str(row.Prijs)))
            self.table.setItem(rowCount, 4, QtWidgets.QTableWidgetItem(str(row.Inhoud)))
            self.table.setItem(rowCount, 5, QtWidgets.QTableWidgetItem(str(row.Suiker)))
            self.table.setItem(
                rowCount, 6, QtWidgets.QTableWidgetItem(str(row.Calorieen))
            )
            rowCount += 1

    def on_changed(self):
        # print(self.table.currentColumn())
        # print(self.table.currentItem())
        self.msgWarn = QMessageBox()
        self.msgWarn.setIcon(QMessageBox.Warning)
        self.msgWarn.setStandardButtons(QMessageBox.Ok)

        if self.master.master.kantine.Productcode.str.contains(
            self.table.currentItem().text()
        ).any():
            curProdcode = self.table.item(
                self.table.currentRow(), self.table.currentColumn()
            ).text()
            self.msgWarn.setText("Productcode bestaat al. Aanpassen mislukt.")
            self.msgWarn.setWindowTitle("Aanmaken mislukt")
            self.msgWarn.show()
            self.table.item(
                self.table.currentRow(), self.table.currentColumn()
            ).setText(
                self.master.master.kantine.iloc[
                    self.table.currentRow(), self.table.currentColumn()
                ]
            )
        elif (
            self.table.currentColumn() == 3
            or self.table.currentColumn() == 4
            or self.table.currentColumn() == 5
            or self.table.currentColumn() == 6
        ):
            self.master.master.kantine.iloc[
                self.table.currentRow(), self.table.currentColumn()
            ] = float(self.table.currentItem().text().replace(",", "."))
        else:
            self.master.master.kantine.iloc[
                self.table.currentRow(), self.table.currentColumn()
            ] = self.table.currentItem().text()

        # print(self.master.master.kantine)

    def on_changed_combo(self):
        self.master.master.kantine.iloc[
            self.sender().property("Row"), 0
        ] = self.sender().currentText()

    def new_article(self):
        self.master.change_screens("ArtikelAanmaken")

    def delete_article(self):
        try:
            # print(self.master.master.kantine)
            curRow = self.table.currentRow()

            curProdoms = self.getItem("Productomschrijving", curRow)
            curProdcode = self.getItem("Productcode", curRow)

            self.msgWarn = QMessageBox()
            self.msgWarn.setIcon(QMessageBox.Warning)
            self.msgWarn.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msgWarn.setText(
                "Weet je zeker dat je " + curProdoms + " wilt verwijderen?"
            )
            self.msgWarn.setWindowTitle("Verwijderen")

            retval = self.msgWarn.exec_()

            if retval == QMessageBox.Yes:
                self.table.removeRow(curRow)
                self.master.master.kantine.drop(
                    self.master.master.kantine[
                        self.master.master.kantine.Productcode.astype(str)
                        == curProdcode
                    ].index,
                    inplace=True,
                )
                # self.master.master.kantine = self.master.master.kantine[self.master.master.kantine.Productcode != curProdcode]
                # print(self.master.master.kantine)
            else:
                print("Error: Artikel niet verwijderd.")
        except IndexError:
            print("Geen regel geselecteerd om te verwijderen!!!")

    def getItem(self, columnname, row):
        headercount = self.table.columnCount()
        for x in range(0, headercount, 1):
            headertext = self.table.horizontalHeaderItem(x).text()
            if headertext == columnname:
                cell = self.table.item(row, x).text()
                return cell

    def ex(self):
        self.master.change_screens("KantineHome")


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    screen = ArtikelBeheer(app)
    screen.show()
    sys.exit(app.exec_())
