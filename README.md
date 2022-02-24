# Resolution-Enforcer
Enforce desktop resolutions on specific applications. (Win32 and UWP apps.)

## Aim
The aim of this project is to create a program that can restore fullscreen resolution changing into applications by enforcing application specific desktop resolutions.
Mostly aimed at games or software which do not offer an option to select the fullscreen resolution. 

## Setup
1. Install Python `3.10`.
2. Install the following modules or use `requirements.txt`.
```
pip install pywintypes
pip install psutil
```
3. Open up `Options.ini`.
Add UWP apps or Win32 apps that should be filtered by the program.

UWP Apps => Only include the name of the app. (Case Sensitive.)
Win32 Apps => Only include the name of executable .(Case Sensitive.)

Example:
```ini
[Applications]
Minecraft = 1280x720
HaloInfinite.exe = 1600x900
```
