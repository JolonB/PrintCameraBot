import sys
import time
import logging
import logging.handlers
import traceback

from lib import two_factor
from lib import img_capture
from lib import email_service
from lib.read_config import read_config


logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
consolehandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(levelname)s:%(asctime)s::%(funcName)s:%(message)s", "%Y-%m-%d %H:%M:%S"
)
consolehandler.setFormatter(formatter)
logger.addHandler(consolehandler)

IMG_FILENAME = ".tmp.jpg"


def process_mail(mail, config):
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
        img_capture.capture_and_save(config, IMG_FILENAME)

        # Send email
        email_service.send_image(request["address"], IMG_FILENAME, config)


def run_daemon(config):
    mail = email_service.open_email(config)
    try:
        while True:
            # Run the main function at the specified polling period
            loop_start = time.time()
            process_mail(mail, config)
            # Delete large emails
            email_service.clear_large_mail(mail, config)
            elapsed = time.time() - loop_start
            try:
                time.sleep(config["polling_period"] - elapsed)
            except ValueError:
                logger.warning(
                    "Sleeping for a negative amount of time. Consider"
                    " increasing polling_period."
                )
    finally:
        # Close email service no matter how the daemon ends
        email_service.close_email(mail)


def main(config_file, interactive=True):
    # Load config
    config = read_config(config_file)
    # Set up the file handler once the config file is read
    filehandler = logging.handlers.RotatingFileHandler(
        "out.log",
        maxBytes=config["logger_filesize"],
        backupCount=max(1, config["log_filecount"]),
    )
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    while True:
        try:
            run_daemon(config)
        except Exception as e:
            # Catch all interrupts but KeyboardInterrupt and SystemExit
            logging.critical(traceback.format_exc())

        # Wait before resetting
        time.sleep(5)


if __name__ == "__main__":
    main(config_file="config.json", interactive=True)
