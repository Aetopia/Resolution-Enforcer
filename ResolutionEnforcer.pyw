# Windows
from psutil import Process
from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from win32api import ChangeDisplaySettings
from win32con import DM_PELSWIDTH, DM_PELSHEIGHT
from pywintypes import DEVMODEType

# Python
from time import sleep
from configparser import ConfigParser
from os import path

# Options
Options = ConfigParser()
Options.read('Options.ini')

# Get title and executable name from an active window.
def Window():
    HWND = GetForegroundWindow()
    PID = GetWindowThreadProcessId(HWND)[1]
    Title = GetWindowText(HWND)
    Executable = path.split(path.abspath(Process(PID).exe()))[1]
    return (Title, Executable)

# Filter out applications to enforce resolutions on.
def EnforceResolution():
    Enforce = False
    while True:
        sleep(0.1)
        Title, Executable = Window()
        
        if Executable == 'ApplicationFrameHost.exe':
            if Title in Options['Applications']:
                if Enforce is False:
                    Resolution = Options['Applications'][str(Title)]
                    Enforce = True   

        elif Executable in Options['Applications']:
            if Enforce is False:
                Resolution = Options['Applications'][str(Executable)]
                Enforce = True 

        else: Resolution = '0x0'  

        Height, Width = Resolution.split('x')
        Resolution = DEVMODEType()
        Resolution.PelsWidth, Resolution.PelsHeight = int(Height.strip()), int(Width.strip()) 
        Resolution.Fields = DM_PELSWIDTH | DM_PELSHEIGHT

        if Enforce:
            ChangeDisplaySettings(Resolution, 0)
            break
    RestoreResolution()

# Restore the default desktop resolution.
def RestoreResolution():
    Restore = False
    while True:
        sleep(0.1)
        Title, Executable = Window()

        if Executable == 'ApplicationFrameHost.exe':
            if Title not in Options['Applications']:
                Restore = True
        
        elif Executable not in Options['Applications']:
            Restore = True

        if Restore:
            ChangeDisplaySettings(None, 0)
            break
    EnforceResolution()    

def Main():
    EnforceResolution()
                             
if __name__ == '__main__':
    Main()
