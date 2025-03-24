import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from kasir import Ui_widget
from PIL import Image, ImageDraw, ImageFont

class AplikasiKasir(QWidget, Ui_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.total_harga = 0

        self.pushButton_2.clicked.connect(self.tambah_barang)
        self.pushButton.clicked.connect(self.reset_keranjang)
        self.pushButton_3.clicked.connect(self.simpan_struk)

        self.init_ui()

    def init_ui(self):
        self.comboBox_5.addItems(["Bimoli (Rp. 20,000)", "Indomie (Rp. 3,000)", "Aqua (Rp. 5,000)", "Rokok Gudang Garam Filter (Rp. 25,000)", "Susu Kental Manis (Rp. 10,000)", "Sarden ABC (Rp. 8,000)", "Teh Botol Sosro (Rp. 6,000)", "Sabun Mandi Lifebuoy (Rp. 5,000)"])
        self.comboBox_6.addItems(["0%", "5%", "10%", "15%"])
        self.comboBox_5.setCurrentIndex(-1)
        self.comboBox_6.setCurrentIndex(-1)

    def tambah_barang(self):
        produk = self.comboBox_5.currentText()
        jumlah = self.lineEdit_3.text()
        diskon = self.comboBox_6.currentText()

        if not produk or not jumlah.isdigit() or not diskon:
            QMessageBox.warning(self, "Perhatian", "Lengkapi Semua Data Dengan Benar!")
            return

        jumlah = int(jumlah)
        diskon = int(diskon.replace("%", ""))

        harga_str = produk.split("Rp.")[1].replace(",", "").replace(")", "").strip()
        harga_satuan = int(harga_str)

        harga_setelah_diskon = harga_satuan - (harga_satuan * diskon / 100)
        total_harga_item = harga_setelah_diskon * jumlah

        teks_item = f"{produk} - {jumlah} x Rp. {harga_satuan:,} (Diskon {diskon}%)"
        self.listWidget.addItem(teks_item)

        self.total_harga += total_harga_item
        self.label.setText(f"Total: Rp. {int(self.total_harga):,}")

    def reset_keranjang(self):
        self.listWidget.clear()
        self.total_harga = 0
        self.label.setText("Total: Rp. 0")

    def simpan_struk(self):
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, "Perhatian", "Keranjang Belanja Masih Kosong !")
            return

        struk_teks = ["=== STRUK BELANJA ===", "-" * 110]
        for i in range(self.listWidget.count()):
            struk_teks.append(self.listWidget.item(i).text())
        struk_teks.append("-" * 110)
        struk_teks.append(f"Total: Rp. {int(self.total_harga):,}")

        img_width, img_height = 800, 500 + len(struk_teks) * 40
        gambar = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(gambar)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

        y_pos = 20
        for teks in struk_teks:
            draw.text((20, y_pos), teks, fill="black", font=font)
            y_pos += 40

        gambar.save("struk_belanja.jpg")
        QMessageBox.information(self, "Struk Tersimpan", "Struk berhasil disimpan sebagai 'struk_belanja.jpg'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AplikasiKasir()
    window.show()
    sys.exit(app.exec_())
