import time
import math
import logging

import cv2

logger = logging.getLogger("root")


def capture(config: dict):
    # Initialise the camera
    cam = cv2.VideoCapture(config["camera_port"])
    cam.set(
        cv2.CAP_PROP_EXPOSURE, round(math.log10(config["exposure_time"] / 1000.0), 4)
    )
    # Read from the camera to give it time to expose (because a delay doesn't seem to work)
    for _ in range(config["camera_boot_time"] * 2):
        _ = cam.read()
        time.sleep(0.5)

    # Attempt to read from the camera
    retval = False
    attempts_remaining = 5
    while not retval:
        retval, frame = cam.read()
        attempts_remaining -= 1
        if attempts_remaining <= 0:
            logger.error("Failed to read from camera")
            cam.release()
            return None

    # Release the camera
    cam.release()
    return frame


def capture_and_save(config: dict, filename: str):
    frame = capture(config)

    if frame is None:
        return False

    # Save the image to a temp location
    logger.info("Successfully read from camera. Saving image to {}".format(filename))
    cv2.imwrite(filename, frame)

    return True
