from enum import Enum

import cv2


def initiate_control_window():
    cv2.namedWindow(CONTROL_WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar(
        TrackBarNames.LOW_HUE.value, CONTROL_WINDOW_NAME, 0, 180, nothing
    )
    cv2.setTrackbarPos(TrackBarNames.LOW_HUE.value, CONTROL_WINDOW_NAME, 160)
    cv2.createTrackbar(
        TrackBarNames.HIGH_HUE.value, CONTROL_WINDOW_NAME, 0, 180, nothing
    )
    cv2.setTrackbarPos(TrackBarNames.HIGH_HUE.value, CONTROL_WINDOW_NAME, 180)
    cv2.createTrackbar(TrackBarNames.C_R.value, CONTROL_WINDOW_NAME, 0, 100, nothing)
    cv2.setTrackbarPos(TrackBarNames.C_R.value, CONTROL_WINDOW_NAME, 10)


def get_params():
    low_h = cv2.getTrackbarPos(TrackBarNames.LOW_HUE.value, CONTROL_WINDOW_NAME)
    high_h = cv2.getTrackbarPos(TrackBarNames.HIGH_HUE.value, CONTROL_WINDOW_NAME)
    c_r = cv2.getTrackbarPos(TrackBarNames.C_R.value, CONTROL_WINDOW_NAME)
    return low_h, high_h, c_r


CONTROL_WINDOW_NAME = "CONTROL"


class TrackBarNames(Enum):
    LOW_HUE = "low_hue"
    HIGH_HUE = "high_hue"
    C_R = "c_r"


def nothing():
    return None
