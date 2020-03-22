# Installing required packages! 
# -----------------------------------------------------------------------------
# Update the pakages in your environment
#  sudo apt-get update
#  sudo apt-get upgrade

# If they are missing, install them using the following commands
#  sudo apt-get install python3
#  sudo apt-get install git

# Clone the OpenCV project repository (NOT NEEDED FOR TRAINING)
#  git clone https://github.com/opencv/opencv.git

# Install required build files
#  sudo apt-get install build-essential

# (POSSIBLE NOT REQUIRED)
#  sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

# Install development liberaries required for training model
#  sudo apt-get install libopencv-dev

# ------------------------------------------------------------------------------
# Guidlines for prepating the working folder
# 1. Make a positive folder with the images of the target object
# 2. Make a negative folder with the images without the traget object
# 3. Create a Data and Info folder for storing the cascade.xml and training sets respectively
# -------------------------------------------------------------------------------

# !Creating index files for negative and positive containing their file names
# -------------------------------------------------------------------------------
#  find ./Negative_Images -name '*.png' > negative.txt
#  find ./Positive_Images -name '*.png' > positive.txt
# -------------------------------------------------------------------------------

# Creating sample images for training (SKIP IF YOU ALREADY HAVE A PREFECTLY LABELED
# POSITIVE IMAGES LIST)
# -------------------------------------------------------------------------------
#  opencv_createsamples -img <target_image> -bg <negative.txt> -info info/positive.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num <little_less_than_num_of_negatives>
# -------------------------------------------------------------------------------

# !Creating Vector(.vec) file from the positive.list or the labeled list of the positive images
# -------------------------------------------------------------------------------
#  opencv_createsamples -info info/positive.lst -num 1950 -w 20 -h 20 -vec positives.vec
# -------------------------------------------------------------------------------

# Train Classifier
# -------------------------------------------------------------------------------
#  opencv_traincascade -data data -vec positives.vec -bg negative.txt -numPos <total_number_of_positive_images> -numNeg <half_of_total_positive> -numStages <no_of_times_it_should_itter> -w <width_of_trarget_image> -h <height_of_target_image>
# -------------------------------------------------------------------------------