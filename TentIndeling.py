import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout, QWidget

import sys
import os
import pandas as pd


class TentenIndeling(QWidget):
    def __init__(self, master): 
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)
        
        # Barcode
        self.barcode_label = QLabel(self, text='Barcode')
        self.barcode = QLineEdit(self)
        self.barcode.returnPressed.connect(self.fillIn)

        self.layout.addWidget(self.barcode_label, 0, 0)
        self.layout.addWidget(self.barcode, 0, 1)

        # Naam
        self.name_label = QLabel(self, text='Naam')
        self.name = QComboBox(self)
        for n in self.master.deelnemers.Naam:
            self.name.addItem(n)
        self.name.currentTextChanged.connect(self.rst)

        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name, 1, 1)
        
        # Tent
        self.tent_label = QLabel(self, text='Tent')
        self.tent = QComboBox(self)
        for t in range(1, 7):
            self.tent.addItem('Tent {}'.format(t))
        self.tent.addItem('Staf')

        self.layout.addWidget(self.tent_label, 2, 0)
        self.layout.addWidget(self.tent, 2, 1)

        # Buttons
        self.confirm = QPushButton(self, text='Bevestigen')
        self.confirm.pressed.connect(self.conf)
        self.layout.addWidget(self.confirm, 3, 1)

        self.kt = QPushButton(self, text='Keer terug')
        self.kt.pressed.connect(self.ret)
        self.layout.addWidget(self.kt, 3, 0)
 



    def fillIn(self):
        if self.barcode.text() in self.master.deelnemers.Barcode.unique():
            n = self.master.deelnemers.loc[self.master.deelnemers[self.master.deelnemers.Barcode == self.barcode.text()].index, 'Naam'].values[0]
            t = self.master.deelnemers.loc[self.master.deelnemers[self.master.deelnemers.Barcode == self.barcode.text()].index, 'Tent'].values[0]

            self.name.setCurrentText(n)
            self.tent.setCurrentText(t)
        else: print('Bestaat niet')
            #self.name.setCurrentText(self.master.deelnemers.loc[self.master.deelnemers[self.master.deelnemers.Barcode == self.barcode.text()].index, 'Naam'].values[0])
            #self.tent.setCurrentText(self.master.deelnemers.loc[self.master.deelnemers[self.master.deelnemers.Barcode == self.barcode.text()].index, 'Tent'].values[0])
        '''
        if len(self.master.deelnemers.Naam.loc[self.master.deelnemers.Barcode == self.barcode.text()]) > 0:
            self.name.setCurrentText(self.master.deelnemers.Naam.loc[self.master.deelnemers.Barcode == self.barcode.text()].values[0])
        if len(self.master.deelnemers.Tent.loc[self.master.deelnemers.Barcode == self.barcode.text()]) > 0:
            self.tent.setCurrentText(self.master.deelnemers.Tent.loc[self.master.deelnemers.Barcode == self.barcode.text()])
        '''


    def rst(self):
        self.barcode.clear()

    def ret(self):
        self.close()

    def conf(self):
        self.master.deelnemers.at[self.master.deelnemers[(self.master.deelnemers.Barcode == self.barcode.text()) | (self.master.deelnemers.Naam == self.name.currentText())].index, 'Tent'] = self.tent.currentText()

        self.barcode.clear()

        self.master.deelnemers.sort_values(by='Tent', inplace=True)
        self.master.deelnemers.reset_index(drop=True, inplace=True)

