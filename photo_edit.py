from tkinter import filedialog
from tqdm import tqdm
import os
from datetime import datetime
import piexif
import re             
import shutil
import time
def Metadata(difference, type, directory):
	#for photo in os.listdir(directory):
	#	exif_dict = piexif.load(os.path.join(directory, photo))
	#	metadata = exif_dict
	#print(os.listdir(directory)[2])
	if os.path.exists(str(os.path.join(directory, "Edit"))):
		shutil.rmtree(str(os.path.join(directory, "Edit")))
	os.mkdir(str(os.path.join(directory, "Edit")))
	files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
	for photo in tqdm(files):
		shutil.copyfile(src=str(os.path.join(directory, photo)), dst=str(os.path.join(directory, str("Edit/" + photo))))
		exif_dict = piexif.load(os.path.join(os.path.join(directory, "Edit"), photo))
		exif_epoch = datetime.strptime(str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])[2:-1], '%Y:%m:%d %H:%M:%S').strftime('%s')	#datetime.strftime(str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])[1:], '%Y-%m-%d %H:%M').strftime('%s')	
		exif_epoch = int(exif_epoch) + difference if type == True else int(exif_epoch) - difference
		exif_epoch = datetime.fromtimestamp(exif_epoch) 
		exif_dict['0th'][piexif.ImageIFD.DateTime] = str(exif_epoch)
		exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = str(exif_epoch)
		exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = str(exif_epoch)
		exif_bytes = piexif.dump(exif_dict)
		piexif.insert(exif_bytes, str(os.path.join(directory, str("Edit/" + photo))))

if __name__ == '__main__':
	folder_path = filedialog.askdirectory(title="Vyberte soubor", initialdir="/home/kongis/Pictures")
	file_name = filedialog.askopenfilename(title="Zvolte vzorový obrázek", initialdir="/home/kongis/Pictures")
	print("Toto je čas pořízené fotografie:" + "   " + datetime.fromtimestamp(os.path.getatime(file_name)).strftime('%Y-%m-%d %H:%M') + "\nNyní napište správný čas (příklad: 2023-01-01 20:15)")
	image = piexif.load(os.path.join(folder_path, file_name))
	#input_time = datetime.fromtimestamp(os.path.getatime(file_name)).strftime('%s')
	input_time = datetime.strptime(str(image['Exif'][piexif.ExifIFD.DateTimeOriginal])[2:-1], '%Y:%m:%d %H:%M:%S').strftime('%s')
	final_time = input()
	final_time = datetime.strptime(final_time, '%Y-%m-%d %H:%M').strftime('%s')
	extend_time = abs(int(final_time)- int(input_time))
	Metadata(extend_time, True if (input_time < final_time) else False, folder_path)