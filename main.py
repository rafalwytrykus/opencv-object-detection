import argparse

import cv2

from cv import find_object
from ui import initiate_control_window, get_params

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

if __name__ == "__main__":
    video = cv2.VideoCapture(args.file)

    if video is None:
        print(f"Unable to open video at {args.file}")
        raise Exception

    initiate_control_window()

    while True:
        _, frame = video.read()

        low_h, high_h, c_r = get_params()

        x, y, radius, frame_processed = find_object(low_h, high_h, c_r, frame)

        frame_width = len(frame[0])
        cv2.circle(frame, (x, y), radius, color=(255, 255, 255), thickness=1)
        cv2.line(
            frame, (frame_width // 2, 20), (x, 20), color=(255, 255, 255), thickness=10
        )

        cv2.imshow("source", frame)
        cv2.imshow("frame_processed", frame_processed)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
