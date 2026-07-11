import sys
import glob
import random

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QUrl

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QProgressBar
)

from worker import Worker

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR APAR Generator")
        self.resize(700, 500)

        self.init_ui()
        self.init_images()
        self.init_audio()

    def init_images(self):
        self.gambar1 = self.add_image(
            "gambar/polines.png",
            600,
            5,
            70,
            70
        )
        # jarak gambar1 dari tepi kanan window, dipakai saat resize
        self.margin_kanan_gambar1 = 30
        self.gambar2 = self.add_image(
            "logo_ehs.png",
            10,
            5,
            120,
            120
        )
        # gambar2 tetap menempel di kiri atas
        self.reposisi_gambar()


    def add_image(self, path, x, y, w, h):
        label = QLabel(self)
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(
            w,
            h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        label.setPixmap(pixmap)
        label.resize(pixmap.size())
        label.move(x, y)
        return label

    # Reposisi Gambar (mengikuti ukuran widget)
    #__________________________________________
    def reposisi_gambar(self):
        # gambar1 selalu menempel di kanan atas, mengikuti lebar window
        x_baru = self.width() - self.gambar1.width() - self.margin_kanan_gambar1
        self.gambar1.move(x_baru, 5)
        # gambar2 tetap di kiri atas
        self.gambar2.move(10, 5)

    def resizeEvent(self, event):
        self.reposisi_gambar()
        super().resizeEvent(event)
 
    # Audio Notifikasi Selesai (random, bergantian)
    #__________________________________________
    def init_audio(self):

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        # kumpulkan semua file mp3 di folder sound/
        # letakkan mp3
        # Nanti diputar random
        self.daftar_suara_selesai = sorted(
            glob.glob("sound/*.mp3")
        )

        # supaya mp3 yang sama tidak langsung terulang di giliran berikutnya
        self.suara_terakhir = None

    def putar_suara_selesai(self):
        if not self.daftar_suara_selesai:
            return

        pilihan = self.daftar_suara_selesai
        # kalau ada lebih dari 1 file, hindari memilih file yang sama
        # dengan yang baru saja diputar
        if len(pilihan) > 1 and self.suara_terakhir in pilihan:
            pilihan = [
                f for f in pilihan
                if f != self.suara_terakhir
            ]

        file_terpilih = random.choice(pilihan)
        self.suara_terakhir = file_terpilih

        self.player.stop()
        self.player.setSource(
            QUrl.fromLocalFile(file_terpilih)
        )
        self.player.play()

    def init_ui(self):
        main_layout = QVBoxLayout()

        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        
        # Judul
        ##################################################
        judul = QLabel("QR Generator V1.2\nBy Mahasiswa PKL Polinice")
        judul.setAlignment(Qt.AlignCenter)
        judul.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        main_layout.addWidget(judul)

        # File Excel
        ##################################################
        label_excel = QLabel("File Excel")

        self.txt_excel = QLineEdit()
        self.txt_excel.setPlaceholderText("Pilih file Excel...")
        self.btn_excel = QPushButton("Browse")

        layout_excel = QHBoxLayout()
        layout_excel.addWidget(self.txt_excel)
        layout_excel.addWidget(self.btn_excel)

        main_layout.addWidget(label_excel)
        main_layout.addLayout(layout_excel)

        # Logo
        ##################################################

        label_logo = QLabel("Logo")

        self.txt_logo = QLineEdit()
        self.txt_logo.setPlaceholderText("Pilih logo...")
        self.btn_logo = QPushButton("Browse")

        layout_logo = QHBoxLayout()
        layout_logo.addWidget(self.txt_logo)
        layout_logo.addWidget(self.btn_logo)

        main_layout.addWidget(label_logo)
        main_layout.addLayout(layout_logo)

        # Folder Output
        ##################################################
        label_output = QLabel("Folder Output")

        self.txt_output = QLineEdit()
        self.txt_output.setPlaceholderText("Pilih folder output...")
        self.btn_output = QPushButton("Browse")

        layout_output = QHBoxLayout()
        layout_output.addWidget(self.txt_output)
        layout_output.addWidget(self.btn_output)

        main_layout.addWidget(label_output)
        main_layout.addLayout(layout_output)

        # Nama File Output
        ##################################################
        label_file = QLabel("Nama File Output")

        self.txt_file = QLineEdit()
        self.txt_file.setText("ubah_nama_sesuai_keinginan.xlsx")

        main_layout.addWidget(label_file)
        main_layout.addWidget(self.txt_file)

        # Base URL
        ##################################################
        label_url = QLabel("Base URL")

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(
            "Masukkan Base URL Microsoft Form..."
        )

        layout_url = QHBoxLayout()
        layout_url.addWidget(
            self.txt_url
        )

        main_layout.addWidget(label_url)
        main_layout.addLayout(layout_url)

        # Progress
        ##################################################
        label_progress = QLabel("Progress")

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        main_layout.addWidget(label_progress)
        main_layout.addWidget(self.progress)

        # Status
        ##################################################
        self.lbl_status = QLabel("Siap.")
        main_layout.addWidget(self.lbl_status)
        self.lbl_count = QLabel("0 / 0 QR")
        main_layout.addWidget(self.lbl_count)

        # Tombol Generate
        ##################################################
        self.btn_generate = QPushButton("Generate QR")
        self.btn_generate.setMinimumHeight(45)
        main_layout.addWidget(self.btn_generate)

        # SIGNAL
        ##################################################
        self.btn_excel.clicked.connect(self.browse_excel)
        self.btn_logo.clicked.connect(self.browse_logo)
        self.btn_output.clicked.connect(self.browse_output)
        self.btn_generate.clicked.connect(self.generate)
        ##################################################

        self.setLayout(main_layout)

        self.setStyleSheet("""
        QWidget {
            background-color: white;
            color: black;
            font-size: 10pt;
        }

        QLineEdit {
            background-color: white;
            color: black;
            border: 1px solid gray;
            padding: 4px;
        }

        QPushButton {
            background-color: #1976D2;
            color: white;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #1565C0;
        }

        QLabel {
            color: black;
        }
        """)

    
    # Fungsi Browse Excel
    #__________________________________________

    def browse_excel(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_name:
            self.txt_excel.setText(file_name)

   
    # Fungsi Browse Logo
    #__________________________________________

    def browse_logo(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih Logo",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if file_name:
            self.txt_logo.setText(file_name)

    # Fungsi Browse Folder
    #__________________________________________

    def browse_output(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Pilih Folder Output"
        )

        if folder:
            self.txt_output.setText(folder)

    def generate(self):
        # reset progress
        self.progress.setValue(0)
        excel = self.txt_excel.text()
        logo = self.txt_logo.text()
        folder = self.txt_output.text()
        output = self.txt_file.text()
        base_url = self.txt_url.text()


        self.worker = Worker(
            excel,
            logo,
            folder,
            output,
            base_url
        )


        self.worker.progress.connect(
            self.progress.setValue
        )

        self.worker.count.connect(
            self.lbl_count.setText
        )

        self.worker.selesai.connect(
            self.proses_selesai
        )

        self.worker.error.connect(
            self.tampil_error
        )

        self.worker.start()
        
    def update_progress(self, value):
        self.progress.setValue(value)

    def update_status(self, text):
        self.label_status.setText(text)
    
    def proses_selesai(self, hasil):

        hasil_tampil = hasil.replace("\\", "/")

        self.lbl_status.setText(
            f"Selesai\nFile: {hasil_tampil}"
        )

        self.putar_suara_selesai()

        QTimer.singleShot(
            0,
            lambda: self.progress.setValue(0)
        )


    def tampil_error(self, pesan):

        self.lbl_status.setText(
            "Error : " + pesan
        )
    

# Main Program
#__________________________________________

app = QApplication(sys.argv)

window = MainWindow()

window.show()    

sys.exit(app.exec())