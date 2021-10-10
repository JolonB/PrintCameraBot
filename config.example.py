config = {
    "credentials": {
        "address": "test@email.com",
        "password": "password",
        "imap_host": "imap.gmail.com",
        "smtp_host": "smtp.gmail.com",
    },
    "email_subject": "Requested Image",  # the subject of the response email
    "polling_freq": 60,  # seconds
    "max_emails": 10,  # latest emails received
    "2fa_lookback": 90,  # seconds (ideally long enough for you to draft and send an email)
    "approved_users": {
        "user1@email.com": "ABCD1234",  # email : OTP secret
        "user2@gmail.com": "EFGH5678",
    },
    "camera_port": 0,
    "image_resolution": (640, 480),
    "exposure_time": 160,  # milliseconds
    "camera_boot_time": 1,  # seconds
    "logger_filesize": 10_000,  # bytes
    "log_filecount": 5,  # files
}
