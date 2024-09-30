# **************************************************
# دوربین امنیتی
# Version 2.5
# نکته مهم و جالب
# می‌کنیم نیز، کار می‌کند Lock این برنامه، حتی زمانی که سیستم را
# **************************************************
import os
import time
import cv2 as cv
import numpy as np
from colorama import Fore
from datetime import datetime

# Initial Settings
WEBCAM_INDEX = 0
SENSITIVITY = 100
PATH = "C:\\Captures"
DISPLAY_BRAND = True
MAX_RESOLUTION = True
DISPLAY_FRAMES = True
DISPLAY_DIFFERENCE = True
INITIAL_DELAY_SECONDS = 10
DISPLAY_NOTIFICATION = True

# WEBCAM_INDEX = 0
# SENSITIVITY = 100
# PATH = "C:\\Captures"
# DISPLAY_BRAND = True
# MAX_RESOLUTION = True
# DISPLAY_FRAMES = False
# DISPLAY_DIFFERENCE = False
# INITIAL_DELAY_SECONDS = 10
# DISPLAY_NOTIFICATION = False


def print_current_webcam_settings() -> None:
    fps = webcam.get(propId=cv.CAP_PROP_FPS)
    width = webcam.get(propId=cv.CAP_PROP_FRAME_WIDTH)
    height = webcam.get(propId=cv.CAP_PROP_FRAME_HEIGHT)

    print(f"Current webcam FPS: {fps}")
    print(f"Current webcam Resolution: {width} * {height}")


def change_webcam_resolution(width: int, height: int) -> None:
    webcam.set(propId=cv.CAP_PROP_FRAME_WIDTH, value=width)
    webcam.set(propId=cv.CAP_PROP_FRAME_HEIGHT, value=height)


def get_difference(frame1: cv.Mat, frame2: cv.Mat) -> int:
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


def check_motion_detection(
    new_frame: cv.Mat,
    new_grayscale_frame: cv.Mat,
    last_grayscale_frame: cv.Mat,
) -> None:
    difference = get_difference(frame1=new_grayscale_frame, frame2=last_grayscale_frame)

    if DISPLAY_DIFFERENCE:
        print(difference)

    if difference < SENSITIVITY:
        return

    now = datetime.now()
    formated_now = now.strftime(format="%Y_%m_%d_%H_%M_%S")

    if DISPLAY_NOTIFICATION:
        print(f"{Fore.RED}{formated_now}: Motion Detected!{Fore.RESET}")

    filename = f"Capture_{formated_now}.png"
    pathname = f"{PATH}\\{filename}"

    if DISPLAY_BRAND:
        brand = f"Dariush Tasdighi - 09121087461 - @IranianExperts - {formated_now}"
        write_text_on_frame(frame=new_frame, text=brand)

    cv.imwrite(filename=pathname, img=new_frame)


os.system(command="cls")

webcam = cv.VideoCapture(index=WEBCAM_INDEX)
if not webcam.isOpened():
    print("You do not have any webcam or it is not ready to use!")
    webcam.release()
    quit()

print_current_webcam_settings()
if MAX_RESOLUTION:
    change_webcam_resolution(width=20_000, height=20_000)
    print_current_webcam_settings()

last_grayscale_frame = None
start_time = datetime.now()

while True:
    time.sleep(1)

    success, new_frame = webcam.read()

    if success:
        new_grayscale_frame = cv.cvtColor(src=new_frame, code=cv.COLOR_BGR2GRAY)

        if last_grayscale_frame is None:
            last_grayscale_frame = new_grayscale_frame
            continue

        if DISPLAY_FRAMES:
            cv.imshow(winname="Webcam", mat=new_frame)

        difference_time = datetime.now() - start_time
        if difference_time.total_seconds() < INITIAL_DELAY_SECONDS:
            cv.waitKey(delay=1)
            print("Initialization...")
        else:
            check_motion_detection(
                new_frame=new_frame,
                new_grayscale_frame=new_grayscale_frame,
                last_grayscale_frame=last_grayscale_frame,
            )

            last_grayscale_frame = new_grayscale_frame

    key = cv.waitKey(delay=1)
    if key == ord("q") or key == ord("Q"):
        break

webcam.release()
cv.destroyAllWindows()
