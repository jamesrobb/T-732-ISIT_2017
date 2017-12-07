import os
import socket
import configparser

from flask import Flask
from flask import jsonify

IMG_BASE_DIR = "images"
CONFIG_FILE = "config.cfg"

app = Flask(__name__)

@app.route('/')
def hello_world():
    initial_config()
    return 'Hello, World!'

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


@app.route('/config')
def config_page():
    return "ftp site for image uploads is: %s" % str(socket.gethostbyname(socket.gethostname()))

@app.route('/get_images')
def get_images():
    # returns a json object listing images for the currently selected image directory

    pictureframe_config = read_config()
    current_image_dir = pictureframe_config["DEFAULT"]["current_image_dir"]
    directories = os.path.join(IMG_BASE_DIR, current_image_dir)
    images = []

    if (not os.path.isdir(os.path.join(IMG_BASE_DIR, current_image_dir))) or current_image_dir == "":
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