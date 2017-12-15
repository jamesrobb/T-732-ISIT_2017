#!/usr/bin/python3

import os
import sys
import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import time
import requests
import random
import subprocess
import netifaces as ni
import logging

import pictureframe_vars

class Slideshow():

    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
    SERVER_URL = pictureframe_vars.SERVER_URL
    ADAPATOR = pictureframe_vars.ADAPTOR
    GET_IMAGES_FREQUENCY = 5 # how many images to display before checking for new images

    images = []
    image_index = 0
    black = None # black image the size of the display
    display_interval = 10000

    # tk components
    root = None
    image_panel = None
    image_ref = None # we must store a reference to any PhotoImage we make, otherwise it will be garbage collected, even when being displayed (says so in Tk docs)

    # picture frame 
    checksum = None
    slide_interval = None
    first_load = True
    images_seen_since_query = 0

    # debug information
    logger = None
    

    def __init__(self, start=False):


        self.logger = logging.getLogger("slideshow-logger")
        self.logger.disabled = False

        # intialize Tk and Tk window
        self.root = tk.Tk()
        #self.root.attributes("-fullscreen", True)
        self.root.title("Slideshow")
        self.root.geometry("%dx%d+%d+%d" % (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT, 0, 0))

        # create black image base (used as a background for images that don't fill screen entirely)
        self.black = Image.new('RGBA', (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.black.paste((0,0,0), (0, 0, self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))   
        
        self.image_ref = ImageTk.PhotoImage(self.black.copy())

        self.image_panel = tk.Label(self.root, image=self.image_ref)
        self.image_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.get_images()
        self.first_load = False

        if start:
            self.logger.debug("Starting slideshow.")
            self.next_image(initial_image=True)

        self.root.mainloop()


    def next_image(self, initial_image=False):

        self.render_image(initial_image)
        self.increment_images_index()

        if initial_image:
            self.image_index = 0
        else:
            self.images_seen_since_query += 1
            if self.images_seen_since_query >= self.GET_IMAGES_FREQUENCY:
                self.images_seen_since_query = 0
                self.get_images()

        self.root.after(self.display_interval, self.next_image)


    def get_black(self):
        return self.black.copy()

    def get_initial_image(self):
        bg = self.get_black()
        draw = ImageDraw.Draw(bg)
        file_dir = os.path.dirname(os.path.realpath(__file__))
        font = ImageFont.truetype(os.path.join(file_dir, "LiberationMono-Regular.ttf"), size=25)
        #font = ImageFont.load_default().font

        draw.text((10, 10), "SSID: %s IP: %s" % (self.get_current_ssid(), self.get_ip_address()), (255, 255, 255), font=font)
        draw.text((10, 90), "IF YOU ARE NOT CONNECTED TO THE INTERNET, CONNECT A KEYBOARD AND MOUSE AND PRESS ALT+F4 TO CLOSE THIS SLIDESHOW.", (255, 255, 255), font=font)
        draw.text((10, 120), "YOU CAN THEN CONFIGURE THE WIFI BY CLICKING ON THE WIFI ON THE TOP RIGHT CORNER OF THE SCREEN.", (255, 255, 255), font=font)

        return bg

    def get_image(self, index):

        if(len(self.images) == 0):
            self.logger.debug("The images array contains no images. A black screen should be displayed")
            return None

        try:
            image = Image.open(self.images[index]).convert('RGBA')
        except:
            self.logger.debug("There was an error loading %s." % self.images[index])
            return None

        # Get width & height of the original image
        width,height = image.size

        # Where to start drawing the new image on black.
        start_width, start_height = (0,0)

        # If we have a portrait photo, we scale height to 100% and width with percentage of height to keep scale.
        if (width/height) <= 1.3:
            """The proportional width is calculated by determining what percentage 
                DISPLAY_HEIGHT pixels is of the original height and then multiplying 
                the original width by that percentage."""
            hpercent = (self.DISPLAY_HEIGHT / float(height))
            wsize = int(float(width) * float(hpercent))
            image = image.resize((wsize, self.DISPLAY_HEIGHT), Image.ANTIALIAS)
            # Calculate how much of the screen is not filled up by the image so we can center the image on the display.
            start_width = int((self.DISPLAY_WIDTH - wsize) / 2)

        else:
            """The proportional height is calculated by determining what percentage 
                DISPLAY_WIDTH pixels is of the original width and then multiplying 
                the original height by that percentage."""
            wpercent = (self.DISPLAY_WIDTH / float(width))
            hsize = int((float(height) * float(wpercent)))
            image = image.resize((self.DISPLAY_WIDTH, hsize), Image.ANTIALIAS)
            # Calculate how much of the image surpasses the display height and make it even on both sides.
            start_height = int((self.DISPLAY_HEIGHT - hsize) / 2)
            

        black = self.get_black()
        # Adding the image on a black background ath the correct position
        black.paste(image, (start_width, start_height))

        return black
        

    def render_image(self, initial_image=False):

        if initial_image:
            image = self.get_initial_image()
        else:
            image = self.get_image(self.image_index)
            if image is None:
                self.logger.debug("Can't render bogus image. Removing image from images array.")

                if len(self.images) > 0:
                    self.images.pop(self.image_index)

                image = self.get_black()

        self.image_ref = ImageTk.PhotoImage(image)
        self.image_panel.configure(image=self.image_ref)

        return


    def increment_images_index(self):

        self.image_index += 1

        if self.image_index > len(self.images) - 1:
            self.image_index = 0

        return

    def get_images(self):
        r = requests.get(self.SERVER_URL+"get_images")
        new_checksum = r.json()["checksum"]

        if self.checksum == new_checksum and (not self.first_load):
            return

        self.logger.debug("Images refreshed.")
        self.images = [img["image"] for img in r.json()["images"]]
        random.shuffle(self.images)
        self.image_index = 0
        self.checksum = new_checksum
        self.slide_interval = r.json()["slide_interval"]

    def get_current_ssid(self):
        process = subprocess.Popen(["/sbin/iwgetid | sed -e 's/\\(.*\\)ESSID:\"\\(.*\\)\"/\\2/g'"], stdout=subprocess.PIPE, shell=True)
        ssid = process.communicate()[0].strip()
        return ssid.decode("utf-8")

    def get_ip_address(self):
        # Check if the interface exists on the machine running program
        if self.ADAPATOR not in ni.interfaces():
            return "0.0.0.0"
        inet = ni.ifaddresses(self.ADAPATOR)
        # Check if there was any ip
        if ni.AF_INET in inet:
            return inet[ni.AF_INET][0]['addr']
        else:
            return "0.0.0.0"


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    app = Slideshow(start=True)

if __name__ == '__main__':
    main()
