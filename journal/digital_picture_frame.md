# Digital Picture Frame

## 05/12/2017

**Materials gathered today**
* Old laptop screen (LP156WF4 from Dell Inspiron 7537)
* HDMI LCD Controller Board for 15.6" NT156WHM LP156WF4 1920x1080 30 Pins EDP LCD
* 12V 5A power supply for controller board
* Raspberry Pi 3
* 5v 1.2A power supply for raspberry pi
* HDMI cable

We installed Raspbian on the raspberry pi. The image was flashed to a class 10, 16 GB sd microSD card using Etcher, but also flashed extra card using the following dd command
`dd bs=4M if=2017-11-29-raspbian-stretch.img of=/dev/mmcblk0 status=progress conv=fsync`

We downloaded the raspbian image from https://www.raspberrypi.org/downloads/raspbian/
* Version: November 2017
* Release date: 2017-11-29
* Kernel version: 4.9
	
We hooked up the ribbon cable from the controller board to the back of the screen and added power to the board. Next we connected it to a laptop to confirm that the screen worked. We found out that we can't control the backlighting from the operating system and are currently trying to fix that issue.

Once the screen and the installation of Raspbian were confirmed to be working, we installed a VNC server and SSH server on the raspberry pi to allow remote access. Most work performed on the raspberry pi will be done through one of these two services. An FTP server was also installed to allow files to be uploaded easily for use in the picture viewing application we will build.

We talked to a picture frame company that will make our frame to house the screen and it's thick enough to house the electronics behind the screen. We hopefully will get it before the end of the week.

**Security Concerns**
* Default usernames and passwords need to be changed for the OS and varying service (SSH, VNC, FTP)

## 06/12/2017

Started to address the problem of how to provide a somewhat user-friendly way of interfacing with the digital picture frame. A user should be able to easily connect the picture frame to the local wifi network and then interact with it through that. Connecting a keyboard/mouse to the raspberry pi would be cumbersome and not very user-friendly. We therefore have begun following the directions of a tutorial that shows how to configure the raspberry pi to broadcast a wifi hotspot if it cannot connect to a previously configured network. The tutorial can be found at: http://www.raspberryconnect.com/network/item/330-raspberry-pi-auto-wifi-hotspot-switch-internet

The tutorial was not completed by the end of the day, and no tests were performed to asess how successful the solution might be.

## 07/12/2017

Began with finish tutorial from last time. The tutorial works as expected, but some effort needs to be put into making it more user friendly. Current idea is to create a small web page to allow the user to select what wifi network to connect to.

A flask (mini python web framework) server was installed and an endpoint was added that returns a list of images in the picture frames image repository. The picture frame will be configured to look at one directory or all, and the endpoint returns the corresponding images.

A flask based file-manager named browsepy was explored, but unfortunately its upload functionality was poor, and it did not offer the ability to create directories. The current idea is to provide a page that instructs the user to configure a browser based FTP solution for managing the pictures.

We have begun to experiment with "supersized" (https://github.com/buildinternet/supersized), an html/javascript slideshow. We have modified it to accept the list of images it displays from our flask endpoint, and to switch over to a new image set gracefully. The changes to supersized's code can be seen in the git log.

## 08/12/2017

We examined the eDP connect pin diagram to determine if it was possible to control the brightness of the screen from the raspberry pi. We learned that we could send a PWM signal of 0-5V on pin 8 to control the brightness of the screen. A logic level shifter was used to generate a 0-5V signal as the pi only has 3.3V GPIO pins. The brightness of the screen can now be controller via software on the pi.

We started looking for ways to easily display the wifi signals in the area so the user could configure the picture frame to connect to their home network. Since we are using python for all other scripting so far we tried the wifi module in PIP but for some reason it only showed us the currently connected network if not run as sudo (the underlying executable `iwlist` wants to be run as sudo to show all networks while currently connected to one). A solution will need to be found for this.

The first step of the web interface was done by displaying all the directories available for the user to choose pictures from.

## 11/12/2017

Today kiosk mode for the chromium web browser was explored to see if it would work well for displaying the web slide show. It works as one would expect. A package was installed on the raspberry pi called `unclutter` that hides the mouse pointer if it is not moved for some period of time (in our case half a second). We followed this tutorial https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/

API endpoints were added to the flask application to get the SSID of the currently conected network, and the IP address of the raspberry pi. The goal of having the pi act as a hotspot until a network connection can be configured has been abandoned as the methods we have seen so far are error prone and cumbersome. We will address this by having a page that appears for some amount of time on boot instructing the user how to connect a mouse and keyboard to configure the wifi.

The slideshow was updated to check for new images after dispalying x amount of images (currently x=3). When it checks for new images, the flask application it requests images from will return a checksum along with a list of images. If the checksum is different the one the slideshow had seen previously it will reload the web page. We attempted to modify the slideshow so that a completely seemless transition from the current set of images to a new set of images would take place, but we ran into many road blocks. The animations would speed up and become erratic, and we could not determine why. Given how often a user is likely to update the images or change the images to be display, this solution will perfomr adequately.

We test a component Hannes Pall gave us to step down 12VDC to 5VDC, however the component appears to step voltage up. We will consult with him tomorrow on how to step down the 12VDC to 5VDC so that we can power the pi on the same power supply as the screen controller.

https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/

## 12/12/2017

We attempted to use the dc-dc converter so that we would be able to use one power supply to power both devices. Since we came to the conclusion yesterday that the converter stepped up the voltage we tried using it to step up 5V to 12V to power the controller for the screen. Unfortunately the dc-dc converter doesn't seem to be able to supply enough amperage to keep the screen running at fully bightness, the screen just starts to reset as the controller does not get a stable supply of power.

We hooked up the TSL2591 sensor and tested it with a python module (https://github.com/maxlklaxl/python-tsl2591) to make sure everything worked. We tested if some clear acrylic could act as a conduit to pass enough light through the frame to be able to get a good reading but the that did not work as we wanted.

The frame was routed to be able to fit the screen inside with the glass. The screen had some small metal lips that also needed to be cut off, but in the end it fit snugly.

