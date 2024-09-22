# **************************************************
# دوربین امنیتی
# Version 2.4
# **************************************************
import os
import time
import cv2 as cv
import numpy as np
from colorama import Fore
from datetime import datetime

# Initial Settings
webcam_index = 0
sensitivity = 50
path = "C:\\Captures"
display_brand = True
max_resolution = True
display_frames = True
display_difference = True
display_notification = True

# webcam_index = 0
# sensitivity = 50
# path = "C:\\Captures"
# display_brand = False
# max_resolution = False
# display_frames = False
# display_difference = False
# display_notification = False


def print_current_webcam_settings():
    fps = webcam.get(propId=cv.CAP_PROP_FPS)
    width = webcam.get(propId=cv.CAP_PROP_FRAME_WIDTH)
    height = webcam.get(propId=cv.CAP_PROP_FRAME_HEIGHT)

    print(f"Current Webcam FPS: {fps}")
    print(f"Current Webcam Resolution: {width} * {height}")


def change_webcam_resolution(width: int, height: int):
    webcam.set(propId=cv.CAP_PROP_FRAME_WIDTH, value=width)
    webcam.set(propId=cv.CAP_PROP_FRAME_HEIGHT, value=height)


def get_difference(image1, image2):
    image1_mean = np.mean(a=image1)
    image2_mean = np.mean(a=image2)
    difference_frames = np.abs(image1_mean - image2_mean) * 100

    return difference_frames


os.system(command="cls")

webcam = cv.VideoCapture(index=webcam_index)
if not webcam.isOpened():
    print("You do not have any webcam or it is not ready to use!")
    webcam.release()
    quit()

print_current_webcam_settings()
if max_resolution:
    change_webcam_resolution(width=20_000, height=20_000)
    print_current_webcam_settings()

last_frame = None

time.sleep(9)

while True:
    time.sleep(1)

    result, original_frame = webcam.read()

    if result:
        now = datetime.now()
        formated_now = now.strftime(format="%Y_%m_%d_%H_%M_%S")

        grayscale_frame = cv.cvtColor(src=original_frame, code=cv.COLOR_BGR2GRAY)

        if display_frames:
            cv.imshow(winname="Webcam", mat=original_frame)

        if last_frame is None:
            last_frame = grayscale_frame
            continue

        difference = get_difference(image1=grayscale_frame, image2=last_frame)

        if display_difference:
            print(difference)

        if difference > sensitivity:
            if display_notification:
                print(f"{Fore.RED}{formated_now}: Motion Detected!{Fore.RESET}")

            filename = f"Capture_{formated_now}.png"
            pathname = f"{path}\\{filename}"

            if display_brand:
                formated_now = now.strftime(format="%Y/%m/%d %H:%M:%S")

                brand = (
                    f"Dariush Tasdighi - 09121087461 - @IranianExperts - {formated_now}"
                )

                cv.putText(
                    img=original_frame,
                    text=brand,
                    org=(10, original_frame.shape[0] - 15),
                    fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0, 0, 255),
                    thickness=2,
                    lineType=cv.LINE_4,
                )

            cv.imwrite(filename=pathname, img=original_frame)

        last_frame = grayscale_frame

    key = cv.waitKey(delay=1)
    if key == ord("q") or key == ord("Q"):
        break

webcam.release()
cv.destroyAllWindows()
# **************************************************
