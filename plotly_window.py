from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QLabel, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from logger import setup_logger

class PlotlyWindow(QMainWindow):
    """
    A QMainWindow subclass that displays a Plotly plot using QWebEngineView.
    """
    file_opened = pyqtSignal(str)

    def __init__(self, raw_html=None):
        """
        Initialize the window with the provided raw HTML.
        """
        super().__init__()
        self.logger = setup_logger()
        self.raw_html = raw_html
        self.file_name = None
        self.initialize_ui()

    def initialize_ui(self):
        """
        Initialize the user interface.
        """
        self.configure_window()
        self.setup_menu()
        self.setup_initial_message_label()

    def setup_initial_message_label(self):
        """
        Set up the initial message.
        """
        label = QLabel("Select video file")
        font = QFont()
        font.setPointSize(20)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def setup_browser(self, raw_html):
        """
        Set up the QWebEngineView.
        """
        self.browser = QWebEngineView()
        self.browser.setHtml(raw_html)
        self.setCentralWidget(self.browser)

    def configure_window(self):
        """
        Configure the window settings.
        """
        self.setWindowTitle('FPS Analyzer')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def setup_menu(self):
        """
        Set up the menu.
        """
        open_file = QAction('Open File', self)
        open_file.triggered.connect(self.open_file_name_dialog)
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction(open_file)

    def open_file_name_dialog(self):
        """
        Open a file dialog and print the selected file path.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if file_name:
            self.logger.info("Selected file: %s", file_name)
            self.file_name = file_name
            self.file_opened.emit(file_name)

    def open_file_open_error_dialog(self, e):
        """
        Open a file open error dialog.
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(f"Failed to open file: {self.file_name}\n"
                             "Check if the file is a video file.")
        error_dialog.setInformativeText(str(e))
        error_dialog.exec_()
