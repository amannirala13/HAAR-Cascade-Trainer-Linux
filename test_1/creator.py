import os

for i in range(0,500):
	os.system('opencv_createsamples -img p/face.png -bg negative.txt -info info/positive.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950')
