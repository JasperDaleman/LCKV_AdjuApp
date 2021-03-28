import pandas as pd
import sys
import os

import PyQt5
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QMessageBox, QLineEdit, QGridLayout, QInputDialog

from InlegEnTentindeling import InlegEnTentindeling


class PersoonToevoegen(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout()
        
        # Naam
        self.name_label = QLabel(self, text='Naam')
        self.name = QLineEdit(self)
        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name, 0, 1)
        
        # Geslacht
        self.combGesl = QComboBox(self)
        for s in self.master.master.geslachten:
            self.combGesl.addItem(s)
        self.gesl_label = QLabel(self, text='Geslacht')
        self.layout.addWidget(self.gesl_label, 1, 0)
        self.layout.addWidget(self.combGesl, 1, 1)
        
        # Functie
        self.combFunc = QComboBox(self)
        for s in self.master.master.functies:
            self.combFunc.addItem(s)
        self.func_label = QLabel(self, text='Functie')
        self.layout.addWidget(self.func_label, 2, 0)
        self.layout.addWidget(self.combFunc, 2,1)

        # Tent
        self.combTent = QComboBox(self)
        for s in self.master.master.tenten:
            self.combTent.addItem(s)
        self.tent_label = QLabel(self, text='Tent')
        self.layout.addWidget(self.tent_label, 3, 0)
        self.layout.addWidget(self.combTent, 3,1)

        # Barcode
        self.bc_label = QLabel(self, text='Barcode bonuskaart')
        self.bc = QLineEdit(self)
        self.layout.addWidget(self.bc_label, 4,0)
        self.layout.addWidget(self.bc, 4,1)
        self.bc.returnPressed.connect(self.conf)
        
        # Buttons
        self.ret = QPushButton(self, text='Keer terug')
        self.ret.pressed.connect(self.kt)
        self.layout.addWidget(self.ret, 5,0)

        self.bev = QPushButton(self, text='Bevestigen')
        self.bev.pressed.connect(self.conf)
        self.layout.addWidget(self.bev, 5,1)
        
        self.setLayout(self.layout)
    
    def conf(self):
        name = self.name.text()
        gesl = self.combGesl.currentText()
        func = self.combFunc.currentText()
        tent = self.combTent.currentText()
        bc = self.bc.text()

        s = pd.Series([name, gesl, func, tent, bc], 
                       index=self.master.master.personen.columns)

        try:
            self.master.master.personen = self.master.master.personen.append(s, ignore_index=True)
            
            msgBox = QMessageBox()
            msgBox.setText('Wil je meteen een bedrag invoeren als inleg?')
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setWindowTitle('Meteen geld inleggen?')
            retval = msgBox.exec_()
            if retval == QMessageBox.Yes:
                # Pop up screen voor inleg
                inleg, ok = QInputDialog.getText(self, 'Inleg', 'Geef inleg: ')
                if ok: 
                    inleg = inleg.replace(',', '.')
                    try: 
                        inleg = float(inleg)
                        s2 = pd.Series([bc, inleg], index=self.master.master.inleg.columns)
                        try: 
                            self.master.master.inleg = self.master.master.inleg.append(s2, ignore_index=True)
                        except (IndexError, ValueError):
                            print('FOUT')
                        
                    except ValueError: 
                        print('Geen goede waarde ingevoerd, voer later opnieuw in') 

            else:
                msgBox = QMessageBox()
                msgBox.setText('Persoon toegevoegd')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setWindowTitle('Success')
                msgBox.exec_()

            self.name.clear()
            self.bc.clear()
            self.name.setFocus()



        except IndexError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Fout in gegevens, opnieuw invoeren')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            print('Verkeerde waarde ingevoerd')

    def kt(self):
        self.master.change_screens('PersonenWijzigen')

