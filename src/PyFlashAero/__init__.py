'''
Created on Jan 4, 2014

Licence: GNU AGPL

@author: Christian Holl
'''
from PyFlashAero import flashair

if __name__ == '__main__':
    a=flashair.connection('192.168.0.16', 80,1000)
    #print(a.send_command(flashair.command.Get_file_list,directory='/'))
    while True:
        a.sync_new_pictures_since_start('/DCIM/101EOS5D', '/home/cyborg-x1/dwhelper')
        pass