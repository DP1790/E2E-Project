import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
import os

from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename


# Initiate the app
app = Flask(__name__)

# HTML
TITLE         = "Image To Text Converter"
FRAME_TITLE   = "Image To Text Converter"
PURPOSE_TITLE = "Convert text within an image into PDF"
GITHUB_LINK   = "https://github.com/DP1790/E2E-Project"


# For uploading images
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
MAX_CONTENT_LENGTH = 1.5 * 1024 * 1024    # 1.5 MB app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024



# pytesseract on Heroku deployment only
pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"




def to_text(img_list: list) -> dict:
    """Convert images of text to pdf
    Args:
        img_list ([list]): [List of image filenames]
    Returns:
        [dict]: [Dictionary of image filenames and their text]
    """

    ret = {}
    for xfile in img_list:
        filename = xfile.split('.')[0]

        # Save as a PDF file
        try:
            # Read image
            img = cv2.imread(os.path.join(UPLOAD_FOLDER, xfile))

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # To text
            output = pytesseract.image_to_string(img, lang='eng').strip()
            res = re.split("\n",txt) # removing empty strings
            for i in res:
                if(len(i)==0):
                    res.remove(i)
            add0 = res[3:7]
            final_add0 = ' '.join(add0) ## final address
            
            dt =re.findall(r'\d+[/.-]\d+[/.-]\d+', txt)
            ft=" "
            ft=ft.join(dt) ## date

            amt = res[16].split() ## getting the total amount
            amt[4]
            
            ## Printing the final desired output
            output = print('Name =', res[1],'\n''Address=',final_add0,'\n''Total=',amt[4],'\n',ft)

            # Remove remove non-ASCII characters but leave periods and spaces
            output = output.encode('ascii', errors='ignore').decode() 


        except Exception as e:
            return None
        

        ret[xfile] = output
    
    return ret








def is_allowed_file(filename: str) -> bool:
    """Check if the file is allowed
    Args:
        filename ([string]): [String of Filename]
    Returns:
        [boolean]: [True/False]
    """
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS



def del_items() -> None:
    """Delete all image files in UPLOAD FOLDER and PDF files in PDF_FOLDER
    Returns:
        [None]
    """
    
    for x in os.listdir(UPLOAD_FOLDER):
        if os.path.splitext(x)[1].lower() in ALLOWED_EXTENSIONS:
            os.remove(os.path.join(UPLOAD_FOLDER, x))
    
    return None





# APIs

@app.route('/')
def home():
    del_items()
    return render_template("index.html",
                           TITLE = TITLE,
                           FRAME_TITLE = FRAME_TITLE,
                           PURPOSE_TITLE = PURPOSE_TITLE,
                           GITHUB_LINK = GITHUB_LINK
    )




@app.route("/convert", methods = ["GET", "POST"])
def convert():
    if request.method == "POST":

        # check if the post request has the file part
        if 'files[]' not in request.files:
            flash("No file part! Add file input to the form.", "danger")
            return redirect(url_for('home')) # or return redirect(request.url) if want to go back /predict
        
        files = request.files.getlist('files[]')
        if len(files) == 1 and files[0].filename == '':
            flash("No selected file! Please choose file(s) to upload.", "danger")
            return redirect(request.url)
        
        if len(files) > 3:
            flash("Too many files! Please select 3 files at max", "danger")
            return redirect(request.url)

        # MAX_CONTENT_LENGTH
        sizes = np.array([len(file.read()) for file in files])
        if np.any(sizes > MAX_CONTENT_LENGTH):
            flash("Files are too large! Please select files with size < " + str(MAX_CONTENT_LENGTH/1024./1024.) + ' MB', "danger")
            return redirect(request.url)

        filenames = []
        for file in files:
            if file and is_allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.seek(0)  # Need to have this to avoid files with 0 bytes
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filenames.append(filename)
            else:
                flash("File types are not allowed! Please select image file types ('.png', '.jpg', '.jpeg', '.gif')", "danger")
                return redirect(request.url)


        results = to_text(filenames)

        if  results is None:
            flash("[Error!] Cannot convert to text. Please select a clean text image and try again!", "danger")
            return redirect(url_for('home'))
        
        msg = "Success! Files uploaded!" if len(files) > 1 else "Success! File uploaded!"
        flash(msg, "success")

        return render_template(
            "process.html",
            results = results,
            TITLE = TITLE,
            FRAME_TITLE = FRAME_TITLE,
            PURPOSE_TITLE = PURPOSE_TITLE,
            GITHUB_LINK = GITHUB_LINK
        )
    
    return render_template("index.html",
                           TITLE = TITLE,
                           FRAME_TITLE = FRAME_TITLE,
                           PURPOSE_TITLE = PURPOSE_TITLE,
                           GITHUB_LINK = GITHUB_LINK
    )





# Run the app
if __name__ == '__main__':
    app.run(debug=True)