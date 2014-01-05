'''
Created on Jan 4, 2014

Licence: GNU AGPL

@author: Christian Holl
'''
from PyFlashAero import flashair
import time

if __name__ == '__main__':
    #                     Host/IP         Port    Timeout   
    a=flashair.connection('192.168.0.16', 80,1000)
    while True:
        #                          REMOTE_FOLDER   DOWNLOAD DIRECTORY
        a.sync_folder_to_remote_folder('/DCIM/', '/downloaddir')
    pass 