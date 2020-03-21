import tkinter as tk
import os
import subprocess as sp

def avail_network():
    available = True
    try:
        sp.check_output('./net_test.sh')
    except:
        available = False
    return available

def prepare_env(missing):
    if avail_network() == False:
        print("SHOW NETWORK ERROR MESSAGE")
    else:
        if 'git' in missing:
            os.system('sudo apt-get install -y git')
        if 'libopencv' in missing:
            os.system('sudo apt-get install -y build-essential')
            os.system('sudo apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev')
            os.system('sudo apt-get install -y libopencv-dev')
        if 'opencv' in missing:
            os.system('sudo apt-get install -y python3-opencv')
        check_env()

def check_env():
    try:
        os.system("git --version")
    except:
        print("Git missing")
        missing.append("git")
    try:
        
        os.system("opencv_createsamples --help")
    except:
        print("Create Samples missing")
        missing.append("libopencv")
    try:
        import cv2 as cv
    except:
        print("OpenCV missing")
        missing.append("opencv")
    if(missing != []):
        prepare_env(missing)

#Starting the application and checking all required libraries
missing=[]
os.system('sudo echo Starting...')
check_env()

main_window = tk.Tk()
main_window.title("HAAR CASCADE CLASSIFIER")