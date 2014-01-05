'''
Created on Jan 4, 2014

@author: cyborg-x1
'''
from PyFlashAir import flashair
import time

if __name__ == '__main__':
    a=flashair.connection('192.168.0.16', 80,1000)
    #print(a.send_command(flashair.command.Get_file_list,directory='/'))
    while True:
        print('sync')
        a.sync_folder_to_remote_folder('/DCIM/101EOS5D', '/home/cyborg-x1/dwhelper')
        time.sleep(1)
    pass