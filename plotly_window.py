from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QLabel, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class PlotlyWindow(QMainWindow):
    """
    A QMainWindow subclass that displays a Plotly plot using QWebEngineView.
    """
    fileOpened = pyqtSignal(str)

    def __init__(self, rawHtml=None):
        """
        Initialize the window with the provided raw HTML.
        """
        super().__init__()
        self.rawHtml = rawHtml
        self.fileName = None
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the user interface.
        """
        self.configureWindow()
        self.setupMenu()
        self.setupInitialMessageLabel()

    def setupInitialMessageLabel(self):
        """
        Set up the initial message.
        """
        label = QLabel("Select video file")
        font = QFont()
        font.setPointSize(20)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def setupBrowser(self, rawHtml):
        """
        Set up the QWebEngineView.
        """
        self.browser = QWebEngineView()
        self.browser.setHtml(rawHtml)
        self.setCentralWidget(self.browser)

    def configureWindow(self):
        """
        Configure the window settings.
        """
        self.setWindowTitle('FPS Analyzer')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def setupMenu(self):
        """
        Set up the menu.
        """
        openFile = QAction('Open File', self)
        openFile.triggered.connect(self.openFileNameDialog)
        fileMenu = self.menuBar().addMenu('File')
        fileMenu.addAction(openFile)

    def openFileNameDialog(self):
        """
        Open a file dialog and print the selected file path.
        """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(f"Selected file: {fileName}")
            self.fileName = fileName
            self.fileOpened.emit(fileName)

    def openFileOpenErrorDialog(self, e):
        """
        Open a file open error dialog.
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(f"Failed to open file: {self.fileName}\n"
                             "Check if the file is a video file.")
        error_dialog.setInformativeText(str(e))
        error_dialog.exec_()
