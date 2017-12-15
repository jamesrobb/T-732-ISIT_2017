import tkinter as tk
from PIL import Image, ImageTk
import time

class Slideshow():

    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
    PATH_TO_IMG = './static/slideshow_images/'


    images = [
        PATH_TO_IMG+"the_map_of_mathematics.jpg",
        PATH_TO_IMG+"WP_000391.jpg",
        PATH_TO_IMG+"WP_000277.jpg",
        PATH_TO_IMG+"DSC_0228.JPG",
        PATH_TO_IMG+"DSC_0032.JPG",
        PATH_TO_IMG+"math_stud/math_nerd_meme1.png",
        PATH_TO_IMG+"math_stud/math_nerd_meme2.png",
        PATH_TO_IMG+"math_stud/math_nerd_meme3.png",
        PATH_TO_IMG+"memes/25360371_1524785207616645_2128903139_n.png",
        PATH_TO_IMG+"memes/24203471_922915184523301_583399852_n.jpg"
    ]
    image_index = 0
    black = None # black image the size of the display
    display_interval = 3000

    # tk components
    root = None
    image_panel = None
    image_ref = None # we must store a reference to any PhotoImage we make, otherwise it will be garbage collected, even when being displayed (says so in Tk docs)

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

        if start:
            print("starting")
            self.next_image()

        self.root.mainloop()

    def next_image(self):

        self.render_image()
        self.increment_images_index()
        self.root.after(self.display_interval, self.next_image)

    def get_black(self):
        return self.black.copy()

    def get_image(self, index):

        try:
            image = Image.open(self.images[index]).convert('RGBA')
        except:
            print("There was an error loading %s" % self.images[index])
            return None

        # come back here to do image resizing so the frame is filled up with landscape photos
        # portrait or box photos will have black bars on the sides
        # if width > height:
        #     # landscape image
        # else:
        #     # box or portrait

        image = image.resize((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        black = self.get_black()
        black.paste(image, (0, 0))

        return image
        
    def render_image(self):

        self.image_ref = ImageTk.PhotoImage(self.get_image(self.image_index))
        self.image_panel.configure(image=self.image_ref)

        return

    def increment_images_index(self):

        self.image_index += 1

        if self.image_index > len(self.images) - 1:
            self.image_index = 0

        return

class Example():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('My Pictures')

        # pick an image file you have .bmp  .jpg  .gif.  .png
        # load the file and covert it to a Tkinter image object
        imageFile = "babyAce.jpg"
        self.black = Image.new('RGBA', (800, 600))
        self.black.paste((0,0,0), (0, 0, 800, 600))
        #self.black = ImageTk.PhotoImage(self.black)
        # self.image1 = ImageTk.PhotoImage(Image.open('./static/slideshow_images/DSC_0032.JPG').resize((800, 600)))
        # self.image2 = ImageTk.PhotoImage(Image.open('./static/slideshow_images/00003.jpg').resize((800, 600)))
        self.image1 = Image.open('./static/slideshow_images/DSC_0032.JPG').convert('RGBA').resize((800, 600))
        #self.image2 = Image.open('./static/slideshow_images/00003.jpg').resize((800, 600))
        self.comp = ImageTk.PhotoImage(Image.blend(self.image1, self.black, 0.5))

        # get the image size
        #w = self.image1.width()
        #h = self.image1.height()
        w = 800
        h = 600

        # position coordinates of root 'upper left corner'
        x = 0
        y = 0

        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # root has no image argument, so use a label as a panel
        self.panel1 = tk.Label(self.root, image=self.comp)
        #self.display = self.image1
        self.panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        print("Display image1")
        self.root.after(3000, self.update_image)
        self.root.mainloop()

    def update_image(self):
        print("update image mofucka")
        # if self.display == self.image1:
        #     self.panel1.configure(image=self.image2)
        #     print("Display image2")
        #     self.display = self.image2
        # else:
        #     self.panel1.configure(image=self.image1)
        #     print("Display image1")
        #     self.display = self.image1
        # self.root.after(30000, self.update_image)       # Set to call again in 30 seconds

def main():
    #app = Example()
    app2 = Slideshow(start=True)
    #app2.get_image(0)

if __name__ == '__main__':
    main()