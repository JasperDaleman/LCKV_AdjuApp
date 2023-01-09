from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QWidget, QComboBox, QGridLayout, QPushButton, QLabel, QMessageBox, QTableWidget
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import StandaardFuncties

class OrderIngeven(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)


        self.layout = QGridLayout(self)

        # Deelnemer barcode
        self.dn_label = QLabel(self, text='Deelnemer barcode')
        self.dn = QLineEdit(self)
        self.dn.returnPressed.connect(self.barcode_scanned)

        self.layout.addWidget(self.dn_label, 0,0)
        self.layout.addWidget(self.dn, 0,1)
        
        dt = datetime.now()

        # Deelnemer selectie: Tent
        self.dncombo = QComboBox(self)
        for dn in self.master.master.personen.Naam:
            self.dncombo.addItem(str(dn))

        self.tentcombo = QComboBox(self)
        for t in self.master.master.personen.Tent.unique():
            self.tentcombo.addItem(str(t))

        self.tentcombo.currentTextChanged.connect(self.fltr)

        self.layout.addWidget(self.dncombo, 2, 1)
        self.layout.addWidget(self.tentcombo, 1,1)


        # Datum van de order ingeven
        self.date_label = QtWidgets.QLabel(self, text='Datum')

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

        self.layout.addWidget(self.date_label, 3, 0)
        self.layout.addWidget(self.date_day, 3, 1)
        self.layout.addWidget(self.date_month, 3, 2)
        self.layout.addWidget(self.date_year, 3, 3)

        # Inleg label
        self.inleg = 0
        self.inleg_label = QLabel(self, text='Inleg: {}'.format(self.inleg))
       
        self.layout.addWidget(self.inleg_label, 4, 1, 1, 2)
        

        # Product barcode
        self.productcode = QLineEdit(self)
        self.productcode.returnPressed.connect(self.nxt)
        self.product_label = QLabel(self, text='Enter product barcode: ')
        
        self.layout.addWidget(self.productcode, 6,1)
        self.layout.addWidget(self.product_label, 6, 0)
        
        # Aantal producten
        self.amount = QLineEdit(self)
        self.amount_label = QLabel(self, text='Aantal: ')
        self.amount.returnPressed.connect(self.confirm_line)
        
        self.layout.addWidget(self.amount_label, 7, 0)
        self.layout.addWidget(self.amount, 7, 1)

        self.dn.selectAll()
        self.dn.setFocus()
        

        # Bevestigen Buttons en terug
        self.conf_line = QPushButton(self, text='Bevestig Regel')
        self.conf_order = QPushButton(self, text='Bevestig Order')
        self.keer_terug = QPushButton(self, text='Keer terug')
        self.del_line = QPushButton(self, text='Verwijder regel')

        self.conf_line.clicked.connect(self.confirm_line)
        self.conf_order.clicked.connect(self.confirm_order)
        self.keer_terug.clicked.connect(self.kt)
        self.del_line.clicked.connect(self.delete_line)

        self.layout.addWidget(self.conf_line, 8, 2)
        self.layout.addWidget(self.conf_order, 8, 3)
        self.layout.addWidget(self.keer_terug, 8, 0)
        self.layout.addWidget(self.del_line, 8, 1)
        
        # Opzetten orderlines
        self.orderlines = pd.DataFrame(columns=self.master.master.orders.columns)
        if len(self.master.master.orders) == 0: 
            self.ordernummer = 0
        else: 
            self.ordernummer = self.master.master.orders.Ordernummer.max() + 1


        # Opzetten tabel voor orderregels
        self.setup_table()
    

    def setup_table(self):
        columns = len(self.master.master.orders.columns)+1
        rows = len(self.orderlines)

        header = self.master.master.orders.columns

        self.table = QTableWidget(rows, columns, self)
        self.header = self.table.horizontalHeader()
        self.table.setHorizontalHeaderLabels(['Regelnummer'] + list(self.master.master.orders.columns))
        
        for i in range(columns):
            if i == 0 or i == columns-1:
                self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else: self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table, 5, 0, 1, 4)

        self.fill_table()

    def fill_table(self):
        self.table.setRowCount(len(self.orderlines))
        for i, row in self.orderlines.iterrows():
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row.Ordernummer)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.DatumTijd)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(row.PersoonID)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(row.Productcode)))
            self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(str(row.Product)))
            self.table.setItem(i, 6, QtWidgets.QTableWidgetItem(str(row.Aantal)))
            self.table.setItem(i, 7, QtWidgets.QTableWidgetItem(str(row.Bedrag)))

    def delete_line(self):
        if len(self.table.selectedItems()) > 0: 
            curRow = self.table.currentRow()
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msgBox.setText('Weet je zeker dat je deze regel wilt verwijderen?')
            self.msgBox.setWindowTitle('Regel verwijderen')
            self.msgBox.show()
            self.retval = self.msgBox.exec_()
            if self.retval == QMessageBox.Yes:
                self.table.removeRow(curRow)
                self.orderlines.drop(int(curRow), inplace=True)
                print(self.orderlines)
                self.fill_table()
        else:
            print('Geen rij geselecteerd')
            StandaardFuncties.warning(self, "Geen rij geselecteerd!", "Regel verwijderen")
 
    def fltr(self):
        self.dncombo.clear()
        #sel = self.master.master.deelnemers[self.master.master.deelnemers.Tent == self.tentcombo.currentText()]
        sel = self.master.master.personen[self.master.master.personen.Tent == self.tentcombo.currentText()]
        
        for n in sel.Naam:
            self.dncombo.addItem(n)

    def barcode_scanned(self):
        if self.dn.text() not in self.master.master.personen.Barcode:
            StandaardFuncties.warning(self, "Barcode niet gevonden", "Helaas")
        else:
            name = self.master.master.personen.Naam.loc[self.master.master.personen.Barcode == self.dn.text()]
            tent = self.master.master.personen.Tent.loc[self.master.master.personen.Barcode == self.dn.text()]
            self.persID = self.master.master.personen.index[self.master.master.personen.Barcode == self.dn.text()][0]

            print(name, tent)
            
            if len(name) > 0:
                self.tentcombo.setCurrentText(self.master.master.personen.at[tent.index[0], 'Tent'])
                self.dncombo.setCurrentText(self.master.master.personen.at[name.index[0], 'Naam'])

            #self.dn.clear()
            self.productcode.setFocus()
        
            # Inleg opzoeken
            try:
                self.inleg = self.master.master.inleg.loc[self.master.master.inleg[self.master.master.inleg.PersoonID == self.persID].index[0], 'InlegHuidig']
                self.inleg_label.setText('Inleg: {}'.format(self.inleg))
            except IndexError:
                StandaardFuncties.warning(self, "Geen inleg beschikbaar", "Foutmelding")

    def confirm_order(self):
        self.dncombo.clear()

        for n in self.master.master.personen.Naam:
            self.dncombo.addItem(n)

        self.dn.clear()

        self.master.master.orders = self.master.master.orders.append(self.orderlines, ignore_index=True, sort=False)
        self.orderlines.drop(self.orderlines.index, inplace=True)
        while self.table.rowCount() > 0: 
            self.table.removeRow(0)
        self.inleg_label.setText('Inleg: 0')
        self.master.master.inleg.loc[self.master.master.inleg['PersoonID'] == self.persID, 'InlegHuidig'] = self.inleg

        print(self.master.master.orders)

    def confirm_line(self):
        on = self.ordernummer
        persid = self.persID
        prodc = self.productcode.text()
        if prodc != '':
            try: 
                prod = self.master.master.kantine.Productomschrijving.loc[self.master.master.kantine.Productcode == prodc].values[0]
                
                date = '{}-{}-{}'.format(self.date_day.currentText(), self.date_month.currentText(),
                                     self.date_year.text())

                am = self.amount.text()
                bedr = self.master.master.kantine.Prijs.loc[self.master.master.kantine.Productcode == prodc].values[0] * int(am)
            
                s = pd.Series([on, date, persid, prodc, prod, am, bedr], index=self.orderlines.columns)
                self.orderlines = self.orderlines.append(s, ignore_index=True, sort=False)

                self.update_label_text(bedr)
                self.fill_table() 
                print(self.orderlines)
            except IndexError: 
                print('Productcode onjuist')

        
        self.productcode.clear()
        self.amount.clear()

        self.productcode.setFocus()


    def kt(self):
        self.master.change_screens('KantineHome')


    def nxt(self):
        self.amount.setFocus()

    def update_label_text(self, bedrag):
        if self.inleg - float(bedrag) > 0: 
            self.inleg -= float(bedrag)
            self.inleg_label.setText('Inleg: {}'.format(self.inleg))
        else: 
            msg = QMessageBox()
            msg.setText('Maximale inleg bereikt, controleer order')
            msg.setWindowTitle('Waarschuwing!!')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    screen = OrderIngeven(None)
    screen.show()
    sys.exit(app.exec_())

