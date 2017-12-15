import tkinter as tk
from PIL import Image, ImageTk
import time
import requests

class Slideshow():

    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
    SERVER_URL = 'http://localhost:5000/'

    images = []
    image_index = 0
    black = None # black image the size of the display
    display_interval = 3000

    # tk components
    root = None
    image_panel = None
    image_ref = None # we must store a reference to any PhotoImage we make, otherwise it will be garbage collected, even when being displayed (says so in Tk docs)

    # picture frame 
    checksum = None
    slide_interval = None
    first_load = True
    

    def __init__(self, start=False):

        # intialize Tk and Tk window
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("test macaroni")
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
            print("starting")
            self.next_image()

        self.root.mainloop()


    def next_image(self):

        self.render_image()
        self.increment_images_index()
        self.get_images()
        self.root.after(self.display_interval, self.next_image)


    def get_black(self):
        return self.black.copy()


    def get_image(self, index):

        try:
            image = Image.open(self.images[index]).convert('RGBA')
        except:
            print("There was an error loading %s" % self.images[index])
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
        

    def render_image(self):

        self.image_ref = ImageTk.PhotoImage(self.get_image(self.image_index))
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
        if self.checksum == new_checksum:
            return

        self.images = [img["image"] for img in r.json()["images"]]
        self.checksum = new_checksum
        self.slide_interval = r.json()["slide_interval"]


def main():
    #app = Example()
    app2 = Slideshow(start=True)
    #app2.get_image(0)

if __name__ == '__main__':
    main()
