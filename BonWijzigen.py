from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)
import sys


class BonWijzigen(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        self.setup_table()

        self.setGeometry(0, 0, 640, 480)

        terug = QPushButton(self, text="Keer terug")
        terug.clicked.connect(self.ex)
        self.layout.addWidget(terug, 1, 0)

        self.setLayout(self.layout)

    def setup_table(self):
        self.columns = len(self.master.master.bonnen.columns)
        self.rows = len(self.master.master.bonnen)

        self.table = QTableWidget(self.rows, self.columns, self)
        self.table.setGeometry(0, 0, 640, 400)
        self.header = self.table.horizontalHeader()
        self.table.setHorizontalHeaderLabels(list(self.master.master.bonnen.columns))

        for i in range(self.columns):
            if i == 0 or i == self.columns - 1:
                self.header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table, 0, 0, 1, 2)

        self.fill_table()
        self.table.cellChanged.connect(self.on_changed)

    def fill_table(self):
        self.sources = [
            "Voeding",
            "Vrije besteding",
            "Fietsverhuur_Outdoor",
            "Brandstof",
            "Overig",
            "Kantine",
            "Statiegeld",
            "Stafhap",
            "PBs",
        ]

        self.boxes = []

        for i, row in self.master.master.bonnen.iterrows():
            i = int(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(row["Bonnummer"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row["Datum"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row["Omschrijving"])))

            comb = QComboBox(self)
            for s in self.sources:
                comb.addItem(s)

            comb.setCurrentText(row.Pot)
            comb.currentTextChanged.connect(self.on_changed_combo)
            comb.setProperty("Row", i)
            comb.setProperty("Column", 3)
            self.boxes.append(comb)
            self.table.setCellWidget(i, 3, comb)

            self.table.setItem(i, 4, QTableWidgetItem(str(row["Bedrag"])))

    def on_changed(self):
        if self.table.currentColumn() == 5:
            self.master.master.bonnen.iloc[
                self.table.currentRow(), self.table.currentColumn()
            ] = float(self.table.currentItem().text().replace(",", "."))
        else:
            self.master.master.bonnen.iloc[
                self.table.currentRow(), self.table.currentColumn()
            ] = self.table.currentItem().text()

    def on_changed_combo(self):
        self.master.master.bonnen.iloc[
            self.sender().property("Row"), 2
        ] = self.sender().currentText()

        print(self.master.master.bonnen)

    def ex(self):
        self.master.change_screens("KampHome")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = BonWijzigen(app)
    screen.show()
    sys.exit(app.exec_())
