import os
import socket
import configparser
import hashlib
import subprocess
import netifaces as ni

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_cors import CORS

IMG_BASE_DIR = "static/slideshow_images"
CONFIG_FILE = "config.cfg"
ADAPTOR = "wlan0"

app = Flask(__name__)
CORS(app)


def initial_config():
    config = configparser.ConfigParser()

    config["DEFAULT"] = {"current_image_dir":"", "slide_interval":"7"}

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


def save_slide_interval(interval_time):
    """Saving slide interval to the config file.
        The interval time is in seconds."""
    try:
        new_interval = int(interval_time)
    except ValueError:
        return False
    
    config = configparser.ConfigParser()
    config = read_config()
    config["DEFAULT"]["slide_interval"] = interval_time

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


def get_all_ssids():
    process = subprocess.Popen(["sudo /sbin/iwlist wlan0 scan | grep SSID | sed -e 's/\\(.*\\)ESSID:\"\\(.*\\)\"/\\2/g' | sort | uniq"], stdout=subprocess.PIPE, shell=True)
    wifi = process.communicate()[0].strip()
    return wifi.decode("utf-8").split('\n')

def get_current_ssid():
    process = subprocess.Popen(["/sbin/iwgetid | sed -e 's/\\(.*\\)ESSID:\"\\(.*\\)\"/\\2/g'"], stdout=subprocess.PIPE, shell=True)
    ssid = process.communicate()[0].strip()
    return ssid.decode("utf-8")

def create_wpa_password(ssid, pw):
    command = "wpa_passphrase \"{}\" \"{}\"".format(ssid, pw)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    data = process.communicate()[0].strip()
    return data.decode("utf-8").split('\n')


def get_ip_address(adapter):
    # Check if the interface exists on the machine running program
    if adapter not in ni.interfaces():
        return "0.0.0.0"
    inet = ni.ifaddresses(adapter)
    # Check if there was any ip
    if ni.AF_INET in inet:
        return inet[ni.AF_INET][0]['addr']
    else:
        return "0.0.0.0"

@app.route('/')
@app.route('/index')
def index():
    params = {}
    # Get current image dir to auto select in selection box
    current_image_dir = read_config()["DEFAULT"]["current_image_dir"]
    current_image_dir = "All" if current_image_dir == "" else current_image_dir
    params["current_image_dir"] = current_image_dir
    # Get all directories that are available under IMG_BASE_DIR
    directories = get_base_directories()
    directories.insert(0, "All")
    params["directories"] = directories
    # Get network info
    ssid = get_current_ssid()
    params["ssid"] = ssid
    ip = get_ip_address(ADAPTOR)
    params["ip"] = ip
    # Get slide interval
    params["slide_interval"] = read_config()["DEFAULT"]["slide_interval"]
    return render_template('index.html', params=params)


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
    checksum = hashlib.md5()

    if (not os.path.isdir(directories[0])) or current_image_dir == "":
        directories = [IMG_BASE_DIR]
        for obj in os.listdir(IMG_BASE_DIR):

            if os.path.isdir(os.path.join(IMG_BASE_DIR, obj)):
                directories.append(os.path.join(IMG_BASE_DIR, obj))

    for directory in directories:

        for base_file in os.listdir(directory):

            file = os.path.join(directory, base_file)
            if os.path.isfile(file):
                img_obj = {"image": file, "title": "", "thumbnail": "", "url": ""}
                checksum.update(file.encode("utf-8"))
                images.append(img_obj)
                
    slide_interval = read_config()["DEFAULT"]["slide_interval"]
    response = {"checksum": checksum.hexdigest(), "slide_interval": slide_interval , "images": images}
    return jsonify(response)

@app.route('/slideshow')
def slideshow():
    return render_template('slideshow.html')

@app.route('/save_img_dir', methods=['POST'])
def save_img_dir():
    dir =  request.form['directory']    
    if save_dir(dir):
        return jsonify({'status':'OK','directory': dir})
    else:
        return jsonify({'status': 400, 'message': "Directory could not be changed."})


@app.route('/wifi')
def wifi():
    return render_template('wifi.html')

@app.route('/get_ip')
def get_ip():
    ip = get_ip_address(ADAPTOR)
    return jsonify({'status': 'OK', 'ip': ip})


@app.route('/slide_interval', methods=['POST'])
def slide_interval():
    interval = request.form['slide_interval']
    if save_slide_interval(interval):
        return jsonify({'status': 'OK','slide_interval': interval})
    else:
        return jsonify({'status': 400, 'message': "Slide interval was not changed."})