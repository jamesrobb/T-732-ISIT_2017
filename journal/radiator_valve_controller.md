# Radiator Valve Controller

## 29/11/2017

We aimed to create a radiator valve controller for radiators used for heat in homes and offices. The valve controller would be aware of the temperature in the room and then open or close the valve to bring the room temperature to the desired temperature. In order to do this we needed to devise a cheap and effective method of opening and closing a radiator valve.

The first idea was to affix a stepper motor to the valve and then use it to open and close the valve as we could then turn the valve in known amounts. We obtained a reasonably large stepper motor from the electronics lab at RU and then hooked it up to see if it could produce the required torque to turn a radiator valve reliably.

We used SparkFun's EasyDriver and the HUZZAH Feather to drive the stepper motor. The motor voltage was supplied by a 9V DC power supply. With the EasyDriver set at max current and the step size (via the MS1 and MS2 pins) set at max torque, the stepper motor could still easily be prevented from moving by hand. Unfortunately not nearly enough torque was available to turn an average radiator valve. It would have been good to measure the actual torque required to turn a radiator valve, but the disparity between the torque produced by the motor and what seemed to be needed to turn a radiator valve was large enough to justify not looking any further into using a stepper motor for turning a radiator valve.

See `stepper_motor_circuit.pdf` for the schematic used.

## 05/12/2017

We spoke to Joseph Foley in the engineering department at RU to discuss other possible solutions for turning a radiator valve with precision and the ability to know where the valve is positioned after power lost. Joseph had suggest a few things like a servo valve and a thrust berring, but all unfortunately were atleast 20000ISK or more in price. This did not fit within our budget.

At this point we abandoned the idea of a radiator valve controller. It is a feasable project to complete given a larger budget and more time. Unfortunately the time required to get the parts, and thier cost excluded this idea from being one we could sucessfully execute on.