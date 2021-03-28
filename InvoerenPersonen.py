import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None

import sys
import os

import PyQt5
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QComboBox

class InvoerenPersonen(QWidget):
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

        # Functie
        self.functie_label = QLabel(self, text='Functie')
        self.functie = QComboBox(self)
        for f in ['Deelnemer', 'Hoofdleiding', 'Kok', 'Adjudant', 'Sportknots', 
                    'Tentchef', 'Joker', 'DS']:
            self.functie.addItem(f)
        self.functie.setCurrentText('Deelnemer')
        self.layout.addWidget(self.functie_label, 2, 0)
        self.layout.addWidget(self.functie, 2,1)

        # Terug
        self.terug = QPushButton(self, text='Keer terug')
        self.terug.pressed.connect(self.kt)
        self.layout.addWidget(self.terug, 3,0)

        self.bevestigen = QPushButton(self, text='Bevestigen')
        self.bevestigen.pressed.connect(self.conf)
        self.layout.addWidget(self.bevestigen, 3,1)
        

    def kt(self):
        self.close()

    def conf(self):
        naam = self.name.text()
        gender = self.gender.currentText()
        functie = self.functie.currentText()

        s = pd.Series([naam, gender, functie, '', ''], index=['Naam', 'Geslacht', 'Functie', 'Tent', 'Barcode'])

        self.master.personen = self.master.personen.append(s, ignore_index=True)

        self.name.clear()
