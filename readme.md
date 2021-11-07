The Microsoft SideWinder Precision Racing Wheel is a wheel and 2-pedal controller which
was introduced to the market in 1999 and is still used by many people. 

Windows 10 has a built-in driver for this wheel, however the two pedals are seperated into 2 different
axis (Y and Z axis), thus rendering this wheel incompatible with many games.

This little python script solves this problem by casting the wheel and pedal position into
a virtual XBox360 gamepad and combining the two axis into one Y axis:

Y axis: gas pedal axis values: not pressed (1.0) to pressed (-1.0)
Z axis: brake pedal axis values: not pressed (1.0) to pressed (-1.0)

therefore, the virtual Y axis is calculated by (Z-Y)/2

Possible edits:
===============
SIDEWINDER_NAME_SUBSTR:
The script finds the SideWinder controller by iterating through all connected controllers and searching 
for this substring in the controller name. 

BUTTON_MAP:
The 8 wheel buttons are mapped into some of the XBox360 controller buttons and this mapping can 
be modified by editing BUTTON_MAP.

STEERING_AXIS:
The axis which is used for the steering (X axis). Set to 0

GAS_PEDAL_AXIS:
The axis which is used for the gas pedal (Y axis). Set to 1

BRAKE_PEDAL_AXIS:
The axis which is used for the brake pedal(Z axis). Set to 2


Limitations: 
============
The script does not handle force feedback

---------------------------------------------------------------
I hope this script will help you enjoy this wheel once again :)
Feel free to use, modify and share this script.

