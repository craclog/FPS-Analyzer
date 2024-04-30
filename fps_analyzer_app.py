import sys
from PyQt5.QtWidgets import QApplication
from video_analyzer import VideoAnalyzer
from plotly_window import PlotlyWindow
from logger import setup_logger

WINDOW_INSTANCE = None
logger = setup_logger()

def analyzeVideo(videoPath):
    analyzer = VideoAnalyzer(videoPath)
    rawHtml = analyzer.generateHtmlFile()
    return rawHtml

def onFileOpened(fileName):
    """
    Slot that is called when a file is opened in the PlotlyWindow app.
    """
    logger.info("A file was opened: %s", fileName)
    try:
        rawHtml = analyzeVideo(fileName)
        WINDOW_INSTANCE.setupBrowser(rawHtml)
    except Exception as e:
        logger.error("Type of error: %s", type(e).__name__)
        logger.error("Failed to analyze video: %s", e)
        WINDOW_INSTANCE.openFileOpenErrorDialog(e)

def main():
    """
    Main function that initializes the VideoAnalyzer and PlotlyWindow,
    and starts the QApplication event loop.
    """
    global WINDOW_INSTANCE

    app = QApplication(sys.argv)
    WINDOW_INSTANCE = PlotlyWindow()
    WINDOW_INSTANCE.fileOpened.connect(onFileOpened)
    sys.exit(app.exec_())

if '__main__' == __name__:
    main()
