import sys
from PyQt5.QtWidgets import QApplication
from video_analyzer import VideoAnalyzer
from plotly_window import PlotlyWindow
from logger import setup_logger
from timer import timer_decorator

WINDOW_INSTANCE = None
logger = setup_logger()

@timer_decorator
def analyze_video(video_path):
    logger.info("Starting to analyze video: %s", video_path)
    analyzer = VideoAnalyzer(video_path)
    raw_html = analyzer.generate_html_file()
    logger.info("Finished analyzing video: %s", video_path)
    return raw_html

def on_file_opened(file_name):
    """
    Slot that is called when a file is opened in the PlotlyWindow app.
    """
    logger.info("A file was opened: %s", file_name)
    try:
        raw_html = analyze_video(file_name)
        WINDOW_INSTANCE.setup_browser(raw_html)
    except Exception as e:
        logger.error("Type of error: %s", type(e).__name__)
        logger.error("Failed to analyze video: %s", e)
        WINDOW_INSTANCE.open_file_open_error_dialog(e)

def main():
    """
    Main function that initializes the VideoAnalyzer and PlotlyWindow,
    and starts the QApplication event loop.
    """
    global WINDOW_INSTANCE

    app = QApplication(sys.argv)
    WINDOW_INSTANCE = PlotlyWindow()
    WINDOW_INSTANCE.file_opened.connect(on_file_opened)
    sys.exit(app.exec_())

if '__main__' == __name__:
    main()
