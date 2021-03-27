import math
import numpy as np

import cv2


def find_object(low_h, high_h, c_r, frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_mask = np.array([low_h, 155, 84])
    high_mask = np.array([high_h, 255, 255])
    frame_filtered = cv2.inRange(frame_hsv, low_mask, high_mask)

    frame_processed = cv2.erode(
        frame_filtered, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (c_r, c_r))
    )
    frame_processed = cv2.dilate(
        frame_filtered, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (c_r, c_r))
    )

    o_moments = cv2.moments(frame_processed)
    d_m_01 = o_moments["m01"]
    d_m_10 = o_moments["m10"]
    d_area = o_moments["m00"]

    y = int(d_m_01 / d_area)
    x = int(d_m_10 / d_area)
    radius = int(math.sqrt(d_area / 255 / math.pi))

    return x, y, radius, frame_processed
