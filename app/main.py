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

# The Haar Cascade Linux Tool Requirement:
#
# conda create -n haar_trainer_opencv
# conda activate haar_trainer_opencv
# conda install py-opencv=3.4.2 (minimum requirement)
#
# Usage: python3 main.py

posSampleTempFile = "pos_sample_temp.lst"
negSampleTempFile = "neg_sample_temp.lst"
openCV_checkRev = "3.4.2"

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

def open_input_dir_chooser():
    location = fileDialog.askdirectory()
    print("Input dataset dir: ", location)
    input_entry_variable.set(location)

def generate_dataset_list():
    purge_folder_files(input_entry_variable.get())    # remove all previous vector & pos/neg list files

    # build pos/neg image file lists for creating samples and training classifier
    included_extensions = ['jpg','jpeg','png']
    try:
        filelist = [fn for fn in os.listdir(input_entry_variable.get()+"/n")
                    if any(fn.lower().endswith(ext) for ext in included_extensions)]
        with open(input_entry_variable.get()+"/neg.lst", 'w') as output:
            for item in filelist:
              output.write("n/" + item + "\n")
        output.close()
        print("Successfully generated: ", input_entry_variable.get()+"/neg.lst")
    except:
        sys.exit("ERROR: Couldn't generate ", input_entry_variable.get()+"/neg.lst")
    try:
        filelist = [fn for fn in os.listdir(input_entry_variable.get()+"/p")
                    if any(fn.lower().endswith(ext) for ext in included_extensions)]
        with open(input_entry_variable.get()+"/pos.lst", 'w') as output:
            for item in filelist:
              output.write("p/" + item + "\n")
        output.close()
        print("Successfully generated: ", input_entry_variable.get()+"/pos.lst")
    except:
        sys.exit("ERROR: Couldn't generate ", input_entry_variable.get()+"/pos.lst")
    generate_positive_sample_list()

        
def generate_positive_sample_list():
    purge_folder_files(input_entry_variable.get()+"/classifier")    # remove all previous classifier param/stage contents

    # open positive list file 
    try:
        pos_list = open(input_entry_variable.get()+"/pos.lst")
    except:
        sys.exit("ERROR: Unable to open ", input_entry_variable.get()+"/pos.lst")
    posImgs = pos_list.readlines()

    # create positive sample list w/ image params for opencv_createsamples
    if os.path.isfile(posSampleTempFile):   
        os.remove(posSampleTempFile) 
    try: 
        pos_sample_list = open(posSampleTempFile, 'a')
    except:
        sys.exit("ERROR: Unable to open ", input_entry_variable.get()+"/"+posSampleTempFile)
    for i in range (0, len(posImgs)):
        posImgPath = input_entry_variable.get()+"/"+posImgs[i].split('\n')[0]
        try:
            height = cv.imread(posImgPath).shape[0]
            width = cv.imread(posImgPath).shape[1]
        except:
            sys.exit("ERROR: Could not open image file: "+posImgs[i].split('\n')[0])
        pos_sample_list.write(posImgPath+" 1 0 0 "+str(width)+" "+str(height)+"\n")

    # cleanup file i/o
    pos_sample_list.close()
    pos_list.close()

    generate_positive_vector()

def generate_positive_vector():
    try:
        pos_sample_list = open(posSampleTempFile)
    except:
        sys.exit("ERROR: Unable to read file: ", posSampleTempFile)
    pos_sample_num = len(pos_sample_list.readlines())
    # create positive vector list file for cascade trainer
    try:
        print("Creating samples vector file ", input_entry_variable.get()+"/pos_samples.vec")
        os.system("opencv_createsamples " + "-info "+posSampleTempFile+" -num "+str(pos_sample_num)+" -w "+image_width_variable.get()+" -h "+image_height_variable.get()+" -vec "+input_entry_variable.get()+"/pos_samples.vec")
    except:
        sys.exit("ERROR: Unable to create file: ", posSampleTempFile)

    # cleanup file i/o
    pos_sample_list.close()
    os.remove(posSampleTempFile) 

    train_classifier(pos_sample_num)
    
def train_classifier(pos_sample_num):
    retVal = 0

    # reduce positive sample num usage % if required to help cascade training for weaker positive datasets
    total_pos = str(int((int(sample_usage_percent_variable.get())/100)*pos_sample_num))

    # get negative sample size to use for training classifier
    try:
        neg_list=open(input_entry_variable.get()+"/neg.lst")
    except:
        sys.exit("ERROR: Unable to open neg.lst files at "+input_entry_variable.get()+"/neg.lst")
    negImgs = neg_list.readlines()
    total_neg = str(len(negImgs))

    # create negative temp sample list w/ absolute paths for opencv_traincascade
    if os.path.isfile(negSampleTempFile):   
        os.remove(negSampleTempFile) 
    try: 
        neg_sample_list = open(negSampleTempFile, 'a')
    except:
        sys.exit("ERROR: Unable to open ", input_entry_variable.get()+"/"+negSampleTempFile)
    for i in range (0, len(negImgs)):
        neg_sample_list.write(input_entry_variable.get()+"/"+negImgs[i].split('\n')[0]+"\n")

    # make classifier folder if needed for training 
    try:
        os.system("./dir_gen.sh "+input_entry_variable.get())
    except:
        sys.exit("ERROR: Couldn't make classifier directory at "+input_entry_variable.get()+" | Possible error in execution on ./dir_gen.sh")

    # Train cascade using positive vector list created by createSamples
    try:
        retVal = sp.call(("opencv_traincascade -data "+input_entry_variable.get()+"/classifier -vec "+input_entry_variable.get()+"/pos_samples.vec -bg "+
                 negSampleTempFile+" -numPos "+total_pos+" -numNeg "+total_neg+" -numStages "+num_stage_variable.get()+
                 " -w "+image_width_variable.get()+" -h "+image_height_variable.get()+" -mode "+mode_variable.get()+" -numThreads "+num_threads_variable.get()+
                 " -precalcValBufSize "+val_buf_size_variable.get()+" -precalcIdxBufSize "+index_buf_size_variable.get()+
                 " -acceptanceRatioBreakValue "+acceptance_ratio_break_variable.get()+" -minHitRate "+min_hit_rate_variable.get()+
                 " -maxFalseAlarmRate "+max_false_alarm_rate_variable.get()+" -bt "+boost_type_variable.get()+" -featureType "+feature_type_variable.get()).split(' '))

    except:
        print("ERROR: couldn't train network for some unknown error!")
        retVal = -99

    # cleanup file i/o
    neg_sample_list.close()
    os.remove(negSampleTempFile) 
    neg_list.close()

    training_results(retVal)

def training_results(errorVal):
    update_start_btn("Start")
    if errorVal != 0:
        print("Training Unsuccessful")
        message.showinfo('Training Unsuccessful','Unable to train HAAR Cascade, error: ' + str(errorVal))
    else:
        print("Training Completed Successfully")
        message.showinfo('Successful','Your HAAR Cascade has been successfully trained. The classifier is located at '+input_entry_variable.get()+"/classifier")
        
def start_training():
    if check_val():
        update_start_btn("Training classifier...")
        generate_dataset_list()

def update_start_btn(text):
    start_btn_text.set(text)
    start_btn.update_idletasks()   # force update control

def check_val(): 
    if str(cv.__version__) != openCV_checkRev:
        message.showinfo("Invalid openCV Version!","HAAR Cascade Trainer requires OpenCV v" + openCV_checkRev + ", 'install py-opencv=3.4.2`.")
        return False
    if input_entry_variable.get() == "":
        message.showinfo("Invalid Classifier Samples Folder!","HAAR Cascade Trainer requires valid classifier samples folder containing path to p/n dataset folders.")
        return False
    return True

def purge_folder_files(directory_path):
    if os.path.isdir(directory_path): 
        try:
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files deleted successfully from: ", directory_path)
        except OSError:
            print("Error occurred while deleting files from: ",directory_path )
  
# Starting the application and checking all required libraries
try:
    os.system('sudo echo Starting...')
except:
    sys.exit('Run as a super user!')
python_version = sys.version
check_env()

#Creating UI
main_window = tk.Tk()
main_window.title("HAAR CASCADE CLASSIFIER TRAINER")
main_window.resizable(0,0)

task_status = tk.StringVar()
task_status.set("HAAR Cascade Trainer v1.1 | OpenCV v" + str(cv.__version__) )
head_status = tk.Label(main_window, textvariable=task_status, bg="#33ff8a", pady=3).grid(column=0,row=0, columnspan=3, sticky="ew")

input_label = tk.Label(main_window,text="Classifier samples folder:", pady=3).grid(column=0,row=3, sticky="ew")
input_entry_variable = tk.StringVar()
input_entry = tk.Entry(main_window, textvariable=input_entry_variable).grid(column=1, row=3, sticky="ew")
input_entry_btn = tk.Button(text="...", height = 1, width=5, command = open_input_dir_chooser).grid(column=2, row=3, sticky="ew")

image_width_label = tk.Label(main_window, text="Sample Image: WIDTH", pady=3).grid(column=0, row=4, sticky="ew")
image_width_variable = tk.StringVar()
image_width_variable.set('24')
image_width_entry = tk.Spinbox(main_window, from_=5, to=50, textvariable=image_width_variable).grid(column=1, row=4, sticky="ew")

image_height_label = tk.Label(main_window, text="Sample Image: HEIGHT", pady=3).grid(column=0, row=5, sticky="ew")
image_height_variable = tk.StringVar()
image_height_variable.set('24')
image_height_entry = tk.Spinbox(main_window, from_=5, to=50, textvariable=image_height_variable).grid(column=1, row=5, sticky="ew")

sample_usage_percent_label = tk.Label(main_window, text="Sample image usage percent(%)", pady=3).grid(column=0,row=6, sticky="ew")
sample_usage_percent_variable = tk.StringVar()
sample_usage_percent_variable.set('100')
sample_usage_percent_entry = tk.Spinbox(main_window, from_=0, to=100, textvariable=sample_usage_percent_variable).grid(column=1, row=6, sticky="ew")

num_stage_label = tk.Label(main_window, text="Number of training stages", pady=3).grid(column=0,row=7, sticky="ew")
num_stage_variable = tk.StringVar()
num_stage_variable.set('20')
num_stage_enter = tk.Spinbox(main_window, from_=1, to=30, textvariable=num_stage_variable).grid(column=1,row=7, sticky="ew")

num_threads_label = tk.Label(main_window, text="Number of threads to use", pady=3).grid(column=0,row=8, sticky="ew")
num_threads_variable = tk.StringVar()
num_threads_variable.set('5')
num_threads_enter = tk.Spinbox(main_window, from_=1, to=10, textvariable=num_threads_variable).grid(column=1,row=8, sticky="ew")

val_buf_size_label = tk.Label(main_window, text="Precalculated feature value buffer size (MB)", pady=3).grid(column=0,row=9, sticky="ew")
val_buf_size_variable = tk.StringVar()
val_buf_size_variable.set('1024')
val_buf_size_enter = tk.Spinbox(main_window, from_=1, to=100000, textvariable=val_buf_size_variable).grid(column=1,row=9, sticky="ew")

index_buf_size_label = tk.Label(main_window, text="Precalculated feature index buffer size (MB)", pady=3).grid(column=0,row=10, sticky="ew")
index_buf_size_variable = tk.StringVar()
index_buf_size_variable.set('1024')
index_buf_size_enter = tk.Spinbox(main_window, from_=1, to=100000, textvariable=index_buf_size_variable).grid(column=1,row=10, sticky="ew")

acceptance_ratio_break_label = tk.Label(main_window, text="Acceptance ratio break value", pady=3).grid(column=0,row=11, sticky="ew")
acceptance_ratio_break_variable = tk.StringVar()
acceptance_ratio_break_variable.set('-1')
acceptance_ratio_break_enter = tk.Entry(main_window, textvariable=acceptance_ratio_break_variable).grid(column=1,row=11, sticky="ew")

min_hit_rate_label = tk.Label(main_window, text="Minimal hit rate", pady=3).grid(column=0,row=12, sticky="ew")
min_hit_rate_variable = tk.StringVar()
min_hit_rate_variable.set('0.9950')
min_hit_rate_enter = tk.Spinbox(main_window, from_=0.5, to=1, increment=0.0001, textvariable=min_hit_rate_variable).grid(column=1,row=12, sticky="ew")

max_false_alarm_rate_label = tk.Label(main_window, text="Maximal false alarm rate", pady=3).grid(column=0,row=13, sticky="ew")
max_false_alarm_rate_variable = tk.StringVar()
max_false_alarm_rate_variable.set('0.50')
max_false_alarm_rate_enter = tk.Spinbox(main_window, from_=0, to=1, increment=0.01, textvariable=max_false_alarm_rate_variable).grid(column=1,row=13, sticky="ew")

# More options here

feature_type_label = tk.Label(main_window, text="Classifier feature type to use", pady=3).grid(column=0,row=17, sticky="ew")
feature_type_options = ["HAAR", "LBP"]
feature_type_variable = tk.StringVar()
feature_type_variable.set(feature_type_options[0])
feature_type_enter = tk.OptionMenu(main_window, feature_type_variable, *feature_type_options).grid(column=1,row=17, sticky="ew")

boost_type_label = tk.Label(main_window, text="Boosted classifier type to use", pady=3).grid(column=0,row=18, sticky="ew")
boost_type_options = ["GAB", "RAB", "LB", "DAB"]
boost_type_variable = tk.StringVar()
boost_type_variable.set(boost_type_options[0])
boost_type_enter = tk.OptionMenu(main_window, boost_type_variable, *boost_type_options).grid(column=1,row=18, sticky="ew")

mode_label = tk.Label(main_window, text="HAAR feature set to use", pady=3).grid(column=0,row=19, sticky="ew")
mode_options = ["BASIC", "CORE", "ALL"]
mode_variable = tk.StringVar()
mode_variable.set(mode_options[2])
mode_enter = tk.OptionMenu(main_window, mode_variable, *mode_options).grid(column=1,row=19, sticky="ew")

start_btn_text = tk.StringVar()
start_btn_text.set("Start")
start_btn = tk.Button(main_window,textvariable=start_btn_text, fg = "#000000", bg = "#00FF55", height = 2, width = 20, command = start_training)
start_btn.grid(column=0,row=20,columnspan=3,sticky="ew")

# developer_label = tk.Label(main_window, bg="#000000", fg="#ffffff", text="Developed by github.com/amannirala13").grid(column = 0, row=10, columnspan = 3, sticky="ew")

main_window.mainloop()