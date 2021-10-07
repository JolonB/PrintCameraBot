config = {
    "credentials": {
        "address": "test@email.com",
        "password": "password",
    },
    "polling_freq": 60,  # seconds
    "max_emails": 10,  # latest emails received
    "2fa_lookback": 60,  # seconds
    "approved_users": {
        "user1@email.com": "ABCD1234",  # email : OTP secret
    },
    "camera_port": "/dev/video0",
    "image_resolution": (640, 480),
}
