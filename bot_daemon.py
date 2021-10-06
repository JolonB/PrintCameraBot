import sys
import time
import logging
import logging.handlers
import traceback

from config import config
from lib import two_factor
from lib import img_capture
from lib import email_service


logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
filehandler = logging.handlers.RotatingFileHandler(
    "out.log", maxBytes=10_000_000, backupCount=5
)
consolehandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(levelname)s:%(asctime)s::%(funcName)s:%(message)s", "%Y-%m-%d %H:%M:%S"
)
filehandler.setFormatter(formatter)
consolehandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.addHandler(consolehandler)


def main(mail):
    logger.info("Running main loop")

    # Read mail
    requests = email_service.check_mail(mail, config)
    logger.info("Requests received: {}".format(requests))

    # Process mail
    for request in requests:
        logger.info("Processing request: {}".format(request))
        # Check if two-factor code is valid
        success = two_factor.verify_otp_code(
            request["address"], request["body"], request["timestamp"], config
        )
        if not success:
            logger.info("Two-factor code invalid")
            continue

        # If two-factor code is valid, take a photo
        logger.info("Two-factor code valid")
        img_path = img_capture.take_photo(config)


def run_daemon():
    mail = email_service.open_email(config)
    try:
        while True:
            # Run the main function at the specified polling period
            loop_start = time.time()
            main(mail)
            elapsed = time.time() - loop_start
            time.sleep(config["polling_period"] - elapsed)
    finally:
        # Close email service no matter how the daemon ends
        email_service.close_email(mail)


if __name__ == "__main__":
    while True:
        try:
            run_daemon()
        except Exception as e:
            # Catch all interrupts but KeyboardInterrupt and SystemExit
            logging.critical(traceback.format_exc())

        # Wait before resetting
        time.sleep(5)
