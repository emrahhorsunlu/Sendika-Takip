import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem
from sendika_takip_ui import Ui_MainWindow
from sendika_ekle import Ui_SendikaEkle
from uye_ekle import Ui_UyeEkle
from uye_liste import Ui_UyeListe
import mysql.connector

class SendikaEkle(QDialog, Ui_SendikaEkle):
    def __init__(self):
        super(SendikaEkle, self).__init__()
        self.setupUi(self)
        self.kaydetButton.clicked.connect(self.kaydet)
        self.iptalButton.clicked.connect(self.reject)
        
    def kaydet(self):  # Line edit'teki bilgileri alarak veritabanına kaydeden metod
        adi = self.sendikaAdiLineEdit.text()
        kodu = self.sendikaKoduLineEdit.text()
        baskani = self.sendikaBaskaniLineEdit.text()
        kurulus_tarihi = self.kurulusTarihiDateEdit.date().toPyDate()
        uye_sayisi =0
        if adi and kodu:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="emrah12345",
                database="sendika_db",
                auth_plugin='mysql_native_password'
            )
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO sendikalar (adi, kodu, baskani, kurulus_tarihi, uye_sayisi) VALUES (%s, %s, %s, %s, %s)",
                (adi, kodu, baskani, kurulus_tarihi, uye_sayisi)
            )
            self.conn.commit()
            QMessageBox.warning(self, "Uyarı", "Başarıyla Eklenmiştir.")
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Sendika adı ve kodu boş olamaz")

class UyeEkle(QDialog, Ui_UyeEkle):
    def __init__(self, sendika_id):
        super(UyeEkle, self).__init__()
        self.setupUi(self)
        self.sendika_id = sendika_id
        self.kaydetButton.clicked.connect(self.kaydet)
        self.iptalButton.clicked.connect(self.reject)

    def kaydet(self):  # Line edit'teki bilgileri alarak veritabanına kaydeden metod
        adi = self.uyeAdiLineEdit.text()
        yasi = self.uyeYasiSpinBox.value()
        meslegi = self.uyeMeslegiLineEdit.text()

        if adi and meslegi:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="emrah12345",
                database="sendika_db",
                auth_plugin='mysql_native_password'
            )
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO uyeler (sendika_id, adi, yasi, meslegi) VALUES (%s, %s, %s, %s)",
                (self.sendika_id, adi, yasi, meslegi)
            )
            self.conn.commit()

            # Üye eklendiğinde sendikadaki üye sayısını güncelle
            cursor.execute("SELECT COUNT(*) FROM uyeler WHERE sendika_id = %s", (self.sendika_id,))
            uye_sayisi = cursor.fetchone()[0]

            # Sendikadaki üye sayısını güncelle
            cursor.execute(
                "UPDATE sendikalar SET uye_sayisi = %s WHERE id = %s",
                (uye_sayisi, self.sendika_id)
            )
            self.conn.commit()

            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Üye adı ve mesleği boş olamaz")

class UyeListe(QDialog, Ui_UyeListe):
    def __init__(self, sendika_id):
        super(UyeListe, self).__init__()
        self.setupUi(self)
        self.sendika_id = sendika_id

        # MySQL bağlantısı
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emrah12345",
            database="sendika_db",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.conn.cursor()

        # Butonları Bağladığım Kısım
        self.ekleButton.clicked.connect(self.uyeEkle)
        self.silButton.clicked.connect(self.uyeSil)

        # Üyeleri listeleme
        self.uyeListele()

    def uyeListele(self):  # Üyeleri listelemek için metod
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emrah12345",
            database="sendika_db",
            auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        
        try:
            mycursor.execute("SELECT id, adi, yasi, meslegi FROM uyeler WHERE sendika_id = %s", (self.sendika_id,))
            rows = mycursor.fetchall()
            self.uyeListeView.setRowCount(len(rows))
            self.uyeListeView.setColumnCount(4)
            self.uyeListeView.setHorizontalHeaderLabels(["ID", "Adı", "Yaşı", "Mesleği"])

            for rowIndex, row in enumerate(rows):
                for colIndex, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.uyeListeView.setItem(rowIndex, colIndex, item)
        except Exception as e:
            print(f"Hata: {str(e)}")

    def uyeEkle(self):  # Üye ekleme dialogunu açan metod
        dialog = UyeEkle(self.sendika_id)
        if dialog.exec_() == QDialog.Accepted:
            self.uyeListele()

    def uyeSil(self):  # Seçili üyeyi silen metod
        selected_row = self.uyeListeView.currentRow()
        if selected_row != -1:
            uye_id_item = self.uyeListeView.item(selected_row, 0)
            uye_id = int(uye_id_item.text())

            self.cursor.execute("DELETE FROM uyeler WHERE id = %s", (uye_id,))
            self.conn.commit()
            self.uyeListele()
            QMessageBox.warning(self, "Uyarı", "Üye başarıyla silindi")
        else:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir üye seçin")

    def yenile(self):  # Kayıtlardan sonra üye listesini yenileyen metod
        self.uyeListele()

class SendikaTakip(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SendikaTakip, self).__init__()
        self.setupUi(self)

        # MySQL bağlantısı
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emrah12345",
            database="sendika_db",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.conn.cursor()

        # Butonları Bağladığım Kısım
        self.ekleButton.clicked.connect(self.sendikaEkle)
        self.silButton.clicked.connect(self.sil)
        self.araButton.clicked.connect(self.ara)
        self.yenileButton.clicked.connect(self.tabloyuGuncelle)
        self.tableWidget.cellDoubleClicked.connect(self.uyeListeAc)

        # Tabloyu güncelleme
        self.tabloyuGuncelle()

    def tabloyuGuncelle(self):  # Tabloyu güncelleyen metod
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="emrah12345",
            database="sendika_db",
            auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        
        try:
            mycursor.execute("SELECT * FROM sendikalar")
            rows = mycursor.fetchall()
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Adı", "Kodu", "Başkanı", "Kuruluş Tarihi", "Üye Sayısı"])

            for rowIndex, row in enumerate(rows):
                for colIndex, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(rowIndex, colIndex, item)
        except Exception as e:
            print(f"Hata: {str(e)}")

    def sendikaEkle(self):  # Sendika ekleme dialogunu açan metod
        dialog = SendikaEkle()
        if dialog.exec_() == QDialog.Accepted:
            self.tabloyuGuncelle()

    def uyeListeAc(self, row, column):  # Üye listesi penceresini açan metod
        sendika_id_item = self.tableWidget.item(row, 0)
        sendika_id = int(sendika_id_item.text())
        self.uyeListeDialog = UyeListe(sendika_id)
        self.uyeListeDialog.exec_()

    def sil(self):  # Seçili sendikayı silen metod
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            sendika_id_item = self.tableWidget.item(selected_row, 0)
            sendika_id = int(sendika_id_item.text())

            self.cursor.execute("DELETE FROM sendikalar WHERE id = %s", (sendika_id,))
            self.conn.commit()
            self.tabloyuGuncelle()
            QMessageBox.warning(self, "Uyarı", "Sendika başarıyla silindi")
        else:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir sendika seçin")

    def ara(self):  # Arama yapılan kriterlere göre tabloyu güncelleyen metod
        arama_kriteri = self.sendikaAdiLineEdit.text()
        if arama_kriteri:
            query = "SELECT * FROM sendikalar WHERE adi LIKE %s"
            self.cursor.execute(query, ('%' + arama_kriteri + '%',))
            rows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Adı", "Kodu", "Başkanı", "Kuruluş Tarihi", "Üye Sayısı"])
            for rowIndex, row in enumerate(rows):
                for colIndex, col in enumerate(row):
                    self.tableWidget.setItem(rowIndex, colIndex, QTableWidgetItem(str(col)))
        else:
            self.tabloyuGuncelle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SendikaTakip()
    window.show()
    sys.exit(app.exec_())
