import pandas as pd
import sys
import os

import PyQt5
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QGridLayout, QLabel, QMessageBox


class TentWijzigen(QWidget):
    def __init__(self, master): 
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        self.bc_label = QLabel(self, text='Barcode') 
        self.layout.addWidget(self.bc_label, 0, 0)
        self.bc = QLineEdit(self)
        self.layout.addWidget(self.bc, 0, 1)
        self.bc.returnPressed.connect(self.fltr)

        self.naam_label = QLabel(self, text='Naam')
        self.layout.addWidget(self.naam_label, 1, 0)
        self.naam = QComboBox(self)
        for n in self.master.personen.Naam.sort_values():
            self.naam.addItem(n)
        self.layout.addWidget(self.naam, 1, 1)

        self.tent_label = QLabel(self, text='Nieuwe tent')
        self.layout.addWidget(self.tent_label, 2,0)
        self.tent = QComboBox(self)
        tents = ['Tent {}'.format(i) for i in range(1, 7)] 
        tents.append('Staf')
        for n in tents:
            self.tent.addItem(str(n))
        self.layout.addWidget(self.tent, 2,1)

        self.kt = QPushButton(self, text='Keer terug') 
        self.kt.pressed.connect(self.ret)
        self.layout.addWidget(self.kt, 3,0) 
    
        self.conf = QPushButton(self, text='Bevestigen')
        self.conf.pressed.connect(self.bev)
        self.layout.addWidget(self.conf, 3,1) 
        
        self.setLayout(self.layout)



    def fltr(self):
        try:
            naam = self.master.personen.loc[self.master.personen.Barcode == self.bc.text(), 'Naam'].values[0]
            self.naam.setCurrentText(naam)
            self.bc.clear()
        except IndexError:
            print('Geen goede waarde ingevoerd') 
    
    def bev(self):
        try: 
            self.master.personen.at[self.master.personen[self.master.personen.Naam == self.naam.currentText()].index, 'Tent'] = self.tent.currentText()
            print(self.master.personen) 
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.setText('Tent is aangepast!')
            self.msgBox.setWindowTitle('Success')
            self.msgBox.show()
            self.msgBox.exec_()
 

        except IndexError: 
            print('Niet gevonden') 
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.setText('Barcode bestaat niet,  gelieve opnieuw te scannen.')
            self.msgBox.setWindowTitle('Verkeerde code gescand')
            self.msgBox.show()
            self.msgBox.exec_()
    
    def ret(self):
        self.close()
    

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv) 
    w = TentWijzigen(None) 
    w.show()
    sys.exit(app.exec_())
