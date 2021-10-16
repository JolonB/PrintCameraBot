# Print Monitor

Print Monitor is a way to securely monitor your 3D prints from anywhere with Internet access.
Simply by sending an email to the Print Monitor, you will receive a reply with a photo showing the current state of the print.

The benefit of this solution over others is that it doesn't require forwarding any ports and it can run on most devices even if they don't have OctoPrint set up (like [this one](https://github.com/cameroncros/OctoPrint-DiscordRemote) which I would suggest if you *do* have OctoPrint).

## Setup

These instructions are written to *hopefully* allow anyone to run this on their own device.
If you're already familiar with Git and Python, you'll be able to skip some of these steps.

Note that these instructions were written while testing on Ubuntu 20.04.
I've tried to write instructions for Windows based on the information I can find online, but feel free to let me know if any instructions are wrong by raising an issue in Github.

### Cloning the repository

If you have git installed on your device, simply clone it with `git clone https://github.com/JolonB/PrintCameraBot`.

If you don't have git, you can download this repo by clicking the **Code** button in the top right and then selecting **Download ZIP**.
Make sure to unzip the project before continuing.

### Setting up Python

If you are unfamiliar with Python, these instructions will help you set it up.

To begin, install Python3 on your device.  
If running Linux, this can be done with `sudo apt install python3`.  
If running Windows, you can get it from the Windows Store or the Python website (make sure you get Python3).

After installing, you need to set up a virtual environment.
This can be done by running `python3 -m venv venv`.
On Windows, you may need to replace `python3` with `py`.

You then should activate the virtual environment.
**You will need to do this any time you leave the environment before you can run the scripts again.**  
On Linux, `. venv/bin/activate`.  
On Windows, `.\venv\Scripts\activate`.

Finally, you need to install all of the required packages.
This can be done with `python -m pip install -r requirements.txt`.

Now you're ready to go.

### Creating the email address

The instructions here are specific to Gmail accounts.
You will need to find how to make it work with a different account if you choose to use one.

1. Create a new Google Account. Take note of the email address and password.
1. Enable less secure apps by going to [this page](https://myaccount.google.com/lesssecureapps) and setting *"Allow less secure apps"* to **ON**.

That's all that needs to be done, however, if you want additional security, you may be able to set up a whitelist on the account to only allow emails from the desired sender.

### Generating a 2-factor authentication code

To generate a 2-factor authentication code, make sure your virtual environment is set up (see above).
Run the following command: `python setup_2fa.py`.

This will generate an 8-digit OTP *key* that you should copy into your authenticator app (Google Authenticator, Authy, etc.).  
Your authenticator app will generate a 6-digit *code* every 30 seconds.
Copy the latest *code* into your terminal when the program requests it.
If it matches, your *code* is set up; if it doesn't, you probably entered it wrong and should enter the key again into your authenticator app.

Once that is set up, you should move on to the config file step and add the email address and 8-digit authenticator *key* to the `approved_users` field.
When you add a new user, you have the option to reuse the same key or to generate a new one for them.

### Setting up the config file

To begin, create a copy of `config.example.py` and rename it to `config.py`.
Modify the values in the file to suit your needs.
The values marked with a **\*** must be changed.

* **credentials**
    * **address**\* - the email address created for the bot
    * **password**\* - the password for the above email address
    * **imap_host** - the IMAP host address; only change this if you aren't using Gmail
    * **smtp_host** - the SMTP host address; only change this if you aren't using Gmail
* **email_subject** - the subject of the email sent by the Printer Monitor
* **polling_period** - the number of seconds the Monitor waits between checking for new emails
* **max_emails** - the number of emails the monitor will process, any more will be discarded to prevent spam; set to 0 if you want to read all emails
* **2fa_lookback** - the number of seconds for the two-factor authentication to look back for codes; this should be enough time to copy the code and send an email
* **approved_users**\* - email address : OTP secret pairs; each user that can access the Monitor should be set up
* **camera_port**\* - the port on your device that the camera is connected to; it is probably easiest to guess and check until you get the correct value
* **image_resolution** - the resolution of the image to take; most webcams should support 640x480, but you can set if higher if yours supports it
* **camera_boot_time** - the time taken in seconds to initialise the camera; this should be increased if your images look too dark
* **logger_filesize** - the maximum size of each log file (in bytes); decrease this if your device has limited storage capacity
* **log_filecount** - the number of log files to produce before overwriting the first one; minimum value: 1

**IMPORTANT:** make sure you keep this file private as it contains the password for your email service

### Testing the camera

After setting up the configuration file, you can test the camera to ensure your settings work.
This can be done by running `python camera_test.py`.
If everything works, the script will ask you if you want to save or display the image.
If you are using SSH (without X11 forwarding) or Windows Subsystem for Linux, it will be better to save the image.

There are a few possible issues you may face:

| Issue | Fix |
| --- | --- |
| "can't open camera by index" | Camera is disabled. Try restarting your device or reinstalling the drivers |
| "Failed to read from camera" | `camera_port` is incorrect; try providing a different one |
| Image isn't correct resolution | Your camera probably doesn't support the resolution and is providing the closest one it can find |
| Image is too dark | Increase `exposure_time` or `camera_boot_time` to allow the camera to expose itself to more light OR turn on a light near your printer OR try rebooting your device | 

### Starting up

To get started, you need to run the main.py script.
If you are running it manually (i.e. by typing the command yourself), you should simply enter `python main.py`.

This script will ask you which script you wish to run.
The options you are given are to run the main script, run the camera test, or run the 2-factor authentication setup.

Running the main script will start up the email polling loop which will automatically fetch emails according to the config file.
If a valid email is received, the Monitor will send a response email with the photo captured from the webcam.

The camera test script will take a photo and allow the user to choose to save it to the disk or display it.
There may be issues with displaying the image, so saving it to disk is always recommended.

The 2-factor authentication script allows you to set up your one-time password.
This will generate a key that you should enter into your authenticator app and then will request the code given by the app.
If the code matches, then it was a success.
You should copy the key into the config file along with the email address you wish to associate with it (one key can be associated with multiple email addresses, but not vice versa).

---

If you want to automate this script (to run it on boot, for example), there are also command line arguments that you can set.
These can be viewed by running `python main.py -h`.

Note that the camera test will automatically save the file on disk if started with the `-c`/`--cam-test` flag.

## Security

When developing this, I tried to make this as secure as I could, without relying on a paid service.
The most important part was that I didn't trust myself to be able to maintain security on a port if I opened one up on my network.
I didn't feel that it was worth the risk for being able to view a print.

The system has 3 layers of security:

- Secure email servers
- One-time passwords
- Request limiting

The Monitor, by default, uses Gmail but this could be changed if desired.
Any major email client that you choose to use will most likely be very secure.
The photos of your printer are probably going to be the least of your concerns if there was a security breach.

One obvious issue with emails is the possibility of spoofing an email address.
If someone knows the Monitor's email address and your authorised email address, they could send an email as yourself to get a photo.
The addition of one-time passwords solves this issue, as it requires any email to have a one-time password (OTP) in the email body in order for the email to be verified.
Without the correct OTP, the device will reject the request without sending any response.

A malicious user could attempt to send thousands of emails at a time with different passwords.
To prevent this, the system implements request limiting to limit itself to reading only the latest few emails.
This could negatively impact a genuine user if someone is trying to gain access (as it will ignore requests above the limit even if the OTP is correct), but it means that a malicious user will have to get very lucky to get the correct code during the correct period.

Additionally, even if a malicious user does manage to guess the correct OTP within the request limit with a spoofed email address, this does not give them enough information to get the correct OTP immediately a second time.
They improve their guesses each time they get a correct code, but this will be so slow that I doubt they'll be able to do it within any realistic amount of time.

In fact, I am so confident in how secure this is, that I implore anyone to try to get a photo from the camera.
If you can send me a photo taken of my 3D printer, you will be rewarded (once I figure out what the reward should be...).
Nothing needs to be printing, it just needs to be a photo taken from my webcam of my printer.

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


