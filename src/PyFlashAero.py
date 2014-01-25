'''
Created on Jan 25, 2014

@author: cyborg-x1
'''

from PyQt4 import QtGui
from FlashAir import card
from FlashAir import ImageViewer
from urllib.parse import urlparse
import argparse
import socket
import sys

def ImageView(ip, port):
  print("imageView")
  
  
  
  

def SyncFolder(ip, port):
  print("SyncFolder")
  a=card.connection(ip, port,1000)
  print(a.send_command(card.command.Get_file_list,directory='/'))
  while True:
      a.sync_new_pictures_since_start('/DCIM/101EOS5D', '/home/cyborg-x1/dwhelper')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyFlashAero, Download Tool for Toshiba FlashAir SD-Cards')
    parser.add_argument('card_uri', type=urlparse, help='The url to the FlashAir Card')
    parser.add_argument('--ImageViewer', dest='processing', action='store_const',
                        const=ImageView, default=SyncFolder,
                        help='Shows the GUI')
    
    args = parser.parse_args()
    ip = socket.gethostbyname(args.card_uri.hostname)
    port = args.card_uri.port    
    
    



    #parser.add_argument('--ip')
     
    #app = QtGui.QApplication(sys.argv)
    #imageViewer = ImageViewer.ImageViewer()
    #imageViewer.show()
    #sys.exit(app.exec_())