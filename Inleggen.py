from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QGridLayout,
)
import sys

import StandaardFuncties


class Inleggen(QWidget):
    def __init__(self, master):
        self.master = master
        QWidget.__init__(self)

        self.layout = QGridLayout(self)

        # dataframes ophalen
        self.inleg_df = self.master.inleg
        self.personen_df = self.master.personen

        # Barcode
        self.bc_label = QLabel(self, text="Barcode")
        self.bc = QLineEdit(self)
        self.bc.returnPressed.connect(self.scanned)

        self.layout.addWidget(self.bc_label, 0, 0)
        self.layout.addWidget(self.bc, 0, 1)

        # Inleg
        self.inleg_label = QLabel(self, text="Inleg")
        self.inleg = QLineEdit(self)
        self.inleg.returnPressed.connect(self.ingevoerd)

        self.layout.addWidget(self.inleg_label, 1, 0)
        self.layout.addWidget(self.inleg, 1, 1)

        self.ret = QPushButton(self, text="Keer terug")
        self.ret.clicked.connect(self.keer_terug)
        self.conf = QPushButton(self, text="Bevestigen")
        self.conf.clicked.connect(self.ingevoerd)

        self.layout.addWidget(self.ret, 2, 0)
        self.layout.addWidget(self.conf, 2, 1)

    def scanned(self):
        self.inleg.setFocus()

    def ingevoerd(self):
        cur_inleg = float(self.inleg.text())

        if self.bc.text() not in self.personen_df["Barcode"].unique():
            StandaardFuncties.warning(self, "Barcode niet gevonden!", "Fout")
        else:
            # inleg ophogen
            if self.bc.text() in self.inleg_df["Barcode"].unique():
                # TODO: melding met knoppen: ophogen, vervangen
                persoon_filter = self.inleg_df["Barcode"] == self.bc.text()
                self.inleg_df.loc[persoon_filter, "InlegOrigineel"] += cur_inleg
                self.inleg_df.loc[persoon_filter, "InlegHuidig"] += cur_inleg
            # inleg toevoegen
            else:
                inleg_dict = {
                    "Barcode": self.bc.text(),
                    "InlegOrigineel": cur_inleg,
                    "InlegHuidig": cur_inleg,
                }
                self.inleg_df = self.inleg_df.append(inleg_dict, ignore_index=True)

            self.master.inleg = self.inleg_df
            print(self.inleg_df)
        self.bc.clear()
        self.inleg.clear()
        self.bc.setFocus()

    def keer_terug(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = Inleggen(None)
    s.show()
    sys.exit(app.exec_())
