import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QComboBox

import sys
import os
import pandas as pd


class InvoerenDeelnemers(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)
        
        # Naam
        self.name_label = QLabel(self, text='Naam')
        self.name = QLineEdit(self)
        self.name.returnPressed.connect(self.conf)
        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name, 0, 1)
        
        # Geslacht
        self.gender_label = QLabel(self, text='Geslacht')
        self.gender = QComboBox(self)
        for mv in ['Man', 'Vrouw']:
            self.gender.addItem(mv)
        self.layout.addWidget(self.gender_label, 1, 0)
        self.layout.addWidget(self.gender, 1, 1)

        # Tent
        self.tent_label = QLabel(self, text='Tent')
        self.tent = QComboBox(self)
        for t in range(1, 7):
            self.tent.addItem('Tent {}'.format(t))
        self.layout.addWidget(self.tent_label, 2, 0)
        self.layout.addWidget(self.tent, 2, 1)


        # Buttons
        self.confirm = QPushButton(self, text='Bevestigen')
        self.confirm.pressed.connect(self.conf)
        self.layout.addWidget(self.confirm, 3, 1)

        self.kt = QPushButton(self, text='Keer terug')
        self.kt.pressed.connect(self.ret)
        self.layout.addWidget(self.kt, 3, 0)
        
        self.name.setFocus()
        self.setLayout(self.layout)


    def barcode(self):
        n = [v[0] for v in self.name.text().split(' ')]
        g = self.gender.currentText()[0]
        number = len(self.master.deelnemers)

        self.bc = '{}{}{}'.format(''.join(n), g, number)

        print(self.bc)


    def conf(self):
        self.barcode()

        s = pd.Series(data=[self.name.text(), self.gender.currentText(), self.tent.currentText(), self.bc], 
                      index=['Naam', 'Geslacht', 'Tent', 'Barcode'])
        self.master.deelnemers = self.master.deelnemers.append(s, ignore_index=True, sort=False)

        self.name.clear()

    def ret(self):
        self.close()


