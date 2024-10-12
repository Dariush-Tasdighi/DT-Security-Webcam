import constants
import cv2 as cv
import numpy as np
from colorama import Fore
from datetime import datetime


def print_current_webcam_settings(webcam: cv.VideoCapture) -> None:
    fps = webcam.get(propId=cv.CAP_PROP_FPS)
    width = webcam.get(propId=cv.CAP_PROP_FRAME_WIDTH)
    height = webcam.get(propId=cv.CAP_PROP_FRAME_HEIGHT)

    print(f"Current webcam FPS: {fps}")
    print(f"Current webcam Resolution: {width} * {height}")


def change_webcam_resolution(webcam: cv.VideoCapture, width: int, height: int) -> None:
    webcam.set(propId=cv.CAP_PROP_FRAME_WIDTH, value=width)
    webcam.set(propId=cv.CAP_PROP_FRAME_HEIGHT, value=height)


def get_difference(frame1: cv.Mat, frame2: cv.Mat) -> float:
    frame1_mean = np.mean(a=frame1)
    frame2_mean = np.mean(a=frame2)
    difference = np.abs(frame1_mean - frame2_mean) * 100

    return difference


def write_text_on_frame(frame: cv.Mat, text: str) -> None:
    frame_height = frame.shape[0]

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
    result = f"{formated_now} - {int(difference)}"
    if constants.BRAND != "":
        result += f" - {constants.BRAND}"
    return result


def check_motion_detection(
    new_frame: cv.Mat,
    new_grayscale_frame: cv.Mat,
    last_grayscale_frame: cv.Mat,
) -> None:
    difference = get_difference(frame1=new_grayscale_frame, frame2=last_grayscale_frame)

    if constants.DISPLAY_FRAMES_DIFFERENCE:
        print(difference)

    if difference < constants.SENSITIVITY:
        return

    now = datetime.now()
    formated_now = now.strftime(format="%Y_%m_%d_%H_%M_%S")

    if constants.DISPLAY_NOTIFICATION:
        print(f"{Fore.RED}{formated_now}: Motion Detected!{Fore.RESET}")

    filename = f"Capture_{formated_now}.png"
    pathname = f"{constants.PATH}\\{filename}"

    if constants.PUT_TEXT_ON_FRAME:
        text = get_text(formated_now=formated_now, difference=difference)
        write_text_on_frame(frame=new_frame, text=text)

    cv.imwrite(filename=pathname, img=new_frame)
