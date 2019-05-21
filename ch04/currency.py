# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'currency.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(328, 148)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.dateLabel = QtWidgets.QLabel(Dialog)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout.addWidget(self.dateLabel, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(193, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.fromCombo = QtWidgets.QComboBox(Dialog)
        self.fromCombo.setObjectName("fromCombo")
        self.gridLayout.addWidget(self.fromCombo, 1, 0, 1, 1)
        self.amountSpin = QtWidgets.QDoubleSpinBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountSpin.sizePolicy().hasHeightForWidth())
        self.amountSpin.setSizePolicy(sizePolicy)
        self.amountSpin.setMinimum(0.01)
        self.amountSpin.setMaximum(10000000.0)
        self.amountSpin.setProperty("value", 1.0)
        self.amountSpin.setObjectName("amountSpin")
        self.gridLayout.addWidget(self.amountSpin, 1, 1, 1, 1)
        self.toCombo = QtWidgets.QComboBox(Dialog)
        self.toCombo.setObjectName("toCombo")
        self.gridLayout.addWidget(self.toCombo, 2, 0, 1, 1)
        self.resultLabel = QtWidgets.QLabel(Dialog)
        self.resultLabel.setObjectName("resultLabel")
        self.gridLayout.addWidget(self.resultLabel, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        #self.amountSpin.valueChanged['double'].connect(self.resultLabel.setNum)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Currency"))
        self.dateLabel.setText(_translate("Dialog", ""))
        self.resultLabel.setText(_translate("Dialog", "1,00"))

class Window(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        date = self.getdata()
        rates = sorted(self.rates.keys())
        self.ui = Ui_Dialog()
        self. ui.setupUi(self)
        date = self.getdata()
        self.ui.dateLabel.setText(date)
        self.ui.fromCombo.addItems(rates)
        self.ui.toCombo.addItems(rates)


        
        self.ui.amountSpin.valueChanged['double'].connect(self.updateUi)
        self.ui.fromCombo.currentIndexChanged['int'].connect(self.updateUi)
        self.ui.toCombo.currentIndexChanged['int'].connect(self.updateUi)

        self.show()

    def updateUi(self):
        
        to = self.ui.toCombo.currentText()
        from_ = self.ui.fromCombo.currentText()
        amount = (self.rates[from_] / self.rates[to]) * self.ui.amountSpin.value()
        self.ui.resultLabel.setText('{:.2f}'.format(amount).replace(".",","))


    

    def getdata(self): 
        self.rates = {}
            
        try:
            date = "Unknown"
            fh = urlopen("https://www.bportugal.pt/sites/default/files/taxas-relacionados/cambdia_en.csv")
            content = fh.readlines()
            fh.close()
            names = content[7].decode("cp1252") 
            values = content[-2].decode("cp1252") 
            names = names.split(";")
            values = values.split(";")
            date = values[0]
            values = values[1:-1]
            names = [name.split("/")[1].strip() for name in names][1:]
            self.rates = dict(zip(names,values))
            self.rates = dict(filter(lambda entry: entry[1] != '-', self.rates.items()))
            self.rates = { key: float(value) for key, value in  self.rates.items() }
            return "Exchange Rates Date: " + date
        except Exception:
            return "Failed to download:\n%s" % Exception

    
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window= Window()
    sys.exit(app.exec_())

