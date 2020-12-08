#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import queue
import threading
import cv2

class ButtonClickProcessor:
    def __init__(self, axes, label):
        self.button = Button(ax = axes, label = label, color = 'red', hovercolor = 'red')
        self.button.on_clicked(self.process)
        self.activated = False
        self.button_click_processors = None
    def activate(self):
        self.activated = True
        self.button.color = 'green'
        self.button.hovercolor = self.button.color
        self.button.ax.set_facecolor(self.button.color)
    def deactivate(self):
        self.activated = False
        self.button.color = 'red'
        self.button.hovercolor = self.button.color
        self.button.ax.set_facecolor(self.button.color)
    def process(self, event):
        for button_click_processor in self.button_click_processors:
            button_click_processor.deactivate()
        self.activate()
        self.button.ax.figure.canvas.draw()

# bufferless VideoCapture
class VideoCapture:
    def __init__(self, name):
        self.video_capture = cv2.VideoCapture(filename = name)
        self.q = queue.Queue()
        t = threading.Thread(target = self._reader)
        t.daemon = True
        t.start()
    # read frames as soon as they are available, keeping only the most recent one
    def _reader(self):
        while True:
            # capture frame-by-frame
            frame_read_correctly, frame = self.video_capture.read()
            if not frame_read_correctly:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait() # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(item = frame)
    def read(self):
        return self.q.get()

def main():

    earliest_time = datetime.now()

    fig, axes = plt.subplots()
    datetimes = []
    y_values = []
    line, = axes.plot_date(x = datetimes, y = y_values, color = 'blue', linestyle = 'solid', marker = 'None')

    button_show_all_times = ButtonClickProcessor(axes = plt.axes([0.01, 0.01, 0.5, 0.1]), label = 'Show all times')
    button_show_only_last_10_minutes = ButtonClickProcessor(axes = plt.axes([0.5, 0.01, 0.49, 0.1]), label = 'Show only last 10 minutes')
    button_click_processors = (button_show_all_times, button_show_only_last_10_minutes)
    button_show_all_times.button_click_processors = button_click_processors
    button_show_only_last_10_minutes.button_click_processors = button_click_processors

    video_capture = VideoCapture(name = 'http://redacted-rbpi-hostname:8080/stream/video.mjpeg')

    while True:

        # Our operations on the frame come here
        image = cv2.cvtColor(src = video_capture.read(), code = cv2.COLOR_BGR2GRAY)

        now = datetime.now()
        datetimes.append(now)
        y_value = np.sum(image)
        y_values.append(y_value)
        line.set_data(datetimes, y_values)
        axes.relim()
        axes.autoscale(enable = True, axis = 'both', tight = None)

        time_difference = now - earliest_time
        time_window = 10 * 60
        time_reset = 60 * 60
        time_delta = timedelta(seconds = time_window)
        if time_difference.total_seconds() > time_reset:
            if button_show_only_last_10_minutes.activated is True:
                axes.set_xlim(left = now - time_delta)
            for button_click_processor in button_click_processors:
                button_click_processor.deactivate()
            earliest_time = now
            datetimes = []
            y_values = []
        elif time_difference.total_seconds() > time_window:
            if button_show_all_times.activated is True:
                axes.set_xlim(left = datetimes[0] - 0.05 * (datetimes[-1] - datetimes[0]))
            elif button_show_only_last_10_minutes.activated is True:
                axes.set_xlim(left = now - time_delta)

        fig.tight_layout(rect = [0, 0.1, 1, 1])
        plt.pause(interval = 0.0001)

        # Display the resulting frame
        cv2.imshow(winname = 'frame', mat = image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
