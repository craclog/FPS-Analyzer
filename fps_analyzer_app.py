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
    """
    Analyzes a video file and generates an HTML report.

    Parameters:
    - video_path (str): The path to the video file to be analyzed.

    Returns:
    - str: The raw HTML content of the generated report.
    """
    logger.info("Starting to analyze video: %s", video_path)
    analyzer = VideoAnalyzer(video_path)
    raw_html = analyzer.generate_html_file()
    logger.info("Finished analyzing video: %s", video_path)
    return raw_html

def on_file_opened(file_name):
    """
    Slot that is called when a file is opened in the PlotlyWindow app.

    Parameters:
    - file_name (str): The name of the file that was opened.

    Description:
    This method is a slot that is called when a file is opened in the PlotlyWindow app.
    It logs the name of the opened file, analyzes the video using the analyze_video function,
    and sets up the browser in the WINDOW_INSTANCE with the raw HTML obtained from the analysis.
    If an exception occurs during the analysis, it logs the error and opens an error dialog in the
    WINDOW_INSTANCE.
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
