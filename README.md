A downloader written in python for the Toshiba FlashAir Wifi SDHC Cards.

Currently using a setup of Hostname/IP, remote_folder and download directory requires a modification of the __init__.py.
When started the script looks for the card on the given Host/IP if it is able to connect it, it gets the filelist by command.cgi
and checks for every file inside the download directory, if a file is not present, it will be downloaded. This continues as
long as the script is running, terminate it with CTRL-C.