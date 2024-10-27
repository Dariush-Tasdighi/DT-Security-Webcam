"""
DT Webcam Security
Version 3.1
"""

import os
import time
import cv2 as cv
import constants
import functions
from colorama import Fore
from datetime import datetime


def main() -> None:
    """
    Main Function
    """
    try:
        os.system(command="cls")

        webcam = cv.VideoCapture(index=constants.WEBCAM_INDEX)
        if not webcam.isOpened():
            error = f"{Fore.RED}You do not have any webcam or it is not ready to use!{Fore.RESET}"
            print(error)
            webcam.release()
            quit()

        functions.print_current_webcam_settings(webcam=webcam)
        if constants.USE_HD_RESOLUTION:
            functions.change_webcam_resolution(webcam=webcam, width=1280, height=720)
            functions.print_current_webcam_settings(webcam=webcam)

        last_grayscale_frame: cv.Mat = None
        start_time: datetime = datetime.now()

        while True:
            time.sleep(constants.CAPTURE_INTERVAL)

            success, new_frame = webcam.read()

            if success:
                new_grayscale_frame: cv.Mat = cv.cvtColor(
                    src=new_frame, code=cv.COLOR_BGR2GRAY
                )

                if constants.DISPLAY_FRAMES:
                    cv.imshow(winname="Webcam", mat=new_frame)

                difference_time: datetime = datetime.now() - start_time
                if difference_time.total_seconds() < constants.INITIAL_DELAY:
                    print(f"{Fore.YELLOW}Initialization...{Fore.RESET}")
                else:
                    if last_grayscale_frame is None:
                        last_grayscale_frame = new_grayscale_frame
                        continue

                    functions.check_motion_detection(
                        new_frame=new_frame,
                        new_grayscale_frame=new_grayscale_frame,
                        last_grayscale_frame=last_grayscale_frame,
                    )

                    last_grayscale_frame = new_grayscale_frame

            key = cv.waitKey(delay=1)
            if key == ord("q") or key == ord("Q"):
                break
    except KeyboardInterrupt:  # Ctrl + C
        pass
    finally:
        webcam.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
