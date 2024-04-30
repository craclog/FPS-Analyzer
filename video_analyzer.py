import ffmpeg
import plotly.graph_objects as go
import plotly.io as pio
from logger import setup_logger

class VideoAnalyzer:
    def __init__(self, videoPath):
        self.videoPath = videoPath
        self.logger = setup_logger()
        try:
            self.frameDtsTime, self.framePtsTime, self.frameDurationMs, self.fps = self.extractFrameInfo()
            self.figure = None
            self.numFrames = self.getNumberFrames()
            self.avgFrameDurationMs = sum(self.frameDurationMs) / self.numFrames
            self.frameDtsTimeDurations = self.calculateDurations(self.frameDtsTime)
            self.framePtsTimeDurations = self.calculateDurations(self.framePtsTime)
        except ffmpeg.Error as e:
            self.logger.error("Failed to initialize VideoAnalyzer: %s", e)

    def calculateFps(self, avgFrameRate):
        numerator, denominator = map(int, avgFrameRate.split('/'))
        return numerator / denominator

    def extractFrameInfo(self):
        probe = ffmpeg.probe(self.videoPath, select_streams='v:0', show_entries='packet=dts_time,pts_time,duration_time')
        frameDtsTimeMs = [float(packet['dts_time']) * 1000 for packet in probe['packets']]
        framePtsTimeMs = [float(packet['pts_time']) * 1000 for packet in probe['packets']]
        self.logger.debug("frameDtsTimeMs: %s", frameDtsTimeMs[:5])
        self.logger.debug("framePtsTimeMs: %s", framePtsTimeMs[:5])

        # Convert duration_time to milliseconds
        frameDurationMs = [float(packet['duration_time']) * 1000 for packet in probe['packets']]
        self.logger.debug("frameDurationMs: %s", frameDurationMs[:5])
        avgFrameRate = probe['streams'][0]['avg_frame_rate']
        fps = self.calculateFps(avgFrameRate)
        return frameDtsTimeMs, framePtsTimeMs, frameDurationMs, fps

    def calculateDurations(self, frameTimestamp):
        durations = [j - i for i, j in zip(frameTimestamp[:-1], frameTimestamp[1:])]
        return durations

    def getNumberFrames(self):
        return len(self.frameDurationMs)

    def updateFigureAnnotations(self):
        self.figure.add_annotation(text=f"Number of Frames: {self.numFrames}",
                           xref='paper', yref='paper', x=0.5, y=1.05, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Duration: {self.avgFrameDurationMs:.3f} milliseconds",
                           xref='paper', yref='paper', x=0.5, y=1.1, showarrow=False)
        self.figure.add_annotation(text=f"Average Frame Rate: {self.fps}",
                           xref='paper', yref='paper', x=0.5, y=1.15, showarrow=False)

    def updateFigureLayout(self):
        maxDurationTime = max(self.frameDurationMs)
        minDurationTime = min(self.frameDurationMs)
        self.figure.update_layout(title='',
                        xaxis_title='Frame Index',
                        yaxis_title='Duration (milliseconds)',
                        yaxis2=dict(
                            title='DTS/PTS Time (milliseconds)',
                            overlaying='y',
                            side='right'
                        ),
                        template='plotly_dark',
                        yaxis_range=[minDurationTime, maxDurationTime])

    def plotDurations(self):
        self.figure = go.Figure(data=go.Scatter(y=self.frameDurationMs, name='frame duration', mode='markers'))
        self.figure.add_trace(go.Scatter(y=self.frameDtsTimeDurations, mode='markers', name='DTS Time', yaxis='y2'))
        self.figure.add_trace(go.Scatter(y=self.framePtsTimeDurations, mode='markers', name='PTS Time', yaxis='y2', visible='legendonly'))
        self.updateFigureLayout()
        self.updateFigureAnnotations()
        return self.figure

    def getRawHtml(self):
        rawHtml = pio.to_html(self.figure, full_html=False, include_plotlyjs='cdn')
        return rawHtml

    def generateHtmlFile(self):
        self.plotDurations()
        return self.getRawHtml()
