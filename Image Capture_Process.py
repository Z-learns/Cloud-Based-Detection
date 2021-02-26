#!/usr/bin/env python3

import time
startTime = time.time()
import picamera
import cv2
import dropbox



## create dropbox object and upload image
dbx = dropbox.Dropbox('')

def uploadFile(fileFrom, fileTo):
	f = open(fileFrom,"rb")
	dbx.files_upload(f.read(), fileTo, mode = dropbox.files.WriteMode.overwrite)
	f.close()

def downloadFile(fileFrom,fileTo):
	f = open(fileTo,"wb")
	metadata, res = dbx.files_download(path=fileFrom)
	f.write(res.content)




# initialize camera
camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
camera.rotation = 180
camera.start_preview()
time.sleep(5)

#capture and save image
camera.capture('/home/pi/Images/img.jpg')
camera.stop_preview()
print("Image captured")

# Read,Resize and save image in jpg
Image = cv2.imread("/home/pi/Images/img.jpg")
Image = cv2.resize(Image, (400,400))
cv2.imwrite("/home/pi/Images/prepImage.jpg", Image )

# Create and write 1 to a text file
fh = open ('flag_pi.txt', 'w+')
fh.write('1')
fh.close()

# Upload image and textfile to Dropbox
uploadFile("/home/pi/Images/prepImage.jpg", "/capturedImage.jpg")
uploadFile("/home/pi/flag_pi.txt","/flag_pi.txt")
print("Image Uploaded")
time.sleep(30)

# Download textfile and check content

while True:


		downloadFile("/flag_mat.txt","/home/pi/flag_mat.txt")
		with open("/home/pi/flag_mat.txt","r+") as fh:
			value = fh.read()
			print(value)
		fh.close()

		# Download result if content is 2

		if value == '2':
			downloadFile("/DetImg.jpg","/home/pi/Images/DetectedImage.jpg")
			print("file downloaded")


			# display output image
			DetImage = cv2.imread("/home/pi/Images/DetectedImage.jpg")
			cv2.imshow("Detected Image", DetImage)
			endTime = time.time()
			print("Execution time: ","{0:.2f}".format(endTime - startTime)+ "Seconds") 
			cv2.waitKey(0)
			#cv2.destroyAllWindows()
			dbx.files_delete('/DetImg.jpg')
			dbx.files_delete('/flag_mat.txt')
			fh = open ('flag_pi.txt', 'w+')
			fh.write('2')
			fh.close()
			uploadFile("/home/pi/flag_pi.txt","/flag_pi.txt")
			print("file Uploaded")
			break

		else:
			print('Unable to download file')
			endTime = time.time()
			print("Execution time: ","{0:.2f}".format(endTime - startTime)+ " Seconds")
