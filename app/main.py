missing=[]
import os
import sys
import subprocess as sp
try:
    import tkinter as tk
    import tkinter.filedialog as fileDialog
except:
    import Tkinter as tk
    import tkFileDialog as fileDialog
    
def avail_network():
    available = True
    try:
        sp.check_output('./net_test.sh', shell=True)
    except:
        available = False
    return available

def prepare_env(missing):
    if avail_network() == False:
        print("SHOW NETWORK ERROR MESSAGE")
        sys.exit("Couldn't install required packages. Check your internet connection")
    else:
        if 'git' in missing:
            os.system('sudo apt-get install -y git')
        if 'libopencv' in missing:
            os.system('sudo apt-get install -y build-essential')
            os.system('sudo apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev')
            os.system('sudo apt-get install -y libopencv-dev')
        if 'PIL' in missing:
            if python_version[0] =='3':
                os.system('pip3 install Pillow')
            else:
                os.system('pip install Pillow')
        if 'opencv' in missing:
            if python_version[0] =='3':
                os.system('sudo apt-get install -y python3-opencv')
            else:
                os.system('sudo apt-get install -y python-opencv')
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
        from PIL import Image
    except:
        print("PIL missing")
        missing.append("PIL")
    try:
        import cv2 as cv
    except:
        print("OpenCV missing")
        missing.append("opencv")
        
    if(missing != []):
        print("Downloading and install following packages: ",missing)
        prepare_env(missing)
    else:
        print("Environment ready!")
        
def open_pos_dir_chooser():
    location = fileDialog.askdirectory()
    print("Positive Dir selected: ", location)
    positive_entry_variable.set(location)
    
def open_neg_dir_chooser():
    location = fileDialog.askdirectory()
    print("Negative Dir selected: ", location)
    negative_entry_variable.set(location)
    
def open_out_dir_chooser():
    location = fileDialog.askdirectory()
    print("Output Dir selected: ", location)
    output_entry_variable.set(location)
    
def generate_index():
    try:
        os.system("find "+negative_entry_variable.get()+" -name '*.png' -o -name '*.jpg' > "+negative_entry_variable.get()+"/index.txt")
        print("Successfully generated negative images index")
    except:
        print("ERROR: Couldn't generate negative images index file")
    try:
        os.system("find "+positive_entry_variable.get()+" -name '*.png' -o -name '*.jpg' > "+positive_entry_variable.get()+"/index.txt")
        print("Successfully generated positive images index")
    except:
        print("ERROR: Couldn't generate positive images index file")
        
def start_training():
    print("training")
    print("Positive image location: ",positive_entry_variable.get())
    print("Negative image location: ",negative_entry_variable.get())
    generate_index()

#Starting the application and checking all required libraries
try:
    os.system('sudo echo Starting...')
except:
    sys.exit('Are you drunk? Run it as a super user!')
python_version = sys.version
check_env()

#Creating UI
main_window = tk.Tk()
main_window.title("HAAR CASCADE CLASSIFIER")

head_status = tk.Label(main_window, text="Starting", bg="#33ff8a", pady=3).grid(column=0,row=0, columnspan=1)

positive_lable = tk.Label(main_window,text="Positive image dataset location", pady=3).grid(column=0,row=1)
positive_entry_variable = tk.StringVar()
positive_entry = tk.Entry(main_window, textvariable=positive_entry_variable).grid(column=1, row=1)
positive_entry_btn = tk.Button(text="...", height = 2, width=10, command = open_pos_dir_chooser).grid(column=2, row=1)

negative_lable = tk.Label(main_window,text="Negative image dataset location", pady=3).grid(column=0,row=2)
negative_entry_variable = tk.StringVar()
negative_entry = tk.Entry(main_window, textvariable=negative_entry_variable).grid(column=1, row=2)
negative_entry_btn = tk.Button(text="...", height = 2, width=10, command = open_neg_dir_chooser).grid(column=2, row=2)

output_lable = tk.Label(main_window,text="Output location", pady=3).grid(column=0,row=3)
output_entry_variable = tk.StringVar()
output_entry = tk.Entry(main_window, textvariable=output_entry_variable).grid(column=1, row=3)
output_entry_btn = tk.Button(text="...", height = 2, width=10, command = open_out_dir_chooser).grid(column=2, row=3)

start_btn = tk.Button(main_window,text="Start", fg = "#000000", bg = "#00FF55", height = 2, width = 20, command = start_training).grid(column=0,row=4)

main_window.mainloop()