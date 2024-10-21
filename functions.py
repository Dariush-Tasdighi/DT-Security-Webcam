"""
Define Global Functions
"""

import os
import constants
import cv2 as cv
import numpy as np
from colorama import Fore
from datetime import datetime


def print_current_webcam_settings(webcam: cv.VideoCapture) -> None:
    """
    Print Current Webcam Settings
    """

    fps: float = webcam.get(propId=cv.CAP_PROP_FPS)
    width: float = webcam.get(propId=cv.CAP_PROP_FRAME_WIDTH)
    height: float = webcam.get(propId=cv.CAP_PROP_FRAME_HEIGHT)

    print(f"Current webcam FPS: {fps}")
    print(f"Current webcam Resolution: {width} * {height}")


def change_webcam_resolution(webcam: cv.VideoCapture, width: int, height: int) -> None:
    """
    Change Webcam Resolution
    """

    webcam.set(propId=cv.CAP_PROP_FRAME_WIDTH, value=width)
    webcam.set(propId=cv.CAP_PROP_FRAME_HEIGHT, value=height)


def get_difference(frame1: cv.Mat, frame2: cv.Mat) -> float:
    """
    Get Two Frames Difference
    """

    frame1_mean: float = np.mean(a=frame1)
    frame2_mean: float = np.mean(a=frame2)
    difference: float = np.abs(frame1_mean - frame2_mean) * 100

    return difference


def write_text_on_frame(text: str, frame: cv.Mat) -> None:
    """
    Write Text On Frame
    """

    frame_height: float = frame.shape[0]

    cv.putText(
        img=frame,
        text=text,
        org=(10, frame_height - 15),
        fontFace=cv.FONT_HERSHEY_SIMPLEX,
        fontScale=1.0,
        color=(0, 0, 255),
        thickness=2,
        lineType=cv.LINE_4,
    )


def get_text(formated_now: str, difference: float) -> str:
    """
    Get Text
    """

    result: str = f"{formated_now} - {int(difference)}"
    if constants.BRAND != "":
        result = f"{result} - {constants.BRAND}"

    return result


def check_motion_detection(
    new_frame: cv.Mat,
    new_grayscale_frame: cv.Mat,
    last_grayscale_frame: cv.Mat,
) -> None:
    """
    Check Motion Detection
    """

    difference: float = get_difference(
        frame1=new_grayscale_frame, frame2=last_grayscale_frame
    )

    now: datetime = datetime.now()
    formated_today: str = now.strftime(format="%Y_%m_%d")
    formated_now: str = now.strftime(format="%Y_%m_%d_%H_%M_%S")

    if constants.DISPLAY_FRAMES_DIFFERENCE:
        print(f"{formated_now}: {int(difference)}")

    if difference < constants.SENSITIVITY:
        return

    if constants.DISPLAY_NOTIFICATION:
        print(f"{Fore.RED}{formated_now}: Motion Detected!{Fore.RESET}")

    path: str = f"{constants.PATH}\\{formated_today}"
    if not os.path.exists(path):
        os.mkdir(path=path)

    filename: str = f"Capture_{formated_now}.png"
    pathname: str = f"{path}\\{filename}"

    if constants.PUT_TEXT_ON_FRAME:
        text = get_text(formated_now=formated_now, difference=difference)
        write_text_on_frame(text=text, frame=new_frame)

    cv.imwrite(filename=pathname, img=new_frame)


if __name__ == "__main__":
    print("This file is library file and you can not run it!")
