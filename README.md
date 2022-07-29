MB-investigator
===================
# Overview
**MB-investigator** is yet another [Modbus](https://en.wikipedia.org/wiki/Modbus) tool for access and investigate Modbus server/slave.
You can read data (coils or registers) from your Modbus server/slave, and write data to it.

# Features
* Connection via TCP, RTU or RTU over TCP.
* Read coils and registers (FC01, FC02, FC03, FC04).
* Write coils and registers (FC05, FC06, FC15, FC16).
* Use multiple Modbus address ranges simultaneously.
* Import and export configurations.

# Download
You can download the last build made with [PyInstaller](https://pyinstaller.org/en/stable/) here : 
https://github.com/Lorin-lab/MB-investigator/releases

Or you can download the sources and run it in your own Python environment.

# Dependencies
MB-investigator use [modbus-tk](https://github.com/ljean/modbus-tk) (v1.1.2) for modbus protocol.
And [PyQt5](https://pypi.org/project/PyQt5/) (v5.15.6) for graphical interface. 