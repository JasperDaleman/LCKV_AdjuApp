import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGridLayout

import sys
import os

import pandas as pd 


class Inleggen(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        # Barcode
        self.bc_label = QLabel(self, text='Barcode')
        self.bc = QLineEdit(self)
        self.bc.returnPressed.connect(self.scanned)

        self.layout.addWidget(self.bc_label, 0,0)
        self.layout.addWidget(self.bc, 0, 1)
        
        # Inleg
        self.inleg_label = QLabel(self, text='Inleg')
        self.inleg = QLineEdit(self)
        self.inleg.returnPressed.connect(self.ingevoerd)

        self.layout.addWidget(self.inleg_label, 1, 0)
        self.layout.addWidget(self.inleg, 1, 1)


        self.ret = QPushButton(self, text='Keer terug')
        self.ret.clicked.connect(self.keer_terug)
        self.conf = QPushButton(self, text='Bevestigen')
        self.conf.clicked.connect(self.ingevoerd)

        self.layout.addWidget(self.ret, 2, 0)
        self.layout.addWidget(self.conf, 2, 1)


    def scanned(self):
        self.inleg.setFocus()


    def ingevoerd(self):
        if len(self.master.deelnemers_inleg) == 0:
            s = pd.Series([self.bc.text(), int(self.inleg.text())], index=['Barcode', 'Inleg'])
            self.master.deelnemers_inleg = self.master.deelnemers_inleg.append(s, ignore_index=True, sort=False)
        else: 
            idx = self.master.deelnemers_inleg[self.master.deelnemers_inleg.Barcode == self.bc.text()]
            if len(idx) == 0: 
                s = pd.Series([self.bc.text(), self.inleg.text()], index=['Barcode', 'Inleg'])
                self.master.deelnemers_inleg = self.master.deelnemers_inleg.append(s, ignore_index=True, sort=False)
            else: 
                self.master.deelnemers_inleg.at[idx.index.values[0], 'Inleg'] += float(self.inleg.text())

 
        print(self.master.deelnemers_inleg)        

        self.bc.clear()
        self.inleg.clear()
        self.bc.setFocus()


    def keer_terug(self):
        self.close() 



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    s = Inleggen(None)
    s.show()
    sys.exit(app.exec_())

