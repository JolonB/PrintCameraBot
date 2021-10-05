import re
import logging
import smtplib
import imaplib

logger = logging.getLogger('root')

SENDER_REGEX = re.compile(r"From: .+ <(.+@.+\..+)>")
SUBJECT_REGEX = re.compile(r"Subject: (.+)")


def open_email(config: dict):
    logger.info("Opening email")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
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
    result, data = mail.search(None, "(UNSEEN SMALLER 10000)")

    # Check that data was read successfully
    if result != "OK":
        raise RuntimeError("Error searching for unread emails")

    emails = []
    emails_read = 0
    for id_ in reversed(data[0].split()):
        if emails_read >= config["max_emails"]:
            break

        # Skip any empty IDs
        if id_ == b"":
            continue

        # Retrieve email subject, body, and sender
        success, data = mail.fetch(
            id_, "(BODY[HEADER.FIELDS (SUBJECT)] BODY[HEADER.FIELDS (FROM)] BODY[1])"
        )
        # Skip if success!='OK'
        if success != "OK":
            raise RuntimeError("Error fetching email")

        # Remove any data that isn't a tuple because we don't care about those
        data = [x for x in data if isinstance(x, tuple)]

        # Extract data from tuple
        subject = data[0][1].decode("utf-8")
        from_address = data[1][1].decode("utf-8")
        message_body = data[2][1].decode("utf-8")
        from_address = SENDER_REGEX.match(from_address).group(1).strip()

        # Skip processing remaining fields is address is not an approved user
        if from_address not in config["approved_users"]:
            continue

        subject = SUBJECT_REGEX.match(subject).group(1).strip()
        message_body = message_body.strip()

        emails.append(
            {"address": from_address, "subject": subject, "body": message_body}
        )
        emails_read += 1

    return emails


def clear_large_mail(mail: imaplib.IMAP4_SSL, config: dict):
    mail.noop()
    # Search for all mail that is large and was sent *to* the configured email address
    result, data = mail.search(
        None, '(NOT SMALLER 10000 TO "{}")'.format(config["credentials"]["address"])
    )

    if result != "OK":
        raise RuntimeError("Error searching for large emails")

    # Delete all mail in data
    for id_ in data[0].split():
        mail.store(id_, "+FLAGS", "\\Deleted")
    # Permanently delete large mail (at least, it *should* delete the mail)
    mail.expunge()
