import os
import socket
import configparser

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_cors import CORS

IMG_BASE_DIR = "./static/slideshow_images"
CONFIG_FILE = "config.cfg"

app = Flask(__name__)
CORS(app)


def initial_config():
    config = configparser.ConfigParser()

    config["DEFAULT"] = {"current_image_dir":""}

    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)


def read_config():
    config = configparser.ConfigParser()

    if not os.path.isfile(CONFIG_FILE):
        initial_config()

    config.read(CONFIG_FILE)
    return config


def save_dir(img_dir):
    """ Save what image directory the user has chosen to config. """
    if not os.path.isdir(os.path.join(IMG_BASE_DIR, img_dir)) and img_dir != "All":
        return False

    config = configparser.ConfigParser()
    config = read_config()
    # If img_dir equals "All" we set the path to "" else the directory the user requested
    config["DEFAULT"]["current_image_dir"] = "" if img_dir == "All" else img_dir

    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)
    
    return True


def get_base_directories():
    directories = []
    if not os.path.isdir(IMG_BASE_DIR):
        return directories

    for obj in os.listdir(IMG_BASE_DIR):

        if os.path.isdir(os.path.join(IMG_BASE_DIR, obj)):
            directories.append(obj)
    return directories


@app.route('/')
def index():
    current_image_dir = read_config()["DEFAULT"]["current_image_dir"]
    current_image_dir = "All" if current_image_dir == "" else current_image_dir
    directories = get_base_directories()
    directories.insert(0, "All")
    return render_template('index.html', dirTarget=current_image_dir, directories=directories)


@app.route('/config')
def config_page():
    return "ftp site for image uploads is: %s" % str(socket.gethostbyname(socket.gethostname()))


@app.route('/get_images')
def get_images():
    # returns a json object listing images for the currently selected image directory

    pictureframe_config = read_config()
    current_image_dir = pictureframe_config["DEFAULT"]["current_image_dir"]
    directories = [os.path.join(IMG_BASE_DIR, current_image_dir)]
    images = []

    if (not os.path.isdir(directories[0])) or current_image_dir == "":
        directories = []

        for obj in os.listdir(IMG_BASE_DIR):

            if os.path.isdir(os.path.join(IMG_BASE_DIR, obj)):
                directories.append(os.path.join(IMG_BASE_DIR, obj))

    for directory in directories:

        for base_file in os.listdir(directory):

            file = os.path.join(directory, base_file)
            if os.path.isfile(file):
                img_obj = {"image": file, "title": "", "thumbnail": "", "url": ""}
                images.append(img_obj)

    return jsonify(images)

@app.route('/slideshow')
def slideshow():
    return render_template('slideshow.html')

@app.route('/save_img_dir', methods=['POST'])
def save_img_dir():
    dir =  request.form['directory']
    print("The directory body request: {}".format(dir))
    
    if save_dir(dir):
        return jsonify({'status':'OK','directory': dir})
    else:
        return jsonify({'status': 400, 'directory': dir})

