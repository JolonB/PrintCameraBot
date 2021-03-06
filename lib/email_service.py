import re
import time
import logging
import smtplib
import imaplib
import email.utils
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("root")

SENDER_REGEX = re.compile(r"From: .+ <(.+@.+\..+)>")
SUBJECT_REGEX = re.compile(r"Subject: (.+)")
DATE_REGEX = re.compile(r"Date: (.+)")


def open_email(config: dict):
    logger.info("Opening email")
    mail = imaplib.IMAP4_SSL(config["credentials"]["imap_host"])
    mail.login(config["credentials"]["address"], config["credentials"]["password"])
    mail.select("inbox")
    return mail


def close_email(mail: imaplib.IMAP4_SSL):
    mail.close()
    mail.logout()


def check_mail(mail: imaplib.IMAP4_SSL, config: dict):
    """Check for new emails"""
    # Get new emails
    mail.noop()
    result, email_ids = mail.search(None, "(UNSEEN SMALLER 10000)")

    # Check that data was read successfully
    if result != "OK":
        raise RuntimeError("Error searching for unread emails")

    email_ids = email_ids[0].split()
    logger.info("Found {} new emails".format(len(email_ids)))

    emails = []
    emails_read = 0
    for id_ in reversed(email_ids):

        # Skip any empty IDs (this shouldn't happen, but just in case)
        if id_ == b"":
            continue

        # Retrieve email subject, body, and sender
        success, data = mail.fetch(
            id_,
            "(BODY[HEADER.FIELDS (SUBJECT)] BODY[HEADER.FIELDS (FROM)] BODY[HEADER.FIELDS (DATE)] BODY[1])",
        )
        # Skip if success!='OK'
        if success != "OK":
            raise RuntimeError("Error fetching email")

        # Open emails but don't process them if the max number of emails has been reached
        # If we don't open them, they won't be marked as read and will be opened later
        if config["max_emails"] > 0 and emails_read >= config["max_emails"]:
            logger.info("Reached max number of emails; marking as read")
            continue

        # Remove any data that isn't a tuple because we don't care about those
        data = [x for x in data if isinstance(x, tuple)]

        # Extract data from tuple
        subject = data[0][1].decode("utf-8")
        from_address = data[1][1].decode("utf-8")
        datetime = data[2][1].decode("utf-8")
        message_body = data[3][1].decode("utf-8")

        from_address = SENDER_REGEX.match(from_address).group(1).strip()
        # Skip processing remaining fields is address is not an approved user
        if from_address not in config["approved_users"]:
            continue

        subject = SUBJECT_REGEX.match(subject).group(1).strip()
        message_body = message_body.strip()
        datetime = DATE_REGEX.match(datetime).group(1).strip()
        datetime = _parse_email_datetime(datetime)

        emails.append(
            {
                "address": from_address,
                "subject": subject,
                "body": message_body,
                "timestamp": datetime,
            }
        )
        emails_read += 1

    return emails


def _parse_email_datetime(datetime_str: str):
    datetime_str = datetime_str.strip()
    parsed_datetime = email.utils.parsedate(datetime_str)
    return int(time.mktime(parsed_datetime))


def send_image(address: str, filename: str, config: dict):
    logger.info("Sending image to {}".format(address))

    msg = MIMEMultipart()
    msg["From"] = config["credentials"]["address"]
    msg["To"] = address
    msg["Subject"] = config["email_subject"]

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read(), Name=filename)

    part["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
    msg.attach(part)

    with smtplib.SMTP(config["credentials"]["smtp_host"]) as smtp:
        smtp.starttls()
        smtp.login(config["credentials"]["address"], config["credentials"]["password"])
        smtp.sendmail(config["credentials"]["address"], address, msg.as_string())


def clear_large_mail(mail: imaplib.IMAP4_SSL, config: dict):
    mail.noop()
    logger.info("Searching for large mail")
    # Search for all mail that is large and was sent *to* the configured email address
    result, email_ids = mail.search(
        None, '(NOT SMALLER 10000 TO "{}")'.format(config["credentials"]["address"])
    )

    if result != "OK":
        raise RuntimeError("Error searching for large emails")

    email_ids = email_ids[0].split()
    logger.info("Found {} large emails".format(len(email_ids)))

    # Delete all mail in data
    for id_ in email_ids:
        mail.store(id_, "+FLAGS", "\\Deleted")
    # Permanently delete large mail (at least, it *should* delete the mail)
    mail.expunge()
