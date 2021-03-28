import PyQt5
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

import pandas as pd
import sys




class InzienCashflow(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()

        begr = self.master.master.begroting
        bon = self.master.master.bonnen

        # Overig = Stafpresentje & Fooi pot
        ov = begr.loc['Fooi', 1] + begr.loc['Stafpresentje', 1]

        self.potjes = ['Voeding', 'Vrije besteding', 'Fietsverhuur_Outdoor', 
                  'Brandstof', 'Overig', 'Kantine', 'Statiegeld', 'Stafhap', 'PBs']

        # Totalen berekenen
        bonTot = bon.groupby('Pot').Bedrag.sum()
        print(bonTot)
        

