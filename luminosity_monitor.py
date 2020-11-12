#!/usr/bin/env python3

import numpy as np
import cv2

def main():

    video_capture = cv2.VideoCapture(filename = 'http://redacted-rbpi-hostname:8080/stream/video.mjpeg')

    while True:
        # Capture frame-by-frame
        frame_read_correctly, frame = video_capture.read()

        # Our operations on the frame come here
        image = cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow(winname = 'frame', mat = image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
