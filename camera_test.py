import sys

import cv2

from config import config
from lib.img_capture import capture

if __name__ == "__main__":
    frame = capture(config)

    if frame is None:
        print("No image detected", file=sys.stderr)
        exit(1)

    input_val = None
    while input_val not in {"1", "2"}:
        input_val = input(
            "Would you like to save the image or display it?\n" "1) Save\n2) Display\n"
        )

    print(
        "If the image is too dark (and the lights are on), increase"
        " camera_boot_time in your config.py file"
    )

    if input_val == "1":
        cv2.imwrite("camera_test.jpg", frame)
        print("Image saved as camera_test.jpg")
    else:
        cv2.imshow("Camera Test", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
