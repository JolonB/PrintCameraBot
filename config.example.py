config = {
    "credentials": {
        "address": "test@email.com",
        "password": "password",
    },
    "email_subject": "Requested Image", # the subject of the response email
    "polling_freq": 60,  # seconds
    "max_emails": 10,  # latest emails received
    "2fa_lookback": 60,  # seconds (ideally long enough for you to draft and send an email)
    "approved_users": {
        "user1@email.com": "ABCD1234",  # email : OTP secret
        "user2@gmail.com": "EFGH5678",
    },
    "camera_port": "/dev/video0",
    "image_resolution": (640, 480),
}
