from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UyeListe(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.uyeListeView = QtWidgets.QTableWidget(Dialog)
        self.uyeListeView.setObjectName("uyeListeView")
        self.uyeListeView.setColumnCount(4)
        self.uyeListeView.setHorizontalHeaderLabels(["ID", "Adı", "Yaşı", "Mesleği"])
        self.uyeListeView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.uyeListeView.setSelectionMode(QtWidgets.QTableView.SingleSelection)

        self.verticalLayout.addWidget(self.uyeListeView)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.ekleButton = QtWidgets.QPushButton(Dialog)
        self.ekleButton.setObjectName("ekleButton")
        self.horizontalLayout.addWidget(self.ekleButton)

        self.silButton = QtWidgets.QPushButton(Dialog)
        self.silButton.setObjectName("silButton")
        self.horizontalLayout.addWidget(self.silButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Üye Listesi"))
        self.ekleButton.setText(_translate("Dialog", "Ekle"))
        self.silButton.setText(_translate("Dialog", "Sil"))
