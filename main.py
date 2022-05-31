import platform
import getpass
import os
import json
import subprocess
from OSC import OSCClient, OSCMessage, OSCServer
import time
import threading
import socket
import sys

PORT = 12344
MAIN_PATH = "/home/Documents/osc_rpi_shutdown"

class SimpleServer(OSCServer):
    def __init__(self, t):
        OSCServer.__init__(self, t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    def handleMsg(self, oscAddress, tags, data, client_address):

        print("OSC message received on : "+oscAddress)
        print("data: ")
        print(data)

        splitAddress = oscAddress.split("/") 

        ############## RPI itself #############
        if(splitAddress[1] == "rpi"):
            if(splitAddress[2] == "shutdown"):
                print("Turning off the rpi")
                powerOff() 
            if(splitAddress[2] == "reboot"):
                print("Reboot the machine")
                #setVeille(True) # NOT IMPLETEMED YET
                reboot() # 

def powerOff():

    time.sleep(5)
    print("========= POWER OFF ======")
    os.chdir(MAIN_PATH+"/script")
    subprocess.call(['./shutdown.sh'])

def reboot():

    time.sleep(5)
    print("========= POWER OFF ======")
    os.chdir(MAIN_PATH+"/script")
    subprocess.call(['./reboot.sh'])

def launchCmd(dir, cmd):
    try:
        os.chdir(dir)
        subprocess.Popen(cmd)
    except Exception as e:
        print(" error on running cmd " + str(cmd))
        print(e)

def get_ip():   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main():
  
    print(" ===== OSC_RPI_SHUTDOWN ====")
    # OSC SERVER
    print(" ===== OSC SERVER ====")
    myip = "0.0.0.0"
    #myip = get_ip()
    myport = PORT
    print("IP adress is : "+myip+" port="+str(myport))
    server = None
    while server == None :
        try: 
            server = SimpleServer((myip, myport))
            print("Server created on port :"+str(myport))
        except Exception as inst:
            print(" ERROR : creating server")
            print("Unexpected error:", sys.exc_info()[0])
            print(inst)
            print("retry now")
        time.sleep(1)

    try:
        st = threading.Thread(target=server.serve_forever)
    except:
        print(" ERROR : creating thread")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)
    try:
        st.start()
    except:
        print(" ERROR : starting thread")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)

    print(" OSC server is running")

    # MAIN LOOP
    global runningApp
    runningApp = True

    print(" ===== STARTING MAIN LOOP ====")
    while runningApp:
        # This is the main loop
        try:
            time.sleep(1)
        except:
            print("User attempt to close programm")
            runningApp = False

    # CLOSING THREAD AND SERVER
    print(" Ending programme")
    server.running = False
    print(" Join thread")
    st.join()
    print(" Close Server")
    server.close()
    print(" End of sript . Bye Bye")

if __name__ == "__main__":
    main()
