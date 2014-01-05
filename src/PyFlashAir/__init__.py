'''
Created on Jan 4, 2014

@author: cyborg-x1
'''
from PyFlashAir import flashair

if __name__ == '__main__':
    
    print(len(flashair.command.Disable_Photo_Share_mode))
    a=flashair.connection('192.168.0.16', 80,1000)
    print(a.get_file_list('/'))
    pass