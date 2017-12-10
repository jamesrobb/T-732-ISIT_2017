import os
import socket
import configparser

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_cors import CORS

IMG_BASE_DIR = "images"
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
    if not os.path.isdir(os.path.join(IMG_BASE_DIR, img_dir)):
        return False

    config = configparser.ConfigParser()
    config = read_config()
    config["DEFAULT"]["current_image_dir"] = img_dir

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
    directories = get_base_directories()
    directories.insert(0, "All")
    return render_template('hello.html', dirTarget="All", directories=directories)


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


@app.route('/save_img_dir', methods=['POST'])
def save_img_dir():
    dir =  request.form['directory']
    
    #TODO: Need to validate that dir is valid and write it to config file.
    if save_dir(dir):
        return jsonify({'status':'OK','directory': dir})
    else:
        return jsonify({'status': 400, 'directory': dir})

