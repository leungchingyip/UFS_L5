import os
from flask import request

# set the upload directory and allowed file types of photo  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/static/image"


def allowed_file(filename):
	"""Get the filename and return its file type.
	Args:
		filename(str): get the name from the upload file"""
	if '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
		return "."+filename.rsplit('.', 1)[1]

def upload_image(set_name):
	"""Get the upload file from form and save it in the UPLOAD_FOLDER.
	Args:
		set_name(str): It will be the new name of the file save in local 
		server."""
	if request.method == 'POST':
		file = request.files['photo']
		if file and allowed_file(file.filename):
			file_type=allowed_file(file.filename)
			filename=str(set_name)+file_type 
			file.save(os.path.join(IMAGE_PATH, filename))
			return "/static/image/"+filename
		else:
			return "http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
	else:
                return "http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
