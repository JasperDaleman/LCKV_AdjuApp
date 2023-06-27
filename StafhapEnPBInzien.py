from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QLineEdit,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QTableWidget,
)

from datetime import datetime

import pandas as pd
import numpy as np

from datetime import datetime


class StafhapEnPBInzien(QWidget):  # TODO: misschien child van StafhapEnPB maken
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        self.keer_terug = QPushButton(self, text="Keer terug")
        self.keer_terug.clicked.connect(self.kt)
        self.layout.addWidget(self.keer_terug, 10, 0)

        self.stafleden = self.master.master.personen.sort_values("Naam").loc[
            self.master.master.personen["Tent"] == "Staf", "Naam"
        ]

        self.stafhapPB_pivot = pd.pivot_table(
            self.master.master.stafhapPB,
            "Bedrag",
            ["Bonnummer", "Type", "Datum"],
            columns=["Naam"],
            aggfunc=np.sum,
        )

        self.setup_table()

    def setup_table(self):
        columns = len(self.stafleden) + 3  # type, bonnr en datum
        rows = len(self.stafhapPB_pivot)  # print(rows)

        self.table = QTableWidget(rows, columns, self)
        self.table.setGeometry(0, 0, 640, 400)
        # self.table.setSortingEnabled(True)
        self.header = self.table.horizontalHeader()

        indexList = list(self.stafhapPB_pivot.index.names)
        stafledenList = list(self.stafleden)  # self.stafhapPB_pivot.columns)
        columnList = indexList + stafledenList
        # print(columnList)
        self.table.setHorizontalHeaderLabels(columnList)

        for i in range(columns):
            self.header.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents
            )  # Stretch)

        self.layout.addWidget(self.table, 0, 0, 1, 6)

        self.fill_table()
        self.table.cellChanged.connect(self.on_changed)

    def fill_table(self):
        rowCount_i = 0

        for i, row_i in self.stafhapPB_pivot.iterrows():
            cur_bonnr = i[0]
            cur_type = i[1]
            cur_datum = i[2]

            bonItem = QtWidgets.QTableWidgetItem(str(cur_bonnr))
            self.table.setItem(rowCount_i, 0, bonItem)
            typeItem = QtWidgets.QTableWidgetItem(str(cur_type))
            self.table.setItem(rowCount_i, 1, typeItem)
            datumItem = QtWidgets.QTableWidgetItem(str(cur_datum))
            self.table.setItem(rowCount_i, 2, datumItem)

            rowCount_j = 0
            for j in self.stafleden:
                if j in self.stafhapPB_pivot.columns:
                    cur_bedr = self.stafhapPB_pivot.loc[i, j]
                    if not np.isnan(cur_bedr):
                        self.table.setItem(
                            rowCount_i,
                            rowCount_j + 3,
                            QtWidgets.QTableWidgetItem(str(cur_bedr)),
                        )

                rowCount_j += 1

            rowCount_i += 1

    def on_changed(self):
        if self.table.currentColumn() >= 3:
            rowCount_i = 0
            for i, staflid in self.stafleden.iteritems():
                cur_Colnr = self.table.currentColumn() - 3

                if cur_Colnr == rowCount_i:
                    cur_bonnr = self.getItem("Bonnummer", self.table.currentRow())
                    cur_type = self.getItem("Type", self.table.currentRow())
                    cur_datum = self.getItem("Datum", self.table.currentRow())
                    cur_bedr = float(self.table.currentItem().text().replace(",", "."))

                    print(cur_bonnr, i, staflid, type(i))

                    fltr_bon = self.master.master.stafhapPB["Bonnummer"] == int(
                        cur_bonnr
                    )
                    fltr_staflid = self.master.master.stafhapPB["Barcode"] == i

                    try:
                        self.master.master.stafhapPB.loc[
                            fltr_bon & fltr_staflid, "Bedrag"
                        ].item()
                        self.master.master.stafhapPB.loc[
                            fltr_bon & fltr_staflid, "Bedrag"
                        ] = cur_bedr
                    except:
                        serie = pd.Series(
                            [cur_type, cur_bonnr, cur_datum, i, staflid, cur_bedr],
                            index=self.master.master.stafhapPB.columns,
                        )
                        self.master.master.stafhapPB = (
                            self.master.master.stafhapPB.append(
                                serie, ignore_index=True, sort=False
                            )
                        )

                    print(self.master.master.stafhapPB)

                rowCount_i += 1

    def getItem(self, columnname, row):
        headercount = self.table.columnCount()
        for x in range(0, headercount, 1):
            headertext = self.table.horizontalHeaderItem(x).text()
            if headertext == columnname:
                cell = self.table.item(row, x).text()
                return cell

    def kt(self):
        self.master.change_screens("StafhapEnPB")
