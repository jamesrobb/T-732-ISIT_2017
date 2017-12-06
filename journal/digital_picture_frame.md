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
