import ffmpeg
from logger import setup_logger

import plotly.graph_objects as go
import plotly.io as pio

class VideoAnalyzer:
    def __init__(self, video_path):
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
        numerator, denominator = map(int, avg_frame_rate.split('/'))
        return numerator / denominator

    def extract_frame_info(self):
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
        durations = [j - i for i, j in zip(frame_timestamp[:-1], frame_timestamp[1:])]
        return durations

    def get_number_frames(self):
        return len(self.frame_duration_ms)

    def update_figure_annotations(self):
        self.figure.add_annotation(text=f"Number of Frames: {self.num_frames}",
                           xref='paper', yref='paper', x=0.5, y=1.05, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Duration: {self.avg_frame_duration_ms:.3f} milliseconds",
                           xref='paper', yref='paper', x=0.5, y=1.1, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Rate: {self.fps}",
                           xref='paper', yref='paper', x=0.5, y=1.15, showarrow=False)

    def update_figure_layout(self):
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
        self.figure = go.Figure(data=go.Scatter(y=self.frame_duration_ms, name='frame duration', mode='markers'))
        self.figure.add_trace(go.Scatter(y=self.frame_dts_time_durations, mode='markers', name='DTS Time', yaxis='y2'))
        self.figure.add_trace(go.Scatter(y=self.frame_pts_time_durations, mode='markers', name='PTS Time', yaxis='y2', visible='legendonly'))
        self.update_figure_layout()
        self.update_figure_annotations()
        return self.figure

    def get_raw_html(self):
        raw_html = pio.to_html(self.figure, full_html=False, include_plotlyjs='cdn')
        return raw_html

    def generate_html_file(self):
        self.plot_durations()
        return self.get_raw_html()
