# Print Monitor

Print Monitor is a way to securely monitor your 3D prints from anywhere with Internet access.
Simply by sending an email to the Print Monitor, you will receive a reply with a photo showing the current state of the print.

The benefit of this solution over others is that it doesn't require forwarding any ports and it can run on most devices even if they don't have OctoPrint set up.

## Setup

### Creating the email address

The instructions here are specific to Gmail accounts.
You will need to find how to make it work with a different account if you choose to use one.

1. Create a new Google Account. Take note of the email address and password.
1. Enable less secure apps by going to [this page](https://myaccount.google.com/lesssecureapps) and setting *"Allow less secure apps"* to **ON**.

That's all that needs to be done, however, if you want additional security, you may be able to set up a whitelist on the account to only allow emails from the desired sender.

### Setting up Python

If you are unfamiliar with Python, these instructions will help you set it up.

To begin, install Python3 on your device.  
If running Linux, this can be done with `sudo apt install python3`.  
If running Windows, you can get it from the Windows Store or the Python website (make sure you get Python3).

After installing, you need to set up a virtual environment.
This can be done by running `python3 -m venv venv`.
On Windows, you may need to replace `python3` with `py`.

You then should activate the virtual environment.
You will need to do this any time you leave the environment before you can run the scripts again.  
On Linux, `. venv/bin/activate`.  
On Windows, `.\venv\Scripts\activate`.

Finally, you need to install all of the required packages.
This can be done with `python -m pip install -r requirements.txt`.

Now you're ready to go.

### Generating a 2-factor authentication code

To generate a 2-factor authentication code, make sure your virtual environment is set up (see above).
Run the following command: `python setup_2fa.py`.

This will generate an OTP key that you should copy into your authenticator app (Google Authenticator, Authy, etc.).  
Your authenticator app will generate a 6-digit code every 30 seconds.
Copy the latest code into your terminal when the program requests it.
If it matches, your code is set up; if it doesn't, you should rerun the command.

### Setting up the config file

To begin, create a copy of `config.example.py` and rename it to `config.py`.
Modify the values in the file to suit your needs.
The values marked with a **\*** must be changed.

* credentials
    * address**\*** - the email address created for the bot
    * password**\*** - the password for the above email address
    * imap_host - the IMAP host address; only change this if you aren't using Gmail
    * smtp_host - the SMTP host address; only change this if you aren't using Gmail
* email_subject - the subject of the email sent by the Printer Monitor
* polling_freq - the number of seconds the Monitor waits between checking for new emails
* max_emails - the number of emails the monitor will process, any more will be discarded to prevent spam; set to 0 if you want to read all emails
* 2fa_lookback - the number of seconds for the two-factor authentication to look back for codes; this should be enough time to copy the code and send an email
* approved_users**\*** - email address : OTP secret pairs; each user that can access the Monitor should be set up
* camera_port**\*** - the port on your device that the camera is connected to; on Linux devices this will probably be `"/dev/video0"` (you may need to change the number), on Windows this will probably be `0` (notice that there are no speech marks)
* image_resolution - the resolution of the image to take; most webcams should support 640x480, but you can set if higher if yours supports it
* camera_boot_time - the time taken in seconds to initialise the camera; this should be increased if your images look too dark
* logger_filesize - the maximum size of each log file (in bytes); decrease this if your device has limited storage capacity
* log_filecount - the number of log files to produce before overwriting the first one; minimum value: 1

**IMPORTANT:** make sure you keep this file private as it contains the password for your email service

### Testing the Camera

### Starting Up

## Security

## Limitations

- Unable to provide information about the current progress of the print, as there is no integration with OctoPrint whatsoever.
If you want progress information, you can position the camera so the printer's display is in view.



<!--I wanted a way to securely monitor my 3D prints remotely, either as a live stream or just photos (this is the latter).

I had seen [a solution using a Discord bot](https://github.com/cameroncros/OctoPrint-DiscordRemote), however, is required OctoPrint to be set up on a device (as well as Discord).  
I considered setting up a server on my network and configuring port forwarding on my router. My issue with that solution is that there could be security risks if I configured it incorrectly (and maybe even if I did it correctly) which I didn't think were worth having a constant stream from my printer.

The solution I ultimately settled on was one that allowed me to send an email from an approved email address with a 2-factor authentication code.
Sending from an approved address (mostly) means that the user must have the credentials for the email address, but the 2-factor code provides an extra layer of protection against spoofing.
A malicious agent *could* try to send thousands of emails to the address from a spoofed address, but the bot will only read a few of them every polling frequency.  
In the worst case scenario, it would be possible for someone to find out both the sending and receiving email address, spoof the sending email address, and send the correct 2-factor code within the batch read during the polling period; however, even then the person will receive a only single photo of your printer, as opposed to gaining access to an unsecured network.
The system also ignores any emails over a certain size, so there's no way of someone sending a large email and chewing up all of your device's RAM.-->


