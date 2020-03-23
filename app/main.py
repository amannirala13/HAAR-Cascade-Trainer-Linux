import os
import sys
import subprocess as sp
try:
    import tkinter as tk
    import tkinter.filedialog as fileDialog
    import tkinter.messagebox as message
except:
    import Tkinter as tk
    import tkFileDialog as fileDialog
    import tkMessageBox as message
cv = None
   
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
        sys.exit("ERROR: Couldn't install required packages. Check your internet connection.")
    else:
        os.system('sudo apt-get update')
        if 'git' in missing:
            os.system('sudo apt-get install -y git')
        if 'libopencv' in missing:
            os.system('sudo apt-get install -y build-essential')
            os.system('sudo apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev')
            os.system('sudo apt-get install -y libopencv-dev')
        if 'opencv' in missing:
            if python_version[0] =='3':
                os.system('sudo apt-get install -y python3-opencv')
            else:
                os.system('sudo apt-get install -y python-opencv')
        missing = []
        check_env()


def check_env():
    missing = []
    try:
        os.system("git --version")
    except:
        print("Git missing")
        missing.append("git")
    try:
        os.system("opencv_createsamples")
    except:
        print("Create Samples missing")
        missing.append("libopencv")
    try:
        global cv
        import cv2 as cv_local
        cv = cv_local
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
        sys.exit("ERROR: Couldn't generate negative images index file.")
    try:
        os.system("find "+positive_entry_variable.get()+" -name '*.png' -o -name '*.jpg' > "+positive_entry_variable.get()+"/index.txt")
        print("Successfully generated positive images index")
    except:
        sys.exit("ERROR: Couldn't generate positive images index file.")
    generate_positive_list()

        
def generate_positive_list():
    if os.path.exists(output_entry_variable.get()+"/positive.lst"):
        os.remove(output_entry_variable.get()+"/positive.lst")
    try:
        index = open(positive_entry_variable.get()+"/index.txt")
    except:
        sys.exit("ERROR: Unable to open positive images index file.")
    images = index.readlines()
    try:
        pos_list = open("positive.lst", 'a')
    except:
        sys.exit("ERROR: Unable to open/create positive.lst file.")
    for i in range (0, len(images)):
        try:
            height = cv.imread(images[i].split('\n')[0]).shape[0]
            width = cv.imread(images[i].split('\n')[0]).shape[1]
        except:
            sys.exit("ERROR: Could not open image file: "+images[i].split('\n')[0])
        pos_list.write(images[i].split('\n')[0]+" 1 0 0 "+str(width)+" "+str(height)+"\n")
    pos_list.close()
    index.close()
    generate_positive_vector()

def generate_positive_vector():
    try:
        pos_list = open("positive.lst")
    except:
        sys.exit("ERROR: Unable to read the file at: ",output_entry_variable.get()+"/positive.lst")
    file_len = len(pos_list.readlines())
    usage_num = str(int((int(sample_usage_percent_variable.get())/100)*file_len))
    try:
        os.system("opencv_createsamples -info positive.lst -num "+usage_num+" -w "+image_width_variable.get()+" -h "+image_height_variable.get()+" -vec "+output_entry_variable.get()+"/positive.vec")
    except:
        sys.exit("ERROR: Unable to create file "+output_entry_variable.get()+"/positive.vec")
    pos_list.close()
    os.remove('positive.lst')
    train_classifier()
    
    
def train_classifier():
    try:
        pos_index=open(positive_entry_variable.get()+"/index.txt")
    except:
        sys.exit("ERROR: Unable to open positive index.txt files at "+positive_entry_variable.get()+"/index.txt")
    try:
        neg_index=open(negative_entry_variable.get()+"/index.txt")
    except:
        sys.exit("ERROR: Unable to open negative index.txt files at "+negative_entry_variable.get()+"/index.txt")
    total_pos = str(len(pos_index.readlines()))
    total_neg = str(len(neg_index.readlines()))
    try:
        os.system("./dir_gen.sh "+output_entry_variable.get())
    except:
        sys.exit("ERROR: Couldn't maike classifier directory at "+output_entry_variable.get()+" | Possible error in execution on ./dir_gen.sh")
    try:
        sp.call(("opencv_traincascade -data "+output_entry_variable.get()+"/classifier -vec "+output_entry_variable.get()+"/positive.vec -bg "+negative_entry_variable.get()+"/index.txt -numPos "+total_pos+" -numNeg "+total_neg+" -numStages "+num_stage_variable.get()+" -w "+image_width_variable.get()+" -h "+image_height_variable.get()).split(' '))
    except:
        sys.exit("ERROR: Couldnt train network for some unknown error!")
    pos_index.close()
    neg_index.close()
    training_successful()
    
def training_successful():
    start_btn_text.set("Start")
    print("Training Completed Successfully")
    message.showinfo('Successful','Your HAAR Cascade has been successfully trained. The classifier is located at '+output_entry_variable.get()+"/cascade")
        
def start_training():
    if check_val():
        start_btn_text.set("Training...")
        generate_index()
    else:
        message.showerror("Value error", "You have entered unexpected values, please check again... ")
        
def check_val():  # ToDo >>> Need to work on this function to check values range!
    return True

#Starting the application and checking all required libraries
try:
    os.system('sudo echo Starting...')
except:
    sys.exit('Are you drunk? Run it as a super user!')
python_version = sys.version
check_env()

#Creating UI
main_window = tk.Tk()
main_window.title("HAAR CASCADE CLASSIFIER TRAINER")
main_window.resizable(0,0)

task_status = tk.StringVar()
task_status.set("HAAR Cascade Trainer v1.0 | Environment read!")
head_status = tk.Label(main_window, textvariable=task_status, bg="#33ff8a", pady=3).grid(column=0,row=0, columnspan=3, sticky="ew")

positive_label = tk.Label(main_window,text="Positive image dataset location", pady=3).grid(column=0,row=1, sticky="ew")
positive_entry_variable = tk.StringVar()
positive_entry = tk.Entry(main_window, textvariable=positive_entry_variable).grid(column=1, row=1, sticky="ew")
positive_entry_btn = tk.Button(text="...", height = 1, width=5, command = open_pos_dir_chooser).grid(column=2, row=1, sticky="ew")

negative_label = tk.Label(main_window,text="Negative image dataset location", pady=3).grid(column=0,row=2, sticky="ew")
negative_entry_variable = tk.StringVar()
negative_entry = tk.Entry(main_window, textvariable=negative_entry_variable).grid(column=1, row=2, sticky="ew")
negative_entry_btn = tk.Button(text="...", height = 1, width=5, command = open_neg_dir_chooser).grid(column=2, row=2, sticky="ew")

output_label = tk.Label(main_window,text="Output location", pady=3).grid(column=0,row=3, sticky="ew")
output_entry_variable = tk.StringVar()
output_entry = tk.Entry(main_window, textvariable=output_entry_variable).grid(column=1, row=3, sticky="ew")
output_entry_btn = tk.Button(text="...", height = 1, width=5, command = open_out_dir_chooser).grid(column=2, row=3, sticky="ew")

image_width_label = tk.Label(main_window, text="Sample Image: WIDTH", pady=3).grid(column=0, row=4, sticky="ew")
image_width_variable = tk.StringVar()
image_width_variable.set('24')
image_width_entry = tk.Spinbox(main_window, textvariable=image_width_variable).grid(column=1, row=4, sticky="ew")

image_height_label = tk.Label(main_window, text="Sample Image: HEIGHT", pady=3).grid(column=0, row=5, sticky="ew")
image_height_variable = tk.StringVar()
image_height_variable.set('24')
image_height_entry = tk.Spinbox(main_window, textvariable=image_height_variable).grid(column=1, row=5, sticky="ew")

sample_usage_percent_label = tk.Label(main_window, text="Sample image usage percent(%)", pady=3).grid(column=0,row=6, sticky="ew")
sample_usage_percent_variable = tk.StringVar()
sample_usage_percent_variable.set('100')
sample_usage_percent_entry = tk.Spinbox(main_window, from_=0, to=100, textvariable=sample_usage_percent_variable).grid(column=1, row=6, sticky="ew")

num_satge_label = tk.Label(main_window, text="Number of training stages", pady=3).grid(column=0,row=7, sticky="ew")
num_stage_variable = tk.StringVar()
num_stage_variable.set('10')
num_stage_enter = tk.Spinbox(main_window, textvariable=num_stage_variable).grid(column=1,row=7, sticky="ew")

start_btn_text = tk.StringVar()
start_btn_text.set("Start")
start_btn = tk.Button(main_window,textvariable=start_btn_text, fg = "#000000", bg = "#00FF55", height = 2, width = 20, command = start_training).grid(column=0,row=8,columnspan=3,sticky="ew")

developer_label = tk.Label(main_window, bg="#000000", fg="#ffffff", text="Developed by github.com/amannirala13").grid(column = 0, row=9, columnspan = 3, sticky="ew")

main_window.mainloop()