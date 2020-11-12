#!/usr/bin/env python3

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import cv2

def main():

    fig, axes = plt.subplots()
    datetimes = []
    y_values = []
    line, = axes.plot_date(x = datetimes, y = y_values, color = 'blue', linestyle = 'solid', marker = 'None')

    video_capture = cv2.VideoCapture(filename = 'http://redacted-rbpi-hostname:8080/stream/video.mjpeg')

    while True:
        # Capture frame-by-frame
        frame_read_correctly, frame = video_capture.read()

        # Our operations on the frame come here
        image = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)

        now = datetime.now()
        datetimes.append(now)
        y_value = np.sum(image)
        y_values.append(y_value)
        line.set_data(datetimes, y_values)
        axes.relim()
        axes.autoscale(enable = True, axis = 'both', tight = None)

        fig.tight_layout()
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
