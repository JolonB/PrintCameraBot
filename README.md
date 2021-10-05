# 3D Printer Camera Bot

I wanted a way to securely monitor my 3D prints remotely, either as a live stream or just photos (this is the latter).

I had seen [a solution using a Discord bot](https://github.com/cameroncros/OctoPrint-DiscordRemote), however, is required OctoPrint to be set up on a device (as well as Discord).  
I considered setting up a server on my network and configuring port forwarding on my router. My issue with that solution is that there could be security risks if I configured it incorrectly (and maybe even if I did it correctly) which I didn't think were worth having a constant stream from my printer.

The solution I ultimately settled on was one that allowed me to send an email from an approved email address with a 2-factor authentication code.
Sending from an approved address (mostly) means that the user must have the credentials for the email address, but the 2-factor code provides an extra layer of protection against spoofing.
A malicious agent *could* try to send thousands of emails to the address from a spoofed address, but the bot will only read a few of them every polling frequency.  
In the worst case scenario, it would be possible for someone to find out both the sending and receiving email address, spoof the sending email address, and send the correct 2-factor code within the batch read during the polling period; however, even then the person will receive a only single photo of your printer, as opposed to gaining access to an unsecured network.
The system also ignores any emails over a certain size, so there's no way of someone sending a large email and chewing up all of your device's RAM.

## Creating the email address

The instructions here are specific to Gmail accounts.
You will need to find how to make it work with a different account if you choose to use one.

1. Create a Google Account. Make a note of the email address and password in your `config.py` file.
1. Enable less secure apps by going to [this page](https://myaccount.google.com/lesssecureapps) and setting *"Allow less secure apps"* to **ON**.
