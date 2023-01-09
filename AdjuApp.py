from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import os
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from MainWindow import MainWindow

#TODO: config file maken

class App(QtWidgets.QApplication):
    def __init__(self, arg):
        QtWidgets.QApplication.__init__(self, arg)

        self.MainWindow = MainWindow(self)
        self.MainWindow.show()

        self.db_setup()

        self.tenten = ['Tent 1', 'Tent 2', 'Tent 3', 'Tent 4', 'Tent 5', 'Tent 6', 'Staf']
        self.geslachten = ['Man', 'Vrouw', 'm/v']
        self.potjes = ['Voeding', 'Vrije besteding', 'Fietsverhuur_Outdoor', 
                  'Brandstof', 'Overig', 'Kantine', 'Statiegeld', 'Stafhap', 'PBs']
        self.functies = ['Deelnemer', 'Adjudant', 'Sportknots', 'Hoofdleiding', 'Kok',
                         'Joker', 'Tentchef']
        self.locaties = ['Diever', 'Chaam', 'Terschelling', 'Bladel', 'Terschelling_geh', 'Haute_Roche', 
                         'Wiltz', 'Lieler', 'Nahin']
    def db_setup(self):
        self.cwd = os.getcwd()
        try:
            self.bonnen = pd.read_csv('{}/data/bonnen.csv'.format(self.cwd), index_col=0, header=0)
        except FileNotFoundError:
            self.bonnen = pd.DataFrame(columns=['Bonnummer', 'Datum', 'Omschrijving', 'Pot', 'Bedrag'])
            self.bonnen.set_index('Bonnummer', inplace=True)

        try:
            self.kantine = pd.read_csv('{}/data/kantine.csv'.format(self.cwd), header=0, index_col=0, dtype=str)
            self.kantine.Prijs = self.kantine.Prijs.astype(float)
            self.kantine.Inhoud = self.kantine.Inhoud.astype(float)
            self.kantine.Suiker = self.kantine.Suiker.astype(float)
            self.kantine.Calorieen = self.kantine.Calorieen.astype(float)
        except FileNotFoundError:
            self.kantine = pd.DataFrame(columns=['Productgroep', 'Productomschrijving', 'Productcode', 'Prijs', 'Inhoud', 'Suiker', 'Calorieen'])

        '''
        try: 
            self.deelnemers_inleg = pd.read_csv('{}/data/deelnemers_inleg.csv'.format(self.cwd), header=0, index_col=0)
        except FileNotFoundError: 
            self.deelnemers_inleg = pd.DataFrame(columns=['Barcode', 'Inleg'])

        try: 
            self.deelnemers = pd.read_csv('{}/data/deelnemers.csv'.format(self.cwd), header=0, index_col=0)
        except FileNotFoundError:
            self.deelnemers = pd.DataFrame(columns=['Naam', 'Geslacht', 'Barcode', 'Tent'])
        '''
        try:
            self.orders = pd.read_csv('{}/data/orders.csv'.format(self.cwd), header=0, index_col=0,
                                      dtype=str)
            self.orders.Aantal = self.orders.Aantal.astype(int)
            self.orders.Bedrag = self.orders.Bedrag.astype(float)
            self.orders.Ordernummer = self.orders.Ordernummer.astype(int)
        except FileNotFoundError:
            self.orders = pd.DataFrame(columns=['Ordernummer', 'DatumTijd', 'Barcode', 'Productcode', 'Product', 'Aantal', 'Bedrag'])
        '''
        try: 
            self.stafleden = pd.read_csv('{}/data/stafleden.csv'.format(self.cwd), header=0, index_col=0)
        except FileNotFoundError:
            self.stafleden = pd.DataFrame(columns=['Naam', 'Geslacht', 'Functie', 'Barcode', 'Inleg'])
        '''

        try: 
            self.personen = pd.read_csv('{}/data/personen.csv'.format(self.cwd), header=0, index_col=0, 
                                        dtype=str)
        except FileNotFoundError:
            self.personen = pd.DataFrame(columns=['Naam', 'Geslacht', 'Functie', 'Tent', 'Barcode'])

        try: 
            self.inleg = pd.read_csv('{}/data/inleg.csv'.format(self.cwd), header=0, index_col=0, 
                    dtype={'Barcode': str,
                           'Inleg': float})
        except FileNotFoundError: 
            self.inleg = pd.DataFrame(columns=['Barcode', 'Inleg'])

        try: 
            self.stafhapPB = pd.read_csv('{}/data/stafhapPB.csv'.format(self.cwd), header=0, index_col=0)
        except FileNotFoundError:
            self.stafhapPB = pd.DataFrame(columns=['Type', 'Bonnummer', 'Datum', 'PersoonID', 'Naam', 'Bedrag'])  
            self.stafhapPB.Bonnummer = self.stafhapPB.Bonnummer.astype(float)
            self.stafhapPB.PersoonID = self.stafhapPB.PersoonID.astype(float)
            self.stafhapPB.Bedrag = self.stafhapPB.Bedrag.astype(float)

        try:
            self.begroting = pd.read_csv('{}/data/begroting.csv'.format(self.cwd), header=None, index_col=0)
        except FileNotFoundError:
            self.begroting = pd.Series(index=['Kampnummer', 'Locatie', 'Voeding', 'Vrije besteding',
                                              'Fietsverhuur_outdoor', 'Fooi', 'Brandstof', 'Stafpresentje'])
            self.begroting.dropna(inplace=True)
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText('Voer de begroting in voordat je verdergaat')
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            


    def close(self):
        self.check_inleg()

        self.bonnen.to_csv('{}/data/bonnen.csv'.format(self.cwd), index='Bonnummer')
        self.kantine.to_csv('{}/data/kantine.csv'.format(self.cwd))
        #self.deelnemers.to_csv('{}/data/deelnemers.csv'.format(self.cwd))
        self.orders.to_csv('{}/data/orders.csv'.format(self.cwd))
        #self.stafleden.to_csv('{}/data/stafleden.csv'.format(self.cwd))
        #self.deelnemers_inleg.to_csv('{}/data/deelnemers_inleg.csv'.format(self.cwd))
        self.personen.sort_values(by=['Tent', 'Functie']).reset_index(drop=True).to_csv('{}/data/personen.csv'.format(self.cwd))
        self.inleg.to_csv('{}/data/inleg.csv'.format(self.cwd))
        self.stafhapPB.to_csv('{}/data/stafhapPB.csv'.format(self.cwd))
        self.begroting.to_csv('{}/data/begroting.csv'.format(self.cwd), header=None)

        QtWidgets.QApplication.quit()
    
    def check_inleg(self):
        over = self.inleg[~self.inleg.PersoonID.isin(self.personen.index)]
        self.msgWarn = QtWidgets.QMessageBox()
        if len(over) > 0:
            for i,row in over.iterrows():
                self.msgWarn.setText(f'{row.PersoonID} is niet toegewezen aan een deelnemer.\nVerwijderen?')
                self.msgWarn.setWindowTitle('Niet toegewezen barcode')
                self.msgWarn.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                self.msgWarn.show()
                retval = self.msgWarn.exec_()
        
                if retval == QtWidgets.QMessageBox.Yes:
                    self.inleg.drop(i, inplace=True)
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText(f'{row.PersoonID} verwijderd')
                    self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msgBox.show()
                    self.msgBox.exec_()

                else:
                    self.msgBox = QtWidgets.QMessageBox()
                    self.msgBox.setText(f'{row.PersoonID} niet verwijderd, zoek uit bij wie deze barcode met inleg hoort.')
                    self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msgBox.show()
                    self.msgBox.exec_()
        
        else: pass
 


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
