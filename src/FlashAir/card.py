'''
Created on Jan 4, 2014

Licence: GNU AGPL

@author: Christian Holl
'''

import os
import http.client

class file_list_entry(object):
    file_name=''
    directory_name=''
    byte_size=-1
    attribute_Archive=False;
    attribute_Directly=False;
    attribute_Volume=False;
    attribute_System=False;
    attribute_Hidden=False;
    attribute_ReadOnly=False;
    date_human=()
    time_human=()
    time=0
    date=0
    def __init__(self, file_name, directory_name, size, attributes, date, time):
        self.file_name=file_name
        self.directory_name=directory_name
        self.byte_size=size
        

        
        attributes=int(attributes)
        self.attribute_Archive=  not not(attributes & 1<<5)
        self.attribute_Directly= not not(attributes & 1<<4)
        self.attribute_Volume=   not not(attributes & 1<<3)
        self.attribute_System=   not not(attributes & 1<<2)
        self.attribute_Hidden=   not not(attributes & 1<<1)
        self.attribute_ReadOnly= not not(attributes & 1<<0)

        time=int(time)
        self.time=time;
        self.time_human=(((time&(0x1F<<11))>>11),((time&(0x3F<<5))>>5),(time&(0x1F))*2)
    
        date=int(date)
        self.date=date;
        self.date_human=(((date&(0x3F<<9))>>9)+1980,((date&(0x1F<<5))>>5),date&(0x1F))
        
        
class command(object):
    '''OPCODE - DIR DATE ADDR LENGTH DATA  REQUIRED FWVERSION (Bigger/Smaller)'''
    Get_file_list=                      (100,1,0,0,0,0,'1.00.03',True)
    Get_the_number_of_files=            (101,1,0,0,0,0,'1.00.00',True)
    Get_update_status=                  (102,0,0,0,0,0,'1.00.00',True)
    Get_SSID=                           (104,0,0,0,0,0,'1.00.00',True)
    Get_network_password=               (105,0,0,0,0,0,'1.00.00',True)
    Get_MAC_address=                    (106,0,0,0,0,0,'1.00.00',True)
    Set_browser_language=               (107,0,0,0,0,0,'1.00.00',True)
    Get_the_firmware_version=           (108,0,0,0,0,0,''       ,True)
    Get_the_control_image=              (109,0,0,0,0,0,'2.00.00',True)
    Get_Wireless_LAN_mode=              (110,0,0,0,0,0,'2.00.00',True)
    Set_Wireless_LAN_timeout_length=    (111,0,0,0,0,0,'2.00.00',True)
    Get_application_unique_information= (117,0,0,0,0,0,'2.00.00',True)
    Get_CID=                            (120,0,0,0,0,0,'1.00.03',True)
    Get_data_from_shared_memory=        (130,0,0,1,1,0,'2.00.00',True)
    Set_data_to_shared_memory=          (131,0,0,0,0,0,'2.00.00',True)
    Get_the_number_of_empty_sectors=    (140,0,0,0,0,0,'1.00.03',True)
    Enable_Photo_Share_mode=            (200,0,0,0,0,0,'2.00.00',True)
    Disable_Photo_Share_mode=           (201,0,0,0,0,0,'2.00.00',True)
    Get_Photo_Share_mode_status=        (202,0,0,0,0,0,'2.00.00',True)
    Get_SSID_for_Photo_Share_mode=      (203,0,0,0,0,0,'2.00.00',True)
          
class connection(object):
    '''
    classdocs
    '''
    
    
    list_directory=100
    fwversion=''
    host=0
    port=0
    timeout=0
    start_date=-1
    start_time=-1
    
    def __init__(self, host, port, timeout):
        '''
        Constructor
        '''
        self.host=host
        self.port=port
        self.timeout=timeout
  
        
    def send_command(self, opcode, directory='', date=-1, addr=-1, data=(), length=-1):
        if(len(opcode)==8):
            url="/command.cgi?op=" + str(opcode[0])
    
            if(opcode[1] and len(directory)==0 ):     
                print("ERROR Oppcode " + str(opcode[0]) + " requires directory")
                return(-1,'')
            elif(opcode[1]):
                url += '&DIR=' + directory
            
            if(opcode[2] and date<0 ):    
                print("ERROR Oppcode " + str(opcode[0]) + " requires date")
                return(-1,'')
            elif(opcode[2]):
                url += '&DATE=' + date
            
            if(opcode[3] and addr<0 ):      
                print("ERROR Oppcode " + str(opcode[0]) + " requires addr")
                return(-1,'')
            elif(opcode[3]):
                url += '&ADDR=' + str(addr)
            
            if(opcode[4] and length==0 ):      
                print("ERROR Oppcode " + str(opcode[0]) + " requires length")
                return(-1,'')
            elif(opcode[4]):
                url += '&LEN=' + str(length)
            
            if(opcode[5] and len(data)==0 ):      
                print("ERROR Oppcode " + str(opcode[0]) + " requires data")
                return(-1,'')
            elif(opcode[5]):
                url += '&DATA=' + data

            #Is it a firmware query?
            if(len(opcode[6])!=0):

                if(len(self.fwversion)==0):

                    (ret, ver)=self.send_command(command.Get_the_firmware_version)
                    if(not ret):
                        self.fwversion=ver.decode("utf-8")[9:]
                        print("Firmware is: ")
                        print(self.fwversion)
                    else:
                        if(ret!=-2):
                            print("ERROR: Could not determine firmware version!")
                        return(-1,'')
                    
                if(opcode[7]): #must be bigger than or equal to firmware version
                    if(opcode[6]>self.fwversion):
                        print("ERROR Opcode " + str(opcode[0]) + " not supported in firmware!")
                        return(-1,'')
                else:
                    if(opcode[6]>self.fwversion):
                        print("ERROR Opcode " + str(opcode[0]) + " not supported in firmware!")
                        return(-1,'')
            
                
            #Connect
            connection = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)

            try:
                connection.request("GET", url) 
                response=connection.getresponse();
                return (response.status!=200,response.read())
            except:
                return (-2,'')
                pass
            
        
    def get_file_list(self,directory):
        (ret,lst)=self.send_command(command.Get_file_list,directory=directory)
        
        if(ret==0):
            
            lines=lst.decode("utf-8").split("\r\n")
            if(lines[0]=="WLANSD_FILELIST"):
                lines=lines[1:-1] #skip headline, and current dir at the end
            else:
                return (0,())
                        
            outlst=[]
            for file in lines:
                e=file.split(",")
                
                if(len(e)!=6):
                    print("Error file list entry has " +str(len(e)) +" entrie(s) instead of expected 6, skipping entry")
                    continue;
                #(file_name, directory_name, size, attributes, date, time):
                f=file_list_entry(e[1],e[0],int(e[2]),int(e[3]),int(e[4]),int(e[5]))
                outlst.append(f)                
                
            return (0,outlst)
        else:
            return (1,())
        
    def download_file(self, remote_location, local_path='', local_file_name=''):
        conn = http.client.HTTPConnection(self.host)
        if(len(local_file_name)==0):
            local_file_name = remote_location.split('/')[-1]
        file_size=0


        #does folder exist?
        if(not os.access(local_path, os.R_OK)):
            return (2,0,'')
        
        #add / if it is not there already
        if(len(local_path)!=0 and local_path[-1]!='/'):
            local_path+='/'
        
        #combine path and file
        local_path+=local_file_name
                        
        #does file exist already?
        if(os.path.isfile(local_path)):  
            return (3,0,'')
        
        print("Downloading:" + local_file_name)
        #get the stuff from the FlashAir
        conn.request("GET", remote_location)
        download = conn.getresponse()
        file = open(local_path, 'wb')   
        if(download.status==200):

            while True:
                buffer=download.read(1024*8)
                if not buffer:
                    break;
                file_size += len(buffer) 
                file.write(buffer)
            file.close()
        return (int(download.status!=200), file_size,local_path)
    
    def download_file_list_entry(self, entry,local_path='', local_filename=''):
        (status,size,local_filename)=self.download_file(entry.directory_name + '/' + entry.file_name, local_path, local_filename)
        if(status):
            return(1)
        
        
        if(size!=entry.byte_size):
            print("Error Size does not match")
            os.remove(local_filename)
            return(2)

        return(0)

    def sync_folder_to_remote_folder(self,remote_path='',local_path='',extensions=['JPG']):
        #all extensions to upper case
        extensions=[x.upper() for x in extensions]
        
        #get list of remote files
        (status, outlist)=self.get_file_list(remote_path)
        if(not status and len(outlist)):
            if(not os.access(local_path, os.R_OK)):
                return 2
            for entry in outlist:
                if ((entry.file_name.split('.')[-1].upper() in extensions) or len(extensions)==0):
                    self.download_file_list_entry(entry, local_path)

    def sync_new_pictures_since_start(self,remote_path='',local_path='',extensions=['JPG']):
        last_file=''
        
        #all extensions to upper case
        extensions=[x.upper() for x in extensions]
        
        #get list of remote files
        (status, outlist)=self.get_file_list(remote_path)
        
        #determine latest file date and time
        
        if(self.start_date < 0):
            last_entry=None
            for entry in outlist:
                if(entry.date>self.start_date):
                    self.start_date=entry.date
                    self.start_time=entry.time
                    last_entry=entry
                elif (entry.date==self.start_date):
                    if(entry.time>self.start_time):
                        self.start_time=entry.time
                        last_entry=entry
            if(last_entry!=None):
                last_file=local_path+'/'+last_entry.file_name
                self.download_file_list_entry(last_entry, local_path) #download latest file
                
        if(not status and len(outlist)):
            if(not os.access(local_path, os.R_OK)):
                return ()
            for entry in outlist:
                if ((entry.file_name.split('.')[-1].upper() in extensions) or len(extensions)==0):
                    if(entry.date>=self.start_date):
                        if(entry.date>self.start_date or entry.time>self.start_time):
                            if(not self.download_file_list_entry(entry, local_path)):
                                last_file=local_path+'/'+entry.file_name    
        return last_file
