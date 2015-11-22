A downloader written in python for the Toshiba FlashAir Wifi SDHC Cards.

Requirements:
Python3 & PyQt4

It is highly recommended to use the card with API Mode 5 (card connects to access point).
 
The downloader can be run with Preview of the latest image from the card or just downloading the images to a folder.
(
currently the functions are only set for downloading JPEGs as preview, had trouble with my camera switching off, before finished downloading RAW
also QImage might not support RAW images ...
)

For the Preview execute:
  
![alt tag](https://raw.github.com/cyborg-x1/PyFlashAero/dev/screenshot.png)

	python3 PyFlashAero.py --card_uri http://192.168.0.17 #The URL of your card
	                       --ImageViewer     #shows the ImageViewer
	                       --GUIinstant      #Has to be supplied (currently there is no option on the GUI to start or stop downloading!)
	                       --folder_remote /DCIM/100EOS5D #The remote folder on your card you want it to look into
	                       --folder_local /folder_on_local_disk #The folder where the images should be stored

For the console execute:


	python3 PyFlashAero.py --card_uri http://192.168.0.17 #The URL of your card
	                       --folder_remote /DCIM/100EOS5D #The remote folder on your card you want it to look into
	                       --folder_local /folder_on_local_disk #The folder where the images should be stored

argument   | helper       | default value
---------- | -------------|-------------
--card_uri | URI of the Toshiba FlashAir SDCard | http://192.168.0.1
--timeout  | Timeout in milliseconds | 1000
--folder_local|Folder for storing downloaded images |'.'
--folder_remote|Folder where to search for new images (remote)| '/'
--recursive | Search for new images in the folder recursively (not implemented yet) | False
--ImageViewer|Shows the GUI|SyncFolder 
--GUIinstant|GUI will start looking for images directly|False
--GUIDebugImage|path for picture to debug the GUI
--ext||'JPG'
