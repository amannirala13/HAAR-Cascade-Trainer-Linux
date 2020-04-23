# HAAR Cascade GUI Trainer 1.0 - Linux
This is a HAAR Cascade Classifier training GUI application for Linux. This application make it really easy to train classifiers for object detection and tracking using opencv by providing a Graphical user interface to set parameters and perform necessary steps.

<br>

# 🦺 Requirements
This script has some minimum system requirements to run. They are listed as follows:
<details>
<summary><b>Linux based system/terminal</b></summary>

This application runs shell scripts with Linux specific commands. So, you would need a linux based system to perform tasks with the application.<br><br>
</details>

<details>
<summary><b>Python 3.6.9 (tested)</b></summary>

Python should come pre-installed on your linux system. You can still check for the version of it with the command:

#### ` python3 --version`
If for any reason python is missing or is of oler version, use the following command to install python3 on your system.
#### ` sudo apt-get install python3 `
</details>

<br>

The script can run with these minimum requirements and can install other packages automatically. However, it is recommended that you install the following packages before running the application:
<details>
<summary><b>Git</b></summary>

Git should be pre-installed on your linux system but for any reason if it's not, you can run the following command to install it:
#### `sudo apt-get install git `
</details>

<details>
<summary><b>Tkinter</b></summary>

This library is present by default in python3. But if still missing you can install it by using the following command provided:
#### `sudo apt-get install python3-tk`
</details>

<details>
<summary><b>OpenCV 3.2.0 (tested)</b></summary>

This library would not be install by default, you can install openCV with the following command:
#### `sudo apt-get install python3-opencv`
</details>

<details>
<summary><b>LibOpenCV</b></summary>

This library would not be install by default, you can install openCV with the following commands:
#### `sudo apt-get install -y build-essential`
#### `sudo apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev`
#### `sudo apt-get install -y libopencv-dev`
</details>

<br>

# 💡 How to use?
This application is super easy to use! Here are all the step from downloading the application till testing your classifier:

### [WATCH VIDEO!](https://www.amannirala.com)

1. You need to first clone all the files from the github repository. Visit [the repositiry](https://github.com/amannirala13/HAAR-Cascade-Trainer-Linux.git) and download it as a zip file or just **open the terminal** and type the following command:
   #### `git clone https://github.com/amannirala13/HAAR-Cascade-Trainer-Linux.git`

2. Once downloaded open the terminal in the downloaded directory to make it the present working directory.

3. Once changed the pwd, you need to make all the file in the **`./app`** directory **executable**, use the following command to change the permission of the files:
   #### `chmod -R a+x ./app`

4. Change you pwd to the **app** and execute the **`main.py`** with python using the following command:
   #### `python3 main.py`

5. This will launch the application interface with which you can train your HAAR Cascade classifier with your dataset.

> Now, you have the application ready and running to train you classifier. The steps below tell you how you can train the classifier using actual dataset.

6. To train a HAAR Cascade Classifier you will have to create two directories with **positive** and **negative** images i.e. **images with the target object** and the **images without the target object** accordingly. Provide the location of the directories of the positive dataset and negative dataset as per asked in the application.
   
7. Then you need to select an output directory to tell the application where to store the **`classifier.xml`** file. Its recommended although not necessage to keep both the directories in the same directory and use that directory as the output directory.

8. Now provide the width and height of the traget object which is by default set to 24x24.

9. Now provide the percent of positive sample you want to use for the training of the classifier.

10. Set the number of stages of training of your classifier which by default is set to 10.

11. Press the start button to start training!

12. When the training is done, you can file your **`classifier.xml`** file in the output directory as **`./classifier/classifier.xml`**

<br>

## Recommendation for Dataset creation:
This application doesn't cleans the data and the vectors are generate automatically on the positive dataset so its highly recommended that your positive images are well cropped and only contain the target object. I will be adding a cropper, an image labeler, seperate vector file providing and positive dataset generation using single image features in the coming versions. Till then just manage with this small drawback. 

<br>

# **❤ Support**
If you like my work, a bit of contribution would motivate me a lot for more open source contributions.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/amannirala13)

*Please support the work:*
 - [Follow on **Github**](https://github.com/amannirala13)
 - [Follow on **LinkedIn**](https://www.linkedin.com/in/amannirala13/)
 - [Follow on **Twitter**](https://twitter.com/AmanNirala13)
 - [Follow on **Instagram**](https://www.instagram.com/amannirala13/)
 - [Follow on **Research Gate**](https://www.researchgate.net/profile/Aman_Nirala)
