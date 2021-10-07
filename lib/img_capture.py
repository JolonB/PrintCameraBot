import time
import logging

import cv2

logger = logging.getLogger("root")


def capture(config: dict):
    # Initialise the camera
    cam = cv2.VideoCapture(config["camera_port"])
    time.sleep(1)

    # Attempt to read from the camera
    retval = False
    attempts_remaining = 5
    while not retval:
        retval, frame = cam.read()
        attempts_remaining -= 1
        if attempts_remaining <= 0:
            logger.error("Failed to read from camera")
            cam.release()
            return False

    # Save the image to a temp location
    logger.info("Successfully read from camera. Saving image to .tmp.jpg")
    cv2.imwrite(".tmp.jpg", frame)
    cam.release()

    return True
