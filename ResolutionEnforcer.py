from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from time import sleep
from psutil import Process
from win32api import ChangeDisplaySettings
from win32con import DM_PELSWIDTH, DM_PELSHEIGHT
from  pywintypes import DEVMODEType
from configparser import ConfigParser
from os import path

Options = ConfigParser()
Options.read('Options.ini')

def EnforceResolution():
    Hook = False
    while True:
        sleep(float(Options['General']['Speed']))
        HWND = GetForegroundWindow()
        Title = GetWindowText(HWND)
        PID = GetWindowThreadProcessId(HWND)[1]  
        Executable = path.split(path.abspath(Process(PID).exe()))[1]

        if Executable == 'ApplicationFrameHost.exe':
            if Title in Options['Applications']:
                if Hook is False:
                    Resolution = Options['Applications'][str(Title)]
                    Hook = True   

        elif Executable in Options['Applications']:
            if Hook is False:
                Resolution = Options['Applications'][str(Executable)]
                Hook = True 
        else:
            Resolution = '0x0'  

        Height, Width = Resolution.split('x')
        Resolution = DEVMODEType()
        Resolution.PelsWidth = int(Height.strip())
        Resolution.PelsHeight = int(Width.strip())
        Resolution.Fields = DM_PELSWIDTH | DM_PELSHEIGHT

        if Hook:
            ChangeDisplaySettings(Resolution, 0)
            break
    RestoreResolution()

def RestoreResolution():
    Reset = False
    while True:
        sleep(float(Options['General']['Speed']))
        HWND = GetForegroundWindow()
        Title = GetWindowText(HWND)
        PID = GetWindowThreadProcessId(HWND)[1] 
        Executable = path.split(path.abspath(Process(PID).exe()))[1]

        if Executable == 'ApplicationFrameHost.exe':
            if Title not in Options['Applications']:
                Reset = True
        
        elif Executable not in Options['Applications']:
            Reset = True

        if Reset:
            ChangeDisplaySettings(None, 0)
            break
    EnforceResolution()    

def Main():
    EnforceResolution()
                             
if __name__ == '__main__':
    Main()