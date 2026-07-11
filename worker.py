from PySide6.QtCore import QThread, Signal

from generator import generate_qr


class Worker(QThread):

    # kirim data ke UI
    progress = Signal(int)

    status = Signal(str)

    count = Signal(str)

    selesai = Signal(str)

    error = Signal(str)


    def __init__(
        self,
        excel_file,
        logo_path,
        output_folder,
        output_filename,
        url_template
    ):
        super().__init__()

        self.excel_file = excel_file
        self.logo_path = logo_path
        self.output_folder = output_folder
        self.output_filename = output_filename
        self.url_template = url_template


    def run(self):

        try:

            hasil = generate_qr(
                excel_file=self.excel_file,
                logo_path=self.logo_path,
                output_folder=self.output_folder,
                output_filename=self.output_filename,
                url_template=self.url_template,
                status_callback=self.update_status,
                progress_callback=self.update_progress,
                count_callback=self.update_count
            )


            # kalau selesai
            self.selesai.emit(
                hasil
            )


        except Exception as e:

            self.error.emit(
                str(e)
            )


    def update_status(self, text):

        self.status.emit(
            text
        )


    def update_progress(self, value):

        self.progress.emit(
            value
        )

    def update_count(self, text):

        self.count.emit(text)