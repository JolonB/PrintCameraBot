import time
import base64
import random
import logging

logger = logging.getLogger("root")

import pyotp

ENCODING = "utf-8"
TWO_FACT_AUTH_TIMEOUT = 30


def generate_secret_token():
    # Generate a random token
    secret_string = "{}".format(time.time() * random.random())
    return base64.b32encode(secret_string.encode(ENCODING)).decode(ENCODING)[4:12]


def verify_otp_code(user: str, code: str, timestamp: int, config: dict):
    # Get the user's secret key
    secret = config["approved_users"][user]

    # Create a TOTP object
    totp = pyotp.TOTP(secret)

    two_fact_lookback = config["2fa_lookback"]

    # Iterate over all valid timestamps
    for lookback in range(two_fact_lookback // TWO_FACT_AUTH_TIMEOUT + 1):
        excepted_code = totp.at(timestamp - lookback * TWO_FACT_AUTH_TIMEOUT)
        logger.debug("Expected code: {}. Got: {}".format(excepted_code, code))
        # Return True if the code is valid within the timestamps
        if excepted_code == code:
            return True
    return False
