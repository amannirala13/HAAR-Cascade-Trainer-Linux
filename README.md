# HAAR Cascade GUI Trainer - Linux
This is a HAAR Cascade Classifier training GUI application for Linux. This application make it really easy to train classifiers for object detection and tracking using opencv by providing a Graphical user interface to set parameters and perform necessary steps.

# Requirements:
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
<br>
</details>

___

The script can run with these minimum requirements and can install other packages automatically. However, it is recommended that you install the following packages before running the application:
<details>
<summary><b>Tkinter</b>
</summary>
This library is present by default in python3. But if still missing you can install it by using the following command provided:

#### `sudo apt-get install python3-tk`
</details>
<details>
<summary><b>OpenCV</b>
</summary>
This library would not be install by default, you can install openCV with the following commad:

#### `sudo apt-get install python3-opencv`
</details>