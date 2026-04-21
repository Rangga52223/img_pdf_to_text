import logging
class CustomLogger:
    def __init__(self, name="OCR_App"):
        # Setup dasar
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger(name)

    # Buat fungsi untuk masing-masing level
    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, show_traceback=True):
        self.logger.error(message, exc_info=show_traceback)

    def critical(self, message):
        self.logger.critical(message)

# Inisialisasi Class (lakukan ini di luar fungsi agar jadi Singleton)
app_logger = CustomLogger()