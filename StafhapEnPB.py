import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QWidget, QComboBox, QGridLayout, QPushButton, QLabel, QMessageBox, QRadioButton, QButtonGroup
from PyQt5 import QtGui
# from PyQt5.QtGui import QPainter
# from PyQt5.QtCore import *

from datetime import datetime

import sys
import os
import pandas as pd
import numpy as np

from datetime import datetime

class StafhapEnPB(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        self.bonnr = QLineEdit(self)
        self.bonnr.returnPressed.connect(self.get_bon)
        self.bonnr_label = QLabel(self, text='Bonnummer: ')
        self.layout.addWidget(self.bonnr_label, 0, 0)
        self.layout.addWidget(self.bonnr, 0, 1)

        self.bonomsc = ''
        self.bonomsc_label = QLabel(self, text=self.bonomsc)
        self.layout.addWidget(self.bonomsc_label, 0, 2, 1, 2)

        #TODO: totaal lijn tekenen
        # self.lijn = QPainter(self)
        # self.lijn.setPen(Qt.red)
        # self.lijn.drawLine(10,10,100,140)

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
        # print(self.stafleden)

        self.countStaf = self.stafleden.count()
        self.aantal_label = QLabel(self, text=str(self.countStaf))
        self.aantal_txt_label = QLabel(self, text='Aantal: ')
        self.layout.addWidget(self.aantal_txt_label, 1, 4)
        self.layout.addWidget(self.aantal_label, 1, 5)

        self.bedrag = 0
        self.bedrag_label = QLabel(self, text='€' + str(self.bedrag))
        self.totaal_label = QLabel(self, text='Totaal: ')
        self.layout.addWidget(self.totaal_label, 10, 1)
        self.layout.addWidget(self.bedrag_label, 10, 2)

        self.bedragpp = 0
        self.bedragpp_label = QLabel(self, text='€' + str(self.bedragpp))
        self.pp_label = QLabel(self, text='Per persoon: ')
        self.layout.addWidget(self.pp_label, 10, 3)
        self.layout.addWidget(self.bedragpp_label, 10, 4)

        self.bevestig = QPushButton(self, text='Bevestig')
        self.bevestig.clicked.connect(self.bevestig_stafhap_pb)
        self.layout.addWidget(self.bevestig, 10, 5)

        self.inzien = QPushButton(self, text='Inzien')
        self.inzien.clicked.connect(self.inzien_stafhap_pb)
        self.layout.addWidget(self.inzien, 9, 5)

        self.keer_terug = QPushButton(self, text='Keer terug')
        self.keer_terug.clicked.connect(self.kt)
        self.layout.addWidget(self.keer_terug, 10, 0)

        self.staf_toevoegen()

        self.stafledenDF = pd.DataFrame(columns=['Deelname','Radiobutton'])
        self.stafledenDF = self.stafledenDF.assign(Naam=self.stafleden)

        radio_count = 0 
        for idx, row in self.stafledenDF.iterrows():
             self.stafledenDF.loc[idx,'Deelname'] = True
             self.stafledenDF.loc[idx,'Radiobutton'] = radio_count
             radio_count += 1

        # print(self.stafledenDF)

    def staf_toevoegen(self):
        self.staf_label = list()
        self.radiobtn_group = list(range(self.countStaf))
        self.radiobtn_yes = list(range(self.countStaf))
        self.radiobtn_no = list(range(self.countStaf))

        for i in range(self.countStaf):
            self.staf_label += [QLabel(str(i), self, text=self.stafleden.iloc[i])]

            self.radiobtn_yes[i] = QRadioButton("Ja")
            self.radiobtn_no[i] = QRadioButton("Nee")

            self.radiobtn_group[i] = QButtonGroup()
            self.radiobtn_group[i].addButton(self.radiobtn_yes[i], 1)
            self.radiobtn_group[i].addButton(self.radiobtn_no[i], 1)

            self.radiobtn_yes[i].setChecked(True)
            self.radiobtn_yes[i].yesno = "Yes"
            self.radiobtn_no[i].yesno = "No"

            #https://stackoverflow.com/questions/4578861/connecting-slots-and-signals-in-pyqt4-in-a-loop
            self.radiobtn_yes[i].toggled.connect(lambda i=i, btn_idx=i: self.onclick(self.radiobtn_yes[i],btn_idx))
            self.radiobtn_no[i].toggled.connect(lambda i=i, btn_idx=i: self.onclick(self.radiobtn_no[i],btn_idx))

            if i < 8:
                self.layout.addWidget(self.staf_label[i], i+2, 0)
                self.layout.addWidget(self.radiobtn_yes[i], i+2, 1)
                self.layout.addWidget(self.radiobtn_no[i], i+2, 2)
            else:
                self.layout.addWidget(self.staf_label[i], i-6, 3)
                self.layout.addWidget(self.radiobtn_yes[i], i-6, 4)
                self.layout.addWidget(self.radiobtn_no[i], i-6, 5)

            # bold=QtGui.QFont()
            # bold.setBold(True)
            # staf00_label.setFont(bold)

    def get_bon(self):
        print(self.master.master.bonnen)

        #check of bon bestaat
        if int(self.bonnr.text()) in self.master.master.bonnen.index:
            #als bon bestaat, dan kijken of die al verdeeld is
            self.bonomsc = self.master.master.bonnen.loc[float(self.bonnr.text()), 'Omschrijving']
            if self.master.master.stafhapPB.Bonnummer.astype(str).str.contains(self.bonnr.text()).any():
                msgYesNo = QMessageBox()
                msgYesNo.setIcon(QMessageBox.Information)
                msgYesNo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msgYesNo.setText("Bon " + self.bonnr.text() + " \'" + self.bonomsc + "\' is al verdeeld. Opnieuw verdelen?")
                msgYesNo.setWindowTitle("Opnieuw verdelen")

                retval = msgYesNo.exec_()

                #Bij oppnieuw verdelen, eerst de oude waardes verwijderen
                if retval == QMessageBox.Yes:
                   self.fill_widgets()
            else:
                self.fill_widgets()    
                
        else:
            self.msgWarn = QMessageBox()
            self.msgWarn.setIcon(QMessageBox.Warning)
            self.msgWarn.setStandardButtons(QMessageBox.Ok)
            self.msgWarn.setText("Bonnummer bestaat niet. Probeer een ander.")
            self.msgWarn.setWindowTitle("Bon niet gevonden")
            self.msgWarn.show()

        # print(self.master.master.bonnen.iloc[self.master.master.bonnen.iloc[:,0] == self.bonnr])

    def fill_widgets(self):
        self.bonomsc_label.setText(self.bonomsc)

        self.bondate = datetime.strptime(self.master.master.bonnen.loc[float(self.bonnr.text()), 'Datum'], '%d-%m-%Y')
        bonday = self.bondate.day
        bonmonth = self.bondate.month
        bonyear = self.bondate.year

        self.date_day.setCurrentIndex(int(bonday)-1)
        self.date_month.setCurrentIndex(int(bonmonth)-1)
        self.date_year.setText(str(bonyear))

        self.bedrag = self.master.master.bonnen.loc[float(self.bonnr.text()), 'Bedrag']
        self.bedrag_label.setText('€ ' + str(self.bedrag))

        self.bedragpp = round(self.bedrag / self.countStaf,2)
        self.bedragpp_label.setText('€' + str(self.bedragpp))

    def bevestig_stafhap_pb(self):
        #Bonnummer   Datum   PersoonID  Naam    Bedrag
        self.cur_bonnr = self.bonnr.text()
        msgOk = QMessageBox()
        msgOk.setIcon(QMessageBox.Warning)
        msgOk.setStandardButtons(QMessageBox.Ok)

        #check of er iets te verdelen valt.
        if self.bedragpp == 0:
            msgOk.setText("Het te verdelen bedrag is € 0,00. Wijs de bon aan één of meerdere stafleden toe.")
            msgOk.setWindowTitle("Geen bedrag")
            msgOk.exec_()

        #check of alle stafleden van deze bon inleg hebben.
        elif self.checkInleg():
            msgOk.setText(self.persZonderInleg + " heeft geen inleg. Voeg deze eerst toe.")
            msgOk.setWindowTitle("Geen inleg")
            msgOk.exec_()

        #Opnieuw verdelen?
        elif self.master.master.stafhapPB.Bonnummer.astype(str).str.contains(self.cur_bonnr).any():
                bonomsc = self.master.master.bonnen.loc[float(self.cur_bonnr), 'Omschrijving']

                msgYesNo = QMessageBox()
                msgYesNo.setIcon(QMessageBox.Information)
                msgYesNo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msgYesNo.setText("Je gaat de bon opnieuw verdelen. De oude verdeling wordt verwijderd. Doorgaan?")
                msgYesNo.setWindowTitle("Opnieuw verdelen")

                retval = msgYesNo.exec_()

                #Bij oppnieuw verdelen, eerst de oude waardes verwijderen
                if retval == QMessageBox.Yes:
                    self.master.master.stafhapPB = self.master.master.stafhapPB[self.master.master.stafhapPB['Bonnummer'] != int(self.bonnr.text())]
                    self.verdeel_bon()
        else:
            self.verdeel_bon()

    def verdeel_bon(self):
        cur_day = self.date_day.currentText()
        cur_month = self.date_month.currentText()
        cur_year = self.date_year.text()
        cur_date = cur_day + '-' + cur_month + '-' + cur_year

        if self.pb_radiobtn.isChecked() == True:
            typeBon = 'PB'
        else:
            typeBon = 'Stafhap'

        for idx, row in self.stafledenDF.loc[self.stafledenDF['Deelname'] == True].iterrows():
            cur_persoonID = idx
            cur_naam = self.stafledenDF.loc[idx,'Naam']
            serie = pd.Series([typeBon, self.cur_bonnr, cur_date, cur_persoonID, cur_naam, self.bedragpp], index=self.master.master.stafhapPB.columns)
            self.master.master.stafhapPB = self.master.master.stafhapPB.append(serie, ignore_index=True, sort=False)
            cur_inleg = self.master.master.inleg.loc[self.master.master.inleg['PersoonID'] == cur_persoonID, 'InlegHuidig']
            self.master.master.inleg.loc[self.master.master.inleg['PersoonID'] == cur_persoonID, 'InlegHuidig'] = cur_inleg - self.bedragpp

        msgOk = QMessageBox()
        msgOk.setIcon(QMessageBox.Information)
        msgOk.setStandardButtons(QMessageBox.Ok)
        msgOk.setText("Goed gedaan! Je hebt bon " + self.bonnr.text() + " ter waarde van €" + str(self.bedrag) + " over " + str(self.countStaf) + " stafleden verdeeld.")
        msgOk.setWindowTitle("Gelukt!")
        msgOk.exec_()

        self.bonnr.clear()
        self.bedrag = 0
        self.bedragpp = 0
        self.bedrag_label.setText('€' + str(self.bedrag))
        self.bedragpp_label.setText('€' + str(self.bedragpp))

    def checkInleg(self):
        for idx, row in self.stafledenDF.loc[self.stafledenDF['Deelname'] == True].iterrows():
            cur_inleg = self.master.master.inleg.loc[self.master.master.inleg['PersoonID'] == idx, 'InlegHuidig']
            
            if len(cur_inleg) == 0:
                self.persZonderInleg = self.stafledenDF.loc[idx,'Naam']
                return True

        return False

    def onclick(self,btn,btn_idx):
        #Bij stafhap alles aan en bij PB alles uit

        if btn.text() == "PB":
            if self.pb_radiobtn.isChecked() == True:
                radio_count = 0
                for idx, row in self.stafledenDF.iterrows():
                    self.stafledenDF.loc[idx,'Deelname'] = False
                    self.radiobtn_no[radio_count].setChecked(True)
                    radio_count += 1
                
        elif btn.text() == "Stafhap":
            if self.stafhap_radiobtn.isChecked() == True:
                radio_count = 0
                for idx, row in self.stafledenDF.iterrows():
                    self.stafledenDF.loc[idx,'Deelname'] = True
                    self.radiobtn_yes[radio_count].setChecked(True)
                    radio_count += 1

        elif btn.text() == "Ja":
            if self.radiobtn_yes[btn_idx].isChecked():
                self.stafledenDF.loc[self.stafledenDF['Radiobutton'] == btn_idx,'Deelname'] = True
                self.countStaf += 1

        elif btn.text() == "Nee":
            if self.radiobtn_no[btn_idx].isChecked():
                self.stafledenDF.loc[self.stafledenDF['Radiobutton'] == btn_idx,'Deelname'] = False
                self.countStaf -= 1   
        
        if self.countStaf == 0:
            self.bedragpp = 0
        else:        
            self.bedragpp = round(self.bedrag / self.countStaf,2)
        
        self.bedragpp_label.setText('€' + str(self.bedragpp))

        self.aantal_label.setText(str(self.countStaf))

        # print(self.stafledenDF)

    def inzien_stafhap_pb(self):
        self.master.change_screens('StafhapEnPBInzien')

        
    def kt(self):
        self.master.change_screens('KampHome')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    screen = StafhapEnPB(None)
    screen.show()
    sys.exit(app.exec_())