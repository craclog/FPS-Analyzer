import ffmpeg
from logger import setup_logger

import plotly.graph_objects as go
import plotly.io as pio

class VideoAnalyzer:
    """
    A class for analyzing video frames and extracting frame information.
    """

    def __init__(self, video_path):
        """
        Initializes the VideoAnalyzer object.

        Parameters:
        - video_path (str): The path to the video file.

        """
        self.video_path = video_path
        self.logger = setup_logger()
        try:
            self.frame_dts_time, self.frame_pts_time, self.frame_duration_ms, self.fps = self.extract_frame_info()
            self.figure = None
            self.num_frames = self.get_number_frames()
            self.avg_frame_duration_ms = sum(self.frame_duration_ms) / self.num_frames
            self.frame_dts_time_durations = self.calculate_durations(self.frame_dts_time)
            self.frame_pts_time_durations = self.calculate_durations(self.frame_pts_time)
        except ffmpeg.Error as e:
            self.logger.error("Failed to initialize VideoAnalyzer: %s", e)

    def calculate_fps(self, avg_frame_rate):
        """
        Calculates the frames per second (fps) based on the average frame rate.

        Parameters:
        - avg_frame_rate (str): The average frame rate in the format "numerator/denominator".

        Returns:
        - float: The frames per second (fps).

        """
        numerator, denominator = map(int, avg_frame_rate.split('/'))
        return numerator / denominator

    def extract_frame_info(self):
        """
        Extracts frame information from the video using FFmpeg.

        Returns:
        - tuple: A tuple containing the frame DTS times, frame PTS times, frame durations, and fps.

        """
        probe = ffmpeg.probe(self.video_path, select_streams='v:0', show_entries='packet=dts_time,pts_time,duration_time')
        frame_dts_time_ms = [float(packet['dts_time']) * 1000 for packet in probe['packets']]
        frame_pts_time_ms = [float(packet['pts_time']) * 1000 for packet in probe['packets']]
        self.logger.debug("frame_dts_time_ms: %s", frame_dts_time_ms[:5])
        self.logger.debug("frame_pts_time_ms: %s", frame_pts_time_ms[:5])

        # Convert duration_time to milliseconds
        frame_duration_ms = [float(packet['duration_time']) * 1000 for packet in probe['packets']]
        self.logger.debug("frame_duration_ms: %s", frame_duration_ms[:5])
        avg_frame_rate = probe['streams'][0]['avg_frame_rate']
        fps = self.calculate_fps(avg_frame_rate)
        return frame_dts_time_ms, frame_pts_time_ms, frame_duration_ms, fps

    def calculate_durations(self, frame_timestamp):
        """
        Calculates the durations between consecutive frame timestamps.

        Parameters:
        - frame_timestamp (list): A list of frame timestamps.

        Returns:
        - list: A list of durations between consecutive frame timestamps.

        """
        durations = [j - i for i, j in zip(frame_timestamp[:-1], frame_timestamp[1:])]
        return durations

    def get_number_frames(self):
        """
        Returns the number of frames in the video.

        Returns:
        - int: The number of frames.

        """
        return len(self.frame_duration_ms)

    def update_figure_annotations(self):
        """
        Updates the figure annotations with frame information.

        """
        self.figure.add_annotation(text=f"Number of Frames: {self.num_frames}",
                           xref='paper', yref='paper', x=0.5, y=1.05, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Duration: {self.avg_frame_duration_ms:.3f} milliseconds",
                           xref='paper', yref='paper', x=0.5, y=1.1, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Rate: {self.fps}",
                           xref='paper', yref='paper', x=0.5, y=1.15, showarrow=False)

    def update_figure_layout(self):
        """
        Updates the figure layout with appropriate titles and axis labels.

        """
        max_duration_time = max(self.frame_duration_ms)
        min_duration_time = min(self.frame_duration_ms)
        self.figure.update_layout(title='',
                        xaxis_title='Frame Index',
                        yaxis_title='Duration (milliseconds)',
                        yaxis2=dict(
                            title='DTS/PTS Time (milliseconds)',
                            overlaying='y',
                            side='right'
                        ),
                        template='plotly_dark',
                        yaxis_range=[min_duration_time, max_duration_time])

    def plot_durations(self):
        """
        Plots the frame durations, DTS time durations, and PTS time durations.

        Returns:
        - plotly.graph_objects.Figure: The generated plotly figure.

        """
        self.figure = go.Figure(data=go.Scatter(y=self.frame_duration_ms, name='frame duration', mode='markers'))
        self.figure.add_trace(go.Scatter(y=self.frame_dts_time_durations, mode='markers', name='DTS Time', yaxis='y2'))
        self.figure.add_trace(go.Scatter(y=self.frame_pts_time_durations, mode='markers', name='PTS Time', yaxis='y2', visible='legendonly'))
        self.update_figure_layout()
        self.update_figure_annotations()
        return self.figure

    def get_raw_html(self):
        """
        Returns the raw HTML representation of the plotly figure.

        Returns:
        - str: The raw HTML.

        """
        raw_html = pio.to_html(self.figure, full_html=False, include_plotlyjs='cdn')
        return raw_html

    def generate_html_file(self):
        """
        Generates an HTML file containing the plotly figure.

        Returns:
        - str: The generated HTML.

        """
        self.plot_durations()
        return self.get_raw_html()
