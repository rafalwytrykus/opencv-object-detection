from controller import Robot
import struct
from typing import Tuple
import numpy as np
import math

import cv2

robot = Robot()

TIMESTEP = 64
CAMERA_CHANELS = 4
MAX_VELOCITY = 7


camera = robot.getCamera("cam1")
camera.enable(TIMESTEP)
left_motor = robot.getMotor("lMotor")
right_motor = robot.getMotor("rMotor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


def get_frame(camera):
    """
    Returns frame in a format compatible opencv
    """
    frame = camera.getImage()
    if frame is None:
        return None
    CHUNK = camera.getWidth() * camera.getHeight() * CAMERA_CHANELS
    tfmd = struct.unpack(str(CHUNK) + "B", frame)
    tfmd = np.array(tfmd, dtype=np.uint8).reshape(
        camera.getWidth(), camera.getHeight(), CAMERA_CHANELS
    )
    tfmd = tfmd[:, :, 0:3]
    return tfmd


def search():
    """
    Turn the robot around in place searching for the object.
    """
    left_motor.setVelocity(MAX_VELOCITY * 1)
    right_motor.setVelocity(MAX_VELOCITY * -1)


def follow_object(input: float):
    """
    Follow the object located at position `input`.
    `input` must be in the range [-1, 1]:
    -1 - object at the left edge of the frame
    0  - object at the center of the frame
    1  - object at the right edge of the frame
    """
    correction = input
    left_motor.setVelocity(MAX_VELOCITY + correction)
    right_motor.setVelocity(MAX_VELOCITY - correction)


def find_object(
    low_h: int, high_h: int, c_r: int, frame: np.array
) -> Tuple[int, int, int, np.array]:
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

    if not d_area:
        return None, None, 0, frame_processed

    y = int(d_m_01 / d_area)
    x = int(d_m_10 / d_area)
    radius = int(math.sqrt(d_area / 255 / math.pi))

    return x, y, radius, frame_processed


while robot.step(TIMESTEP) != -1:
    frame = get_frame(camera)
    x, y, radius, frame_processed = find_object(160, 180, 10, frame)
    frame_width = len(frame[0])

    if x is not None:
        # Found the object in frame, follow it
        object_position = (x - (frame_width // 2)) / (frame_width // 2)
        follow_object(object_position)
        print(object_position)
    else:
        # Object not found in frame, turn around searching for it
        search()
        print("Not found, searching...")
