'''
Created on Jan 4, 2014

Licence: GNU AGPL

@author: Christian Holl
'''
from PyFlashAero import flashair
from PyFlashAero import ImageViewer
from PyQt4 import QtGui

# if __name__ == '__main__':
#     print("PyFlashAero")
#     a=flashair.connection('192.168.0.16', 80,1000)
#     print(a.send_command(flashair.command.Get_file_list,directory='/'))
#     while True:
#         a.sync_new_pictures_since_start('/DCIM/101EOS5D', '/home/cyborg-x1/dwhelper')
#         pass



if __name__ == '__main__':
 
    import sys
 
    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer.ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())