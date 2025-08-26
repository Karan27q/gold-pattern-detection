from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import os
import uuid
import threading
import time
from werkzeug.utils import secure_filename
from app.utils import process_image
import cv2

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def delete_file_later(filepath, delay=20):
    def delete():
        import time
        time.sleep(delay)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)  # This deletes the file from your local device
        except Exception:
            pass
    import threading
    threading.Thread(target=delete, daemon=True).start()

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/detect', methods=['GET', 'POST'])
def index():
    input_image = None
    result_image = None
    input_path = None
    result_path = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filename = f"{uuid.uuid4().hex}_{filename}"
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(input_path)
                input_image = filename
            else:
                input_path = None
        else:
            input_path = None

        if input_image:
            result, mask = process_image(input_path)
            result_filename = f"{uuid.uuid4().hex}_result.png"
            result_path = os.path.join(UPLOAD_FOLDER, result_filename)
            cv2.imwrite(result_path, result)
            result_image = result_filename

            # Schedule deletion after 20 seconds
            delete_file_later(input_path, delay=20)
            delete_file_later(result_path, delay=20)

    return render_template(
        'index.html',
        input_image=input_image,
        result_image=result_image
    )

@routes.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)