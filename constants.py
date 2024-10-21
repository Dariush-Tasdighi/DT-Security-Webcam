"""
Define Constants
"""

WEBCAM_INDEX: int = 0  # -1 [OR] 0 [OR] 1 ...
SENSITIVITY: int = 120
PATH: str = "C:\\Captures"
USE_HD_RESOLUTION: bool = True  # False: LD: 640x480 | True: HD: 1280x720

PUT_TEXT_ON_FRAME: bool = True
DISPLAY_FRAMES: bool = True  # False
DISPLAY_NOTIFICATION: bool = True  # False
DISPLAY_FRAMES_DIFFERENCE: bool = True  # False

INITIAL_DELAY: int = 10  # Second(s)
CAPTURE_INTERVAL: int = 1  # Second(s)

BRAND: str = "Dariush Tasdighi - @IranianExperts - 09121087461"  # Your Company / Name

if __name__ == "__main__":
    print("This file is library file and you can not run it!")
