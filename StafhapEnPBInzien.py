from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QWidget, QGridLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QTableWidget

from datetime import datetime

import pandas as pd
import numpy as np

from datetime import datetime


class StafhapEnPBInzien(QWidget): #TODO: misschien child van StafhapEnPB maken
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        self.bonnr = QLineEdit(self)
        # self.bonnr.returnPressed.connect(self.get_bon)
        self.bonnr_label = QLabel(self, text='Bonnummer: ')
        self.layout.addWidget(self.bonnr_label, 0, 0)
        self.layout.addWidget(self.bonnr, 0, 1)

        self.bonomsc = ''
        self.bonomsc_label = QLabel(self, text=self.bonomsc)
        self.layout.addWidget(self.bonomsc_label, 0, 2, 1, 2)

        self.keer_terug = QPushButton(self, text='Keer terug')
        self.keer_terug.clicked.connect(self.kt)
        self.layout.addWidget(self.keer_terug, 10, 0)

        #stafhap of pb
        self.sthp_pb_group = QButtonGroup()
        self.stafhap_radiobtn = QRadioButton("Stafhap")
        self.sthp_pb_group.addButton(self.stafhap_radiobtn, 1)
        self.stafhap_radiobtn.setChecked(True)
        self.stafhap_radiobtn.sthp_pb = "Stafhap"
        self.layout.addWidget(self.stafhap_radiobtn, 0, 4)
        self.stafhap_radiobtn.toggled.connect(lambda:self.onclick(self.stafhap_radiobtn,-1))
        self.pb_radiobtn = QRadioButton("PB")
        self.sthp_pb_group.addButton(self.pb_radiobtn, 1)
        self.pb_radiobtn.sthp_pb = "PB"
        self.layout.addWidget(self.pb_radiobtn, 0, 5)
        self.pb_radiobtn.toggled.connect(lambda:self.onclick(self.pb_radiobtn,-1))

         # Datum van de stafhap of pb ingeven
        dt = datetime.now()
        self.date_label = QtWidgets.QLabel(self, text='Datum')

        self.date_day = QtWidgets.QComboBox(self)
        for d in np.arange(1, 32):
            self.date_day.addItem(str(d))

        self.date_month = QtWidgets.QComboBox(self)
        for m in np.arange(1, 13):
            self.date_month.addItem(str(m))

        self.date_year = QtWidgets.QLineEdit(self)

        self.layout.addWidget(self.date_label, 1, 0)
        self.layout.addWidget(self.date_day, 1, 1)
        self.layout.addWidget(self.date_month, 1, 2)
        self.layout.addWidget(self.date_year, 1, 3)

        self.stafleden = self.master.master.personen.sort_values('Naam').loc[self.master.master.personen['Tent'] == 'Staf', 'Naam']

        self.stafhapPB_pivot = pd.pivot_table(self.master.master.stafhapPB, 'Bedrag', ['Bonnummer','Type','Datum'], columns= ['Naam'], aggfunc=np.sum)

        self.setup_table()

    def setup_table(self):
        columns = len(self.stafleden) + 3 #type, bonnr en datum
        rows = len(self.stafhapPB_pivot) # print(rows)

        self.table = QTableWidget(rows, columns, self)
        self.table.setGeometry(0, 0, 640, 400)
        # self.table.setSortingEnabled(True)
        self.header = self.table.horizontalHeader()
    
        indexList = list(self.stafhapPB_pivot.index.names)
        stafledenList = list(self.stafleden)#self.stafhapPB_pivot.columns)
        columnList = indexList + stafledenList
        # print(columnList)
        self.table.setHorizontalHeaderLabels(columnList)

        for i in range(columns):
             self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents) #Stretch)

        self.layout.addWidget(self.table, 2, 0, 1, 6)

        self.fill_table()
        # self.table.cellChanged.connect(self.on_changed)


    def fill_table(self):
        rowCount_i = 0

        for i, row_i in self.stafhapPB_pivot.iterrows():
            cur_bonnr = i[0]
            cur_type = i[1]
            cur_datum = i[2]

            bonItem = QtWidgets.QTableWidgetItem(str(cur_bonnr))
            self.table.setItem(rowCount_i, 0, bonItem)
            typeItem = QtWidgets.QTableWidgetItem(str(cur_type)) #.setFlags(~QtCore.Qt.ItemIsEnabled )
            self.table.setItem(rowCount_i, 1, typeItem)
            datumItem = QtWidgets.QTableWidgetItem(str(cur_datum))
            self.table.setItem(rowCount_i, 2, datumItem)

            rowCount_j = 0
            for j in self.stafleden:
                if j in self.stafhapPB_pivot.columns:
                    cur_bedr = self.stafhapPB_pivot.loc[i,j]
                    if not np.isnan(cur_bedr):
                        self.table.setItem(rowCount_i, rowCount_j + 3, QtWidgets.QTableWidgetItem(str(cur_bedr)))
                        # print(i,j,cur_bedr,np.isnan(cur_bedr))

                rowCount_j += 1

            rowCount_i += 1


    def on_changed(self):
        # print(self.table.currentColumn())
        # print(self.table.currentItem())

        if self.table.currentColumn() >= 3:
            
            rowCount_i = 0
            for i, staflid in self.stafleden.iteritems():
                cur_Colnr = self.table.currentColumn()-3

                if cur_Colnr == rowCount_i:
                    cur_bonnr = self.getItem('Bonnummer',self.table.currentRow())
                    cur_type = self.getItem('Type',self.table.currentRow())
                    cur_datum = self.getItem('Datum',self.table.currentRow())
                    cur_bedr = float(self.table.currentItem().text().replace(',','.'))

                    print(cur_bonnr, i, staflid, type(i))

                    fltr_bon = (self.master.master.stafhapPB['Bonnummer'] == int(cur_bonnr))
                    fltr_staflid = (self.master.master.stafhapPB['PersoonID'] == i)

                    # print(self.master.master.stafhapPB.loc[fltr_bon, 'PersoonID'].astype(int))
                    # print(i in self.master.master.stafhapPB.loc[fltr_bon, 'PersoonID'].astype(int))
                    # print(self.master.master.stafhapPB.loc[fltr_bon & fltr_staflid, 'Bedrag'].index.values)

                    # print(self.master.master.stafhapPB.loc[fltr_bon & fltr_staflid, 'Bedrag'].item())
                    # print(type(self.master.master.stafhapPB.loc[fltr_bon & fltr_staflid, 'Bedrag'].item()))

                    try:
                        self.master.master.stafhapPB.loc[fltr_bon & fltr_staflid, 'Bedrag'].item()
                        self.master.master.stafhapPB.loc[fltr_bon & fltr_staflid, 'Bedrag'] = cur_bedr
                    except:                    
                        serie = pd.Series([cur_type, cur_bonnr, cur_datum, i, staflid, cur_bedr], index=self.master.master.stafhapPB.columns)
                        self.master.master.stafhapPB = self.master.master.stafhapPB.append(serie, ignore_index=True, sort=False)
                    
                    print(self.master.master.stafhapPB)
                    # self.master.master.stafhapPB.to_csv("C:\\Users\\Lars\\Documents\\LCKV\\Adju App\\Grafisch\\app_opzet2.3\\data\\sthp.csv")
                    # print(self.master.master.stafhapPB.loc[self.master.master.stafhapPB['Bonnummer'] == cur_bonnr])
                    # print(j.index, j)


                rowCount_i += 1

            # print(cur_persID)
            # self.master.master.stafhapPB.iloc[self.table.currentRow(), self.table.currentColumn()] = float(self.table.currentItem().text().replace(',','.'))

    def getItem(self, columnname, row):
        headercount = self.table.columnCount()
        for x in range(0,headercount,1):
            headertext = self.table.horizontalHeaderItem(x).text()
            if headertext == columnname:
                cell = self.table.item(row, x).text()
                return cell

    def kt(self):
        self.master.change_screens('StafhapEnPB')