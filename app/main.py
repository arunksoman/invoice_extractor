from flask import (
    Blueprint,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    current_app,
)
from werkzeug.utils import secure_filename
import uuid
import os
from . import UPLOAD_FOLDER
from .lib.pdf_to_image import pdf_to_image


if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


main_bp = Blueprint("main_bp", __name__)


@main_bp.post("/")
@main_bp.get("/")
def index():
    if request.method == "POST":
        print(request.files)
        # check if the post request has the file part
        if "file" not in request.files:
            flash("Please select a file to upload", "red")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("Please select a file to upload", "red")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            folder_name = str(uuid.uuid4())
            folder_path = os.path.join(current_app.config["UPLOAD_FOLDER"], folder_name)
            os.mkdir(folder_path)
            file_up_path = os.path.join(folder_path, filename)
            file.save(file_up_path)
            current_app.logger.info(
                f"[Info ] File Uploaded Successfully to {file_up_path}"
            )
            out_image = pdf_to_image(file_up_path, 1)
            out_image_with_dir_name = rf"{out_image}"
            return redirect(
                url_for(
                    "main_bp.process_data",
                    folder_name=folder_name,
                    img_name=out_image_with_dir_name,
                )
            )
    return render_template("index.html")


@main_bp.get("/process/<string:folder_name>/<string:img_name>")
def process_data(folder_name, img_name):
    image_path = rf"/upload/{folder_name}/{img_name}.png"
    return render_template("xtract_page_konva.html", image_path=image_path)
