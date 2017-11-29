
# Embedded systems

### Definition
* Context  (f.e. only lives in the context of a car)
* Closed compuer system,
* specific purpose, 
* generally not upgradeable
	* Cost (Software and hardware)

### 3 examples
* Coffee machines
* Car systems (brakes)
* POS   <- Gray area?

BitCoin miners?

## 3 Counter examples
* laptop/desktop 	-> Not special purpose
* Smart phones, tablets
* Super computers, servers
* Server (easy to upgrade) 


--- 
### Who decides the purpose ?
* If end user decides the purpose -> General purpose
	* often thought as some kind of black box's
* Embedded systems determined by designers/manufacturers


# IoT
**Network connected embedded devices**

### IoT examples
* security cameras
* Modern home "smart" devices
* Weather stations/devices

### Counter examples
* Remote controle
* Medical device
* Alarm clock 

---

## Kevin Ashton coined the term IoT
	RFID at MIT
	M2M
	Standardized way to understand the environment

## Mark Weiser - 1992 paper
	Ubiquitous Computing
	Had an idea about the computer for the 21 century, formulated the idea that the computer for the 21 century will not be a didicated device, will be computers that are around us.

## Norman Anders - 1994 paper
	Context aware computing application

## Proposal of Interent of thigs (IoT) 
	The internet of things is the infrastructior of interconnected objects, people, systems and information resources together with
	togeather with intelligent services to allow the to process information of the physical and virtual world and react (ISO/IEC)
	
**Interconnected objects, people, systems and information resources**
* Object
	* things that can act
* People
	* infrastructure of people
* Sytsems:
	* collection of things
	* services
* Information resources: things that can provide data
	* sensors
	* data bases

**Information: it's the interpritation of data** 
* Sensonrs don't have information, there needs to be some one to interprit.
	* There needs to be data to be able to interprit info

* Intelligent services

* information of the physical world
	* sensors on the device
	* f.e. temp & humid sensor in a room gives info about the room
* information of the virtual world
	* data and information

**Process, React**
* Process
	* decide on the sensor values and stored information
* react
	* actuate
	* send messages
	* change system state (store information)

**Infrastructure**
* Internet 
* Cloud services
* Software services

# IoT:
## Network layer protocols
* IETF protocols
	* IPv6, IPv4, 6lowPAN
	* TCP, UDP, ...
* Bluetooth
* WiFi, LTE
* Ethernet, CAN (Controlled Area Network)
* Infrared
* 433 MHz Radio

## Application layer protocol
* http
* xml
* JSON
* CoRe (Compress rest)
* MQTT, CoAP (constrant application protocol (rest proposal for IoT)) 

---

1. Read about Ada Box 003
2. What do I want to design?
	* 3 axis accelerometer BNO 055
	* Temperature + Humidity + Air pressure sensor
	* ToF distance
	1. Why do I think it is useful?
	2. Who would buy it?
