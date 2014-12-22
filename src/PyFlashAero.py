'''
Created on Jan 25, 2014

@author: cyborg-x1
'''

from FlashAir import card
from urllib.parse import urlparse
import argparse
import socket
import sys
import os
from os.path import expanduser
import time




def ImageView(args):
    print("imageView")
    
    try:
        import PyQt4.QtGui as QtGui
    except ImportError:
        sys.exit("Using --imageViewer requires PyQt4, which is not installed.")
    
    from FlashAir import ImageViewer
    
    app = QtGui.QApplication(sys.argv)
    port=args.card_uri.port    
    if(port == None):
        port = 80
    imageViewer = ImageViewer.ImageViewer(socket.gethostbyname(args.card_uri.hostname), port, args.timeout, args.folder_local, args.folder_remote, args.instant, args.recursive, args.debug_image)
    imageViewer.show()
    sys.exit(app.exec_())
  
def SyncFolder(args):
    print("SyncFolder")
    print(socket.gethostbyname(args.card_uri.hostname))
    
    port=args.card_uri.port    
    if(port == None):
        port = 80
    
    a=card.connection(socket.gethostbyname(args.card_uri.hostname), port, args.timeout)
    print("Use ctrl-c to exit!")
    while True:
        a.sync_folder_to_remote_folder(args.folder_remote, args.folder_local, extensions=args.ext)
        time.sleep(1)
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyFlashAero, Download Tool for Toshiba FlashAir SD-Cards')
    parser.add_argument('--card_uri', dest='card_uri', type=urlparse, help='URI of the Toshiba FlashAir SDCard', default="http://192.168.0.1")
    parser.add_argument('--timeout', dest='timeout', type=int, help='Timeout in milliseconds', default=1000)
    
    parser.add_argument('--folder_local', dest='folder_local', help='Folder for storing downloaded images', default='.')
    parser.add_argument('--folder_remote', dest='folder_remote', help='Folder where to search for new images (remote)', default='/')
    parser.add_argument('--recursive', dest='recursive', action='store_const',
                        const=True, default=False,
                        help='Search for new images in the folder recursively (not implemented yet)')
    
    parser.add_argument('--ImageViewer', dest='processing', action='store_const',
                        const=ImageView, default=SyncFolder,
                        help='Shows the GUI')
    

    parser.add_argument('--GUIinstant', dest='instant', action='store_const',
                        const=True, default=False,
                        help='GUI will start looking for images directly')
    
    parser.add_argument('--GUIDebugImage', dest='debug_image', help='path for picture to debug the GUI')
    
    parser.add_argument('--ext', action='append', default=['JPG'], dest='ext')
    
    args = parser.parse_args()
    ip = socket.gethostbyname(args.card_uri.hostname)
    
    if(not os.path.isdir(args.folder_local)):
        print("Given folder(local) does not exist or isn't a folder!",  end='\n', file=sys.stderr)
        exit(1)
        
    if((args.instant or args.debug_image!=None) and not args.processing==ImageView):
        print("Selected GUI option without selecting GUI!",  end='\n', file=sys.stderr) 
        exit(1)
        
    if(args.debug_image != None):
        if(not os.path.isfile(args.debug_image)):            
            print("Debug image file does not exist!", end='\n', file=sys.stderr)
            exit(1)
        
    args.processing(args)
        
    
